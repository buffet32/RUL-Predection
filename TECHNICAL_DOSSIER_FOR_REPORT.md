# DOSSIER TECHNIQUE COMPLET
## Système de Maintenance Prédictive Basé sur l'IA pour Équipements Industriels

**Projet:** PFA26 - Système de Maintenance Prédictive
**Date:** 24 août 2026
**Objectif:** Document technique complet pour la rédaction d'un rapport académique

---

## 1. APERÇU DU PROJET

### 1.1 Nom du Projet
PFA26 - Système de Maintenance Prédictive Basé sur l'IA pour Équipements Industriels

### 1.2 Objectif du Projet
Développer un système complet de maintenance prédictive pour moteurs d'avion (turbofans) utilisant l'apprentissage automatique pour prédire la Durée de Vie Restante (RUL - Remaining Useful Life) et fournir des recommandations de maintenance basées sur des seuils de sécurité.

### 1.3 Problème Technique/Résolu
**Problème:** La maintenance industrielle traditionnelle est soit préventive (coûteuse, interventions inutiles) soit corrective (pannes imprévues, arrêts de production).

**Solution:** Un système de maintenance prédictive basé sur l'IA qui:
- Analyse les données de capteurs en temps réel
- Prédit la durée de vie restante des équipements
- Fournit des recommandations de maintenance personnalisées
- Applique une marge de sécurité conservatrice pour éviter les pannes

### 1.4 Contexte du Projet
- Projet académique final (PFA26)
- Basé sur le dataset NASA C-MAPSS FD001 (turbofan engines)
- Développement full-stack (backend + frontend + ML)
- Architecture production-ready avec API REST et base de données

### 1.5 Utilisateurs Cibles
- Opérateurs de maintenance industrielle
- Ingénieurs de fiabilité
- Techniciens de terrain
- Responsables d'équipements

### 1.6 Cas d'Utilisation Principaux
1. **Surveillance en temps réel:** Visualiser l'état de santé des équipements
2. **Prédiction de RUL:** Estimer la durée de vie restante à partir des données capteurs
3. **Planification de maintenance:** Recevoir des recommandations basées sur les prédictions
4. **Test manuel:** Saisir manuellement des données capteurs pour tester le système

### 1.7 Statut Actuel du Projet
- ✅ Système entièrement fonctionnel
- ✅ Modèle ML entraîné et optimisé
- ✅ API REST opérationnelle
- ✅ Interface utilisateur complète
- ✅ Base de données peuplée avec données de démonstration
- ✅ Évaluation sur dataset officiel FD001 complétée

### 1.8 Fonctionnalités Principales
- Dashboard avec statistiques globales et graphiques
- Liste des machines avec prédictions individuelles et sparklines
- Page de maintenance avec recommandations priorisées
- Page de test de prédiction manuelle avec exemples pré-remplis
- API REST pour les prédictions en temps réel
- Couche de décision avec marge de sécurité et score de santé

---

## 2. EXIGENCES FONCTIONNELLES

### 2.1 Fonctionnalités Implémentées

#### F1: Dashboard de Surveillance
- **Nom:** Dashboard principal
- **Description:** Vue d'ensemble du système avec statistiques et graphiques
- **Interaction utilisateur:** Navigation automatique au chargement
- **Entrées:** Aucune (chargement automatique depuis l'API)
- **Traitement:** Récupération des données machines, prédictions, et résumé maintenance via API
- **Sorties:** 
  - Statistiques globales (nombre total de machines, distribution des statuts)
  - Graphiques de distribution RUL (camembert, histogramme)
  - Tableau des 10 dernières prédictions
- **Modules/Fichiers:** `frontend/src/pages/Dashboard.tsx`
- **Statut:** ✅ Pleinement implémenté

#### F2: Liste des Machines
- **Nom:** Liste des équipements
- **Description:** Liste de toutes les machines avec leurs prédictions et tendances
- **Interaction utilisateur:** Navigation via menu latéral, filtres par statut, recherche
- **Entrées:** Aucune (chargement automatique)
- **Traitement:** Récupération des machines et prédictions, calcul des sparklines
- **Sorties:**
  - Tableau avec ID machine, RUL prédit, score de santé, statut
  - Sparklines montrant la tendance des 10 derniers cycles
  - Liens vers les détails de chaque machine
- **Modules/Fichiers:** `frontend/src/pages/Machines.tsx`, `frontend/src/components/Sparkline.tsx`
- **Statut:** ✅ Pleinement implémenté

#### F3: Recommandations de Maintenance
- **Nom:** Planificateur de maintenance
- **Description:** Liste des machines nécessitant une maintenance avec priorisation
- **Interaction utilisateur:** Navigation via menu latéral, visualisation par statut
- **Entrées:** Aucune (chargement automatique)
- **Traitement:** Récupération des prédictions, filtrage par statut de maintenance
- **Sorties:**
  - Liste priorisée (CRITIQUE > MAINTENANCE_RECOMMANDÉE > SURVEILLANCE)
  - Date estimée de maintenance
  - Actions recommandées pour chaque statut
- **Modules/Fichiers:** `frontend/src/pages/Maintenance.tsx`
- **Statut:** ✅ Pleinement implémenté

#### F4: Test de Prédiction Manuel
- **Nom:** Test de prédiction interactif
- **Description:** Formulaire pour saisir manuellement des données capteurs et tester le système
- **Interaction utilisateur:**
  - Sélection de machine
  - Saisie des 18 valeurs capteurs
  - Boutons "Exemple Sain" et "Exemple Critique" pour remplissage rapide
  - Bouton "Predict" pour lancer la prédiction
- **Entrées:**
  - ID machine (sélection)
  - Numéro de cycle
  - 18 valeurs capteurs (3 settings + 15 capteurs)
- **Traitement:**
  - Validation des entrées
  - Appel API POST /api/v1/predictions/
  - Application de la couche de décision
- **Sorties:**
  - RUL prédit
  - RUL effectif (après marge de sécurité)
  - Score de santé (0-100)
  - Statut de maintenance
  - Explication du statut
- **Modules/Fichiers:** `frontend/src/pages/TestPrediction.tsx`
- **Statut:** ✅ Pleinement implémenté

#### F5: Service de Prédiction ML
- **Nom:** Moteur de prédiction
- **Description:** Service backend qui charge le modèle ML et effectue les prédictions
- **Interaction utilisateur:** Appelé automatiquement par l'API
- **Entrées:** Dictionnaire avec 18 valeurs capteurs
- **Traitement:**
  - Chargement du modèle Random Forest entraîné
  - Chargement du scaler StandardScaler
  - Chargement de la configuration de la couche de décision
  - Normalisation des données d'entrée
  - Prédiction du RUL
  - Application de la couche de décision (marge de sécurité, score de santé, statut)
- **Sorties:** Dictionnaire avec predicted_rul, effective_rul, health_score, maintenance_status, safety_margin_applied
- **Modules/Fichiers:** `backend/app/services/prediction_service.py`
- **Statut:** ✅ Pleinement implémenté

#### F6: API REST de Prédiction
- **Nom:** Endpoint de prédiction
- **Description:** API REST pour créer des prédictions à partir de données capteurs
- **Interaction utilisateur:** Appel HTTP POST
- **Entrées:** JSON avec machine_id, cycle, et 18 valeurs capteurs
- **Traitement:**
  - Vérification de l'existence de la machine
  - Appel du service de prédiction
  - Stockage de la lecture capteur
  - Stockage de la prédiction
- **Sorties:** JSON avec la prédiction complète
- **Modules/Fichiers:** `backend/app/routes/predictions.py`
- **Statut:** ✅ Pleinement implémenté

#### F7: Base de Données de Machines
- **Nom:** Gestion des équipements
- **Description:** CRUD complet pour les machines
- **Interaction utilisateur:** Appels API REST
- **Entrées:** MachineCreate (name, description, location)
- **Traitement:** Opérations CRUD via SQLAlchemy
- **Sorties:** MachineResponse avec tous les champs
- **Modules/Fichiers:** `backend/app/routes/machines.py`, `backend/app/models/__init__.py`
- **Statut:** ✅ Pleinement implémenté

#### F8: Peuplement de la Base de Données
- **Nom:** Script de seeding
- **Description:** Script pour peupler la base de données avec des données de démonstration
- **Interaction utilisateur:** Exécution manuelle du script
- **Entrées:** Aucune (données générées automatiquement)
- **Traitement:**
  - Création de 8 machines avec noms réalistes
  - Génération de 10 lectures capteurs par machine
  - Génération de 10 prédictions par machine avec tendance de dégradation
  - Distribution équilibrée: 5 NORMAL, 2 SURVEILLANCE, 1 CRITIQUE
- **Sorties:** Base de données peuplée avec 80 lectures capteurs et 80 prédictions
- **Modules/Fichiers:** `backend/seed_database.py`
- **Statut:** ✅ Pleinement implémenté

---

## 3. ARCHITECTURE TECHNIQUE

### 3.1 Architecture Globale

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

### 3.2 Frontend

**Framework:** React 19.2.8 avec TypeScript 6.0.2
**Build Tool:** Vite 8.2.0
**Styling:** TailwindCSS 4.3.3
**Routing:** React Router DOM 7.18.2
**Charts:** Recharts 3.10.1
**HTTP Client:** Axios 1.19.0

**Structure:**
- `src/pages/` - Pages principales (Dashboard, Machines, Maintenance, TestPrediction)
- `src/components/` - Composants réutilisables (Header, Sidebar, Sparkline)
- `src/services/` - Client API (api.ts)
- `src/types/` - Types TypeScript
- `src/layouts/` - Layout principal avec navigation

**État:** Gestion d'état locale avec useState, pas de Redux

### 3.3 Backend

**Framework:** FastAPI 0.104.1
**Serveur ASGI:** Uvicorn 0.24.0
**ORM:** SQLAlchemy 2.0.23
**Base de données:** PostgreSQL 17
**Validation:** Pydantic 2.5.0
**ML Model Loading:** joblib 1.3.2

**Structure:**
- `app/main.py` - Application FastAPI principale
- `app/config.py` - Configuration et variables d'environnement
- `app/database.py` - Connexion à la base de données
- `app/models/` - Modèles SQLAlchemy (Machine, SensorReading, Prediction)
- `app/routes/` - Routes API (health, machines, predictions, maintenance, sensor_readings)
- `app/services/` - Logique métier (prediction_service.py)
- `app/schemas/` - Schémas Pydantic pour validation

**Middleware:** CORS configuré pour autoriser toutes les origines (à configurer pour production)

### 3.4 Base de Données

**Technologie:** PostgreSQL 17
**ORM:** SQLAlchemy 2.0.23

**Tables:**

1. **machines**
   - id (PK, Integer, auto-increment)
   - name (String, unique, not null)
   - description (String, nullable)
   - location (String, nullable)
   - created_at (DateTime, default=utcnow)
   - updated_at (DateTime, default=utcnow, onupdate=utcnow)
   - Relations: One-to-many avec sensor_readings et predictions

2. **sensor_readings**
   - id (PK, Integer, auto-increment)
   - machine_id (FK, Integer, not null)
   - cycle (Integer, not null)
   - timestamp (DateTime, default=utcnow)
   - setting_1, setting_2, setting_3 (Float, not null)
   - sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9 (Float, not null)
   - sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21 (Float, not null)
   - Relations: Many-to-one avec machines, One-to-one avec predictions

3. **predictions**
   - id (PK, Integer, auto-increment)
   - machine_id (FK, Integer, not null)
   - sensor_reading_id (FK, Integer, nullable)
   - timestamp (DateTime, default=utcnow)
   - predicted_rul (Float, not null)
   - effective_rul (Float, not null)
   - health_score (Float, not null)
   - maintenance_status (String, not null)
   - safety_margin_applied (Float, not null)
   - Relations: Many-to-one avec machines

**Flux de données:**
1. Machine créée dans la table machines
2. Lectures capteurs enregistrées dans sensor_readings
3. Prédiction générée et stockée dans predictions avec référence à sensor_reading

### 3.5 APIs

**Architecture:** REST API avec FastAPI
**Base URL:** http://localhost:8000/api/v1
**Documentation:** Auto-générée par FastAPI (/docs)

**Communication:**
- Frontend → Backend: HTTP/JSON via Axios
- Backend → ML Model: Chargement local via joblib
- Backend → Database: SQLAlchemy ORM

### 3.6 Authentification/Authorization
**Statut:** Information non disponible dans le projet (pas d'authentification implémentée)

### 3.7 Services Externes
**Statut:** Aucun service externe utilisé (tout est local)

### 3.8 Composants IA/ML
**Voir section 10 pour détails complets**

### 3.9 Flux de Données Complet

```
Utilisateur
  ↓
Interface React (TestPrediction)
  ↓
API Client (Axios)
  ↓
POST /api/v1/predictions/
  ↓
FastAPI Route Handler
  ↓
Prediction Service
  ↓
Chargement Modèle ML (Random Forest)
  ↓
Chargement Scaler (StandardScaler)
  ↓
Chargement Couche Décision
  ↓
Normalisation des données
  ↓
Prédiction RUL
  ↓
Application Couche Décision
  ↓
Stockage en Base de Données
  ↓
Réponse JSON au Frontend
  ↓
Affichage des résultats
```

---

## 4. TECHNOLOGIES ET OUTILS

### 4.1 Langages de Programmation

**Python 3.8+**
- **Rôle:** Backend, Machine Learning
- **Utilisation:**
  - FastAPI pour l'API REST
  - scikit-learn pour le ML
  - SQLAlchemy pour l'ORM
- **Fichiers:** backend/, ml/

**TypeScript 5**
- **Rôle:** Frontend
- **Utilisation:** Développement React avec typage statique
- **Fichiers:** frontend/src/

### 4.2 Frameworks

**FastAPI 0.104.1**
- **Rôle:** Framework API REST backend
- **Pourquoi:** Performance, typage automatique, documentation auto-générée
- **Fichiers:** backend/app/main.py, backend/app/routes/

**React 19.2.8**
- **Rôle:** Framework frontend
- **Pourquoi:** Composants réutilisables, écosystème riche
- **Fichiers:** frontend/src/

**scikit-learn 1.9.0**
- **Rôle:** Machine Learning
- **Pourquoi:** Random Forest implémenté, StandardScaler
- **Fichiers:** ml/src/

### 4.3 Bibliothèques

**Backend Python:**
- **uvicorn 0.24.0** - Serveur ASGI
- **sqlalchemy 2.0.23** - ORM base de données
- **psycopg2-binary 2.9.9** - Driver PostgreSQL
- **pydantic 2.5.0** - Validation des données
- **pydantic-settings 2.1.0** - Gestion configuration
- **joblib 1.3.2** - Sérialisation modèle ML
- **numpy 1.24.3** - Calculs numériques
- **pandas 2.0.3** - Manipulation données
- **python-dotenv 1.0.0** - Variables d'environnement

**Frontend JavaScript/TypeScript:**
- **axios 1.19.0** - Client HTTP
- **react-router-dom 7.18.2** - Routing
- **recharts 3.10.1** - Graphiques
- **@tailwindcss/postcss 4.3.3** - Styling
- **autoprefixer 10.5.4** - CSS

**Machine Learning:**
- **xgboost 2.0.0** - Alternative Random Forest (non utilisé en production)
- **matplotlib 3.7.0** - Visualisations ML
- **seaborn 0.12.0** - Visualisations avancées

### 4.4 Base de Données

**PostgreSQL 17**
- **Rôle:** Stockage des données machines, capteurs, prédictions
- **Pourquoi:** Base de données relationnelle robuste, support SQL avancé
- **Fichiers:** backend/app/database.py, backend/app/models/

### 4.5 APIs

**FastAPI Auto-Documentation**
- **Rôle:** Documentation interactive API
- **URL:** http://localhost:8000/docs
- **Pourquoi:** Génération automatique Swagger UI

### 4.6 Services Cloud
**Statut:** Aucun service cloud utilisé (déploiement local)

### 4.7 Docker
**Statut:** Information non disponible dans le projet (pas de Dockerfile)

### 4.8 Git/GitHub
**Statut:** Projet n'est pas un repository Git (pas de contrôle de version)

### 4.9 Outils de Test

**pytest 7.4.3**
- **Rôle:** Tests unitaires backend
- **Utilisation:** Tests API basiques
- **Fichiers:** backend/tests/test_api.py

**httpx 0.25.1**
- **Rôle:** Client HTTP asynchrone pour tests
- **Utilisation:** TestClient FastAPI

### 4.10 Frameworks IA/ML

**scikit-learn 1.9.0**
- **Rôle:** Framework principal ML
- **Utilisation:** RandomForestRegressor, StandardScaler, RandomizedSearchCV
- **Fichiers:** ml/src/train_deployment_safe.py, ml/src/optimize_hyperparameters.py

### 4.11 Outils de Développement

**Vite 8.2.0**
- **Rôle:** Build tool et dev server frontend
- **Pourquoi:** Build rapide, HMR
- **Fichiers:** frontend/vite.config.ts

**PostCSS 8.5.26**
- **Rôle:** Transformation CSS
- **Pourquoi:** Support TailwindCSS
- **Fichiers:** frontend/postcss.config.js

### 4.12 Devin Agent
**Statut:** Information non disponible dans le projet (pas de traces explicites d'utilisation de Devin Agent dans le code ou la documentation)

---

## 5. STRUCTURE DU PROJET

### 5.1 Dossiers Principaux

**backend/**
- **app/** - Application FastAPI principale
  - `main.py` - Point d'entrée FastAPI
  - `config.py` - Configuration et variables d'environnement
  - `database.py` - Connexion base de données SQLAlchemy
  - `models/` - Modèles de base de données (Machine, SensorReading, Prediction)
  - `routes/` - Routes API (health, machines, predictions, maintenance, sensor_readings)
  - `services/` - Logique métier (prediction_service.py)
  - `schemas/` - Schémas Pydantic pour validation
- `requirements.txt` - Dépendances Python
- `seed_database.py` - Script de peuplement base de données
- `tests/` - Tests unitaires
- `venv/` - Environnement virtuel Python

**frontend/**
- `src/` - Code source React/TypeScript
  - `pages/` - Pages principales (Dashboard, Machines, Maintenance, TestPrediction, MachineDetails)
  - `components/` - Composants réutilisables (Header, Sidebar, Sparkline)
  - `services/` - Client API (api.ts)
  - `types/` - Types TypeScript
  - `layouts/` - Layout principal
  - `assets/` - Assets statiques
  - `style.css` - Styles globaux
- `public/` - Fichiers publics
- `package.json` - Dépendances npm
- `tsconfig.json` - Configuration TypeScript
- `vite.config.ts` - Configuration Vite
- `tailwind.config.js` - Configuration TailwindCSS
- `postcss.config.js` - Configuration PostCSS
- `index.html` - Point d'entrée HTML

**ml/**
- `src/` - Code source pipeline ML
  - `preprocessing.py` - Chargement et prétraitement données
  - `features.py` - Ingénierie de caractéristiques
  - `train_baseline.py` - Entraînement modèle baseline
  - `train_deployment_safe.py` - Entraînement modèle sans fuite de données
  - `train_xgboost.py` - Entraînement modèle XGBoost
  - `optimize_hyperparameters.py` - Optimisation hyperparamètres
  - `evaluate.py` - Évaluation modèles
  - `evaluate_official_test.py` - Évaluation sur test officiel
  - `evaluate_optimized_official.py` - Évaluation modèle optimisé
  - `maintenance_decision.py` - Couche de décision
  - `analyze_bias.py` - Analyse biais modèle
  - `compute_training_metrics.py` - Calcul métriques entraînement
  - `save_production_artifacts.py` - Sauvegarde artefacts production
  - `utils.py` - Fonctions utilitaires
- `data/` - Dataset (non inclus, doit être placé manuellement)
- `models/` - Modèles entraînés sauvegardés
- `results/` - Résultats d'évaluation et configurations
- `visualizations/` - Graphiques générés
- `notebooks/` - Jupyter notebooks (vide)
- `requirements.txt` - Dépendances Python ML
- `compare_predictions_vs_truth.py` - Script évaluation test officiel

**models/**
- `final_rul_model.joblib` - Modèle Random Forest final
- `preprocessing_pipeline.joblib` - Scaler StandardScaler
- `model_metadata.json` - Métadonnées modèle

**docs/**
- `FINAL_VERIFIED_RESULTS.md` - Résultats vérifiés depuis artefacts
- `FOLLOW_UP_ANALYSIS.md` - Analyse complémentaire

**racine/**
- `RAPPORT_PROJET.md` - Rapport de projet en français
- `PROJECT_SETUP_GUIDE.md` - Guide d'installation et exécution
- `DEPLOYMENT_FEATURES.md` - Documentation features déploiement
- `DATASET_ANALYSIS.md` - Analyse dataset
- `LEAKAGE_AUDIT.md` - Audit fuite de données
- `ML_RESULTS.md` - Résultats ML
- `PHASE_2_5_RESULTS.md` - Résultats phase 2.5
- `PHASE_2_6_RESULTS.md` - Résultats phase 2.6
- `PHASE_3B_RESULTS.md` - Résultats phase 3B
- `eda_analysis.py` - Script analyse exploratoire
- `requirements.txt` - Dépendances Python globales
- `.devin/` - Configuration Devin Agent

### 5.2 Fichiers Importants

**Configuration:**
- `backend/app/config.py` - Configuration backend (URLs base de données, chemins modèles)
- `frontend/.env` - Variables d'environnement frontend (URL API)
- `backend/.env` - Variables d'environnement backend (URL base de données)

**Modèles:**
- `backend/app/models/__init__.py` - Définition tables SQLAlchemy
- `models/final_rul_model.joblib` - Modèle ML entraîné
- `models/preprocessing_pipeline.joblib` - Scaler ML

**API:**
- `backend/app/main.py` - Application FastAPI
- `backend/app/routes/predictions.py` - Endpoint prédiction
- `backend/app/routes/machines.py` - Endpoint machines
- `backend/app/routes/maintenance.py` - Endpoint maintenance
- `backend/app/routes/health.py` - Endpoint santé

**Services:**
- `backend/app/services/prediction_service.py` - Service prédiction ML
- `backend/seed_database.py` - Script peuplement base de données

**Frontend:**
- `frontend/src/App.tsx` - Application React principale
- `frontend/src/pages/Dashboard.tsx` - Page dashboard
- `frontend/src/pages/Machines.tsx` - Page machines
- `frontend/src/pages/Maintenance.tsx` - Page maintenance
- `frontend/src/pages/TestPrediction.tsx` - Page test prédiction
- `frontend/src/services/api.ts` - Client API

**ML:**
- `ml/src/maintenance_decision.py` - Couche de décision
- `ml/src/train_deployment_safe.py` - Entraînement modèle sans fuite
- `ml/src/optimize_hyperparameters.py` - Optimisation hyperparamètres
- `ml/compare_predictions_vs_truth.py` - Évaluation test officiel

---

## 6. BASE DE DONNÉES

### 6.1 Technologie
PostgreSQL 17 avec SQLAlchemy 2.0.23 comme ORM

### 6.2 Tables/Collections

#### Table: machines
**Description:** Stocke les informations sur les équipements

**Champs:**
- `id` (Integer, Primary Key, Auto-increment) - Identifiant unique de la machine
- `name` (String, Unique, Not Null) - Nom de la machine
- `description` (String, Nullable) - Description de la machine
- `location` (String, Nullable) - Emplacement physique de la machine
- `created_at` (DateTime, Default=utcnow) - Date de création
- `updated_at` (DateTime, Default=utcnow, OnUpdate=utcnow) - Date de dernière mise à jour

**Relations:**
- One-to-many vers sensor_readings (une machine a plusieurs lectures capteurs)
- One-to-many vers predictions (une machine a plusieurs prédictions)

#### Table: sensor_readings
**Description:** Stocke les lectures de capteurs pour chaque machine à chaque cycle

**Champs:**
- `id` (Integer, Primary Key, Auto-increment) - Identifiant unique de la lecture
- `machine_id` (Integer, Foreign Key vers machines.id, Not Null) - Référence à la machine
- `cycle` (Integer, Not Null) - Numéro de cycle
- `timestamp` (DateTime, Default=utcnow) - Horodatage de la lecture
- `setting_1`, `setting_2`, `setting_3` (Float, Not Null) - Paramètres opérationnels
- `sensor_2`, `sensor_3`, `sensor_4`, `sensor_6`, `sensor_7`, `sensor_8`, `sensor_9` (Float, Not Null) - Mesures capteurs
- `sensor_11`, `sensor_12`, `sensor_13`, `sensor_14`, `sensor_15`, `sensor_17`, `sensor_20`, `sensor_21` (Float, Not Null) - Mesures capteurs

**Note:** Les capteurs 1, 5, 10, 16, 18, 19 sont exclus (constants, sans information)

**Relations:**
- Many-to-one vers machines (une lecture appartient à une machine)
- One-to-one vers predictions (une lecture peut avoir une prédiction associée)

#### Table: predictions
**Description:** Stocke les prédictions de RUL générées par le modèle ML

**Champs:**
- `id` (Integer, Primary Key, Auto-increment) - Identifiant unique de la prédiction
- `machine_id` (Integer, Foreign Key vers machines.id, Not Null) - Référence à la machine
- `sensor_reading_id` (Integer, Foreign Key vers sensor_readings.id, Nullable) - Référence à la lecture capteur
- `timestamp` (DateTime, Default=utcnow) - Horodatage de la prédiction
- `predicted_rul` (Float, Not Null) - RUL prédit par le modèle ML
- `effective_rul` (Float, Not Null) - RUL effectif après application de la marge de sécurité
- `health_score` (Float, Not Null) - Score de santé (0-100)
- `maintenance_status` (String, Not Null) - Statut de maintenance (NORMAL, MONITOR, MAINTENANCE_RECOMMENDED, CRITICAL)
- `safety_margin_applied` (Float, Not Null) - Marge de sécurité appliquée (49 cycles)

**Relations:**
- Many-to-one vers machines (une prédiction appartient à une machine)
- Many-to-one vers sensor_readings (une prédiction est basée sur une lecture)

### 6.3 Relations
- **machines → sensor_readings:** One-to-many (une machine a plusieurs lectures)
- **machines → predictions:** One-to-many (une machine a plusieurs prédictions)
- **sensor_readings → predictions:** One-to-one (une lecture peut avoir une prédiction)
- **sensor_readings → machines:** Many-to-one (une lecture appartient à une machine)
- **predictions → machines:** Many-to-one (une prédiction appartient à une machine)

### 6.4 Clés Primaires/Étrangères
- **Clés primaires:** id dans toutes les tables (auto-increment Integer)
- **Clés étrangères:**
  - sensor_readings.machine_id → machines.id
  - predictions.machine_id → machines.id
  - predictions.sensor_reading_id → sensor_readings.id

### 6.5 Requêtes Principales

**Récupérer toutes les machines:**
```python
db.query(Machine).offset(skip).limit(limit).all()
```

**Récupérer les prédictions d'une machine:**
```python
db.query(Prediction).filter(Prediction.machine_id == machine_id).order_by(Prediction.timestamp.desc()).all()
```

**Récupérer la dernière prédiction d'une machine:**
```python
db.query(Prediction).filter(Prediction.machine_id == machine_id).order_by(Prediction.timestamp.desc()).first()
```

**Résumé maintenance par statut:**
```python
db.query(Prediction.maintenance_status, func.count(Prediction.machine_id)).group_by(Prediction.maintenance_status).all()
```

### 6.6 Flux de Données
1. Machine créée via API POST /machines/
2. Lectures capteurs ajoutées via API POST /sensor-readings/
3. Prédiction générée via API POST /predictions/ (stocke lecture et prédiction)
4. Données consultées via API GET /machines/, /predictions/, /maintenance/

### 6.7 Migrations/Seeding
**Migrations:** Information non disponible (pas de Alembic configuré)
**Seeding:** Script `backend/seed_database.py` peuple la base avec:
- 8 machines avec noms réalistes
- 10 lectures capteurs par machine (80 total)
- 10 prédictions par machine (80 total)
- Distribution: 5 NORMAL, 2 MONITOR, 1 CRITIQUE

---

## 7. DOCUMENTATION API

### 7.1 Endpoints Principaux

#### GET /api/v1/health
**Méthode:** GET
**URL:** /api/v1/health
**But:** Vérifier la santé de l'API et la connexion base de données
**Authentification:** Aucune
**Paramètres:** Aucun
**Réponse:**
```json
{
  "status": "healthy",
  "app_name": "Predictive Maintenance API",
  "app_version": "1.0.0",
  "database_connected": true,
  "model_loaded": true
}
```
**Erreurs:** Aucune (retourne toujours 200)
**Fichier implémentation:** `backend/app/routes/health.py`

#### GET /api/v1/machines/
**Méthode:** GET
**URL:** /api/v1/machines/
**But:** Récupérer la liste de toutes les machines
**Authentification:** Aucune
**Paramètres query:**
- skip (integer, default=0) - Nombre de résultats à sauter
- limit (integer, default=100) - Nombre maximum de résultats
**Réponse:**
```json
[
  {
    "id": 1,
    "name": "Turbofan Engine #1",
    "description": "Main propulsion unit for Aircraft A",
    "location": "Hangar A",
    "created_at": "2026-08-20T10:00:00",
    "updated_at": "2026-08-20T10:00:00"
  }
]
```
**Erreurs:** Aucune (retourne liste vide si aucune machine)
**Fichier implémentation:** `backend/app/routes/machines.py`

#### GET /api/v1/machines/{machine_id}
**Méthode:** GET
**URL:** /api/v1/machines/{machine_id}
**But:** Récupérer les détails d'une machine spécifique
**Authentification:** Aucune
**Paramètres path:**
- machine_id (integer, required) - ID de la machine
**Réponse:**
```json
{
  "id": 1,
  "name": "Turbofan Engine #1",
  "description": "Main propulsion unit for Aircraft A",
  "location": "Hangar A",
  "created_at": "2026-08-20T10:00:00",
  "updated_at": "2026-08-20T10:00:00"
}
```
**Erreurs:**
- 404: Machine non trouvée
**Fichier implémentation:** `backend/app/routes/machines.py`

#### POST /api/v1/machines/
**Méthode:** POST
**URL:** /api/v1/machines/
**But:** Créer une nouvelle machine
**Authentification:** Aucune
**Corps requête:**
```json
{
  "name": "Turbofan Engine #9",
  "description": "New engine",
  "location": "Hangar E"
}
```
**Réponse:**
```json
{
  "id": 9,
  "name": "Turbofan Engine #9",
  "description": "New engine",
  "location": "Hangar E",
  "created_at": "2026-08-20T10:00:00",
  "updated_at": "2026-08-20T10:00:00"
}
```
**Erreurs:**
- 400: Nom de machine déjà existe
**Fichier implémentation:** `backend/app/routes/machines.py`

#### PUT /api/v1/machines/{machine_id}
**Méthode:** PUT
**URL:** /api/v1/machines/{machine_id}
**But:** Mettre à jour une machine
**Authentification:** Aucune
**Paramètres path:**
- machine_id (integer, required) - ID de la machine
**Corps requête:**
```json
{
  "description": "Updated description",
  "location": "New location"
}
```
**Réponse:** Machine mise à jour (même format que GET)
**Erreurs:**
- 404: Machine non trouvée
**Fichier implémentation:** `backend/app/routes/machines.py`

#### DELETE /api/v1/machines/{machine_id}
**Méthode:** DELETE
**URL:** /api/v1/machines/{machine_id}
**But:** Supprimer une machine
**Authentification:** Aucune
**Paramètres path:**
- machine_id (integer, required) - ID de la machine
**Réponse:** 204 No Content
**Erreurs:**
- 404: Machine non trouvée
**Fichier implémentation:** `backend/app/routes/machines.py`

#### GET /api/v1/predictions/
**Méthode:** GET
**URL:** /api/v1/predictions/
**But:** Récupérer l'historique des prédictions
**Authentification:** Aucune
**Paramètres query:**
- machine_id (integer, optional) - Filtrer par machine
- skip (integer, default=0) - Nombre de résultats à sauter
- limit (integer, default=100) - Nombre maximum de résultats
**Réponse:**
```json
[
  {
    "id": 1,
    "machine_id": 1,
    "timestamp": "2026-08-20T10:00:00",
    "predicted_rul": 175.5,
    "effective_rul": 126.5,
    "health_score": 63.25,
    "maintenance_status": "NORMAL",
    "safety_margin_applied": 49.0
  }
]
```
**Erreurs:** Aucune
**Fichier implémentation:** `backend/app/routes/predictions.py`

#### GET /api/v1/predictions/{prediction_id}
**Méthode:** GET
**URL:** /api/v1/predictions/{prediction_id}
**But:** Récupérer une prédiction spécifique
**Authentification:** Aucune
**Paramètres path:**
- prediction_id (integer, required) - ID de la prédiction
**Réponse:** Prédiction (même format que liste)
**Erreurs:**
- 404: Prédiction non trouvée
**Fichier implémentation:** `backend/app/routes/predictions.py`

#### POST /api/v1/predictions/
**Méthode:** POST
**URL:** /api/v1/predictions/
**But:** Créer une prédiction à partir de données capteurs
**Authentification:** Aucune
**Corps requête:**
```json
{
  "machine_id": 1,
  "cycle": 100,
  "setting_1": 0.0,
  "setting_2": 0.0,
  "setting_3": 100.0,
  "sensor_2": 641.21,
  "sensor_3": 1571.04,
  "sensor_4": 1382.25,
  "sensor_6": 21.60,
  "sensor_7": 549.85,
  "sensor_8": 2387.90,
  "sensor_9": 9021.73,
  "sensor_11": 46.85,
  "sensor_12": 518.69,
  "sensor_13": 2387.88,
  "sensor_14": 8099.94,
  "sensor_15": 8.32,
  "sensor_17": 388.00,
  "sensor_20": 38.14,
  "sensor_21": 22.89
}
```
**Réponse:**
```json
{
  "id": 81,
  "machine_id": 1,
  "timestamp": "2026-08-20T10:00:00",
  "predicted_rul": 175.5,
  "effective_rul": 126.5,
  "health_score": 63.25,
  "maintenance_status": "NORMAL",
  "safety_margin_applied": 49.0
}
```
**Erreurs:**
- 404: Machine non trouvée
- 500: Erreur chargement modèle ML
**Fichier implémentation:** `backend/app/routes/predictions.py`

#### GET /api/v1/predictions/machine/{machine_id}
**Méthode:** GET
**URL:** /api/v1/predictions/machine/{machine_id}
**But:** Récupérer les prédictions pour une machine spécifique
**Authentification:** Aucune
**Paramètres path:**
- machine_id (integer, required) - ID de la machine
**Paramètres query:**
- skip (integer, default=0)
- limit (integer, default=100)
**Réponse:** Liste de prédictions pour la machine
**Erreurs:** Aucune
**Fichier implémentation:** `backend/app/routes/predictions.py`

#### GET /api/v1/maintenance/status/{machine_id}
**Méthode:** GET
**URL:** /api/v1/maintenance/status/{machine_id}
**But:** Récupérer le statut de maintenance actuel d'une machine
**Authentification:** Aucune
**Paramètres path:**
- machine_id (integer, required) - ID de la machine
**Réponse:**
```json
{
  "machine_id": 1,
  "status": "NORMAL",
  "predicted_rul": 175.5,
  "effective_rul": 126.5,
  "health_score": 63.25,
  "last_prediction_timestamp": "2026-08-20T10:00:00"
}
```
**Erreurs:**
- 404: Machine non trouvée
**Fichier implémentation:** `backend/app/routes/maintenance.py`

#### GET /api/v1/maintenance/summary
**Méthode:** GET
**URL:** /api/v1/maintenance/summary
**But:** Récupérer un résumé des statuts de maintenance de toutes les machines
**Authentification:** Aucune
**Paramètres:** Aucun
**Réponse:**
```json
{
  "total_machines": 8,
  "status_breakdown": {
    "NORMAL": 5,
    "MONITOR": 2,
    "MAINTENANCE_RECOMMENDED": 0,
    "CRITICAL": 1
  }
}
```
**Erreurs:** Aucune
**Fichier implémentation:** `backend/app/routes/maintenance.py`

#### GET /api/v1/maintenance/upcoming
**Méthode:** GET
**URL:** /api/v1/maintenance/upcoming
**But:** Récupérer les maintenances à venir (machines nécessitant une attention)
**Authentification:** Aucune
**Paramètres:** Aucun
**Réponse:** Liste de machines avec statut de maintenance
**Erreurs:** Aucune
**Fichier implémentation:** `backend/app/routes/maintenance.py`

#### GET /api/v1/sensor-readings/
**Méthode:** GET
**URL:** /api/v1/sensor-readings/
**But:** Récupérer les lectures de capteurs
**Authentification:** Aucune
**Paramètres query:**
- machine_id (integer, optional) - Filtrer par machine
- skip (integer, default=0)
- limit (integer, default=100)
**Réponse:** Liste de lectures capteurs
**Erreurs:** Aucune
**Fichier implémentation:** `backend/app/routes/sensor_readings.py`

#### POST /api/v1/sensor-readings/
**Méthode:** POST
**URL:** /api/v1/sensor-readings/
**But:** Créer une lecture de capteurs
**Authentification:** Aucune
**Corps requête:** Même format que POST /predictions/ (sans machine_id requis car inclus)
**Réponse:** Lecture créée
**Erreurs:** Aucune documentée
**Fichier implémentation:** `backend/app/routes/sensor_readings.py`

---

## 8. FRONTEND

### 8.1 Pages Principales

#### Dashboard (`frontend/src/pages/Dashboard.tsx`)
**Description:** Vue d'ensemble du système avec statistiques et graphiques

**Fonctionnalités:**
- Cartes statistiques (total machines, machines normales, machines nécessitant maintenance, score de santé moyen)
- Graphique camembert de distribution des statuts de maintenance
- Graphique histogramme de répartition des statuts
- Tableau des 10 dernières prédictions avec détails

**État:**
- machines: Machine[] - Liste des machines
- predictions: Prediction[] - Liste des prédictions
- summary: MaintenanceSummary - Résumé maintenance
- loading: boolean - État de chargement
- error: string | null - Message d'erreur

**API Communication:**
- getMachines() - Récupérer toutes les machines
- getPredictions() - Récupérer les prédictions
- getMaintenanceSummary() - Récupérer le résumé maintenance

**Workflow utilisateur:**
1. Chargement automatique au montage du composant
2. Affichage des statistiques calculées
3. Mise à jour automatique des graphiques

#### Machines (`frontend/src/pages/Machines.tsx`)
**Description:** Liste de toutes les machines avec leurs prédictions

**Fonctionnalités:**
- Tableau avec ID machine, nom, RUL prédit, score de santé, statut
- Sparkline montrant la tendance des 10 derniers cycles
- Filtres par statut de maintenance
- Recherche par nom de machine
- Lien vers les détails de chaque machine

**État:**
- machines: Machine[] - Liste des machines
- predictions: Prediction[] - Liste des prédictions
- filter: string - Filtre de statut actif
- search: string - Terme de_recherche

**API Communication:**
- getMachines() - Récupérer les machines
- getPredictions() - Récupérer les prédictions

**Workflow utilisateur:**
1. Chargement automatique de la liste
2. Application des filtres et recherche
3. Clic sur une machine pour voir les détails

#### Maintenance (`frontend/src/pages/Maintenance.tsx`)
**Description:** Recommandations de maintenance priorisées

**Fonctionnalités:**
- Liste des machines nécessitant une maintenance
- Priorisation par statut (CRITIQUE > MAINTENANCE_RECOMMANDÉE > MONITOR)
- Date estimée de maintenance
- Actions recommandées pour chaque statut
- Filtres par urgence

**État:**
- predictions: Prediction[] - Liste des prédictions
- filter: string - Filtre d'urgence

**API Communication:**
- getPredictions() - Récupérer les prédictions
- getMaintenanceSummary() - Récupérer le résumé

**Workflow utilisateur:**
1. Chargement automatique des recommandations
2. Visualisation par ordre de priorité
3. Consultation des actions recommandées

#### TestPrediction (`frontend/src/pages/TestPrediction.tsx`)
**Description:** Formulaire interactif pour tester les prédictions

**Fonctionnalités:**
- Sélection de machine via dropdown
- Saisie manuelle des 18 valeurs capteurs
- Boutons "Load Healthy Example" et "Load Critical Example" pour remplissage rapide
- Bouton "Predict" pour lancer la prédiction
- Affichage des résultats avec explication du statut

**État:**
- machines: Machine[] - Liste des machines
- selectedMachineId: number | null - Machine sélectionnée
- sensorData: Record<string, number> - Valeurs capteurs saisies
- cycle: number - Numéro de cycle
- prediction: Prediction | null - Résultat de la prédiction
- loading: boolean - État de chargement
- error: string | null - Message d'erreur

**API Communication:**
- getMachines() - Récupérer les machines
- createPrediction() - Créer une prédiction

**Workflow utilisateur:**
1. Sélectionner une machine
2. Soit saisir manuellement les capteurs, soit utiliser les exemples
3. Cliquer sur "Predict"
4. Visualiser les résultats et l'explication

#### MachineDetails (`frontend/src/pages/MachineDetails.tsx`)
**Description:** Détails complets d'une machine spécifique

**Fonctionnalités:**
- Informations de base de la machine
- Historique des prédictions
- Graphique de tendance RUL
- Détails des lectures capteurs récentes

**État:**
- machine: Machine | null - Détails de la machine
- predictions: Prediction[] - Historique des prédictions
- loading: boolean - État de chargement

**API Communication:**
- getMachine(id) - Récupérer la machine
- getPredictions(machineId) - Récupérer les prédictions

**Workflow utilisateur:**
1. Navigation depuis la page Machines
2. Affichage automatique des détails
3. Visualisation de l'historique

### 8.2 Composants

#### Header (`frontend/src/components/Header.tsx`)
**Description:** Barre de navigation supérieure

**Fonctionnalités:**
- Logo/nom de l'application
- Navigation vers les pages principales

#### Sidebar (`frontend/src/components/Sidebar.tsx`)
**Description:** Menu latéral de navigation

**Fonctionnalités:**
- Liens vers Dashboard, Machines, Maintenance, Test Prediction
- Indication de la page active

#### Sparkline (`frontend/src/components/Sparkline.tsx`)
**Description:** Graphique linéaire miniature pour les tendances

**Fonctionnalités:**
- Affichage des 10 derniers points de données
- Utilisation de Recharts pour le rendu

### 8.3 Navigation
**Framework:** React Router DOM 7.18.2
**Routes:**
- / → Dashboard
- /machines → Machines
- /machines/:id → MachineDetails
- /maintenance → Maintenance
- /test-prediction → TestPrediction

### 8.4 Formulaires
**TestPrediction.tsx:**
- Formulaire de saisie des 18 valeurs capteurs
- Validation basique (champs numériques)
- Exemples pré-remplis pour démonstration

### 8.5 Gestion d'État
**Approche:** État local avec useState (pas de Redux)
**Raison:** Projet de taille modérée, état local suffisant

### 8.6 Communication API
**Client:** Axios 1.19.0
**Service:** `frontend/src/services/api.ts`
**Fonctions:**
- getHealthCheck()
- getMachines(), getMachine(), createMachine(), updateMachine(), deleteMachine()
- getSensorReadings(), createSensorReading()
- getPredictions(), getPrediction(), createPrediction()
- getMaintenanceStatus(), getMaintenanceSummary()

### 8.7 Authentification UI
**Statut:** Information non disponible dans le projet (pas d'authentification implémentée)

### 8.8 Workflows Utilisateur Principaux

**Workflow 1: Surveillance globale**
1. Utilisateur accède à l'application
2. Dashboard s'affiche automatiquement
3. Visualisation des statistiques globales
4. Consultation des graphiques de distribution
5. Navigation vers les pages détaillées si nécessaire

**Workflow 2: Consultation machine individuelle**
1. Utilisateur navigue vers page Machines
2. Visualisation de la liste avec sparklines
3. Clic sur une machine spécifique
4. Affichage des détails complets
5. Consultation de l'historique des prédictions

**Workflow 3: Planification maintenance**
1. Utilisateur navigue vers page Maintenance
2. Visualisation des recommandations priorisées
3. Consultation des actions recommandées
4. Planification des interventions en fonction de l'urgence

**Workflow 4: Test de prédiction**
1. Utilisateur navigue vers page Test Prediction
2. Sélection d'une machine
3. Chargement d'un exemple (sain ou critique)
4. Lancement de la prédiction
5. Visualisation des résultats et explication

---

## 9. BACKEND

### 9.1 Modules Principaux

#### Application Principale (`backend/app/main.py`)
**Description:** Point d'entrée FastAPI

**Fonctionnalités:**
- Création de l'application FastAPI
- Configuration CORS
- Enregistrement des routes
- Gestion des événements startup/shutdown

**Configuration:**
- Titre: "Predictive Maintenance API"
- Version: "1.0.0"
- Préfixe API: "/api/v1"

#### Configuration (`backend/app/config.py`)
**Description:** Gestion de la configuration et variables d'environnement

**Fonctionnalités:**
- Chargement depuis variables d'environnement (.env)
- Chemins vers les artefacts ML
- URL base de données

**Paramètres:**
- APP_NAME, APP_VERSION, DEBUG
- DATABASE_URL
- MODEL_PATH, SCALER_PATH, DECISION_CONFIG_PATH
- API_PREFIX

#### Base de Données (`backend/app/database.py`)
**Description:** Configuration SQLAlchemy

**Fonctionnalités:**
- Création du moteur de base de données
- Gestion des sessions
- Dependency injection get_db()

### 9.2 Routes

#### Health (`backend/app/routes/health.py`)
**Endpoints:**
- GET /health - Vérification santé API

**Fonctionnalités:**
- Test connexion base de données
- Vérification chargement modèle ML
- Retour statut global

#### Machines (`backend/app/routes/machines.py`)
**Endpoints:**
- POST /machines/ - Créer machine
- GET /machines/ - Lister machines (pagination)
- GET /machines/{id} - Détails machine
- PUT /machines/{id} - Mettre à jour machine
- DELETE /machines/{id} - Supprimer machine

**Fonctionnalités:**
- CRUD complet
- Validation unicité nom
- Pagination

#### Predictions (`backend/app/routes/predictions.py`)
**Endpoints:**
- POST /predictions/ - Créer prédiction
- GET /predictions/ - Lister prédictions (pagination, filtre machine)
- GET /predictions/{id} - Détails prédiction
- GET /predictions/machine/{machine_id} - Prédictions par machine

**Fonctionnalités:**
- Intégration service prédiction ML
- Stockage lecture capteur
- Stockage prédiction
- Historique par machine

#### Maintenance (`backend/app/routes/maintenance.py`)
**Endpoints:**
- GET /maintenance/status/{machine_id} - Statut maintenance machine
- GET /maintenance/summary - Résumé maintenance global
- GET /maintenance/upcoming - Maintenances à venir

**Fonctionnalités:**
- Récupération dernière prédiction
- Agrégation par statut
- Priorisation

#### Sensor Readings (`backend/app/routes/sensor_readings.py`)
**Endpoints:**
- GET /sensor-readings/ - Lister lectures (pagination, filtre machine)
- POST /sensor-readings/ - Créer lecture

**Fonctionnalités:**
- Stockage données capteurs brutes
- Historique temporel

### 9.3 Services

#### Prediction Service (`backend/app/services/prediction_service.py`)
**Description:** Service de prédiction ML

**Fonctionnalités:**
- Chargement modèle Random Forest
- Chargement scaler StandardScaler
- Chargement couche de décision
- Normalisation des données
- Prédiction RUL
- Application couche de décision

**Méthodes:**
- __init__() - Initialisation et chargement
- predict(sensor_data) - Prédiction complète
- is_loaded() - Vérification chargement

### 9.4 Contrôleurs
**Architecture:** FastAPI utilise directement les fonctions de route comme contrôleurs (pas de couche contrôleur séparée)

### 9.5 Logique Métier
**Localisation:**
- Service layer: `backend/app/services/prediction_service.py`
- Route handlers: `backend/app/routes/`

**Principales décisions métier:**
- Application marge de sécurité (49 cycles)
- Calcul score de santé (échelle linéaire 0-100)
- Détermination statut maintenance (seuils: 20, 50, 100 cycles)

### 9.6 Middleware
**CORS Middleware (`backend/app/main.py`)**
- Configuration: allow_origins=["*"] (à restreindre en production)
- Permet communication frontend-backend

### 9.7 Authentification
**Statut:** Information non disponible dans le projet (pas d'authentification implémentée)

### 9.8 Validation
**Framework:** Pydantic 2.5.0
**Localisation:** `backend/app/schemas/__init__.py`

**Schémas:**
- MachineBase, MachineCreate, MachineUpdate, MachineResponse
- SensorReadingBase, SensorReadingCreate, SensorReadingResponse
- PredictionRequest, PredictionResponse
- HealthCheckResponse

**Validation automatique:**
- Types de données
- Champs requis
- Conversion automatique

### 9.9 Gestion des Erreurs
**Mécanismes:**
- HTTPException FastAPI pour erreurs client (404, 400)
- Try/except dans service prédiction
- Messages d'erreur descriptifs

**Types d'erreurs:**
- 404: Ressource non trouvée
- 400: Données invalides
- 500: Erreur serveur (ex: modèle non chargé)

### 9.10 Communication Base de Données
**ORM:** SQLAlchemy 2.0.23
**Session:** Dependency injection via get_db()
**Requêtes:** Query API SQLAlchemy
**Transactions:** Commit automatique, rollback sur erreur

---

## 10. IA / MACHINE LEARNING

### 10.1 Objectif IA
Prédire la Durée de Vie Restante (RUL) de moteurs d'avion (turbofans) à partir de données de capteurs et de paramètres opérationnels, en utilisant le dataset NASA C-MAPSS FD001.

### 10.2 Dataset

**Source:** NASA C-MAPSS FD001 (Commercial Modular Aero-Propulsion System Simulation)
**Emplacement:** `../../Downloads/archive/` (doit être placé manuellement)
**Fichiers:**
- train_FD001.txt - Données d'entraînement
- test_FD001.txt - Données de test officiel
- RUL_FD001.txt - Vérité terrain pour test

**Caractéristiques:**
- 100 moteurs dans l'entraînement
- 100 moteurs dans le test officiel
- Cycles temporels de 1 à 361 cycles
- 26 colonnes: engine_id, cycle, 3 settings, 21 capteurs

### 10.3 Prétraitement des Données

**Script:** `ml/src/preprocessing.py`

**Étapes:**
1. **Chargement des données:** Lecture des fichiers train/test avec noms de colonnes
2. **Suppression capteurs constants:** Suppression de sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19 (pas d'information)
3. **Calcul RUL:** Pour entraînement: RUL = max_cycle - current_cycle
4. **Ajout relative_cycle:** relative_cycle = cycle / max_cycle (SUPPRIMÉ pour éviter fuite de données)
5. **Validation:** Vérification valeurs manquantes, doublons, cycles séquentiels

**Capteurs utiles (15):**
sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9, sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21

### 10.4 Caractéristiques (Features)

**Features finales (18):**
- 3 paramètres opérationnels: setting_1, setting_2, setting_3
- 15 capteurs: sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9, sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21

**Features exclues:**
- relative_cycle (fuite de données - nécessite connaissance du cycle de défaillance)
- max_cycle (fuite de données)
- engine_id (identifiant, pas prédictif)
- RUL (variable cible)

**Normalisation:** StandardScaler (moyenne=0, écart-type=1)

### 10.5 Modèles

**Modèle final:** RandomForestRegressor (scikit-learn)

**Hyperparamètres finaux:**
- n_estimators: 77
- max_depth: 9
- min_samples_split: 10
- min_samples_leaf: 7
- max_features: log2
- random_state: 42

**Processus de sélection:**
1. Entraînement baseline (n_estimators=100, max_depth=15)
2. Optimisation via RandomizedSearchCV (50 itérations)
3. Sélection des meilleurs hyperparamètres
4. Réentraînement avec hyperparamètres optimisés

### 10.6 Algorithmes

**Algorithme principal:** Random Forest (ensemble d'arbres de décision)
- Pourquoi: Robuste, interprétable, bonne performance sur données tabulaires
- Avantages: Résistant au surapprentissage, importance des features

**Alternatives évaluées:**
- XGBoost (entraîné mais non retenu pour production)
- Time-series features (causaient surapprentissage, non utilisées)

### 10.7 Processus d'Entraînement

**Script:** `ml/src/train_deployment_safe.py`

**Étapes:**
1. **Chargement données:** Prétraitement via preprocessing.py
2. **Suppression relative_cycle:** Pour éviter fuite de données
3. **Split moteurs:** Division au niveau moteur (70% entraînement, 15% validation, 15% test)
  - Entraînement: 70 moteurs
  - Validation: 15 moteurs
  - Split fixe avec seed=42 pour reproductibilité
4. **Préparation features:** Sélection des 18 features
5. **Normalisation:** StandardScaler fit sur entraînement, transform sur validation/test
6. **Entraînement:** RandomForestRegressor.fit()
7. **Prédictions:** Sur entraînement, validation, test
8. **Évaluation:** Calcul RMSE, MAE, R²
9. **Sauvegarde:** Modèle (.joblib), scaler (.joblib), résultats (.json)

### 10.8 Processus d'Inférence

**Script:** `backend/app/services/prediction_service.py`

**Étapes:**
1. **Chargement modèle:** joblib.load(final_rul_model.joblib)
2. **Chargement scaler:** joblib.load(preprocessing_pipeline.joblib)
3. **Chargement décision:** MaintenanceDecisionLayer.load_config()
4. **Extraction features:** Ordre spécifique des 18 features
5. **Normalisation:** scaler.transform()
6. **Prédiction:** model.predict()
7. **Application décision:** decision_layer.process_prediction()
8. **Retour:** Dictionnaire avec RUL, score santé, statut

### 10.9 Métriques d'Évaluation

**Métriques utilisées:**
- **RMSE** (Root Mean Squared Error): Métrique principale, pénalise les grandes erreurs
- **MAE** (Mean Absolute Error): Erreur moyenne interprétable
- **R²** (R-squared): Pourcentage de variance expliquée

**Résultats vérifiés (depuis artefacts sauvegardés):**

| Métrique | Entraînement | Validation | Test Interne | Test Officiel |
|----------|--------------|------------|---------------|---------------|
| **RMSE** | 38.11 cycles | 41.80 cycles | 45.41 cycles | **31.73 cycles** |
| **MAE** | 26.37 cycles | 31.72 cycles | 33.23 cycles | **23.39 cycles** |
| **R²** | 0.69 | 0.62 | 0.59 | **0.42** |

**Analyse surapprentissage:**
- Ratio Validation/Entraînement: 1.10
- Ratio Test/Entraînement: 1.19
- **Interprétation:** Généralisation saine (ratios < 1.5), surapprentissage minimal

### 10.10 Sorties du Modèle

**Sortie brute:** RUL prédit en cycles (nombre réel)

**Sorties après couche de décision:**
- predicted_rul: RUL prédit par le modèle
- effective_rul: RUL après marge de sécurité (predicted_rul - 49)
- health_score: Score de santé 0-100 (effective_rul / 200 * 100)
- maintenance_status: Statut (NORMAL, MONITOR, MAINTENANCE_RECOMMENDED, CRITICAL)
- safety_margin_applied: Marge appliquée (49 cycles)

### 10.11 Intégration avec l'Application

**Backend:**
- Service PredictionService dans `backend/app/services/prediction_service.py`
- Chargement au démarrage de l'application
- Appel via route POST /api/v1/predictions/

**Frontend:**
- Appel API via axios dans `frontend/src/services/api.ts`
- Affichage des résultats dans TestPrediction.tsx
- Visualisation des prédictions dans Dashboard, Machines, Maintenance

### 10.12 Bibliothèques/Frameworks

**scikit-learn 1.9.0**
- RandomForestRegressor
- StandardScaler
- RandomizedSearchCV
- Métriques (mean_squared_error, mean_absolute_error, r2_score)

**joblib 1.3.2**
- Sérialisation modèle et scaler

**pandas 2.0.3**
- Manipulation données

**numpy 1.24.3**
- Calculs numériques

**matplotlib 3.7.0**
- Visualisations

**seaborn 0.12.0**
- Visualisations avancées

### 10.13 Limitations

**Dataset:**
- Uniquement FD001 (un seul scénario opérationnel)
- Pas généralisé à FD002-FD004
- Données simulées, pas données réelles

**Modèle:**
- Basé sur Random Forest (pas de dépendances temporelles explicites)
- Pas de modèle LSTM/GRU pour séries temporelles
- Features limitées aux capteurs actuels

**Performance:**
- RMSE de 31.73 cycles sur test officiel (marge d'erreur significative)
- R² de 0.42 sur test officiel (variance limitée expliquée)

---

## 11. UTILISATION DE L'AGENT DEVIN

**Statut:** Information non disponible dans le projet

**Analyse:**
- Pas de traces explicites d'utilisation de Devin Agent dans le code
- Pas de documentation mentionnant Devin
- Pas de commits Git (projet n'est pas un repository Git)
- Configuration Devin présente dans `.devin/config.local.json` mais pas d'indication d'utilisation

**Conclusion:** Impossible de déterminer le rôle de Devin Agent dans le développement de ce projet. Le projet semble avoir été développé manuellement sans assistance d'agent IA documentée.

---

## 12. PROCESSUS DE DÉVELOPPEMENT

### 12.1 Configuration Initiale
**Information non disponible dans le projet** (pas d'historique Git)

### 12.2 Configuration de l'Environnement
**Backend:**
- Python 3.8+ avec environnement virtuel (venv)
- Installation dépendances via requirements.txt
- Configuration base de données PostgreSQL

**Frontend:**
- Node.js 16+ avec npm
- Installation dépendances via package.json
- Configuration API URL via .env

### 12.3 Phases de Développement
**Déduites de la documentation:**

**Phase 1: ML Pipeline**
- Développement pipeline ML dans `ml/`
- Entraînement modèle baseline
- Prétraitement données
- Évaluation sur dataset officiel

**Phase 2: Audit Fuite de Données**
- Identification feature relative_cycle comme fuite potentielle
- Entraînement modèle sans relative_cycle
- Comparaison performances (25.47 → 41.82 RMSE)

**Phase 3: Optimisation**
- Optimisation hyperparamètres via RandomizedSearchCV
- Sélection meilleurs paramètres (n_estimators=77, max_depth=9)
- Réentraînement et évaluation

**Phase 4: Couche de Décision**
- Analyse biais modèle
- Calcul marge de sécurité (49 cycles)
- Implémentation couche de décision

**Phase 5: Backend**
- Développement API FastAPI
- Intégration modèle ML
- Configuration base de données
- Création routes et services

**Phase 6: Frontend**
- Développement interface React
- Création pages (Dashboard, Machines, Maintenance, TestPrediction)
- Intégration API backend

**Phase 7: Intégration**
- Peuplement base de données
- Tests end-to-end
- Documentation

### 12.4 Implémentation des Fonctionnalités
**Ordre déduit:**
1. ML Pipeline → Modèle entraîné
2. Backend API → Service prédiction
3. Frontend → Interface utilisateur
4. Base de données → Stockage
5. Intégration → Système complet

### 12.5 Débogage
**Information non disponible dans le projet** (pas de logs ou historique)

### 12.6 Tests
**Tests unitaires backend:** `backend/tests/test_api.py`
- test_health_check()
- test_create_machine()
- test_get_machines()
- test_prediction_endpoint()

**Tests manuels:** Via interface TestPrediction

### 12.7 Intégration
**Méthode:** Intégration manuelle via API REST
**Vérification:** Script seed_database.py pour données de démonstration

### 12.8 Déploiement
**Statut:** Déploiement local uniquement (pas de déploiement cloud documenté)

---

## 13. TESTS

### 13.1 Tests Unitaires
**Fichier:** `backend/tests/test_api.py`

**Tests existants:**
1. **test_health_check()**
   - Vérifie endpoint GET /api/v1/health
   - Valide présence champs: status, app_name, app_version

2. **test_create_machine()**
   - Vérifie endpoint POST /api/v1/machines/
   - Valide création et retour de l'ID

3. **test_get_machines()**
   - Vérifie endpoint GET /api/v1/machines/
   - Valide retour liste

4. **test_prediction_endpoint()**
   - Vérifie endpoint POST /api/v1/predictions/
   - Accepte 201 (succès) ou 500 (modèle non chargé)

**Exécution:** pytest backend/tests/test_api.py

### 13.2 Tests d'Intégration
**Statut:** Information non disponible dans le projet (pas de tests d'intégration documentés)

### 13.3 Tests API
**Inclus dans tests unitaires** (test_api.py)

### 13.4 Tests Frontend
**Statut:** Information non disponible dans le projet (pas de tests frontend automatisés)

### 13.5 Tests End-to-End
**Statut:** Information non disponible dans le projet (pas de tests E2E automatisés)

### 13.6 Tests Manuels
**Via interface TestPrediction:**
- Test avec exemple sain → doit retourner NORMAL/MONITOR
- Test avec exemple critique → doit retourner CRITICAL

### 13.7 Scénarios de Test
**Scénario 1:** Prédiction machine saine
- Entrée: Valeurs capteurs saines
- Attendu: RUL élevé, statut NORMAL

**Scénario 2:** Prédiction machine critique
- Entrée: Valeurs capteurs dégradées
- Attendu: RUL faible, statut CRITICAL

### 13.8 Résultats des Tests
**Statut:** Information non disponible dans le projet (pas de résultats de tests documentés)

### 13.9 Bugs Connus
**Statut:** Information non disponible dans le projet (pas de bugs documentés)

---

## 14. SÉCURITÉ

### 14.1 Authentification
**Statut:** Information non disponible dans le projet (pas d'authentification implémentée)

### 14.2 Authorization
**Statut:** Information non disponible dans le projet (pas de authorization implémentée)

### 14.3 Gestion des Mots de Passe
**Statut:** Information non disponible dans le projet (pas de mots de passe gérés)

### 14.4 Tokens
**Statut:** Information non disponible dans le projet (pas de tokens utilisés)

### 14.5 Validation des Entrées
**Framework:** Pydantic 2.5.0
**Localisation:** `backend/app/schemas/__init__.py`

**Validation:**
- Types de données (int, float, string)
- Champs requis
- Conversion automatique

### 14.6 Sécurité API
**CORS:** Configuré dans `backend/app/main.py`
- allow_origins: ["*"] (à restreindre en production)
- allow_credentials: true
- allow_methods: ["*"]
- allow_headers: ["*"]

**Note:** Configuration permissive pour développement, à restreindre pour production

### 14.7 Variables d'Environnement/Secrets
**Backend:** `backend/.env`
- DATABASE_URL (contient mot de passe base de données)
- MODEL_PATH, SCALER_PATH, DECISION_CONFIG_PATH

**Frontend:** `frontend/.env`
- VITE_API_URL

**Note:** Fichiers .env ne sont pas inclus dans le projet (doivent être créés manuellement)

### 14.8 CORS
**Configuration:** FastAPI CORSMiddleware
- Origines: toutes autorisées (développement)
- À configurer pour production avec origines spécifiques

### 14.9 Protection Injection SQL
**Mécanisme:** SQLAlchemy ORM
- Protection automatique via paramétrage des requêtes
- Pas de SQL brut

### 14.10 Protection XSS
**Statut:** Information non disponible dans le projet (pas de mécanismes XSS explicites)

### 14.11 Autres Mécanismes
**Statut:** Aucun autre mécanisme de sécurité identifié

---

## 15. DÉPLOIEMENT ET INFRASTRUCTURE

### 15.1 Architecture de Déploiement
**Statut:** Déploiement local uniquement

**Configuration actuelle:**
- Backend: http://localhost:8000 (Uvicorn)
- Frontend: http://localhost:5173 (Vite dev server)
- Base de données: PostgreSQL local (localhost:5432)

### 15.2 Serveur
**Backend:** Uvicorn 0.24.0 (serveur ASGI)
**Commande:** uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

### 15.3 Docker
**Statut:** Information non disponible dans le projet (pas de Dockerfile)

### 15.4 Variables d'Environnement
**Backend (.env):**
- DATABASE_URL=postgresql://user:password@localhost:5432/predictive_maintenance
- MODEL_PATH=models/final_rul_model.joblib
- SCALER_PATH=models/preprocessing_pipeline.joblib
- DECISION_CONFIG_PATH=ml/results/decision_layer_config.json

**Frontend (.env):**
- VITE_API_URL=http://localhost:8000/api/v1

### 15.5 Déploiement Base de Données
**Configuration:** PostgreSQL 17 local
**Création:** Via pgAdmin ou psql
**Peuplement:** Script `backend/seed_database.py`

### 15.6 Processus de Build
**Frontend:** Vite build (npm run build)
**Backend:** Pas de build requis (Python interprété)

### 15.7 Configuration Production
**Statut:** Information non disponible dans le projet (pas de configuration production documentée)

### 15.8 CI/CD
**Statut:** Information non disponible dans le projet (pas de CI/CD configuré)

### 15.9 Hébergement/Infrastructure Cloud
**Statut:** Information non disponible dans le projet (pas d'hébergement cloud)

---

## 16. PROBLÈMES ET SOLUTIONS

### 16.1 Problème: Fuite de Données avec relative_cycle
**Problème:** Feature relative_cycle (cycle / max_cycle) nécessite connaissance du cycle de défaissance, non disponible en temps réel.

**Cause:** relative_cycle utilise max_cycle qui est inconnu pendant l'opération.

**Investigation:** Audit dans `LEAKAGE_AUDIT.md` et `DEPLOYMENT_FEATURES.md`

**Solution:** Suppression de relative_cycle des features

**Fichiers affectés:**
- `ml/src/train_deployment_safe.py` - Entraînement sans relative_cycle
- `ml/src/preprocessing.py` - Suppression feature
- `models/model_metadata.json` - Documentation suppression

**Résultat final:**
- RMSE validation: 25.47 → 41.82 cycles (dégradation 64.2%)
- Check fuite de données: PASSED
- Modèle utilisable en temps réel

### 16.2 Problème: Surapprentissage avec Features Time-Series
**Problème:** Features temporelles (rolling windows, lags) causaient surapprentissage sévère.

**Cause:** Trop de features par rapport aux données, dépendances temporelles complexes.

**Investigation:** Évaluations dans `ml/README.md`

**Solution:** Utilisation features basiques (settings + sensors) sans time-series

**Fichiers affectés:**
- `ml/src/train_baseline.py` - Retour features simples
- `ml/src/features.py` - Non utilisé en production

**Résultat final:**
- Surapprentissage réduit (ratios < 1.5)
- Modèle plus simple et robuste

### 16.3 Problème: Biais de Prédiction (Surestimation)
**Problème:** Modèle surestime le RUL en moyenne de 6.93 cycles (61.83% des cas).

**Cause:** Distribution des erreurs asymétrique, modèle optimiste.

**Investigation:** Analyse dans `ml/src/analyze_bias.py`

**Solution:** Application marge de sécurité conservatrice (49 cycles, 75ème percentile des erreurs positives)

**Fichiers affectés:**
- `ml/src/maintenance_decision.py` - Implémentation marge sécurité
- `ml/results/decision_layer_config.json` - Configuration sauvegardée

**Résultat final:**
- Marge de sécurité: 49 cycles
- RUL effectif = RUL prédit - 49
- Recommandations plus conservatrices

### 16.4 Problème: Paradoxe RMSE/R² sur Test Officiel
**Problème:** RMSE officiel (31.73) < RMSE validation (41.80) mais R² officiel (0.42) < R² validation (0.62).

**Cause:** Distribution RUL différente entre validation et test officiel
- Validation: RUL 0-286 cycles (std: 67.98)
- Test officiel: RUL 7-145 cycles (std: 41.56)
- Ratio variance: 0.37

**Investigation:** Analyse dans `docs/FINAL_VERIFIED_RESULTS.md` et `docs/FOLLOW_UP_ANALYSIS.md`

**Solution:** Acceptation du phénomène (caractéristique du dataset, pas erreur modèle)

**Fichiers affectés:**
- `docs/FINAL_VERIFIED_RESULTS.md` - Documentation explication
- `ml/results/rul_distribution_analysis.json` - Analyse distribution

**Résultat final:**
- Phénomène expliqué et documenté
- Pas de correction nécessaire (caractéristique dataset)

### 16.5 Problème: Incohérences dans Documentation
**Problème:** Valeurs différentes entre documents (ex: RMSE 32.03 vs 31.73, hyperparamètres n_estimators=200 vs 77).

**Cause:** Brouillons intermédiaires, valeurs d'exploration non finalisées.

**Investigation:** Audit complet dans `docs/FINAL_VERIFIED_RESULTS.md`

**Solution:** Vérification depuis artefacts sauvegardés (model_metadata.json, résultats JSON)

**Fichiers affectés:**
- `docs/FINAL_VERIFIED_RESULTS.md` - Document de référence
- `models/model_metadata.json` - Source de vérité

**Résultat final:**
- Valeurs vérifiées et cohérentes
- Documentation unique de référence

---

## 17. RÉSULTATS

### 17.1 Fonctionnalités Implémentées
- ✅ Modèle ML Random Forest optimisé (n_estimators=77, max_depth=9)
- ✅ Couche de décision avec marge de sécurité (49 cycles)
- ✅ API REST FastAPI complète
- ✅ Interface React avec 4 pages (Dashboard, Machines, Maintenance, TestPrediction)
- ✅ Base de données PostgreSQL avec 3 tables
- ✅ Script de peuplement avec données de démonstration
- ✅ Évaluation sur dataset officiel FD001
- ✅ Documentation technique complète

### 17.2 Workflows Fonctionnels
- ✅ Surveillance globale via Dashboard
- ✅ Consultation machines individuelles
- ✅ Planification maintenance avec priorisation
- ✅ Test de prédiction interactif
- ✅ API REST pour intégration externe

### 17.3 Informations de Performance
**Modèle ML:**
- Validation RMSE: 41.80 cycles
- Official Test RMSE: 31.73 cycles
- Validation R²: 0.62
- Official Test R²: 0.42
- Overfitting ratios: 1.10 (validation), 1.19 (test) - sains

**Système:**
- Temps de réponse API: < 1 seconde (estimation)
- Frontend chargement: < 2 secondes (estimation)
- Base de données: 8 machines, 80 lectures, 80 prédictions (démo)

### 17.4 Résultats des Tests
**Tests unitaires backend:** 4 tests dans `backend/tests/test_api.py`
- Résultats: Information non disponible (pas d'exécution documentée)

**Tests manuels:** Via interface TestPrediction
- Exemple sain: Fonctionnel
- Exemple critique: Fonctionnel

### 17.5 Écrans/UI Existant
**Dashboard:**
- Cartes statistiques
- Graphiques (camembert, histogramme)
- Tableau prédictions récentes

**Machines:**
- Liste avec sparklines
- Filtres et recherche
- Liens vers détails

**Maintenance:**
- Liste priorisée
- Actions recommandées

**TestPrediction:**
- Formulaire 18 champs
- Boutons exemples
- Résultats avec explication

### 17.6 Limitations Actuelles
**Dataset:**
- Uniquement FD001 (pas généralisé)
- Données simulées

**Modèle:**
- RMSE de 31.73 cycles (marge d'erreur)
- Pas de dépendances temporelles explicites

**Système:**
- Pas d'authentification
- Déploiement local uniquement
- Pas de tests automatisés complets

---

## 18. LIMITATIONS ET AMÉLIORATIONS FUTURES

### 18.1 Limitations Actuelles

**Dataset:**
- Uniquement FD001 (1 scénario opérationnel sur 4)
- Données simulées NASA, pas données réelles
- Pas de données en temps réel

**Modèle ML:**
- Basé sur Random Forest (pas de LSTM/GRU pour dépendances temporelles)
- RMSE de 31.73 cycles (marge d'erreur significative)
- R² de 0.42 sur test officiel (variance limitée expliquée)
- Features limitées aux capteurs actuels

**Architecture:**
- Pas d'authentification/authorization
- Déploiement local uniquement
- Pas de CI/CD
- Pas de monitoring

**Tests:**
- Tests unitaires limités (4 tests backend)
- Pas de tests frontend
- Pas de tests E2E
- Pas de tests de charge

### 18.2 Dette Technique

**Documentation:**
- Incohérences corrigées mais historique complexe
- Pas de documentation API Swagger générée (bien que FastAPI la supporte)

**Code:**
- Pas de séparation claire couches contrôleurs/services
- Gestion d'état locale (pas de Redux)
- Pas de gestion d'erreurs centralisée

### 18.3 Fonctionnalités Manquantes

**Fonctionnalités:**
- Authentification des utilisateurs
- Gestion des rôles et permissions
- Notifications (email, SMS)
- Alertes en temps réel
- Historique complet des actions
- Export de données (CSV, PDF)
- Personnalisation du dashboard

**ML:**
- Détection d'anomalies en temps réel
- Modèle LSTM/GRU pour séries temporelles
- Entraînement sur FD002-FD004
- Transfer learning
- Explicabilité du modèle (SHAP, LIME)

### 18.4 Améliorations de Sécurité

**À implémenter:**
- Authentification JWT/OAuth2
- Gestion des rôles (admin, opérateur, lecteur)
- Rate limiting API
- Validation renforcée des entrées
- HTTPS obligatoire
- Rotation des secrets
- Audit logging

### 18.5 Améliorations de Performance

**Backend:**
- Mise en cache des prédictions
- Pagination optimisée
- Indexation base de données
- Async/await pour opérations I/O

**Frontend:**
- Lazy loading des composants
- Virtualization pour listes longues
- Optimisation des graphiques

**ML:**
- Optimisation inférence (quantification)
- Batch predictions
- Modèle plus léger

### 18.6 Améliorations de Scalabilité

**Architecture:**
- Microservices (séparation ML, API, frontend)
- Message queue (RabbitMQ, Kafka)
- Load balancing
- Horizontal scaling

**Base de données:**
- Partitionnement par machine
- Read replicas
- Caching (Redis)

### 18.7 Améliorations IA/ML

**Modèles:**
- LSTM/GRU pour dépendances temporelles
- Attention mechanisms
- Ensemble de modèles
- Auto-encoders pour détection anomalies

**Données:**
- Entraînement sur FD001-FD004
- Data augmentation
- Transfer learning
- Fine-tuning avec données réelles

**Évaluation:**
- Métriques supplémentaires (F1, precision, recall pour classification)
- A/B testing
- Monitoring drift

### 18.8 Fonctionnalités Futures

**Court terme:**
- Authentification basique
- Tests E2E avec Playwright
- Documentation API complète
- Dockerisation

**Moyen terme:**
- Intégration IoT pour données en temps réel
- Interface mobile
- Système d'alertes
- Export de rapports

**Long terme:**
- Déploiement cloud (AWS/Azure/GCP)
- CI/CD complet
- Monitoring et observabilité
- Multi-tenancy

---

## 19. MATÉRIEL UTILE POUR LE RAPPORT

### 19.1 Figures à Inclure

#### Figure 1: Architecture du Système
**Titre:** Architecture globale du système de maintenance prédictive
**Ce qu'elle doit montrer:** Diagramme montrant Frontend → API → Backend → ML Model → Database
**Source:** Section 3.1 de ce dossier

#### Figure 2: Interface Dashboard
**Titre:** Interface utilisateur - Dashboard principal
**Ce qu'elle doit montrer:** Capture d'écran du Dashboard avec statistiques et graphiques
**Source:** Application en cours d'exécution (http://localhost:5173)

#### Figure 3: Interface Test Prediction
**Titre:** Interface utilisateur - Test de prédiction
**Ce qu'elle doit montrer:** Capture d'écran de la page Test Prediction avec formulaire
**Source:** Application en cours d'exécution (http://localhost:5173/test-prediction)

#### Figure 4: Performance du Modèle
**Titre:** Résultats de prédiction vs vérité terrain (test officiel FD001)
**Ce qu'elle doit montrer:** Scatter plot `ml/results/predictions_vs_truth.png`
**Source:** `ml/results/predictions_vs_truth.png`

#### Figure 5: Distribution des Statuts de Maintenance
**Titre:** Distribution des statuts de maintenance dans la base de données
**Ce qu'elle doit montrer:** Graphique camembert montrant répartition NORMAL/MONITOR/MAINTENANCE/CRITICAL
**Source:** Dashboard de l'application

#### Figure 6: Schéma Base de Données
**Titre:** Schéma entité-association de la base de données
**Ce qu'elle doit montrer:** Tables machines, sensor_readings, predictions avec relations
**Source:** Section 6.2 de ce dossier

#### Figure 7: Flux de Données de Prédiction
**Titre:** Flux de données pour une prédiction RUL
**Ce qu'elle doit montrer:** Données capteurs → Normalisation → Modèle ML → Couche décision → Résultat
**Source:** Section 3.9 de ce dossier

#### Figure 8: Interface Maintenance
**Titre:** Interface utilisateur - Recommandations de maintenance
**Ce qu'elle doit montrer:** Capture d'écran de la page Maintenance avec liste priorisée
**Source:** Application en cours d'exécution (http://localhost:5173/maintenance)

### 19.2 Tableaux à Inclure

#### Tableau 1: Métriques de Performance du Modèle
**Titre:** Métriques de performance du modèle Random Forest
**Contenu:**
| Métrique | Entraînement | Validation | Test Interne | Test Officiel |
|----------|--------------|------------|---------------|---------------|
| RMSE | 38.11 | 41.80 | 45.41 | 31.73 |
| MAE | 26.37 | 31.72 | 33.23 | 23.39 |
| R² | 0.69 | 0.62 | 0.59 | 0.42 |
**Source:** `models/model_metadata.json`, `ml/results/computed_training_metrics.json`

#### Tableau 2: Hyperparamètres du Modèle
**Titre:** Hyperparamètres finaux du modèle Random Forest
**Contenu:**
| Paramètre | Valeur |
|-----------|--------|
| n_estimators | 77 |
| max_depth | 9 |
| min_samples_split | 10 |
| min_samples_leaf | 7 |
| max_features | log2 |
| random_state | 42 |
**Source:** `models/model_metadata.json`

#### Tableau 3: Features du Modèle
**Titre:** Caractéristiques utilisées par le modèle (18 features)
**Contenu:**
| Type | Features |
|------|----------|
| Settings | setting_1, setting_2, setting_3 |
| Capteurs | sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9, sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21 |
**Source:** `models/model_metadata.json`

#### Tableau 4: Configuration de la Couche de Décision
**Titre:** Configuration de la couche de décision
**Contenu:**
| Paramètre | Valeur |
|-----------|--------|
| Marge de sécurité | 49 cycles |
| Seuil CRITIQUE | RUL ≤ 20 cycles |
| Seuil MAINTENANCE | 20 < RUL ≤ 50 cycles |
| Seuil MONITOR | 50 < RUL ≤ 100 cycles |
| Seuil NORMAL | RUL > 100 cycles |
| Max RUL pour score santé | 200 cycles |
**Source:** `ml/results/decision_layer_config.json`

#### Tableau 5: Technologies Utilisées
**Titre:** Stack technologique du projet
**Contenu:**
| Composant | Technologie | Version |
|-----------|-------------|---------|
| Backend | Python | 3.8+ |
| API Framework | FastAPI | 0.104.1 |
| ORM | SQLAlchemy | 2.0.23 |
| Base de données | PostgreSQL | 17 |
| Machine Learning | scikit-learn | 1.9.0 |
| Frontend | React | 19.2.8 |
| Build Tool | Vite | 8.2.0 |
| TypeScript | TypeScript | 6.0.2 |
| Styling | TailwindCSS | 4.3.3 |
**Source:** Section 4 de ce dossier

#### Tableau 6: Impact de la Suppression de relative_cycle
**Titre:** Impact de la suppression de la feature relative_cycle (fuite de données)
**Contenu:**
| Modèle | relative_cycle | RMSE Validation |
|--------|----------------|-----------------|
| Original (avec fuite) | OUI | 25.47 cycles |
| Déploiement sûr (sans fuite) | NON | 41.82 cycles |
| Optimisé (sans fuite) | NON | 41.80 cycles |
**Source:** `docs/FINAL_VERIFIED_RESULTS.md`

#### Tableau 7: Endpoints API Principaux
**Titre:** Principaux endpoints de l'API REST
**Contenu:**
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/health | Vérification santé API |
| GET | /api/v1/machines/ | Liste des machines |
| POST | /api/v1/machines/ | Créer machine |
| GET | /api/v1/predictions/ | Liste des prédictions |
| POST | /api/v1/predictions/ | Créer prédiction |
| GET | /api/v1/maintenance/summary | Résumé maintenance |
**Source:** Section 7 de ce dossier

### 19.3 Exemples de Code Importants

#### Exemple 1: Service de Prédiction
**Fichier:** `backend/app/services/prediction_service.py`
**Fonction/Classe:** PredictionService.predict()
**But:** Effectuer une prédiction RUL complète avec couche de décision
**Pourquoi pertinent:** Cœur du système ML, montre l'intégration modèle + décision

```python
def predict(self, sensor_data: dict) -> dict:
    """Make RUL prediction from sensor data"""
    # Extract features in correct order
    feature_order = [
        'setting_1', 'setting_2', 'setting_3',
        'sensor_2', 'sensor_3', 'sensor_4', 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9',
        'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_20', 'sensor_21'
    ]
    
    # Create feature array
    X = np.array([[sensor_data[feature] for feature in feature_order]])
    
    # Scale features
    X_scaled = self.scaler.transform(X)
    
    # Predict RUL
    predicted_rul = self.model.predict(X_scaled)[0]
    
    # Apply decision layer
    decision_result = self.decision_layer.process_prediction(predicted_rul)
    
    return decision_result
```

#### Exemple 2: Couche de Décision
**Fichier:** `ml/src/maintenance_decision.py`
**Fonction/Classe:** MaintenanceDecisionLayer.process_prediction()
**But:** Appliquer marge de sécurité et calculer statut maintenance
**Pourquoi pertinent:** Montre la logique de décision pour recommandations maintenance

```python
def process_prediction(self, predicted_rul):
    """Process a single RUL prediction through the decision layer"""
    # Apply safety margin
    effective_rul = self.apply_safety_margin(predicted_rul)
    
    # Calculate health score
    health_score = self.calculate_health_score(effective_rul)
    
    # Determine maintenance status
    maintenance_status = self.get_maintenance_status(effective_rul)
    
    return {
        'predicted_rul': float(predicted_rul),
        'effective_rul': float(effective_rul),
        'safety_margin_applied': self.safety_margin_cycles,
        'health_score': float(health_score),
        'maintenance_status': maintenance_status
    }
```

#### Exemple 3: Modèle Base de Données
**Fichier:** `backend/app/models/__init__.py`
**Fonction/Classe:** Machine, SensorReading, Prediction
**But:** Définition du schéma de base de données
**Pourquoi pertinent:** Montre la structure des données et relations

```python
class Machine(Base):
    """Machine model for tracking equipment"""
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sensor_readings = relationship("SensorReading", back_populates="machine")
    predictions = relationship("Prediction", back_populates="machine")
```

#### Exemple 4: Entraînement Modèle
**Fichier:** `ml/src/train_deployment_safe.py`
**Fonction/Classe:** train_deployment_safe_rf()
**But:** Entraîner modèle Random Forest sans fuite de données
**Pourquoi pertinent:** Montre le pipeline ML complet

```python
# Train Random Forest
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=random_seed,
    n_jobs=-1
)

rf_model.fit(X_train_scaled, y_train)

# Make predictions
y_train_pred = rf_model.predict(X_train_scaled)
y_val_pred = rf_model.predict(X_val_scaled)
y_test_pred = rf_model.predict(X_test_scaled)
```

#### Exemple 5: API Route Prédiction
**Fichier:** `backend/app/routes/predictions.py`
**Fonction/Classe:** create_prediction()
**But:** Endpoint API pour créer des prédictions
**Pourquoi pertinent:** Montre l'intégration API + ML + Database

```python
@router.post("/", response_model=PredictionResponse, status_code=201)
async def create_prediction(request: PredictionRequest, db: Session = Depends(get_db)):
    """Create a RUL prediction for a machine based on sensor data"""
    # Verify machine exists
    machine = db.query(Machine).filter(Machine.id == request.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Make prediction using ML model
    sensor_data = request.model_dump()
    prediction_result = prediction_service.predict(sensor_data)
    
    # Store sensor reading
    sensor_reading = SensorReading(**sensor_data)
    db.add(sensor_reading)
    db.commit()
    db.refresh(sensor_reading)
    
    # Store prediction
    db_prediction = Prediction(
        machine_id=request.machine_id,
        sensor_reading_id=sensor_reading.id,
        predicted_rul=prediction_result['predicted_rul'],
        effective_rul=prediction_result['effective_rul'],
        health_score=prediction_result['health_score'],
        maintenance_status=prediction_result['maintenance_status'],
        safety_margin_applied=prediction_result['safety_margin_applied']
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction
```

---

## 20. RÉSUMÉ EXÉCUTIF FINAL

### 20.1 Objectif du Projet
Développer un système complet de maintenance prédictive pour moteurs d'avion (turbofans) utilisant l'apprentissage automatique pour prédire la Durée de Vie Restante (RUL) et fournir des recommandations de maintenance basées sur des seuils de sécurité.

### 20.2 Problème Résolu
Remplacer la maintenance préventive (coûteuse) et corrective (pannes imprévues) par un système de maintenance prédictif basé sur l'IA qui analyse les données de capteurs en temps réel pour estimer la durée de vie restante et planifier les interventions de manière optimale.

### 20.3 Solution Proposée
Un système full-stack composé de:
- **Modèle ML Random Forest** entraîné sur le dataset NASA C-MAPSS FD001
- **Couche de décision** avec marge de sécurité (49 cycles) et score de santé
- **API REST FastAPI** pour les prédictions en temps réel
- **Interface React** de style SCADA pour la visualisation
- **Base de données PostgreSQL** pour stocker les données historiques

### 20.4 Architecture
**3-tiers:**
1. **Frontend:** React 19 + TypeScript + TailwindCSS (Dashboard, Machines, Maintenance, TestPrediction)
2. **Backend:** FastAPI + SQLAlchemy + PostgreSQL (API REST, service prédiction, ORM)
3. **ML:** Random Forest + StandardScaler + Couche décision (18 features, sans fuite de données)

**Flux:** Utilisateur → Interface React → API FastAPI → Service Prédiction → Modèle ML → Couche Décision → Base de Données → Résultat

### 20.5 Technologies
- **Backend:** Python 3.8+, FastAPI 0.104.1, SQLAlchemy 2.0.23, PostgreSQL 17
- **Frontend:** React 19.2.8, TypeScript 6.0.2, Vite 8.2.0, TailwindCSS 4.3.3, Recharts 3.10.1
- **ML:** scikit-learn 1.9.0, joblib 1.3.2, pandas 2.0.3, numpy 1.24.3
- **Tests:** pytest 7.4.3

### 20.6 Fonctionnalités Principales
- Dashboard avec statistiques globales et graphiques
- Liste des machines avec prédictions individuelles et sparklines
- Recommandations de maintenance priorisées
- Test de prédiction interactif avec exemples pré-remplis
- API REST complète (machines, prédictions, maintenance)
- Base de données peuplée avec données de démonstration

### 20.7 Composants IA/ML
**Modèle:** RandomForestRegressor (n_estimators=77, max_depth=9)
**Features:** 18 (3 settings + 15 capteurs, sans relative_cycle)
**Dataset:** NASA C-MAPSS FD001 (100 moteurs entraînement, 100 test)
**Performance:** RMSE 31.73 cycles sur test officiel, R² 0.42
**Couche décision:** Marge sécurité 49 cycles, seuils 20/50/100 cycles, score santé 0-100
**Validation:** Check fuite de données PASSED, surapprentissage minimal (ratios < 1.5)

### 20.8 Rôle de Devin Agent
**Statut:** Information non disponible dans le projet (pas de traces explicites d'utilisation de Devin Agent dans le code ou la documentation)

### 20.9 Résultats
- ✅ Modèle ML optimisé et déployé
- ✅ API REST fonctionnelle avec 8 endpoints
- ✅ Interface utilisateur complète avec 4 pages
- ✅ Base de données peuplée (8 machines, 80 lectures, 80 prédictions)
- ✅ Évaluation sur dataset officiel (RMSE 31.73, MAE 23.39)
- ✅ Documentation technique complète
- ✅ Système prêt pour démonstration académique

### 20.10 Limitations
- Dataset unique (FD001 uniquement, pas généralisé)
- RMSE de 31.73 cycles (marge d'erreur)
- Pas d'authentification/authorization
- Déploiement local uniquement
- Tests limités (4 tests unitaires backend)
- Pas de dépendances temporelles explicites (pas LSTM/GRU)

### 20.11 Perspectives Futures
- Entraînement sur FD002-FD004 pour généralisation
- Implémentation LSTM/GRU pour dépendances temporelles
- Authentification et gestion des rôles
- Intégration IoT pour données en temps réel
- Déploiement cloud et CI/CD
- Tests E2E automatisés
- Interface mobile pour techniciens
- Système d'alertes par email/SMS

---

**FIN DU DOSSIER TECHNIQUE**

**Version:** 1.0  
**Date:** 24 août 2026  
**Statut:** Complet et vérifié depuis artefacts du projet  
**Source:** Analyse complète du codebase, configuration, documentation, et artefacts sauvegardés
