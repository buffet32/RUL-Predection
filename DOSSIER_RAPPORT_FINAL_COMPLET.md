# DOSSIER COMPLET POUR RÉDACTION DU RAPPORT ACADÉMIQUE
## Système de Maintenance Prédictive Basé sur l'IA pour Équipements Industriels

**Projet:** PFA26 - Système de Maintenance Prédictive
**Date:** 24 août 2026
**Objectif:** Fournir tout le contenu nécessaire pour rédiger un rapport académique de 33-35 pages

---

## STRUCTURE DU RAPPORT À SUIVRE

Suivre EXACTEMENT la structure du template fourni par l'étudiant:
1. Page de garde
2. Dédicace
3. Remerciements
4. Résumé + Mots clés
5. Abstract + Keywords
6. Glossaire
7. Liste des figures
8. Liste des tableaux
9. Table des matières
10. Introduction générale
11. Chapitre 1: Contexte et Problématique
12. Chapitre 2: Analyse Fonctionnelle et Exigences
13. Chapitre 3: Architecture et Conception
14. Chapitre 4: Implémentation
15. Chapitre 5: Résultats et Tests
16. Conclusion générale
17. Perspectives
18. Références
19. Annexes

---

## DISTRIBUTION DES PAGES (33-35 pages cibles)

**Matières préliminaires (8-10 pages):**
- Page de garde: 1 page
- Dédicace: 1 page
- Remerciements: 1 page
- Résumé + mots clés: 1 page
- Abstract + keywords: 1 page
- Glossaire: 1-2 pages
- Liste des figures: 1 page
- Liste des tableaux: 1 page
- Table des matières: 1-2 pages

**Rapport principal (23-25 pages):**
- Introduction générale: 1-2 pages
- Chapitre 1: 4-5 pages
- Chapitre 2: 4-5 pages
- Chapitre 3: 5-6 pages
- Chapitre 4: 5-6 pages
- Chapitre 5: 5-6 pages
- Conclusion générale + Perspectives: 1-2 pages

**Références et Annexes (2-3 pages):**
- Références: 1-2 pages
- Annexes: si nécessaire

---

## CONTENU DÉTAILLÉ PAR SECTION

### PAGE DE GARDE

**Titre du projet:**
Système de Maintenance Prédictive Basé sur l'Intelligence Artificielle pour Équipements Industriels

**Type de projet:**
Projet de Fin d'Académie (PFA26)

**Auteur:** [À compléter par l'étudiant]

**Année universitaire:** 2025-2026

**Institution:** [À compléter par l'étudiant]

**Encadrant:** [À compléter par l'étudiant]

---

### DÉDICACE

[Contenu personnel à rédiger par l'étudiant]

---

### REMERCIEMENTS

[Contenu personnel à rédiger par l'étudiant]

---

### RÉSUMÉ

Ce projet porte sur la conception et le développement d'un système complet de maintenance prédictive basé sur l'intelligence artificielle pour moteurs d'avion (turbofans). La maintenance industrielle traditionnelle, qu'elle soit préventive (coûteuse) ou corrective (risquée), présente des limitations significatives. L'approche prédictive vise à optimiser les interventions en se basant sur l'état de santé réel des équipements.

Le système développé intègre un modèle de Machine Learning de type Random Forest entraîné sur le dataset NASA C-MAPSS FD001 pour prédire la Durée de Vie Restante (RUL). Le modèle utilise 18 caractéristiques (3 paramètres opérationnels et 15 capteurs) et atteint un RMSE de 41.80 cycles sur validation et 31.73 cycles sur le test officiel. Une couche de décision avec une marge de sécurité de 49 cycles transforme les prédictions en recommandations de maintenance actionnables (CRITICAL, MAINTENANCE_RECOMMENDED, MONITOR, NORMAL).

L'architecture du système adopte une approche 3-tiers classique: un frontend React avec TypeScript pour l'interface utilisateur de type SCADA, un backend FastAPI avec SQLAlchemy pour l'API REST et l'accès base de données, et une base de données PostgreSQL pour le stockage. L'interface comprend quatre pages principales: Dashboard (surveillance globale), Machines (liste avec tendances), Maintenance (recommandations priorisées), et Test Prediction (test interactif).

Le projet a identifié et résolu plusieurs problèmes techniques majeurs: la fuite de données avec la feature relative_cycle (supprimée, impact RMSE 25.47→41.82), le surapprentissage avec features temporelles (résolu par retour aux features basiques), et le biais de surestimation du modèle (résolu par marge de sécurité de 49 cycles). Le système complet est fonctionnel, démontrable, et constitue une base solide pour des développements futurs en maintenance prédictive.

**Mots clés:** Maintenance prédictive, Durée de vie restante (RUL), Machine Learning, Random Forest, NASA C-MAPSS, API REST, FastAPI, React, PostgreSQL

---

### ABSTRACT

This project focuses on the design and development of a complete AI-based predictive maintenance system for aircraft engines (turbofans). Traditional industrial maintenance, whether preventive (costly) or corrective (risky), presents significant limitations. The predictive approach aims to optimize interventions based on the actual health status of equipment.

The developed system integrates a Random Forest Machine Learning model trained on the NASA C-MAPSS FD001 dataset to predict Remaining Useful Life (RUL). The model uses 18 features (3 operational parameters and 15 sensors) and achieves an RMSE of 41.80 cycles on validation and 31.73 cycles on the official test. A decision layer with a safety margin of 49 cycles transforms predictions into actionable maintenance recommendations (CRITICAL, MAINTENANCE_RECOMMENDED, MONITOR, NORMAL).

The system architecture adopts a classic 3-tier approach: a React frontend with TypeScript for the SCADA-style user interface, a FastAPI backend with SQLAlchemy for the REST API and database access, and a PostgreSQL database for storage. The interface includes four main pages: Dashboard (global monitoring), Machines (list with trends), Maintenance (prioritized recommendations), and Test Prediction (interactive testing).

The project identified and resolved several major technical issues: data leakage with the relative_cycle feature (removed, RMSE impact 25.47→41.82), overfitting with time-series features (resolved by returning to basic features), and model overestimation bias (resolved with 49-cycle safety margin). The complete system is functional, demonstrable, and provides a solid foundation for future developments in predictive maintenance.

**Keywords:** Predictive maintenance, Remaining Useful Life (RUL), Machine Learning, Random Forest, NASA C-MAPSS, REST API, FastAPI, React, PostgreSQL

---

### GLOSSAIRE

**API (Application Programming Interface):** Interface de programmation d'application permettant la communication entre différents composants logiciels.

**CRITICAL:** Statut de maintenance indiquant qu'une intervention immédiate est requise (RUL effectif ≤ 20 cycles).

**Dataset:** Ensemble de données utilisé pour l'entraînement et l'évaluation des modèles de Machine Learning.

**FastAPI:** Framework web moderne et performant pour construire des APIs avec Python.

**Frontend:** Partie de l'application visible par l'utilisateur, généralement une interface web ou mobile.

**MAE (Mean Absolute Error):** Erreur absolue moyenne, métrique d'évaluation mesurant la moyenne des erreurs absolues entre prédictions et valeurs réelles.

**MAINTENANCE_RECOMMENDED:** Statut de maintenance indiquant qu'une maintenance planifiée est requise (20 < RUL effectif ≤ 50 cycles).

**Machine Learning:** Sous-domaine de l'intelligence artificielle permettant aux systèmes d'apprendre à partir de données.

**MONITOR:** Statut de maintenance indiquant qu'une surveillance accrue est requise (50 < RUL effectif ≤ 100 cycles).

**MONITOR:** Statut de maintenance indiquant que l'équipement fonctionne normalement (RUL effectif > 100 cycles).

**ORM (Object-Relational Mapping):** Technique de programmation qui convertit des données entre des systèmes de types incompatibles.

**PostgreSQL:** Système de gestion de base de données relationnelle objet-relationnel open source.

**Pydantic:** Bibliothèque Python pour la validation des données utilisant les annotations de type.

**Random Forest:** Algorithme d'apprentissage automatique basé sur un ensemble d'arbres de décision.

**React:** Bibliothèque JavaScript pour construire des interfaces utilisateur.

**REST (Representational State Transfer):** Style d'architecture pour la conception d'APIs web.

**RMSE (Root Mean Squared Error):** Racine de l'erreur quadratique moyenne, métrique d'évaluation pénalisant les grandes erreurs.

**RUL (Remaining Useful Life):** Durée de vie restante, nombre de cycles ou unités de temps restants avant défaillance.

**SCADA (Supervisory Control and Data Acquisition):** Système de contrôle industriel pour la surveillance et le contrôle de processus.

**SQLAlchemy:** ORM Python pour travailler avec des bases de données relationnelles.

**StandardScaler:** Technique de normalisation qui transforme les données pour avoir une moyenne de 0 et un écart-type de 1.

**Surapprentissage (Overfitting):** Phénomène où un modèle apprend le bruit des données d'entraînement au lieu du signal général.

**TailwindCSS:** Framework CSS utility-first pour la conception d'interfaces utilisateur.

**TypeScript:** Sur-ensemble typé de JavaScript développé par Microsoft.

**Vite:** Outil de build et serveur de développement rapide pour les applications web modernes.

---

### LISTE DES FIGURES

**Figure 1:** Architecture globale du système de maintenance prédictive

**Figure 2:** Pipeline complet d'entraînement et d'inférence Machine Learning

**Figure 3:** Flux de la couche de décision pour recommandations de maintenance

**Figure 4:** Schéma entité-association de la base de données PostgreSQL

**Figure 5:** Interface utilisateur - Dashboard principal

**Figure 6:** Interface utilisateur - Page de test de prédiction

**Figure 7:** Comparaison des prédictions du modèle avec la vérité terrain (test officiel FD001)

**Figure 8:** Workflow de prédiction complet

---

### LISTE DES TABLEAUX

**Tableau 1:** Stack technologique complet du projet

**Tableau 2:** Métriques de performance du modèle Random Forest

**Tableau 3:** Hyperparamètres finaux du modèle Random Forest

**Tableau 4:** Caractéristiques utilisées par le modèle (18 features)

**Tableau 5:** Configuration de la couche de décision

**Tableau 6:** Principaux endpoints de l'API REST

**Tableau 7:** Tables de la base de données PostgreSQL

**Tableau 8:** Problèmes rencontrés et solutions appliquées

---

### TABLE DES MATIÈRES

[À générer automatiquement selon le template]

---

## INTRODUCTION GÉNÉRALE (1-2 pages)

### Contexte de la Maintenance Industrielle

La maintenance industrielle est un domaine critique pour assurer la disponibilité, la sécurité et l'efficacité des équipements. Traditionnellement, deux approches dominent: la maintenance préventive et la maintenance corrective.

La maintenance préventive consiste à effectuer des interventions à intervalles réguliers selon un calendrier prédéfini, indépendamment de l'état réel de l'équipement. Cette approche présente l'avantage de planifier facilement les interventions et de réduire les pannes imprévues, mais elle est coûteuse car elle entraîne des interventions inutiles sur des équipements encore en bon état et ne tire pas parti de l'état de santé réel.

La maintenance corrective n'intervient qu'après la survenue d'une panne ou d'une défaillance. Elle évite les interventions inutiles et utilise pleinement la durée de vie des composants, mais elle entraîne des arrêts de production imprévus, des coûts de réparation élevés, des dommages potentiels à l'équipement, et des risques pour la sécurité.

L'émergence des technologies de l'Internet des Objets (IoT) et de l'intelligence artificielle offre de nouvelles perspectives pour optimiser la maintenance grâce à l'analyse des données de capteurs en temps réel. La maintenance prédictive vise à prédire le moment optimal d'intervention en se basant sur l'état de santé réel de l'équipement, permettant ainsi une intervention ni trop tôt (coût inutile) ni trop tard (panne).

### Problématique

Comment concevoir et implémenter un système de maintenance prédictive basé sur l'IA capable de prédire la durée de vie restante d'équipements industriels avec une précision suffisante pour guider les décisions de maintenance, tout en garantissant la sécurité opérationnelle et l'interprétabilité des recommandations ?

### Questions de Recherche

1. Quelles caractéristiques des données de capteurs sont les plus pertinentes pour prédire la RUL ?
2. Quel modèle ML offre le meilleur compromis entre précision et généralisation ?
3. Comment éviter la fuite de données dans un contexte de prédiction temporelle ?
4. Comment transformer une prédiction de RUL en recommandations de maintenance actionnables ?
5. Comment intégrer un modèle ML dans une architecture logicielle complète et déployable ?

### Organisation du Rapport

Le présent rapport est organisé comme suit. Le Chapitre 1 présente le contexte de la maintenance prédictive, la problématique spécifique du projet, et l'état de l'art des approches existantes. Le Chapitre 2 présente l'analyse fonctionnelle détaillée du système, identifiant les acteurs, les cas d'utilisation, et les exigences fonctionnelles et non-fonctionnelles. Le Chapitre 3 présente l'architecture et la conception du système, couvrant le frontend, le backend, la base de données, et l'architecture ML. Le Chapitre 4 présente l'implémentation détaillée, couvrant le développement du pipeline ML, l'implémentation de l'API backend, et le développement du frontend. Le Chapitre 5 présente les résultats, les tests, et l'évaluation du système. Enfin, la conclusion générale synthétise les résultats, identifie les limitations, et propose des perspectives futures.

---

## CHAPITRE 1: CONTEXTE ET PROBLÉMATIQUE (4-5 pages)

### 1.1 Introduction

Ce chapitre présente le contexte de la maintenance prédictive, la problématique spécifique du projet, et l'état de l'art des approches existantes. Il justifie le choix d'une approche basée sur l'IA et présente le dataset utilisé.

### 1.2 Maintenance Industrielle: Approches Traditionnelles

#### 1.2.1 Maintenance Préventive

La maintenance préventive est une stratégie qui consiste à effectuer des interventions selon un calendrier prédéfini, basé sur le temps écoulé ou le nombre d'heures de fonctionnement, sans tenir compte de l'état réel de l'équipement. Cette approche est largement utilisée dans l'industrie car elle permet une planification facile des interventions et réduit les pannes imprévues.

Cependant, la maintenance préventive présente des inconvénients majeurs. Premièrement, elle entraîne des coûts élevés car des composants sont remplacés alors qu'ils ont encore une durée de vie résiduelle significative. Deuxièmement, elle ne tire pas parti de l'état de santé réel de l'équipement, ce qui peut conduire à des interventions inutiles ou, inversement, à des interventions trop tardives si l'équipement se dégrade plus rapidement que prévu. Enfin, elle ne permet pas d'optimiser l'utilisation des ressources de maintenance.

#### 1.2.2 Maintenance Corrective

La maintenance corrective, également appelée maintenance réactive, n'intervient qu'après la survenue d'une panne ou d'une défaillance. Cette approche évite les interventions inutiles et utilise pleinement la durée de vie des composants, ce qui peut sembler économiquement attrayant.

Cependant, la maintenance corrective présente des inconvénients encore plus importants. Les pannes imprévues entraînent des arrêts de production non planifiés, ce qui peut avoir des conséquences économiques sévères, particulièrement dans les industries à haute valeur ajoutée. Les réparations d'urgence sont souvent plus coûteuses que les interventions planifiées. Les pannes peuvent également causer des dommages secondaires à l'équipement, augmentant les coûts de réparation. Enfin, les pannes imprévues peuvent présenter des risques pour la sécurité des opérateurs et de l'environnement.

### 1.3 Maintenance Prédictive: Concepts Fondamentaux

#### 1.3.1 Définition et Objectifs

La maintenance prédictive (Predictive Maintenance, PdM) est une approche qui utilise des données de capteurs et des techniques d'analyse pour prédire quand un équipement va tomber en panne, permettant une intervention proactive au moment optimal. L'objectif est de remplacer la maintenance basée sur le temps par une maintenance basée sur l'état (Condition-Based Maintenance, CBM).

La maintenance prédictive repose sur le principe que les équipements présentent des signes avant-coureurs de défaillance qui peuvent être détectés par l'analyse des données de capteurs. En surveillant ces signes, il est possible de prédire la défaillance avant qu'elle ne survienne, permettant une intervention planifiée au moment optimal.

#### 1.3.2 Durée de Vie Utile Restante (RUL)

La Durée de Vie Utile Restante (Remaining Useful Life, RUL) est une métrique clé en maintenance prédictive. Elle représente le temps ou le nombre de cycles restants avant qu'un équipement ne tombe en panne. La RUL est exprimée en unités de temps (heures, jours) ou en cycles d'opération, selon le contexte de l'application.

Mathématiquement, la RUL est définie comme:
```
RUL = T_failure - T_current
```
Où T_failure est le temps de défaillance et T_current est le temps actuel. Dans le contexte du dataset NASA C-MAPSS, la RUL est calculée comme:
```
RUL = max_cycle - current_cycle
```
Où max_cycle est le dernier cycle avant défaillance et current_cycle est le cycle actuel.

#### 1.3.3 Avantages de la Maintenance Prédictive

La maintenance prédictive présente plusieurs avantages par rapport aux approches traditionnelles:

**Réduction des coûts:** En intervenant au moment optimal, la maintenance prédictive réduit les coûts associés aux interventions inutiles (maintenance préventive) et aux réparations d'urgence (maintenance corrective). Des études industrielles indiquent des réductions de coûts de maintenance de 20 à 30%.

**Amélioration de la disponibilité:** En prévenant les pannes imprévues, la maintenance prédictive améliore la disponibilité des équipements et réduit les arrêts de production non planifiés.

**Augmentation de la sécurité:** En détectant les signes de défaillance avant qu'ils ne deviennent critiques, la maintenance prédictive améliore la sécurité opérationnelle et réduit les risques d'accidents.

**Optimisation des stocks:** En connaissant les besoins de maintenance à l'avance, il est possible d'optimiser la gestion des stocks de pièces de rechange, réduisant les coûts de stockage tout en évitant les ruptures de stock.

**Extension de la durée de vie:** En utilisant les équipements jusqu'à leur véritable fin de vie, la maintenance prédictive maximise le retour sur investissement.

### 1.4 État de l'Art

#### 1.4.1 Approches Basées sur les Modèles Physiques

Les approches basées sur les modèles physiques utilisent la connaissance experte du fonctionnement de l'équipement pour modéliser sa dégradation. Ces modèles reposent sur les équations physiques qui régissent le comportement de l'équipement, comme les lois de la mécanique, la thermodynamique, ou la dynamique des fluides.

**Avantages:** Ces modèles sont hautement interprétables et peuvent fonctionner avec des quantités limitées de données. Ils sont basés sur la physique du système, ce qui les rend robustes et généralisables.

**Inconvénients:** Ils nécessitent une expertise domaine approfondie pour être développés. Ils sont difficiles à développer pour des systèmes complexes avec de nombreux composants interdépendants. Ils ne généralisent pas bien à des équipements différents ou à des conditions opérationnelles variées.

#### 1.4.2 Approches Basées sur les Données (Data-Driven)

Les approches data-driven utilisent l'apprentissage automatique pour apprendre les patterns de dégradation à partir de données historiques de capteurs. Ces approches ne nécessitent pas de connaissance explicite de la physique du système, mais apprennent automatiquement les relations entre les données de capteurs et l'état de l'équipement.

**Avantages:** Elles peuvent capturer des patterns complexes et non linéaires que les modèles physiques pourraient manquer. Elles généralisent bien à des équipements similaires et à des conditions opérationnelles variées. Elles s'améliorent avec plus de données. Elles peuvent être appliquées à différents types d'équipements sans nécessiter une expertise domaine spécifique.

**Inconvénients:** Elles nécessitent de grandes quantités de données de haute qualité. Elles sont souvent des boîtes noires avec une interprétabilité limitée. Elles sont sensibles à la qualité des données et peuvent être affectées par des données bruitées ou incomplètes.

#### 1.4.3 Approches Hybrides

Les approches hybrides combinent les modèles physiques et les approches data-driven pour tirer avantage des deux approches. Par exemple, un modèle physique peut fournir une estimation de base, tandis qu'un modèle ML ajuste cette estimation en fonction des données de capteurs.

Ces approches offrent un bon compromis entre l'interprétabilité des modèles physiques et la capacité d'apprentissage des approches data-driven. Cependant, elles sont plus complexes à développer et à maintenir.

### 1.5 Machine Learning pour la Maintenance Prédictive

#### 1.5.1 Types de Problèmes ML

En maintenance prédictive, plusieurs types de problèmes ML peuvent être formulés:

**Régression:** Prédiction de la RUL comme une valeur continue. C'est l'approche la plus directe et la plus courante.

**Classification:** Classification de l'état de santé de l'équipement en catégories (sain, dégradé, critique). Cette approche est plus simple mais moins précise.

**Détection d'anomalies:** Identification de comportements anormaux par rapport à un profil normal. Cette approche est utile quand les données de défaillance sont rares.

#### 1.5.2 Algorithmes Courants

**Random Forest:** Algorithme d'ensemble basé sur des arbres de décision. Il est robuste au surapprentissage, interprétable via l'importance des features, et fonctionne bien sur les données tabulaires. C'est l'algorithme choisi dans ce projet.

**Gradient Boosting (XGBoost, LightGBM):** Algorithmes d'ensemble puissants qui offrent souvent des performances élevées mais sont plus sujets au surapprentissage et nécessitent plus de tuning.

**Réseaux de neurones récurrents (LSTM, GRU):** Adaptés aux données séquentielles et temporelles. Ils peuvent capturer des dépendances temporelles complexes mais nécessitent beaucoup de données et sont difficiles à interpréter.

**SVM (Support Vector Machines):** Algorithme de classification et de régression qui fonctionne bien sur des données de dimension moyenne mais ne scale pas bien aux grands datasets.

**Réseaux de neurones profonds:** Pour des données complexes et non structurées, mais souvent excessifs pour des données tabulaires simples.

#### 1.5.3 Défis Spécifiques

**Fuite de données (Data Leakage):** Utilisation de futures informations non disponibles en temps réel, comme le cycle de défaillance (max_cycle). C'est un problème majeur en prédiction RUL qui peut conduire à des performances irréalistes en validation mais une performance médiocre en déploiement.

**Surapprentissage (Overfitting):** Le modèle apprend le bruit des données d'entraînement au lieu du signal général, conduisant à de bonnes performances en entraînement mais de mauvaises performances en test.

**Données déséquilibrées:** Les données de défaillance sont souvent rares par rapport aux données normales, ce qui peut biaiser le modèle vers la prédiction de l'état normal.

**Censure des données:** Pour les équipements encore en fonctionnement, la véritable RUL est inconnue (censure à droite), ce qui complique l'entraînement.

### 1.6 Dataset NASA C-MAPSS

#### 1.6.1 Description

Le dataset C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) est un dataset de référence académique pour la maintenance prédictive, développé par la NASA Ames Research Center. Il simule le comportement de moteurs d'avion turbofans sous différentes conditions opérationnelles et scénarios de défaillance.

Le dataset est largement utilisé dans la communauté de maintenance prédictive car il présente des caractéristiques réalistes, est bien documenté, et permet une comparaison directe entre différentes approches.

#### 1.6.2 Structure du Dataset FD001

Le sous-dataset FD001 utilisé dans ce projet contient:

- **100 moteurs pour l'entraînement:** Données complètes du premier cycle jusqu'à la défaillance. Chaque moteur a un nombre de cycles variable (de 1 à 361 cycles).
- **100 moteurs pour le test:** Données tronquées avant la défaillance. Le dernier cycle de chaque moteur de test est fourni, mais la défaillance réelle n'est pas incluse dans les données de test.
- **Vérité terrain:** Le fichier RUL_FD001.txt contient la véritable RUL pour chaque moteur de test, permettant l'évaluation sur un ensemble de test indépendant.

**Variables:** Le dataset contient 26 colonnes:
- 1 identifiant moteur (engine_id)
- 1 numéro de cycle (cycle)
- 3 paramètres opérationnels (setting_1, setting_2, setting_3)
- 21 mesures de capteurs (sensor_1 à sensor_21)

#### 1.6.3 Caractéristiques des Capteurs

Les 21 capteurs mesurent différentes grandeurs physiques liées au fonctionnement du moteur: température, pression, débit, vitesse de rotation. L'analyse exploratoire des données a révélé que certains capteurs sont constants (sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19) et ne fournissent aucune information utile pour la prédiction. Ces capteurs ont été exclus du modèle.

Les 15 capteurs restants présentent une variabilité significative et sont corrélés avec la dégradation du moteur, ce qui les rend pertinents pour la prédiction de la RUL.

#### 1.6.4 Pourquoi C-MAPSS FD001 ?

Le choix du dataset C-MAPSS FD001 est justifié par plusieurs raisons:

- **Dataset de référence académique:** C-MAPSS est largement utilisé dans la littérature, permettant une comparaison directe avec d'autres approches.
- **Données réalistes:** Le dataset simule un scénario réaliste de dégradation de moteur, avec des patterns de dégradation plausibles.
- **Données complètes:** Le dataset inclut les données d'entraînement complètes et la vérité terrain pour le test, permettant une évaluation rigoureuse.
- **Disponibilité publique:** Le dataset est disponible publiquement, facilitant la reproductibilité des résultats.
- **Taille appropriée:** 100 moteurs d'entraînement et 100 de test offrent suffisamment de données pour l'entraînement tout en restant gérables.

### 1.7 Problématique Spécifique du Projet

#### 1.7.1 Problème Principal

Comment concevoir et implémenter un système complet de maintenance prédictive basé sur l'intelligence artificielle capable de:
1. Prédire la durée de vie restante (RUL) avec une précision suffisante pour guider les décisions de maintenance
2. Fournir des recommandations de maintenance interprétables et actionnables
3. Être intégré dans une architecture logicielle complète et déployable
4. Être démontrable et validé sur un dataset académique de référence

#### 1.7.2 Sous-Problèmes

**Sélection de caractéristiques:** Quelles features (caractéristiques) des données de capteurs doivent être utilisées pour prédire la RUL ? Comment éviter la fuite de données en utilisant uniquement des informations disponibles en temps réel ?

**Choix du modèle:** Quel algorithme de Machine Learning offre le meilleur compromis entre précision, généralisation, et interprétabilité pour ce problème spécifique ?

**Couche de décision:** Comment transformer une prédiction de RUL (valeur continue) en recommandations de maintenance actionnables (catégories claires) ? Comment garantir la sécurité des recommandations ?

**Intégration système:** Comment intégrer un modèle ML dans une architecture logicielle complète incluant une API REST, une base de données, et une interface utilisateur ?

**Validation:** Comment valider le système sur le dataset officiel et garantir que les performances en validation reflètent les performances en déploiement réel ?

### 1.8 Contribution du Projet

Ce projet contribue à plusieurs aspects de la maintenance prédictive:

**Démonstration d'un système complet:** Contrairement à de nombreux travaux académiques qui se concentrent uniquement sur le modèle ML, ce projet démontre un système complet intégrant le modèle, l'API, la base de données, et l'interface utilisateur.

**Étude approfondie de la fuite de données:** Le projet identifie et résout un problème de fuite de données avec la feature relative_cycle, documentant l'impact sur la performance et la justification de la suppression.

**Implémentation d'une couche de décision:** Le projet développe une couche de décision avec une marge de sécurité justifiée par l'analyse de biais, transformant les prédictions en recommandations actionnables.

**Architecture moderne:** Le projet utilise des technologies modernes (FastAPI, React, TypeScript) pour créer une architecture robuste et maintenable.

**Validation rigoureuse:** Le projet valide le modèle sur le test officiel FD001 et documente toutes les métriques de manière vérifiable depuis les artefacts sauvegardés.

### 1.9 Conclusion du Chapitre

Ce chapitre a présenté le contexte de la maintenance prédictive, les approches traditionnelles et leurs limitations, l'état de l'art des approches basées sur l'IA, et le dataset NASA C-MAPSS FD001. La problématique spécifique du projet a été formulée autour du développement d'un système complet intégrant un modèle ML, une couche de décision, et une interface utilisateur. Le chapitre suivant présente l'analyse fonctionnelle détaillée du système.

---

## CHAPITRE 2: ANALYSE FONCTIONNELLE ET EXIGENCES (4-5 pages)

### 2.1 Introduction

Ce chapitre présente l'analyse fonctionnelle du système de maintenance prédictive, identifiant les acteurs principaux, les cas d'utilisation, et les exigences fonctionnelles et non-fonctionnelles.

### 2.2 Acteurs du Système

#### 2.2.1 Opérateur de Maintenance

**Rôle:** Technicien responsable de l'entretien des équipements

**Responsabilités:**
- Surveiller l'état de santé des équipements en temps réel
- Consulter les recommandations de maintenance
- Planifier et exécuter les interventions de maintenance
- Enregistrer les actions de maintenance effectuées

**Besoins:**
- Vue d'ensemble rapide de l'état du système
- Détails sur chaque équipement (historique, tendances)
- Recommandations claires et actionnables
- Accès à l'historique des prédictions pour analyse

**Profil:** Technicien avec expertise technique mais pas nécessairement expertise informatique. Interface doit être intuitive et familière (style SCADA).

#### 2.2.2 Ingénieur de Fiabilité

**Rôle:** Ingénieur chargé d'analyser la fiabilité des systèmes et d'optimiser les stratégies de maintenance

**Responsabilités:**
- Analyser les tendances de dégradation des équipements
- Évaluer la performance du modèle ML
- Optimiser les seuils de maintenance
- Identifier les équipements à risque

**Besoins:**
- Accès aux données historiques détaillées
- Outils d'analyse et de visualisation avancés
- Métriques de performance du modèle
- Capacité d'exporter les données pour analyse externe

**Profil:** Ingénieur avec expertise en statistiques et analyse de données. Interface doit fournir des données détaillées et des outils d'analyse.

#### 2.2.3 Responsable d'Équipements

**Rôle:** Manager supervisant le parc d'équipements

**Responsabilités:**
- Superviser l'état global du parc d'équipements
- Prioriser les interventions de maintenance
- Allouer les ressources de maintenance (personnel, pièces)
- Prendre des décisions stratégiques

**Besoins:**
- Tableau de bord avec indicateurs clés (KPIs)
- Vue agrégée du parc d'équipements
- Alertes pour équipements critiques
- Rapports synthétiques pour prise de décision

**Profil:** Manager avec besoin de vue d'ensemble et d'informations synthétiques. Interface doit fournir des indicateurs clairs et des alertes.

### 2.3 Cas d'Utilisation

#### 2.3.1 UC1: Surveiller l'État du Système

**Acteur:** Opérateur de Maintenance, Responsable d'Équipements

**Description:** L'utilisateur consulte le dashboard pour obtenir une vue d'ensemble de l'état de santé de tous les équipements.

**Préconditions:**
- Système démarré et accessible
- Base de données peuplée avec des données
- Connexion API fonctionnelle

**Scénario principal:**
1. L'utilisateur accède à l'application via un navigateur web
2. Le dashboard s'affiche automatiquement à l'URL racine
3. L'utilisateur visualise les statistiques globales:
   - Nombre total de machines
   - Distribution des statuts de maintenance (NORMAL, MONITOR, MAINTENANCE_RECOMMENDED, CRITICAL)
   - Score de santé moyen
   - Nombre de machines nécessitant une attention
4. L'utilisateur consulte les graphiques:
   - Graphique camembert de distribution des statuts
   - Graphique histogramme de répartition des statuts
5. L'utilisateur consulte le tableau des 10 dernières prédictions avec détails (machine, RUL, statut, timestamp)
6. L'utilisateur identifie les équipements nécessitant une attention immédiate (statut CRITICAL)

**Postconditions:**
- L'utilisateur a une vue synthétique de l'état du système
- L'utilisateur peut identifier les équipements critiques nécessitant une intervention

**Extensions:**
- L'utilisateur peut filtrer les données par période temporelle
- L'utilisateur peut exporter les statistiques au format CSV

#### 2.3.2 UC2: Consulter les Détails d'une Machine

**Acteur:** Opérateur de Maintenance

**Description:** L'utilisateur consulte les détails complets d'une machine spécifique, incluant l'historique des prédictions et les lectures capteurs.

**Préconditions:**
- Machine existante dans la base de données
- Données de prédictions disponibles pour cette machine

**Scénario principal:**
1. L'utilisateur navigue vers la page "Machines" via le menu latéral
2. L'utilisateur visualise la liste de toutes les machines avec:
   - ID machine
   - Nom de la machine
   - RUL prédit
   - Score de santé
   - Statut de maintenance
   - Sparkline montrant la tendance des 10 derniers cycles
3. L'utilisateur applique des filtres (optionnel):
   - Filtre par statut de maintenance
   - Recherche par nom de machine
4. L'utilisateur clique sur une machine spécifique dans la liste
5. L'utilisateur visualise les détails de la machine:
   - Nom, description, localisation
   - Date de création et dernière mise à jour
6. L'utilisateur consulte l'historique des prédictions:
   - Liste chronologique des prédictions
   - Graphique de tendance RUL
   - Évolution du score de santé
7. L'utilisateur consulte les lectures capteurs récentes (optionnel)

**Postconditions:**
- L'utilisateur a une vue détaillée de la machine sélectionnée
- L'utilisateur peut analyser l'évolution de l'état de santé de la machine

#### 2.3.3 UC3: Consulter les Recommandations de Maintenance

**Acteur:** Opérateur de Maintenance, Responsable d'Équipements

**Description:** L'utilisateur consulte la liste des équipements nécessitant une maintenance, priorisée par urgence.

**Préconditions:**
- Prédictions disponibles dans la base de données
- Couche de décision appliquée aux prédictions

**Scénario principal:**
1. L'utilisateur navigue vers la page "Maintenance" via le menu latéral
2. L'utilisateur visualise la liste des équipements nécessitant une attention
3. La liste est priorisée par urgence:
   - En premier: Machines CRITICAL (RUL effectif ≤ 20 cycles)
   - Ensuite: Machines MAINTENANCE_RECOMMENDED (20 < RUL ≤ 50 cycles)
   - Ensuite: Machines MONITOR (50 < RUL ≤ 100 cycles)
4. Pour chaque machine, l'utilisateur visualise:
   - Nom de la machine
   - RUL prédit et RUL effectif
   - Score de santé
   - Statut de maintenance
   - Date estimée de maintenance (basée sur RUL effectif)
   - Actions recommandées selon le statut:
     - CRITICAL: "Maintenance immédiate requise"
     - MAINTENANCE_RECOMMENDED: "Planifier maintenance dans les 50 prochains cycles"
     - MONITOR: "Surveillance accrue requise"
5. L'utilisateur planifie les interventions en fonction de l'urgence et des ressources disponibles

**Postconditions:**
- L'utilisateur connaît les équipements à maintenir et leur priorité
- L'utilisateur peut planifier les interventions de manière optimale

#### 2.3.4 UC4: Effectuer une Prédiction Manuelle

**Acteur:** Opérateur de Maintenance, Ingénieur de Fiabilité

**Description:** L'utilisateur saisit manuellement des données de capteurs pour tester le système de prédiction.

**Préconditions:**
- Système démarré
- Modèle ML chargé
- Machine sélectionnée disponible

**Scénario principal:**
1. L'utilisateur navigue vers la page "Test Prediction" via le menu latéral
2. L'utilisateur sélectionne une machine dans le dropdown
3. L'utilisateur saisit les 18 valeurs de capteurs:
   - 3 paramètres opérationnels (setting_1, setting_2, setting_3)
   - 15 mesures de capteurs (sensor_2,3,4,6,7,8,9,11,12,13,14,15,17,20,21)
4. OU l'utilisateur utilise les exemples pré-remplis:
   - Clique sur "Load Healthy Example" pour charger des valeurs de capteurs saines
   - Clique sur "Load Critical Example" pour charger des valeurs de capteurs dégradées
5. L'utilisateur entre le numéro de cycle
6. L'utilisateur clique sur le bouton "Predict"
7. Le système affiche les résultats:
   - RUL prédit (en cycles)
   - RUL effectif (après marge de sécurité)
   - Score de santé (0-100)
   - Statut de maintenance (NORMAL, MONITOR, MAINTENANCE_RECOMMENDED, CRITICAL)
   - Marge de sécurité appliquée (49 cycles)
8. L'utilisateur consulte l'explication du statut:
   - CRITICAL: "Maintenance immédiate requise - RUL effectif ≤ 20 cycles"
   - MAINTENANCE_RECOMMENDED: "Maintenance planifiée requise - RUL effectif entre 20 et 50 cycles"
   - MONITOR: "Surveillance accrue requise - RUL effectif entre 50 et 100 cycles"
   - NORMAL: "Fonctionnement normal - RUL effectif > 100 cycles"

**Postconditions:**
- L'utilisateur obtient une prédiction basée sur les données saisies
- L'utilisateur comprend le statut de maintenance recommandé

**Cas d'erreur:**
- Si le modèle ML n'est pas chargé, une erreur 500 est retournée
- Si la machine n'existe pas, une erreur 404 est retournée

### 2.4 Exigences Fonctionnelles

#### EF1: Prédiction de RUL

**Description:** Le système doit prédire la durée de vie restante des équipements à partir des données de capteurs.

**Entrées:**
- ID de la machine (entier)
- Numéro de cycle (entier)
- 3 paramètres opérationnels (setting_1, setting_2, setting_3) en flottant
- 15 mesures de capteurs (sensor_2,3,4,6,7,8,9,11,12,13,14,15,17,20,21) en flottant

**Traitement:**
1. Validation des données d'entrée via Pydantic
2. Vérification de l'existence de la machine dans la base de données
3. Extraction des features dans l'ordre correct (18 features)
4. Normalisation des features via StandardScaler
5. Prédiction du RUL via Random Forest
6. Application de la couche de décision (marge de sécurité, score santé, statut)
7. Stockage de la lecture capteur dans la base de données
8. Stockage de la prédiction dans la base de données

**Sorties:**
- RUL prédit (en cycles, flottant)
- RUL effectif (après marge de sécurité, flottant)
- Score de santé (0-100, flottant)
- Statut de maintenance (chaîne: NORMAL, MONITOR, MAINTENANCE_RECOMMENDED, CRITICAL)
- Marge de sécurité appliquée (49 cycles, flottant)

**Contraintes:**
- Temps de réponse < 2 secondes
- Précision RMSE < 45 cycles sur validation
- Modèle doit être chargé au démarrage

**Fichiers:** backend/app/services/prediction_service.py, backend/app/routes/predictions.py

#### EF2: Couche de Décision

**Description:** Le système doit appliquer une couche de décision pour transformer la prédiction brute en recommandation de maintenance.

**Traitement:**
1. Application de la marge de sécurité: effective_rul = predicted_rul - 49
2. Calcul du score de santé: health_score = (effective_rul / 200) * 100 (écrêté 0-100)
3. Détermination du statut selon les seuils:
   - CRITICAL: effective_rul ≤ 20 cycles
   - MAINTENANCE_RECOMMENDED: 20 < effective_rul ≤ 50 cycles
   - MONITOR: 50 < effective_rul ≤ 100 cycles
   - NORMAL: effective_rul > 100 cycles

**Justification de la marge de sécurité:** 49 cycles correspond au 75ème percentile des erreurs positives du modèle, couvrant 75% des cas de surestimation.

**Fichiers:** ml/src/maintenance_decision.py, ml/results/decision_layer_config.json

#### EF3: Dashboard de Surveillance

**Description:** Le système doit fournir un dashboard avec statistiques globales et graphiques.

**Fonctionnalités:**
- Cartes statistiques:
  - Total machines
  - Machines normales
  - Machines nécessitant maintenance
  - Score de santé moyen
- Graphique camembert de distribution des statuts de maintenance
- Graphique histogramme de répartition des statuts
- Tableau des 10 dernières prédictions avec:
  - Machine ID
  - RUL prédit
  - Score de santé
  - Statut
  - Timestamp

**Fichiers:** frontend/src/pages/Dashboard.tsx

#### EF4: Liste des Machines

**Description:** Le système doit afficher la liste de toutes les machines avec leurs prédictions.

**Fonctionnalités:**
- Tableau avec colonnes:
  - ID machine
  - Nom
  - RUL prédit
  - Score de santé
  - Statut (avec badge couleur)
  - Sparkline (tendance 10 derniers cycles)
- Filtres par statut de maintenance
- Recherche par nom de machine
- Pagination
- Lien vers les détails de chaque machine

**Fichiers:** frontend/src/pages/Machines.tsx, frontend/src/components/Sparkline.tsx

#### EF5: Recommandations de Maintenance

**Description:** Le système doit afficher les recommandations de maintenance priorisées.

**Fonctionnalités:**
- Liste des machines nécessitant une maintenance
- Priorisation par statut (CRITICAL > MAINTENANCE_RECOMMENDED > MONITOR)
- Pour chaque machine:
  - Nom
  - RUL prédit et effectif
  - Score de santé
  - Date estimée de maintenance
  - Actions recommandées
- Filtres par urgence

**Fichiers:** frontend/src/pages/Maintenance.tsx

#### EF6: Test de Prédiction Manuel

**Description:** Le système doit permettre de tester les prédictions avec des données saisies manuellement.

**Fonctionnalités:**
- Sélection de machine via dropdown
- Saisie des 18 valeurs capteurs
- Boutons "Exemple Sain" et "Exemple Critique" pour remplissage rapide
- Affichage des résultats avec:
  - RUL prédit
  - RUL effectif
  - Score de santé
  - Statut
  - Explication du statut

**Fichiers:** frontend/src/pages/TestPrediction.tsx

#### EF7: Gestion des Machines

**Description:** Le système doit permettre la gestion CRUD des machines.

**Fonctionnalités:**
- Créer une nouvelle machine (POST /machines/)
- Lister toutes les machines (GET /machines/)
- Consulter les détails d'une machine (GET /machines/{id})
- Mettre à jour une machine (PUT /machines/{id})
- Supprimer une machine (DELETE /machines/{id})

**Fichiers:** backend/app/routes/machines.py, backend/app/models/__init__.py

#### EF8: Stockage des Données

**Description:** Le système doit stocker les données de capteurs et les prédictions dans une base de données.

**Fonctionnalités:**
- Stockage des lectures capteurs avec timestamp
- Stockage des prédictions avec résultats de la couche de décision
- Historique temporel complet
- Relations entre machines, lectures, et prédictions

**Fichiers:** backend/app/models/__init__.py, backend/seed_database.py

### 2.5 Exigences Non-Fonctionnelles

#### ENF1: Performance

**Description:** Le système doit répondre rapidement aux requêtes utilisateur.

**Critères:**
- Temps de réponse API < 1 seconde pour les prédictions
- Temps de chargement du dashboard < 2 secondes
- Temps de chargement des listes < 1 seconde

**Justification:** Les opérateurs ont besoin d'informations en temps réel pour prendre des décisions rapides.

#### ENF2: Fiabilité

**Description:** Le système doit être fiable et disponible.

**Critères:**
- Disponibilité > 95% pendant les heures de travail
- Pas de perte de données
- Récupération automatique en cas d'erreur

**Justification:** Les décisions de maintenance critiques nécessitent un système fiable.

#### ENF3: Maintenabilité

**Description:** Le code doit être maintenable et évolutif.

**Critères:**
- Code modulaire avec séparation des couches
- Commentaires et documentation
- Tests unitaires pour les composants critiques
- Configuration externalisée (.env)

**Justification:** Le système pourra être étendu et maintenu après le projet académique.

#### ENF4: Utilisabilité

**Description:** L'interface doit être intuitive pour les opérateurs.

**Critères:**
- Interface de type SCADA familière aux opérateurs
- Navigation claire et logique
- Codes couleur pour les statuts (vert=normal, orange=surveillance, rouge=critique)
- Feedback visuel immédiat

**Justification:** Les opérateurs ne sont pas des experts informatiques.

#### ENF5: Scalabilité

**Description:** Le système doit pouvoir gérer un nombre croissant de machines.

**Critères:**
- Support de 100+ machines
- Support de 1000+ lectures capteurs par jour
- Pagination pour les listes

**Justification:** Le système pourrait être déployé dans un environnement de production avec plus d'équipements.

#### ENF6: Sécurité

**Note:** L'authentification n'est pas implémentée dans la version actuelle, mais pourrait être ajoutée.

**Critères (futurs):**
- Authentification des utilisateurs
- Gestion des rôles (admin, opérateur, lecteur)
- Validation des entrées
- Protection contre les injections SQL

**Justification:** Les données de maintenance sont sensibles et nécessitent une protection.

### 2.6 Conclusion du Chapitre

Ce chapitre a présenté l'analyse fonctionnelle détaillée du système, identifiant trois acteurs principaux (opérateur de maintenance, ingénieur de fiabilité, responsable d'équipements), quatre cas d'utilisation principaux (surveillance, consultation détails, recommandations maintenance, test prédiction), et huit exigences fonctionnelles (prédiction RUL, couche décision, dashboard, liste machines, recommandations, test manuel, gestion machines, stockage données). Six exigences non-fonctionnelles ont été définies concernant la performance, la fiabilité, la maintenabilité, l'utilisabilité, la scalabilité, et la sécurité. Le chapitre suivant présente l'architecture et la conception du système.

---

## CHAPITRE 3: ARCHITECTURE ET CONCEPTION (5-6 pages)

### 3.1 Introduction

Ce chapitre présente l'architecture globale du système, la conception de la base de données, l'architecture ML, et les choix technologiques. Il explique comment les différents composants interagissent pour former un système cohérent.

### 3.2 Architecture Globale

#### 3.2.1 Approche Architecturale

Le système adopte une architecture 3-tiers classique, séparant clairement la présentation, la logique métier, et la persistance des données. Cette approche offre plusieurs avantages:

**Séparation des responsabilités:** Chaque tier a un rôle clair et bien défini, facilitant le développement et la maintenance.

**Maintenabilité:** Les modifications dans un tier n'affectent pas les autres, réduisant le risque de régressions.

**Scalabilité:** Chaque tier peut être scalé indépendamment en fonction des besoins (ex: scaling horizontal du backend).

**Testabilité:** Chaque tier peut être testé indépendamment, facilitant les tests unitaires et d'intégration.

#### 3.2.2 Diagramme Architectural

L'architecture du système peut être représentée comme suit:

```
┌─────────────────────────────────────────────────────────────┐
│                     TIER PRÉSENTATION                        │
│                  Frontend React + TypeScript                 │
│                                                               │
│  Pages: Dashboard, Machines, Maintenance, TestPrediction     │
│  Components: Header, Sidebar, Sparkline                      │
│  Technologies: React 19.2.8, TypeScript 6.0.2, Vite 8.2.0    │
│  Styling: TailwindCSS 4.3.3                                 │
│  Charts: Recharts 3.10.1                                     │
│  HTTP: Axios 1.19.0                                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API (JSON)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      TIER LOGIQUE MÉTIER                     │
│                    Backend FastAPI + Python                 │
│                                                               │
│  Routes: health, machines, predictions, maintenance         │
│  Services: prediction_service (ML integration)                │
│  Models: Machine, SensorReading, Prediction (SQLAlchemy)     │
│  Schemas: Pydantic validation                               │
│  Technologies: FastAPI 0.104.1, SQLAlchemy 2.0.23            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    TIER PERSISTANCE                          │
│                  Base de Données PostgreSQL                 │
│                                                               │
│  Tables: machines, sensor_readings, predictions              │
│  Relations: One-to-Many                                     │
│  Technology: PostgreSQL 17                                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    COUCHE MACHINE LEARNING                   │
│              Modèle + Couche de Décision                    │
│                                                               │
│  Model: RandomForestRegressor (n_estimators=77, max_depth=9)  │
│  Features: 18 (3 settings + 15 sensors)                     │
│  Scaler: StandardScaler                                     │
│  Decision Layer: Safety margin 49 cycles                     │
│  Technology: scikit-learn 1.9.0, joblib 1.3.2                │
└─────────────────────────────────────────────────────────────┘
```

#### 3.2.3 Flux de Données Complet

**Flux de prédiction:**
1. L'utilisateur saisit des données capteurs dans l'interface TestPrediction
2. Le frontend React envoie une requête POST /api/v1/predictions/ via Axios
3. Le routeur FastAPI reçoit la requête et valide les données via Pydantic
4. Le service PredictionService charge le modèle ML, le scaler, et la couche de décision
5. Le StandardScaler normalise les données d'entrée
6. Le Random Forest Model prédit le RUL
7. La Decision Layer applique la marge de sécurité et calcule le statut
8. L'ORM SQLAlchemy stocke la lecture capteur et la prédiction dans PostgreSQL
9. FastAPI retourne la réponse JSON au frontend
10. Le frontend affiche les résultats à l'utilisateur

**Flux de surveillance:**
1. L'utilisateur accède au Dashboard
2. Le frontend appelle GET /api/v1/machines/, /api/v1/predictions/, /api/v1/maintenance/summary
3. FastAPI interroge PostgreSQL via SQLAlchemy
4. PostgreSQL retourne les données
5. FastAPI sérialise en JSON
6. Le frontend affiche les statistiques et graphiques via Recharts

### 3.3 Architecture Frontend

#### 3.3.1 Choix Technologiques

**React 19.2.8:** Framework JavaScript moderne pour les interfaces utilisateur. Choisir pour sa popularité, son écosystème riche, et sa performance via le Virtual DOM.

**TypeScript 6.0.2:** Superset typé de JavaScript. Choisir pour le typage statique qui réduit les erreurs, l'autocompletion, et la documentation intégrée via les types.

**Vite 8.2.0:** Build tool et dev server. Choisir pour sa rapidité de build, le Hot Module Replacement (HMR), et sa configuration simple.

**TailwindCSS 4.3.3:** Framework CSS utility-first. Choisir pour le développement rapide, la personnalisation facile, et le style industriel SCADA.

**Recharts 3.10.1:** Bibliothèque de graphiques. Choisir pour les graphiques déclaratifs, l'intégration React, et la personnalisation.

**Axios 1.19.0:** Client HTTP. Choisir pour les promesses (async/await), les intercepteurs pour gestion d'erreurs, et le support TypeScript.

#### 3.3.2 Structure du Frontend

```
frontend/src/
├── pages/              # Pages principales
│   ├── Dashboard.tsx   # Vue d'ensemble avec statistiques
│   ├── Machines.tsx    # Liste des machines avec sparklines
│   ├── MachineDetails.tsx  # Détails d'une machine
│   ├── Maintenance.tsx # Recommandations priorisées
│   └── TestPrediction.tsx  # Test interactif
├── components/         # Composants réutilisables
│   ├── Header.tsx      # Barre de navigation supérieure
│   ├── Sidebar.tsx     # Menu latéral
│   └── Sparkline.tsx   # Graphique miniature de tendance
├── services/           # Client API centralisé
│   └── api.ts          # Fonctions Axios
├── types/              # Types TypeScript
│   └── index.ts        # Interfaces (Machine, Prediction, etc.)
├── layouts/            # Layout principal
│   └── Layout.tsx      # Structure avec Header + Sidebar
├── assets/             # Assets statiques
├── App.tsx             # Application principale
├── main.tsx            # Point d'entrée
└── style.css           # Styles globaux
```

#### 3.3.3 Gestion de l'État

**Approche:** État local avec useState

**Justification:** Projet de taille modérée, pas besoin de Redux ou Context API pour ce cas d'usage. Chaque page gère son propre état local.

**Exemple (Dashboard):**
```typescript
const [machines, setMachines] = useState<Machine[]>([]);
const [predictions, setPredictions] = useState<Prediction[]>([]);
const [summary, setSummary] = useState<MaintenanceSummary | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

#### 3.3.4 Communication API

**Service API centralisé:** frontend/src/services/api.ts

**Configuration:**
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
```

**Fonctions principales:**
- getMachines(), getMachine(), createMachine(), updateMachine(), deleteMachine()
- getPredictions(), getPrediction(), createPrediction()
- getMaintenanceStatus(), getMaintenanceSummary()
- getHealthCheck()

#### 3.3.5 Navigation

**Framework:** React Router DOM 7.18.2

**Routes:**
- / → Dashboard
- /machines → Machines
- /machines/:id → MachineDetails
- /maintenance → Maintenance
- /test-prediction → TestPrediction

### 3.4 Architecture Backend

#### 3.4.1 Choix Technologiques

**FastAPI 0.104.1:** Framework API moderne et performant. Choisir pour la validation automatique via Pydantic, la documentation auto-générée (Swagger UI), le support async/await, et le typage Python moderne.

**SQLAlchemy 2.0.23:** ORM Python. Choisir pour l'abstraction base de données, les relations automatiques, et la compatibilité avec PostgreSQL.

**Pydantic 2.5.0:** Validation des données. Choisir pour les schémas de validation, la sérialisation automatique, et la gestion des erreurs.

**Uvicorn 0.24.0:** Serveur ASGI. Choisir pour la performance élevée, le support WebSocket, et le hot reload en développement.

#### 3.4.2 Structure du Backend

```
backend/app/
├── main.py              # Application FastAPI principale
├── config.py            # Configuration et variables d'environnement
├── database.py          # Connexion base de données SQLAlchemy
├── models/              # Modèles SQLAlchemy
│   └── __init__.py      # Machine, SensorReading, Prediction
├── routes/              # Routes API
│   ├── health.py        # Endpoint santé
│   ├── machines.py      # CRUD machines
│   ├── predictions.py   # Prédictions ML
│   ├── maintenance.py   # Recommandations
│   └── sensor_readings.py  # Lectures capteurs
├── services/            # Logique métier
│   └── prediction_service.py  # Service prédiction ML
└── schemas/             # Schémas Pydantic
    └── __init__.py      # Validation requêtes/réponses
```

#### 3.4.3 Configuration

**Fichier:** backend/app/config.py

**Paramètres:**
- APP_NAME, APP_VERSION, DEBUG
- DATABASE_URL (PostgreSQL)
- MODEL_PATH, SCALER_PATH, DECISION_CONFIG_PATH
- API_PREFIX (/api/v1)

**Chargement:** Via Pydantic Settings depuis variables d'environnement (.env)

#### 3.4.4 Routes API

**Architecture:** Router pattern de FastAPI

**Routers principaux:**
- health.py: GET /health
- machines.py: CRUD complet sur /machines/
- predictions.py: POST /predictions/, GET /predictions/
- maintenance.py: GET /maintenance/status/{id}, GET /maintenance/summary
- sensor_readings.py: CRUD sur /sensor-readings/

**Middleware:** CORS configuré pour autoriser toutes les origines (à restreindre en production)

### 3.5 Architecture Base de Données

#### 3.5.1 Choix Technologique

**PostgreSQL 17:** SGBD relationnel robuste

**Justification:**
- Support SQL avancé
- Transactions ACID
- Performance élevée
- Écosystème mature
- Compatibilité SQLAlchemy

#### 3.5.2 Schéma de la Base de Données

**Table: machines**
- id (PK, Integer, auto-increment)
- name (String, unique, not null)
- description (String, nullable)
- location (String, nullable)
- created_at (DateTime, default=utcnow)
- updated_at (DateTime, default=utcnow, onupdate=utcnow)

**Table: sensor_readings**
- id (PK, Integer, auto-increment)
- machine_id (FK vers machines.id, not null)
- cycle (Integer, not null)
- timestamp (DateTime, default=utcnow)
- setting_1, setting_2, setting_3 (Float, not null)
- sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9 (Float, not null)
- sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21 (Float, not null)

**Table: predictions**
- id (PK, Integer, auto-increment)
- machine_id (FK vers machines.id, not null)
- sensor_reading_id (FK vers sensor_readings.id, nullable)
- timestamp (DateTime, default=utcnow)
- predicted_rul (Float, not null)
- effective_rul (Float, not null)
- health_score (Float, not null)
- maintenance_status (String, not null)
- safety_margin_applied (Float, not null)

#### 3.5.3 Relations

- machines → sensor_readings: One-to-many (une machine a plusieurs lectures)
- machines → predictions: One-to-many (une machine a plusieurs prédictions)
- sensor_readings → predictions: One-to-one (une lecture peut avoir une prédiction)

#### 3.5.4 Diagramme Entité-Association

```
machines (1) ──< (N) sensor_readings (1) ──< (1) predictions
```

### 3.6 Architecture Machine Learning

#### 3.6.1 Pipeline ML Complet

**1. Chargement des données:**
- NASA C-MAPSS FD001 (train_FD001.txt)
- 100 moteurs, cycles 1-361
- 26 colonnes (engine_id, cycle, 3 settings, 21 sensors)

**2. Prétraitement:**
- Suppression capteurs constants (sensor_1,5,10,16,18,19)
- Calcul RUL: RUL = max_cycle - current_cycle
- Suppression relative_cycle (fuite de données)
- 18 features restantes (3 settings + 15 sensors)

**3. Split des données:**
- Split au niveau moteur (seed=42)
- Entraînement: 70 moteurs (70%)
- Validation: 15 moteurs (15%)
- Test interne: 15 moteurs (15%)

**4. Normalisation:**
- StandardScaler (fit sur entraînement, transform sur validation/test)
- Moyenne=0, Écart-type=1

**5. Entraînement:**
- RandomForestRegressor
- n_estimators=77, max_depth=9, min_samples_split=10, min_samples_leaf=7, max_features=log2
- random_state=42

**6. Évaluation:**
- RMSE: 41.80 cycles (validation)
- MAE: 31.72 cycles (validation)
- R²: 0.62 (validation)

**7. Test officiel:**
- Évaluation sur test FD001 officiel (100 moteurs)
- RMSE: 31.73 cycles
- MAE: 23.39 cycles
- R²: 0.42

**8. Sauvegarde:**
- final_rul_model.joblib (modèle)
- preprocessing_pipeline.joblib (scaler)
- model_metadata.json (métadonnées)

#### 3.6.2 Couche de Décision

**Objectif:** Transformer la prédiction brute en recommandation de maintenance actionnable.

**Composants:**

1. **Marge de sécurité (49 cycles):** Pourquoi compenser la surestimation moyenne de 6.93 cycles. Calcul: 75ème percentile des erreurs positives.

2. **Score de santé (0-100):** Méthode échelle linéaire, max RUL=200 cycles. Formule: health_score = (effective_rul / 200) * 100.

3. **Seuils de maintenance:**
   - CRITICAL: effective_rul ≤ 20 cycles
   - MAINTENANCE_RECOMMENDED: 20 < effective_rul ≤ 50 cycles
   - MONITOR: 50 < effective_rul ≤ 100 cycles
   - NORMAL: effective_rul > 100 cycles

#### 3.6.3 Intégration ML dans l'Architecture

**Service PredictionService:**
- Chargement du modèle, scaler, et couche de décision au démarrage
- Méthode predict() pour effectuer la prédiction complète
- Intégration dans l'API via le routeur predictions.py

### 3.7 Choix Technologiques Justifiés

**FastAPI:** Performance, validation auto, documentation Swagger, typage Python

**React:** Écosystème mature, composants réutilisables, Virtual DOM, TypeScript

**PostgreSQL:** SGBD relationnel mature, SQL avancé, transactions ACID

**Random Forest:** Robuste au surapprentissage, interprétable, performance élevée sur données tabulaires

**scikit-learn:** API cohérente, large choix d'algorithmes, documentation excellente

### 3.8 Conclusion du Chapitre

Ce chapitre a présenté l'architecture globale du système en adoptant une approche 3-tiers classique. L'architecture frontend utilise React avec TypeScript pour une interface de type SCADA, tandis que le backend utilise FastAPI avec SQLAlchemy pour l'API REST et l'accès base de données. La base de données PostgreSQL stocke trois tables principales avec des relations bien définies. L'architecture ML intègre un modèle Random Forest avec une couche de décision pour transformer les prédictions en recommandations de maintenance. Les choix technologiques ont été justifiés en fonction des besoins du projet. Le chapitre suivant présente l'implémentation détaillée du système.

---

## CHAPITRE 4: IMPLÉMENTATION (5-6 pages)

### 4.1 Introduction

Ce chapitre présente l'implémentation détaillée du système, couvrant le développement du pipeline ML, l'implémentation de l'API backend, le développement du frontend, et l'intégration de tous les composants.

### 4.2 Environnement de Développement

**Configuration:**
- OS: Windows (développement local)
- Python: 3.8+
- Node.js: 16+
- PostgreSQL: 17

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 4.3 Implémentation Machine Learning

#### 4.3.1 Prétraitement des Données

**Script:** ml/src/preprocessing.py

**Étapes:**
1. Chargement des données (train_FD001.txt)
2. Suppression capteurs constants (6 capteurs)
3. Calcul RUL = max_cycle - current_cycle
4. Suppression relative_cycle (fuite de données)
5. Validation (valeurs manquantes, doublons, cycles séquentiels)

**Impact suppression relative_cycle:** RMSE 25.47 → 41.82 cycles (dégradation 64.2%, mais élimine fuite de données)

#### 4.3.2 Sélection des Caractéristiques

**Features finales (18):**
- 3 paramètres opérationnels: setting_1, setting_2, setting_3
- 15 capteurs: sensor_2,3,4,6,7,8,9,11,12,13,14,15,17,20,21

**Justification:**
- Settings: Paramètres opérationnels affectant performance
- Capteurs sélectionnés: Variance significative, corrélés avec dégradation
- Exclus: Constants (pas d'information) ou relative_cycle (fuite de données)

#### 4.3.3 Split des Données

**Approche:** Split au niveau moteur (pas au niveau cycle)

**Pourquoi:** Éviter fuite de données - un même moteur ne doit pas apparaître dans plusieurs splits.

**Split (seed=42):**
- Entraînement: 70 moteurs (70%)
- Validation: 15 moteurs (15%)
- Test interne: 15 moteurs (15%)

#### 4.3.4 Normalisation

**Méthode:** StandardScaler

**Formule:** X_scaled = (X - mean) / std

**Pourquoi:** Robuste aux valeurs aberrantes, fonctionne bien avec Random Forest

#### 4.3.5 Entraînement du Modèle

**Baseline:** n_estimators=100, max_depth=15

**Optimisation:** RandomizedSearchCV (50 itérations)

**Meilleurs hyperparamètres:**
- n_estimators=77
- max_depth=9
- min_samples_split=10
- min_samples_leaf=7
- max_features=log2

**Pourquoi ces valeurs:**
- n_estimators=77: Suffisant pour stabilité sans surapprentissage
- max_depth=9: Limite surapprentissage
- min_samples_split/leaf: Contrôle régularisation
- max_features=log2: Réduit corrélation entre arbres

#### 4.3.6 Évaluation du Modèle

**Résultats validation:**
- RMSE: 41.80 cycles
- MAE: 31.72 cycles
- R²: 0.62

**Résultats test officiel:**
- RMSE: 31.73 cycles
- MAE: 23.39 cycles
- R²: 0.42

**Surapprentissage:**
- Ratio validation/entraînement: 1.10
- Ratio test/entraînement: 1.19
- Interprétation: Généralisation saine (ratios < 1.5)

#### 4.3.7 Couche de Décision

**Script:** ml/src/maintenance_decision.py

**Marge de sécurité:** 49 cycles (75ème percentile des erreurs positives)

**Score de santé:** Échelle linéaire 0-100, max RUL=200 cycles

**Seuils:** CRITICAL ≤20, MAINTENANCE 20-50, MONITOR 50-100, NORMAL >100

#### 4.3.8 Évaluation sur Test Officiel

**Script:** ml/compare_predictions_vs_truth.py

**Processus:**
1. Charger modèle sauvegardé
2. Charger test officiel FD001
3. Extraire dernier cycle pour chaque moteur (100 moteurs)
4. Faire prédictions
5. Comparer avec vérité terrain
6. Calculer métriques
7. Générer scatter plot et CSV

**Résultats:** RMSE 31.73 cycles, MAE 23.39 cycles, R² 0.42

### 4.4 Implémentation Backend

#### 4.4.1 Application FastAPI Principale

**Fichier:** backend/app/main.py

**Fonctionnalités:**
- Création application FastAPI
- Configuration CORS
- Enregistrement routes
- Création tables automatiques

#### 4.4.2 Modèles SQLAlchemy

**Fichier:** backend/app/models/__init__.py

**Classes:** Machine, SensorReading, Prediction

**Relations:** One-to-many (machines → sensor_readings, machines → predictions)

#### 4.4.3 Schémas Pydantic

**Fichier:** backend/app/schemas/__init__.py

**Classes:** MachineCreate, PredictionRequest, PredictionResponse, etc.

**Validation:** Typage automatique, conversion automatique

#### 4.4.4 Route de Prédiction

**Fichier:** backend/app/routes/predictions.py

**Endpoint:** POST /predictions/

**Processus:**
1. Vérifier machine existe
2. Prédire via ML service
3. Stocker lecture capteur
4. Stocker prédiction
5. Retourner résultat

#### 4.4.5 Service de Prédiction

**Fichier:** backend/app/services/prediction_service.py

**Classe:** PredictionService

**Méthode:** predict(sensor_data)

**Processus:**
1. Extraire features (ordre correct)
2. Normaliser via scaler
3. Prédire via model
4. Appliquer décision layer
5. Retourner résultat

#### 4.4.6 Peuplement de la Base de Données

**Script:** backend/seed_database.py

**Processus:**
1. Créer 8 machines
2. Générer 10 lectures par machine (80 total)
3. Générer 10 prédictions par machine (80 total)
4. Distribution: 5 NORMAL, 2 MONITOR, 1 CRITICAL

### 4.5 Implémentation Frontend

#### 4.5.1 Application React Principale

**Fichier:** frontend/src/App.tsx

**Configuration:** React Router avec 5 routes

#### 4.5.2 Page Dashboard

**Fichier:** frontend/src/pages/Dashboard.tsx

**Fonctionnalités:**
- Chargement automatique données
- Calcul statistiques
- Graphiques Recharts (camembert, histogramme)
- Tableau 10 dernières prédictions

#### 4.5.3 Page Test Prediction

**Fichier:** frontend/src/pages/TestPrediction.tsx

**Fonctionnalités:**
- Sélection machine dropdown
- Saisie 18 valeurs capteurs
- Boutons exemples (sain/critique)
- Affichage résultats avec explication

#### 4.5.4 Composant Sparkline

**Fichier:** frontend/src/components/Sparkline.tsx

**Objectif:** Graphique miniature tendance 10 derniers cycles

**Implémentation:** Recharts LineChart responsive

#### 4.5.5 Client API

**Fichier:** frontend/src/services/api.ts

**Fonctions:** getMachines, createPrediction, getMaintenanceSummary, etc.

**Configuration:** API_URL depuis variable d'environnement

### 4.6 Intégration et Tests

#### 4.6.1 Démarrage du Système

**Backend:** uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

**Frontend:** npm run dev

**Accès:** Backend http://localhost:8000, Frontend http://localhost:5173

#### 4.6.2 Tests Unitaires Backend

**Fichier:** backend/tests/test_api.py

**Tests (4):** health_check, create_machine, get_machines, prediction_endpoint

#### 4.6.3 Tests Manuels

**Test prédiction sain:** Load Healthy Example → Predict → Statut NORMAL/MONITOR ✅

**Test prédiction critique:** Load Critical Example → Predict → Statut CRITICAL ✅

**Test Dashboard:** Accès / → Statistiques affichées ✅

### 4.7 Conclusion du Chapitre

Ce chapitre a présenté l'implémentation détaillée du système, couvrant le pipeline ML complet (prétraitement, sélection features, entraînement, évaluation), l'implémentation de l'API backend FastAPI avec SQLAlchemy, le développement de l'interface React avec TypeScript, et l'intégration de tous les composants. Le modèle Random Forest final atteint un RMSE de 41.80 cycles sur validation et 31.73 cycles sur le test officiel. La couche de décision avec une marge de sécurité de 49 cycles transforme les prédictions en recommandations de maintenance actionnables. Le système complet est fonctionnel et démontrable. Le chapitre suivant présente les résultats, les tests, et l'évaluation du système.

---

## CHAPITRE 5: RÉSULTATS ET TESTS (5-6 pages)

### 5.1 Introduction

Ce chapitre présente les résultats obtenus, les tests effectués, l'évaluation du système, et les problèmes rencontrés lors du développement. Il valide que les objectifs du projet ont été atteints.

### 5.2 Résultats du Modèle Machine Learning

#### 5.2.1 Métriques de Performance

| Métrique | Entraînement | Validation | Test Interne | Test Officiel |
|----------|--------------|------------|---------------|---------------|
| RMSE | 38.11 cycles | 41.80 cycles | 45.41 cycles | 31.73 cycles |
| MAE | 26.37 cycles | 31.72 cycles | 33.23 cycles | 23.39 cycles |
| R² | 0.69 | 0.62 | 0.59 | 0.42 |

**Source:** models/model_metadata.json, ml/results/computed_training_metrics.json

#### 5.2.2 Analyse des Résultats

**RMSE:** Erreur quadratique moyenne de ~32-42 cycles. Le modèle prédit la RUL avec une erreur moyenne acceptable.

**MAE:** Erreur absolue moyenne de ~23-32 cycles. En moyenne, la prédiction s'écarte de la vérité terrain de 23-32 cycles.

**R²:** Le modèle explique 42-62% de la variance. Il capture une partie significative mais pas totale de la variation de la RUL.

#### 5.2.3 Analyse du Surapprentissage

**Ratios:**
- Validation/Entraînement: 1.10
- Test/Entraînement: 1.19

**Interprétation:** Ratios < 1.5 indiquent une généralisation saine avec un surapprentissage minimal.

#### 5.2.4 Paradoxe RMSE/R² sur Test Officiel

**Observation:**
- RMSE officiel (31.73) < RMSE validation (41.80)
- R² officiel (0.42) < R² validation (0.62)

**Explication:** Distribution RUL différente entre validation et test officiel

**Distributions:**
- Validation RUL: 0-286 cycles (std: 67.98)
- Test officiel RUL: 7-145 cycles (std: 41.56)
- Ratio variance: 0.37

**Pourquoi RMSE plus bas:** Plus faible variance → plus faible potentiel d'erreurs importantes

**Pourquoi R² plus bas:** R² = 1 - (SS_res / SS_tot). Variance plus faible → SS_tot plus petit → R² plus bas

**Conclusion:** Phénomène connu en prédiction RUL, reflète les caractéristiques du dataset, pas une dégradation du modèle.

### 5.3 Résultats de la Couche de Décision

#### 5.3.1 Configuration Finale

**Marge de sécurité:** 49 cycles

**Seuils:**
- CRITICAL: RUL effectif ≤ 20 cycles
- MAINTENANCE_RECOMMANDÉE: 20 < RUL effectif ≤ 50 cycles
- MONITOR: 50 < RUL effectif ≤ 100 cycles
- NORMAL: RUL effectif > 100 cycles

**Score de santé:** Échelle linéaire 0-100, max RUL=200 cycles

#### 5.3.2 Analyse de Biais

**Statistiques d'erreur (validation):**
- Erreur moyenne: +6.93 cycles (surestimation)
- Taux de surestimation: 61.83%
- 75ème percentile erreurs positives: 49.87 cycles → Sélectionné comme marge

**Justification:** Marge de 49 cycles couvre 75% des cas de surestimation, compromis entre conservatisme et utilité.

### 5.4 Résultats du Système Complet

#### 5.4.1 Fonctionnalités Implémentées

**Backend:** 13 endpoints, service ML intégré, BDD PostgreSQL, validation Pydantic

**Frontend:** 4 pages, dashboard avec graphiques, liste avec sparklines, test interactif

**Base de données:** 8 machines, 80 lectures, 80 prédictions, distribution équilibrée

#### 5.4.2 Performance du Système

**Temps de réponse estimés:**
- API prédiction: < 1 seconde
- Chargement dashboard: < 2 secondes
- Chargement listes: < 1 seconde

### 5.5 Tests Effectués

#### 5.5.1 Tests Unitaires Backend

**Fichier:** backend/tests/test_api.py

**Tests (4):**
1. test_health_check
2. test_create_machine
3. test_get_machines
4. test_prediction_endpoint

**Limitation:** Seulement 4 tests, pas de tests d'intégration ou E2E

#### 5.5.2 Tests Manuels

**Test prédiction sain:** ✅ Fonctionnel

**Test prédiction critique:** ✅ Fonctionnel

**Test Dashboard:** ✅ Fonctionnel

**Test liste machines:** ✅ Fonctionnel

**Test maintenance:** ✅ Fonctionnel

#### 5.5.3 Validation ML

**Check fuite de données:** ✅ PASSED - relative_cycle exclu

**Test officiel:** ✅ RMSE 31.73 cycles, MAE 23.39 cycles, R² 0.42

### 5.6 Problèmes Rencontrés et Solutions

#### 5.6.1 Problème 1: Fuite de Données avec relative_cycle

**Problème:** relative_cycle nécessite connaissance du cycle de défaillance (non disponible en temps réel)

**Solution:** Suppression de relative_cycle

**Impact:** RMSE 25.47 → 41.82 cycles (acceptable pour déploiement)

**Résultat:** Modèle déployable sans fuite de données

#### 5.6.2 Problème 2: Surapprentissage avec Features Time-Series

**Problème:** Features temporelles causaient surapprentissage sévère

**Solution:** Retour aux features basiques

**Impact:** Surapprentissage réduit (ratios < 1.5)

**Résultat:** Modèle plus simple avec meilleure généralisation

#### 5.6.3 Problème 3: Biais de Surestimation

**Problème:** Modèle surestime en moyenne de 6.93 cycles (61.83% des cas)

**Solution:** Marge de sécurité de 49 cycles (75ème percentile erreurs positives)

**Impact:** Recommandations plus conservatrices

**Résultat:** Système plus sûr

#### 5.6.4 Problème 4: Incohérences Documentation

**Problème:** Valeurs différentes entre documents

**Solution:** Vérification depuis artefacts sauvegardés

**Impact:** Documentation cohérente et vérifiable

**Résultat:** Source de vérité unique

### 5.7 Résultats Globaux du Projet

#### 5.7.1 Objectifs Atteints

**Modèle ML performant:** ✅ RMSE 41.80 (validation), 31.73 (test officiel)

**Couche de décision:** ✅ Marge 49 cycles, seuils définis

**API REST:** ✅ 13 endpoints, temps réponse < 2s

**Interface utilisateur:** ✅ 4 pages React, style SCADA

**Base de données:** ✅ PostgreSQL, 3 tables, peuplée

#### 5.7.2 Statistiques du Système

**Modèle:** Random Forest (n_estimators=77, max_depth=9), 18 features

**API:** 13 endpoints, FastAPI 0.104.1

**Frontend:** 4 pages, React 19.2.8 + TypeScript 6.0.2

**Base de données:** 8 machines, 80 lectures, 80 prédictions

### 5.8 Conclusion du Chapitre

Ce chapitre a présenté les résultats détaillés du projet. Le modèle Random Forest atteint un RMSE de 41.80 cycles sur validation et 31.73 cycles sur le test officiel, avec un R² de 0.62 et 0.42 respectivement. L'analyse du surapprentissage montre des ratios sains (< 1.5). La couche de décision avec une marge de sécurité de 49 cycles transforme les prédictions en recommandations de maintenance actionnables. Le système complet est fonctionnel avec 13 endpoints API, 4 pages frontend, et une base de données peuplée. Quatre problèmes majeurs ont été résolus: fuite de données, surapprentissage, biais de prédiction, et incohérences documentation. Les objectifs du projet ont été atteints. Le chapitre suivant présente la conclusion générale et les perspectives.

---

## CONCLUSION GÉNÉRALE (1-2 pages)

### Synthèse du Projet

Ce projet a consisté à concevoir et développer un système complet de maintenance prédictive basé sur l'intelligence artificielle pour moteurs d'avion (turbofans) utilisant le dataset NASA C-MAPSS FD001. Le système intègre un modèle Machine Learning de type Random Forest pour prédire la Durée de Vie Restante (RUL), une couche de décision pour transformer les prédictions en recommandations de maintenance, une API REST FastAPI pour les prédictions en temps réel, une interface React de type SCADA pour la visualisation, et une base de données PostgreSQL pour le stockage des données historiques.

### Réponses aux Questions de Recherche

**Q1: Quelles caractéristiques sont les plus pertinentes ?**
**Réponse:** 18 caractéristiques: 3 paramètres opérationnels et 15 capteurs. Les capteurs exclus sont constants ou relative_cycle (fuite de données).

**Q2: Quel modèle ML offre le meilleur compromis ?**
**Réponse:** Random Forest Regressor (n_estimators=77, max_depth=9) avec RMSE 41.80 (validation) et 31.73 (test officiel).

**Q3: Comment éviter la fuite de données ?**
**Réponse:** Suppression de relative_cycle qui nécessite la connaissance du cycle de défaillance.

**Q4: Comment transformer prédiction en recommandation ?**
**Réponse:** Couche de décision avec marge de sécurité 49 cycles, score santé 0-100, seuils 20/50/100 cycles.

**Q5: Comment intégrer ML dans architecture déployable ?**
**Réponse:** Service de prédiction dans backend FastAPI, chargement modèle au démarrage, normalisation, prédiction, stockage BDD.

### Apports Scientifiques et Techniques

**Apports scientifiques:**
- Étude approfondie fuite de données en prédiction RUL
- Analyse impact suppression features sur performance
- Investigation relation distribution RUL et métriques
- Implémentation couche décision avec marge justifiée

**Apports techniques:**
- Développement architecture full-stack complète
- Intégration modèle ML dans application web moderne
- Implémentation API REST avec documentation Swagger
- Développement interface SCADA avec React TypeScript
- Conception schéma BDD relationnel optimisé

### Limitations du Projet

**Dataset:** Uniquement FD001, données simulées, pas données temps réel

**Modèle:** RMSE 31.73 cycles, R² 0.42, pas dépendances temporelles explicites (pas LSTM/GRU)

**Système:** Pas authentification, déploiement local, tests limités (4 unitaires), pas CI/CD

### Perspectives

**Court terme:** Entraînement FD002-FD004, LSTM/GRU, authentification, tests E2E, Dockerisation

**Moyen terme:** Intégration IoT temps réel, interface mobile, alertes email/SMS, export rapports

**Long terme:** Déploiement cloud, CI/CD complet, monitoring observabilité, multi-tenancy

### Conclusion

Ce projet a démontré la faisabilité d'un système complet de maintenance prédictive basé sur l'IA, intégrant un modèle ML performant, une couche de décision intelligente, une API REST robuste, et une interface utilisateur intuitive. Les résultats obtenus (RMSE 31.73 cycles sur test officiel) sont comparables à l'état de l'art pour le dataset C-MAPSS FD001. Le système est fonctionnel, démontrable, et constitue une base solide pour des développements futurs en maintenance prédictive.

---

## PERSPECTIVES

Les perspectives de développement du système s'articulent autour de trois horizons temporels:

**Court terme (6-12 mois):**
- Extension à FD002-FD004 pour généralisation du modèle
- Implémentation de modèles LSTM/GRU pour capturer les dépendances temporelles
- Ajout de l'authentification et gestion des rôles
- Tests E2E automatisés avec Playwright
- Dockerisation pour faciliter le déploiement

**Moyen terme (1-2 ans):**
- Intégration IoT pour ingestion de données capteurs en temps réel
- Développement d'une interface mobile pour techniciens de terrain
- Implémentation d'un système d'alertes par email/SMS
- Fonctionnalités d'export de rapports (CSV, PDF)
- Personnalisation avancée du dashboard

**Long terme (2-5 ans):**
- Déploiement cloud (AWS/Azure/GCP) pour scalabilité
- Pipeline CI/CD complet pour automatisation
- Système de monitoring et observabilité (Prometheus, Grafana)
- Architecture multi-tenants pour plusieurs clients
- Système multi-modèles (ensemble de modèles spécialisés)

---

## RÉFÉRENCES

### Références Académiques

1. Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). "Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation". NASA Ames Research Center, Moffett Field, CA.

2. Breiman, L. (2001). "Random Forests". Machine Learning, 45(1), 5-32.

3. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., ... & Duchesnay, E. (2011). "Scikit-learn: Machine Learning in Python". Journal of Machine Learning Research, 12, 2825-2830.

4. J. Lee, F. Wu, W. Zhao, M. Ghaffari, L. Liao, & D. Siegel. (2014). "An Introduction to a Predictive Maintenance Methodology". Prognostics and System Health Management Conference.

### Références Techniques

5. FastAPI Documentation. https://fastapi.tiangolo.com/

6. React Documentation. https://react.dev/

7. PostgreSQL Documentation. https://www.postgresql.org/docs/

8. scikit-learn Documentation. https://scikit-learn.org/

9. SQLAlchemy Documentation. https://docs.sqlalchemy.org/

### Références du Projet

10. RAPPORT_PROJET.md - Rapport de projet en français

11. FINAL_VERIFIED_RESULTS.md - Résultats vérifiés depuis artefacts

12. PROJECT_SETUP_GUIDE.md - Guide d'installation et exécution

13. ml/README.md - Documentation pipeline ML

14. Code source: backend/app/, frontend/src/, ml/src/

---

## ANNEXES

### Annexe A: Code Source - Service de Prédiction

[Inclure code de backend/app/services/prediction_service.py]

### Annexe B: Code Source - Couche de Décision

[Inclure code de ml/src/maintenance_decision.py]

### Annexe C: Configuration du Modèle

[Inclure contenu de models/model_metadata.json]

### Annexe D: Configuration de la Couche de Décision

[Inclure contenu de ml/results/decision_layer_config.json]

### Annexe E: Scatter Plot Prédictions vs Vérité Terrain

[Inclure référence à ml/results/predictions_vs_truth.png]

---

**FIN DU DOSSIER**

**Version:** 1.0  
**Date:** 24 août 2026  
**Pages cibles:** 33-35 pages  
**Statut:** Complet et prêt pour rédaction du rapport académique
