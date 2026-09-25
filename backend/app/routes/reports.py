from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
import anthropic

from app.database import get_db
from app.models import Machine, Prediction
from app.config import settings

router = APIRouter()


def compute_weekly_statistics(db: Session) -> Dict[str, Any]:
    """
    Compute aggregate statistics for the weekly report.
    Queries all machines and their predictions from the last 7 days.
    """
    # Calculate date threshold (7 days ago)
    date_threshold = datetime.utcnow() - timedelta(days=7)
    
    # Get all machines
    machines = db.query(Machine).all()
    total_machines = len(machines)
    
    if total_machines == 0:
        return {
            "total_machines": 0,
            "status_counts": {},
            "average_health_score": 0,
            "lowest_health_machines": [],
            "health_decline_machines": [],
            "predictions_analyzed": 0,
            "date_range": "No data available"
        }
    
    # Get predictions from last 7 days (or all if less than 7 days of data)
    predictions = db.query(Prediction).filter(
        Prediction.timestamp >= date_threshold
    ).order_by(Prediction.timestamp.desc()).all()
    
    # If no predictions in last 7 days, get all predictions
    if not predictions:
        predictions = db.query(Prediction).order_by(Prediction.timestamp.desc()).all()
        date_range = "All available data (less than 7 days)"
    else:
        date_range = f"Last 7 days (since {date_threshold.strftime('%Y-%m-%d')})"
    
    predictions_analyzed = len(predictions)
    
    # Count machines per status (using latest prediction per machine)
    status_counts = {
        "NORMAL": 0,
        "MONITOR": 0,
        "MAINTENANCE_RECOMMENDED": 0,
        "CRITICAL": 0
    }
    
    machine_latest_status = {}
    machine_health_scores = []
    
    for pred in predictions:
        if pred.machine_id not in machine_latest_status:
            machine_latest_status[pred.machine_id] = pred.maintenance_status
            status_counts[pred.maintenance_status] = status_counts.get(pred.maintenance_status, 0) + 1
            machine_health_scores.append({
                "machine_id": pred.machine_id,
                "machine_name": pred.machine.name if pred.machine else f"Machine {pred.machine_id}",
                "health_score": pred.health_score,
                "predicted_rul": pred.predicted_rul,
                "effective_rul": pred.effective_rul,
                "status": pred.maintenance_status,
                "timestamp": pred.timestamp.isoformat()
            })
    
    # Calculate average health score
    if machine_health_scores:
        average_health_score = sum(m["health_score"] for m in machine_health_scores) / len(machine_health_scores)
    else:
        average_health_score = 0
    
    # Find machines with lowest health scores (top 5)
    lowest_health_machines = sorted(
        machine_health_scores,
        key=lambda x: x["health_score"]
    )[:5]
    
    # Find machines with steepest health decline (need at least 2 predictions)
    machine_predictions = {}
    for pred in predictions:
        if pred.machine_id not in machine_predictions:
            machine_predictions[pred.machine_id] = []
        machine_predictions[pred.machine_id].append(pred)
    
    health_decline_machines = []
    for machine_id, preds in machine_predictions.items():
        if len(preds) >= 2:
            # Sort by timestamp (oldest first)
            sorted_preds = sorted(preds, key=lambda x: x.timestamp)
            oldest_score = sorted_preds[0].health_score
            newest_score = sorted_preds[-1].health_score
            decline = oldest_score - newest_score
            
            if decline > 0:  # Only include if health declined
                machine = db.query(Machine).filter(Machine.id == machine_id).first()
                health_decline_machines.append({
                    "machine_id": machine_id,
                    "machine_name": machine.name if machine else f"Machine {machine_id}",
                    "health_decline": round(decline, 2),
                    "oldest_health_score": round(oldest_score, 2),
                    "newest_health_score": round(newest_score, 2),
                    "oldest_timestamp": sorted_preds[0].timestamp.isoformat(),
                    "newest_timestamp": sorted_preds[-1].timestamp.isoformat()
                })
    
    # Sort by steepest decline
    health_decline_machines = sorted(
        health_decline_machines,
        key=lambda x: x["health_decline"],
        reverse=True
    )[:5]
    
    return {
        "total_machines": total_machines,
        "status_counts": status_counts,
        "average_health_score": round(average_health_score, 2),
        "lowest_health_machines": lowest_health_machines,
        "health_decline_machines": health_decline_machines,
        "predictions_analyzed": predictions_analyzed,
        "date_range": date_range,
        "report_generated_at": datetime.utcnow().isoformat()
    }


def generate_fallback_report(stats: Dict[str, Any]) -> str:
    """
    Generate a rule-based template summary when LLM is not available.
    """
    report_lines = []
    
    report_lines.append("⚠️ MODE DE SECOURS ACTIF")
    report_lines.append("Ce rapport a été généré sans l'IA (clé API Anthropic non configurée).")
    report_lines.append("")
    
    report_lines.append("📊 RÉSUMÉ HEBDOMADAIRE DE MAINTENANCE")
    report_lines.append(f"Date du rapport: {stats['report_generated_at']}")
    report_lines.append(f"Période analysée: {stats['date_range']}")
    report_lines.append("")
    
    report_lines.append(f"Total des machines: {stats['total_machines']}")
    report_lines.append(f"Prédictions analysées: {stats['predictions_analyzed']}")
    report_lines.append(f"Score de santé moyen de la flotte: {stats['average_health_score']}/100")
    report_lines.append("")
    
    report_lines.append("DISTRIBUTION DES STATUTS:")
    for status, count in stats['status_counts'].items():
        report_lines.append(f"  - {status}: {count}")
    report_lines.append("")
    
    if stats['lowest_health_machines']:
        report_lines.append("MACHINES AVEC LE PLUS FAIBLE SCORE DE SANTÉ:")
        for machine in stats['lowest_health_machines']:
            report_lines.append(f"  - {machine['machine_name']}: Score {machine['health_score']}/100 ({machine['status']})")
        report_lines.append("")
    
    if stats['health_decline_machines']:
        report_lines.append("MACHINES AVEC DÉCLIN DE SANTÉ LE PLUS RAPIDE:")
        for machine in stats['health_decline_machines']:
            report_lines.append(f"  - {machine['machine_name']}: Déclin de {machine['health_decline']} points")
            report_lines.append(f"    (de {machine['oldest_health_score']} à {machine['newest_health_score']})")
        report_lines.append("")
    
    report_lines.append("ACTIONS PRIORITAIRES:")
    
    critical_count = stats['status_counts'].get('CRITICAL', 0)
    maintenance_count = stats['status_counts'].get('MAINTENANCE_RECOMMENDED', 0)
    
    if critical_count > 0:
        report_lines.append(f"  1. URGENT: Intervenir immédiatement sur {critical_count} machine(s) en état CRITIQUE")
    
    if maintenance_count > 0:
        report_lines.append(f"  2. Planifier la maintenance pour {maintenance_count} machine(s) nécessitant une intervention")
    
    if stats['health_decline_machines']:
        report_lines.append(f"  3. Surveiller de près les machines montrant un déclin rapide de santé")
    
    report_lines.append("  4. Continuer la surveillance régulière de toutes les machines")
    
    return "\n".join(report_lines)


def generate_llm_report(stats: Dict[str, Any]) -> str:
    """
    Generate an AI-powered report using Anthropic Claude.
    """
    api_key = settings.ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key or api_key == "your_key_here":
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY not configured. Please add your API key to backend/.env or set ANTHROPIC_API_KEY environment variable. Get your key from https://console.anthropic.com/"
        )
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Build the statistics text for the prompt
        stats_text = f"""
STATISTIQUES DE LA FLOTTE:
- Total des machines: {stats['total_machines']}
- Prédictions analysées: {stats['predictions_analyzed']}
- Période: {stats['date_range']}
- Score de santé moyen: {stats['average_health_score']}/100

DISTRIBUTION DES STATUTS:
"""
        for status, count in stats['status_counts'].items():
            stats_text += f"- {status}: {count}\n"
        
        if stats['lowest_health_machines']:
            stats_text += "\nMACHINES AVEC LE PLUS FAIBLE SCORE DE SANTÉ:\n"
            for machine in stats['lowest_health_machines']:
                stats_text += f"- {machine['machine_name']}: Score {machine['health_score']}/100, RUL effectif {machine['effective_rul']:.1f} cycles, Statut {machine['status']}\n"
        
        if stats['health_decline_machines']:
            stats_text += "\nMACHINES AVEC DÉCLIN DE SANTÉ:\n"
            for machine in stats['health_decline_machines']:
                stats_text += f"- {machine['machine_name']}: Déclin de {machine['health_decline']} points (de {machine['oldest_health_score']} à {machine['newest_health_score']})\n"
        
        system_prompt = """Tu es un analyste des opérations de maintenance industrielle expert. Ta tâche est de rédiger un rapport hebdomadaire de maintenance prédictive en français.

BASES TON RAPPORT UNIQUEMENT SUR LES STATISTIQUES FOURNIES. N'INVENTE AUCUNE INFORMATION.

Structure ton rapport comme suit:
1. Un paragraphe d'introduction (2-3 phrases) résumant l'état global de la flotte
2. Un paragraphe sur les machines nécessitant une attention urgente (statut CRITICAL ou MAINTENANCE_RECOMMENDED)
3. Un paragraphe sur les tendances notables (amélioration ou déclin de la santé de la flotte)
4. Une liste priorisée d'actions concrètes pour l'équipe de maintenance (3-5 actions maximum)

Sois concis et professionnel. Utilise les chiffres réels des statistiques pour justifier tes recommandations."""

        user_message = f"""Génère un rapport hebdomadaire de maintenance basé sur les statistiques suivantes:

{stats_text}

Rapport:"""

        response = client.messages.create(
            model="claude-sonnet-4-5-20240620",
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        return response.content[0].text
        
    except anthropic.AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid ANTHROPIC_API_KEY. Please check your API key in backend/.env"
        )
    except anthropic.APIError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Anthropic API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating LLM report: {str(e)}"
        )


@router.get("/weekly-summary")
async def get_weekly_summary(db: Session = Depends(get_db)):
    """
    Generate a weekly maintenance report.
    
    Returns:
        - If ANTHROPIC_API_KEY is configured: AI-generated report using Claude
        - If ANTHROPIC_API_KEY is not configured: Rule-based fallback report
    """
    # Compute statistics from database
    stats = compute_weekly_statistics(db)
    
    # Check if LLM is available
    api_key = settings.ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    
    if api_key and api_key != "your_key_here":
        # Use LLM
        report_text = generate_llm_report(stats)
        mode = "ai"
    else:
        # Use fallback
        report_text = generate_fallback_report(stats)
        mode = "fallback"
    
    return {
        "mode": mode,
        "statistics": stats,
        "report": report_text
    }
