# RAPPORT DE PROJET
## Système de Maintenance Prédictive Basé sur l'IA pour Équipements Industriels

**Nom du Projet:** PFA26 - Système de Maintenance Prédictive
**Date:** 24 août 2026
**Type:** Projet Académique Final
**Auteur:** Étudiant en IA/ML

---

## 1. RÉSUMÉ EXÉCUTIF

Ce projet présente un système complet de maintenance prédictive pour moteurs d'avion (turbofans) utilisant l'apprentissage automatique. Le système combine:

- **Un modèle ML de Random Forest** entraîné sur le dataset C-MAPSS FD001
- **Une couche de décision** avec marge de sécurité et score de santé
- **Une API FastAPI** pour les prédictions en temps réel
- **Une interface React** de style SCADA pour la visualisation
- **Une base de données PostgreSQL** pour stocker les données historiques

Le système prédit la Durée de Vie Restante (RUL) des moteurs et fournit des recommandations de maintenance basées sur des seuils de sécurité.

---

## 2. ARCHITECTURE DU SYSTÈME

### 2.1 Composants Principaux

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│  - Dashboard SCADA                                         │
│  - Liste des machines avec sparklines                      │
│  - Recommandations de maintenance                          │
│  - Page de test de prédiction manuelle                      │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                         │
│  - API REST pour les prédictions                           │
│  - Service de prédiction ML                                 │
│  - Couche de décision (marge de sécurité)                   │
│  - Base de données PostgreSQL                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              ML MODELE & ARTIFACTS                           │
│  - RandomForestRegressor (n_estimators=77, max_depth=9)     │
│  - StandardScaler pour normalisation                        │
│  - Configuration de la couche de décision                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Technologies Utilisées

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Backend** | Python | 3.8+ |
| **API Framework** | FastAPI | Latest |
| **ORM** | SQLAlchemy | Latest |
| **Base de données** | PostgreSQL | 17 |
| **Machine Learning** | scikit-learn | 1.9.0 |
| **Frontend** | React | 18 |
| **Build Tool** | Vite | 8.2.2 |
| **TypeScript** | TypeScript | 5 |

---

## 3. MODÈLE MACHINE LEARNING

### 3.1 Configuration du Modèle

**Type de modèle:** RandomForestRegressor

**Hyperparamètres finaux (vérifiés depuis les artefacts sauvegardés):**
```json
{
  "n_estimators": 77,
  "max_depth": 9,
  "min_samples_split": 10,
  "min_samples_leaf": 7,
  "max_features": "log2",
  "random_state": 42
}
```

**Caractéristiques (18 features):**
- 3 paramètres de réglage: setting_1, setting_2, setting_3
- 15 capteurs: sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9, sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21
- **IMPORTANT:** relative_cycle EXCLU (vérification de fuite de données)

### 3.2 Processus d'Entraînement

1. **Prétraitement des données:**
   - Suppression des capteurs constants (sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19)
   - Suppression de relative_cycle (fuite de données potentielle)
   - Normalisation StandardScaler

2. **Optimisation des hyperparamètres:**
   - Méthode: RandomizedSearchCV avec 50 itérations
   - Modèle de base: n_estimators=100, max_depth=15
   - Modèle optimisé: n_estimators=77, max_depth=9

3. **Validation:**
   - Validation croisée sur le dataset d'entraînement
   - Évaluation sur le test officiel FD001

---

## 4. MÉTRIQUES DE PERFORMANCE

### 4.1 Résultats de Performance (Vérifiés)

| Métrique | Entraînement | Validation | Test Interne | Test Officiel |
|----------|--------------|------------|---------------|---------------|
| **RMSE** | 38.11 cycles | 41.80 cycles | 45.41 cycles | **31.73 cycles** |
| **MAE** | 26.37 cycles | 31.72 cycles | 33.23 cycles | **23.39 cycles** |
| **R²** | 0.69 | 0.62 | 0.59 | **0.42** |

### 4.2 Analyse du Surapprentissage

**Ratios de surapprentissage:**
- Ratio Validation/Entraînement: 1.10
- Ratio Test/Entraînement: 1.19

**Interprétation:**
- ✅ Généralisation saine (ratios < 1.5)
- Le modèle montre un surapprentissage minimal
- Les performances de validation et de test sont proches de l'entraînement

### 4.3 Impact de la Fuite de Données

| Modèle | relative_cycle | RMSE Validation |
|--------|----------------|-----------------|
| Original (avec fuite) | OUI | 25.47 cycles |
| Déploiement sûr (sans fuite) | NON | **41.82 cycles** |
| Optimisé (sans fuite) | NON | **41.80 cycles** |

**Conclusion:** La suppression de relative_cycle augmente le RMSE de 25.47 → 41.82 cycles (dégradation de 64.2%), mais élimine la fuite de données potentielle.

---

## 5. COUCHE DE DÉCISION

### 5.1 Configuration

**Marge de sécurité:** 49 cycles (75ème percentile des erreurs positives)

**Seuils de maintenance:**
- **CRITIQUE:** RUL ≤ 20 cycles
- **MAINTENANCE RECOMMANDÉE:** 20 < RUL ≤ 50 cycles
- **SURVEILLANCE:** 50 < RUL ≤ 100 cycles
- **NORMAL:** RUL > 100 cycles

**Score de santé:**
- Méthode: Échelle linéaire
- Max RUL pour normalisation: 200 cycles
- Plage: 0-100
- Formule: `health_score = (effective_rul / 200) * 100` (écrêté 0-100)

### 5.2 Formule de Décision

```
1. RUL prédit → ML model
2. RUL effectif = RUL prédit - 49 (marge de sécurité)
3. Score de santé = RUL effectif / 200 * 100 (écrêté 0-100)
4. Statut basé sur RUL effectif selon seuils
```

### 5.3 Analyse de Biais

**Statistiques d'erreur (validation):**
- Erreur moyenne: 6.93 cycles (surestimation)
- Erreur médiane: 6.31 cycles
- Écart-type: 41.22 cycles
- Taux de surestimation: 61.83%
- Taux de sous-estimation: 38.17%

**Marges de sécurité (percentiles des erreurs positives):**
- 50ème percentile: 25.35 cycles
- 75ème percentile: 49.87 cycles
- 90ème percentile: 69.25 cycles
- 95ème percentile: 76.94 cycles

---

## 6. API BACKEND

### 6.1 Endpoints Principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/v1/health` | GET | Vérification de santé de l'API |
| `/api/v1/machines/` | GET | Liste de toutes les machines |
| `/api/v1/machines/{id}` | GET | Détails d'une machine spécifique |
| `/api/v1/predictions/` | GET | Liste de toutes les prédictions |
| `/api/v1/predictions/machine/{machine_id}` | GET | Prédictions pour une machine |
| `/api/v1/predict/` | POST | Prédiction à partir de données capteurs |
| `/api/v1/maintenance/summary` | GET | Résumé des recommandations |
| `/api/v1/maintenance/upcoming` | GET | Maintenance à venir |

### 6.2 Service de Prédiction

Le service de prédiction:
1. Charge le modèle ML entraîné (`final_rul_model.joblib`)
2. Charge le scaler (`preprocessing_pipeline.joblib`)
3. Charge la configuration de décision (`decision_layer_config.json`)
4. Normalise les données d'entrée
5. Prédit le RUL
6. Applique la couche de décision (marge de sécurité, score de santé, statut)

---

## 7. INTERFACE FRONTEND

### 7.1 Pages Principales

**1. Dashboard:**
- Statistiques globales (nombre de machines, distribution des statuts)
- Graphiques de distribution RUL
- Alertes de maintenance
- Score de santé moyen

**2. Machines:**
- Liste de toutes les machines avec:
  - ID de machine
  - RUL prédit
  - Score de santé
  - Sparkline de tendance (10 derniers points)
  - Statut de maintenance
  - Dernière mise à jour
- Filtres par statut et recherche
- Lien vers les détails de chaque machine

**3. Maintenance:**
- Recommandations de maintenance
- Liste des machines nécessitant une attention
- Priorisation par statut (CRITIQUE > MAINTENANCE > SURVEILLANCE)
- Date estimée de maintenance

**4. Test Prediction (NOUVEAU):**
- Formulaire de saisie manuelle des 18 capteurs
- Sélection de machine
- Boutons "Exemple Sain" et "Exemple Critique" pour remplissage rapide
- Affichage des résultats de prédiction:
  - RUL prédit
  - RUL effectif
  - Score de santé
  - Statut de maintenance

### 7.2 Style SCADA

L'interface utilise un style industriel SCADA:
- Palette de couleurs sombres (gris, bleu foncé)
- Badges de statut colorés (vert, orange, rouge)
- Graphiques sparkline pour les tendances
- Typographie monospace pour les données
- Responsive design

---

## 8. BASE DE DONNÉES

### 8.1 Schéma

**Table `machines`:**
- id (PK)
- name
- description
- location
- created_at
- updated_at

**Table `sensor_readings`:**
- id (PK)
- machine_id (FK)
- cycle
- timestamp
- 18 colonnes de capteurs (setting_1-3, sensor_2,3,4,6,7,8,9,11,12,13,14,15,17,20,21)

**Table `predictions`:**
- id (PK)
- machine_id (FK)
- sensor_reading_id (FK)
- timestamp
- predicted_rul
- effective_rul
- health_score
- maintenance_status
- safety_margin_applied

### 8.2 Données de Démonstration

Le script `seed_database.py` crée:
- **8 machines** avec des noms réalistes (Turbofan Engine #1-8)
- **10 lectures de capteurs** par machine (pour les sparklines)
- **10 prédictions** par machine (avec tendance de dégradation)
- **Distribution équilibrée:**
  - 5 machines NORMAL
  - 2 machines SURVEILLANCE
  - 1 machine CRITIQUE

Toutes les prédictions sont mathématiquement cohérentes avec la formule de la couche de décision.

---

## 9. ÉVALUATION SUR TEST OFFICIEL

### 9.1 Méthodologie

Le script `ml/compare_predictions_vs_truth.py`:
1. Charge le modèle ML sauvegardé
2. Charge le dataset de test officiel FD001
3. Extrait le dernier cycle pour chaque moteur (100 moteurs)
4. Fait des prédictions
5. Compare avec les valeurs de vérité terrain
6. Calcule les métriques (RMSE, MAE, R²)
7. Génère un scatter plot et un tableau CSV

### 9.2 Résultats

**Métriques officielles (vérifiées):**
- RMSE: **31.73 cycles**
- MAE: **23.39 cycles**
- R²: **0.42**

**Fichiers générés:**
- `ml/results/predictions_vs_truth.png` - Scatter plot
- `ml/results/predictions_vs_truth.csv` - Tableau de comparaison (100 moteurs)

### 9.3 Explication du Paradoxe RMSE/R²

**Observation:**
- RMSE officiel (31.73) < RMSE validation (41.80)
- R² officiel (0.42) < R² validation (0.62)

**Cause racine:** Distribution RUL différente
- Validation: RUL 0-286 cycles (écart-type 67.98)
- Test officiel: RUL 7-145 cycles (écart-type 41.56)
- Ratio de variance: 0.37 (test a 37% de la variance de validation)

**Explication:**
- Plus faible variance → plus faible potentiel d'erreurs importantes → RMSE plus bas
- Plus faible variance → plus faible SS_tot → même SS_res donne R² plus bas
- Ce phénomène est connu en prédiction RUL et reflète les caractéristiques du test

---

## 10. DÉPLOIEMENT ET UTILISATION

### 10.1 Installation

**Prérequis:**
- Python 3.8+
- Node.js 16+
- PostgreSQL 17

**Étapes:**
1. Cloner le repository
2. Configurer la base de données PostgreSQL
3. Installer les dépendances Python (backend)
4. Installer les dépendances npm (frontend)
5. Exécuter `seed_database.py` pour peupler la base
6. Démarrer le backend: `uvicorn app.main:app --reload --port 8000`
7. Démarrer le frontend: `npm run dev`
8. Accéder à http://localhost:5173

### 10.2 Utilisation en Démonstration

**Flux de présentation recommandé:**
1. **Dashboard** - Vue d'ensemble du système
2. **Machines** - Liste avec prédictions individuelles et sparklines
3. **Maintenance** - Recommandations actionnables
4. **Test Prediction** - Démo interactive:
   - Charger "Exemple Sain" → Prédire → Statut NORMAL/SURVEILLANCE
   - Charger "Exemple Critique" → Prédire → Statut CRITIQUE

---

## 11. POINTS FORTS DU PROJET

### 11.1 Techniques
- ✅ Modèle ML optimisé avec hyperparamètres validés
- ✅ Vérification de fuite de données PASSED
- ✅ Couche de décision avec marge de sécurité conservatrice
- ✅ Métriques de performance cohérentes et vérifiées
- ✅ Généralisation saine (ratios de surapprentissage < 1.5)

### 11.2 Ingénierie
- ✅ Architecture full-stack complète (Backend + Frontend + BDD)
- ✅ API REST bien structurée
- ✅ Interface utilisateur SCADA professionnelle
- ✅ Base de données relationnelle avec données historiques
- ✅ Sparklines pour visualisation des tendances

### 11.3 Qualité du Code
- ✅ Code modulaire et maintenable
- ✅ Utilisation de types TypeScript
- ✅ Configuration centralisée
- ✅ Documentation complète
- ✅ Tests d'évaluation sur dataset officiel

---

## 12. LIMITATIONS ET FUTUR

### 12.1 Limitations Actuelles
- Dataset C-MAPSS FD001 uniquement (pas généralisé à FD002-FD004)
- Score de santé basé sur une simple échelle linéaire
- Pas de modèle de détection d'anomalies en temps réel
- Pas d'intégration avec des systèmes SCADA réels

### 12.5 Améliorations Possibles
- Entraînement sur tous les datasets FD001-FD004
- Utilisation de LSTM/GRU pour dépendances temporelles
- Détection d'anomalies avec isolation forest
- Intégration IoT pour données en temps réel
- Interface mobile pour techniciens
- Système d'alertes par email/SMS
- Tableaux de bord personnalisables

---

## 13. CONCLUSION

Ce projet démontre un système complet de maintenance prédictive avec:

1. **Modèle ML performant:** RMSE de 31.73 cycles sur le test officiel
2. **Couche de décision robuste:** Marge de sécurité de 49 cycles basée sur l'analyse de biais
3. **Architecture production-ready:** API REST, base de données, interface utilisateur
4. **Évaluation rigoureuse:** Métriques vérifiées depuis les artefacts sauvegardés
5. **Utilité pratique:** Recommandations de maintenance actionnables

Le système est prêt pour une démonstration académique et pourrait être étendu pour un déploiement en production avec des données réelles.

---

## 14. FICHIERS CLÉS

### Documentation
- `docs/FINAL_VERIFIED_RESULTS.md` - Métriques vérifiées
- `docs/FOLLOW_UP_ANALYSIS.md` - Analyse détaillée
- `PROJECT_SETUP_GUIDE.md` - Guide d'installation
- `RAPPORT_PROJET.md` - Ce rapport

### ML Artifacts
- `models/final_rul_model.joblib` - Modèle Random Forest
- `models/preprocessing_pipeline.joblib` - StandardScaler
- `models/model_metadata.json` - Métadonnées du modèle

### Résultats d'Évaluation
- `ml/results/predictions_vs_truth.png` - Scatter plot
- `ml/results/predictions_vs_truth.csv` - Tableau de comparaison
- `ml/results/computed_training_metrics.json` - Métriques d'entraînement
- `ml/results/decision_layer_config.json` - Configuration décision

### Code Source
- `backend/app/main.py` - Application FastAPI
- `backend/app/services/prediction_service.py` - Service de prédiction
- `frontend/src/pages/` - Pages React
- `ml/compare_predictions_vs_truth.py` - Script d'évaluation

---

**Fin du Rapport de Projet**
