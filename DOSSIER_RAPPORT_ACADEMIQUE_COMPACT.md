# DOSSIER COMPACT POUR RAPPORT ACADÉMIQUE (33-35 PAGES)

## INSTRUCTIONS GÉNÉRALES
- **Pages cibles:** 33-35 pages
- **Langue:** Français académique
- **Structure:** Suivre exactement le template fourni
- **Contenu:** Basé UNIQUEMENT sur le projet réel

## 1. INFORMATIONS GÉNÉRALES

**Titre:** Système de Maintenance Prédictive Basé sur l'IA pour Équipements Industriels (PFA26)

**Problème:** Maintenance préventive (coûteuse) vs corrective (pannes) → Solution: maintenance prédictive basée sur l'IA

**Objectif:** Prédire la Durée de Vie Restante (RUL) de moteurs d'avion et fournir des recommandations de maintenance

**Dataset:** NASA C-MAPSS FD001 (100 moteurs entraînement, 100 test)

**Résultats obtenus:**
- Modèle Random Forest (n_estimators=77, max_depth=9)
- RMSE validation: 41.80 cycles, RMSE test officiel: 31.73 cycles
- API FastAPI avec 13 endpoints
- Interface React avec 4 pages
- Base de données PostgreSQL peuplée

## 2. INTRODUCTION GÉNÉRALE (1-2 pages)

**Contexte:** Maintenance industrielle traditionnelle (préventive/coûteuse, corrective/risquée)

**Problématique:** Comment prédire la RUL avec précision suffisante pour guider les décisions de maintenance ?

**Questions:** Sélection features ? Choix modèle ? Éviter fuite données ? Transformer prédiction en recommandation ? Intégration système ?

**Plan:** Contexte → Analyse fonctionnelle → Architecture → Implémentation → Résultats

## 3. CHAPITRE 1: CONTEXTE ET PROBLÉMATIQUE (4-5 pages)

### 3.1 Maintenance Industrielle
- Maintenance préventive: interventions programmées, coûteuses
- Maintenance corrective: après panne, arrêts imprévus
- Maintenance prédictive: basée sur état réel, optimale

### 3.2 Concepts Clés
- **RUL (Remaining Useful Life):** Temps restant avant défaillance
- **Approches:** Modèles physiques, data-driven, hybrides
- **Algorithmes ML:** Random Forest, XGBoost, LSTM, SVM

### 3.3 Dataset NASA C-MAPSS FD001
- 100 moteurs entraînement (cycles complets)
- 100 moteurs test (tronqués)
- 26 variables: engine_id, cycle, 3 settings, 21 sensors
- Capteurs constants exclus: sensor_1,5,10,16,18,19

### 3.4 Problématique Spécifique
Développer un système complet intégrant: modèle ML précis, couche de décision, API REST, interface utilisateur, base de données

## 4. CHAPITRE 2: ANALYSE FONCTIONNELLE (4-5 pages)

### 4.1 Acteurs
- Opérateur de maintenance: surveillance, interventions
- Ingénieur de fiabilité: analyse tendances, optimisation
- Responsable d'équipements: supervision, priorisation

### 4.2 Cas d'Utilisation Principaux
- **UC1:** Surveiller état système (Dashboard)
- **UC2:** Consulter détails machine (Liste + Détails)
- **UC3:** Consulter recommandations maintenance (Page Maintenance)
- **UC4:** Effectuer prédiction manuelle (Test Prediction)

### 4.3 Exigences Fonctionnelles
- **EF1:** Prédiction RUL (18 features → RUL + score + statut)
- **EF2:** Couche de décision (marge 49 cycles, seuils 20/50/100)
- **EF3:** Dashboard (statistiques, graphiques)
- **EF4:** Liste machines (sparklines, filtres)
- **EF5:** Recommandations maintenance (priorisées)
- **EF6:** Test prédiction (formulaire + exemples)
- **EF7:** Gestion machines (CRUD)
- **EF8:** Stockage données (PostgreSQL)

### 4.4 Exigences Non-Fonctionnelles
- **ENF1 Performance:** Réponse < 2s
- **ENF2 Fiabilité:** Disponibilité > 95%
- **ENF3 Maintenabilité:** Code modulaire
- **ENF4 Utilisabilité:** Interface SCADA intuitive
- **ENF5 Scalabilité:** Support 100+ machines
- **ENF6 Sécurité:** Validation entrées (pas d'authentification implémentée)

## 5. CHAPITRE 3: ARCHITECTURE (5-6 pages)

### 5.1 Architecture 3-Tiers
```
Frontend (React/TS) → API (FastAPI) → BDD (PostgreSQL) → ML (Random Forest)
```

### 5.2 Frontend
- React 19.2.8, TypeScript 6.0.2, Vite 8.2.0
- TailwindCSS 4.3.3, Recharts 3.10.1, Axios 1.19.0
- Pages: Dashboard, Machines, Maintenance, TestPrediction
- Composants: Header, Sidebar, Sparkline
- État local (pas Redux)

### 5.3 Backend
- FastAPI 0.104.1, SQLAlchemy 2.0.23, Pydantic 2.5.0
- Routes: health, machines, predictions, maintenance, sensor_readings
- Services: prediction_service (ML integration)
- Models: Machine, SensorReading, Prediction
- Schemas: Pydantic validation

### 5.4 Base de Données
- PostgreSQL 17
- Tables: machines, sensor_readings, predictions
- Relations: machines 1:N sensor_readings, machines 1:N predictions

### 5.5 Architecture ML
- Pipeline: Chargement → Prétraitement → Split → Normalisation → Entraînement → Évaluation
- Modèle: RandomForestRegressor (n_estimators=77, max_depth=9)
- Features: 18 (3 settings + 15 sensors, sans relative_cycle)
- Couche décision: Marge 49 cycles, score santé 0-100, seuils 20/50/100

## 6. CHAPITRE 4: IMPLÉMENTATION (5-6 pages)

### 6.1 Environnement
- Python 3.8+, Node.js 16+, PostgreSQL 17
- Backend: venv + requirements.txt
- Frontend: npm install

### 6.2 Implémentation ML
**Prétraitement:**
- Suppression capteurs constants (6 capteurs)
- Calcul RUL = max_cycle - current_cycle
- Suppression relative_cycle (fuite de données)
- Split moteurs: 70 train / 15 val / 15 test (seed=42)
- StandardScaler normalisation

**Entraînement:**
- Baseline: n_estimators=100, max_depth=15
- Optimisation: RandomizedSearchCV (50 itérations)
- Final: n_estimators=77, max_depth=9, min_samples_split=10, min_samples_leaf=7, max_features=log2

**Évaluation:**
- Validation: RMSE 41.80, MAE 31.72, R² 0.62
- Test officiel: RMSE 31.73, MAE 23.39, R² 0.42
- Surapprentissage: ratios 1.10/1.19 (sains)

**Couche décision:**
- Marge sécurité: 49 cycles (75ème percentile erreurs positives)
- Biais: surestimation moyenne +6.93 cycles (61.83%)
- Score santé: (effective_rul / 200) * 100
- Seuils: CRITICAL ≤20, MAINTENANCE 20-50, MONITOR 50-100, NORMAL >100

### 6.3 Implémentation Backend
- main.py: Application FastAPI + CORS
- models/__init__.py: SQLAlchemy models
- routes/: 5 routers (health, machines, predictions, maintenance, sensor_readings)
- services/prediction_service.py: ML integration
- schemas/__init__.py: Pydantic validation
- seed_database.py: 8 machines, 80 lectures, 80 prédictions

### 6.4 Implémentation Frontend
- App.tsx: React Router configuration
- pages/Dashboard.tsx: Statistiques + graphiques Recharts
- pages/Machines.tsx: Liste + sparklines
- pages/Maintenance.tsx: Recommandations priorisées
- pages/TestPrediction.tsx: Formulaire + exemples
- services/api.ts: Axios client
- components/: Header, Sidebar, Sparkline

## 7. CHAPITRE 5: RÉSULTATS (5-6 pages)

### 7.1 Résultats ML
| Métrique | Entraînement | Validation | Test Officiel |
|----------|--------------|------------|---------------|
| RMSE | 38.11 | 41.80 | 31.73 |
| MAE | 26.37 | 31.72 | 23.39 |
| R² | 0.69 | 0.62 | 0.42 |

**Analyse surapprentissage:** Ratios < 1.5 → généralisation saine

**Paradoxe RMSE/R²:** Test officiel RMSE plus bas (31.73 vs 41.80) mais R² plus bas (0.42 vs 0.62) → distribution RUL différente (variance test = 37% variance validation)

### 7.2 Résultats Système
- API: 13 endpoints opérationnels
- Frontend: 4 pages fonctionnelles
- BDD: 8 machines, 80 lectures, 80 prédictions
- Performance: Réponse estimée < 2s

### 7.3 Tests
**Unitaires (4):** test_health_check, test_create_machine, test_get_machines, test_prediction_endpoint

**Manuels:** Test prédiction sain/critique ✅, Dashboard ✅, Liste machines ✅

**Validation ML:** Check fuite PASSED, test officiel RMSE 31.73

### 7.4 Problèmes Résolus
1. **Fuite données relative_cycle:** Suppression → RMSE 25.47→41.82 (acceptable pour déploiement)
2. **Surapprentissage time-series:** Suppression features → ratios sains
3. **Biais surestimation:** Marge sécurité 49 cycles (75ème percentile)
4. **Incohérences documentation:** Vérification artefacts sauvegardés

## 8. CONCLUSION GÉNÉRALE (1-2 pages)

**Synthèse:** Système complet intégrant ML Random Forest (RMSE 31.73), couche décision (marge 49 cycles), API FastAPI (13 endpoints), interface React (4 pages), BDD PostgreSQL.

**Apports:** Étude fuite données, architecture full-stack, intégration ML-web, couche décision justifiée.

**Limitations:** FD001 uniquement, RMSE 31.73 cycles, pas authentification, déploiement local, tests limités.

**Perspectives:** FD002-FD004, LSTM/GRU, authentification, IoT temps réel, cloud déploiement, tests E2E.

## 9. RÉFÉRENCES (1-2 pages)

**Académiques:**
- Saxena et al. (2008) - C-MAPSS Dataset
- Breiman (2001) - Random Forests
- Pedregosa et al. (2011) - Scikit-learn

**Techniques:**
- FastAPI, React, PostgreSQL, scikit-learn documentation

**Projet:**
- RAPPORT_PROJET.md, FINAL_VERIFIED_RESULTS.md, code source

## 10. FIGURES RECOMMANDÉES

1. **Architecture globale** (Chapitre 3)
2. **Pipeline ML** (Chapitre 4)
3. **Couche décision** (Chapitre 3 ou 4)
4. **Schéma BDD** (Chapitre 3)
5. **Dashboard screenshot** (Chapitre 4)
6. **Test Prediction screenshot** (Chapitre 4)
7. **Scatter plot predictions vs truth** (Chapitre 5)
8. **Workflow prédiction** (Chapitre 3)

## 11. TABLEAUX RECOMMANDÉS

1. **Technologies** (Chapitre 3)
2. **Métriques performance** (Chapitre 5)
3. **Hyperparamètres** (Chapitre 4)
4. **Features modèle** (Chapitre 4)
5. **Configuration couche décision** (Chapitre 4)
6. **Endpoints API** (Chapitre 3)
7. **Tables BDD** (Chapitre 3)
8. **Problèmes et solutions** (Chapitre 5)

## 12. ANNEXES RECOMMANDÉES

- Code source key sections (prediction_service.py, maintenance_decision.py)
- Scatter plot (ml/results/predictions_vs_truth.png)
- Configuration files (model_metadata.json, decision_layer_config.json)
