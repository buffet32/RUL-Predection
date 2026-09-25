"""
Script to add adapted "Choix du sujet", "Contextualisation" and "Problématique"
sections to the PFA2026 report, fitted to the predictive maintenance project.
"""
from docx import Document
from docx.shared import Pt
from copy import deepcopy
import os

INPUT_PATH = r'C:\Users\ULTRAPC\Desktop\pfa2026\Rapport_PFA2026.docx'
OUTPUT_PATH = r'C:\Users\ULTRAPC\Desktop\pfa2026\Rapport_PFA2026_updated.docx'

doc = Document(INPUT_PATH)

# ─────────────────────── Helper ───────────────────────
def insert_paragraph_after(paragraph, text, style='Normal'):
    """Insert a new paragraph after the given one."""
    new_p = deepcopy(paragraph._element)
    # clear existing runs
    for child in list(new_p):
        if child.tag.endswith('}r'):
            new_p.remove(child)
    paragraph._element.addnext(new_p)
    from docx.text.paragraph import Paragraph
    new_para = Paragraph(new_p, paragraph._parent)
    new_para.style = doc.styles[style]
    new_para.clear()
    new_para.add_run(text)
    return new_para

# ─────────────────────── Locate insertion points ───────────────────────

# 1) Find "Introduction générale" heading  -> insert "Choix du sujet" content AFTER it
#    (replace the existing intro paragraphs 67-71 with richer versions)
intro_idx = None
chap1_idx = None
problematique_idx = None

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t == "Introduction générale":
        intro_idx = i
    if t == "Chapitre 1 : Contexte général et étude du besoin":
        chap1_idx = i
    if t == "1.3 Problématique":
        problematique_idx = i

print(f"Introduction générale at paragraph {intro_idx}")
print(f"Chapitre 1 at paragraph {chap1_idx}")
print(f"1.3 Problématique at paragraph {problematique_idx}")

# ═══════════════════════════════════════════════════════════════════════
# STRATEGY:
# A) Replace Introduction générale body (paragraphs 67-71) with the adapted
#    "Choix du sujet et intérêt" text
# B) Insert a new section "1.2.4 Contextualisation du projet" before Problématique
# C) Replace the short Problématique (paragraph 85) with the enriched version
# ═══════════════════════════════════════════════════════════════════════

# ── A) Replace Introduction générale body ──
# Paragraphs 67-71 are the 5 body paragraphs of the intro
intro_replacements = [
    (
        "Dans un environnement industriel marqué par une concurrence accrue, "
        "une mondialisation des marchés et une exigence croissante en matière de "
        "disponibilité des équipements, la maintenance ne constitue plus un simple "
        "poste de coûts, mais une condition sine qua non de la pérennité des organisations. "
        "Cette réalité s'impose avec une acuité particulière dans les secteurs à forte "
        "intensité capitalistique — aéronautique, énergie, automobile, production "
        "manufacturière — où l'arrêt imprévu d'un équipement critique peut entraîner "
        "des pertes de production considérables, des coûts de réparation élevés et des "
        "risques pour la sécurité des opérations."
    ),
    (
        "Pour les industriels, cette exigence est doublement prégnante : leur compétitivité "
        "repose précisément sur leur capacité à maximiser le taux de disponibilité de leurs "
        "actifs tout en maîtrisant les coûts d'exploitation. Une entreprise qui pratique "
        "une maintenance exclusivement corrective se trouve dans une position vulnérable "
        "qui fragilise son positionnement sur le marché. C'est dans ce contexte que la "
        "maintenance prédictive émerge comme un levier stratégique fondamental."
    ),
    (
        "Loin d'être un simple prolongement de la maintenance préventive, la maintenance "
        "prédictive incarne un changement de paradigme : elle consiste à exploiter les "
        "données de capteurs en temps réel et les techniques d'intelligence artificielle "
        "pour anticiper les défaillances avant qu'elles ne surviennent. Elle constitue, "
        "selon Jardine et al. (2006), un véritable « outil de gestion des risques » dont "
        "la valeur réelle est conditionnée à la qualité des données, à la robustesse des "
        "modèles prédictifs et à l'appropriation effective par les équipes opérationnelles."
    ),
    (
        "Parallèlement, l'essor de l'intelligence artificielle dans le domaine de la "
        "maintenance industrielle ouvre des perspectives inédites pour dépasser les "
        "limites structurelles des approches traditionnelles. Les technologies "
        "d'apprentissage automatique (Machine Learning), de traitement des séries "
        "temporelles et de modélisation statistique offrent désormais la possibilité de "
        "transformer des flux de données brutes en un système décisionnel intelligent, "
        "capable d'estimer la durée de vie utile restante (RUL) d'un équipement, de "
        "détecter les anomalies et d'anticiper les pannes."
    ),
    (
        "Ce sujet revêt un intérêt particulier pour un futur ingénieur en informatique "
        "et intelligence artificielle, car il se situe précisément à l'intersection de "
        "trois grandes préoccupations contemporaines : la maîtrise des processus "
        "industriels, la gestion des risques opérationnels et l'innovation technologique "
        "par le numérique. Le rapport est organisé en cinq chapitres. Le premier présente "
        "le contexte et la problématique. Le deuxième décrit l'analyse et la conception. "
        "Le troisième est consacré au modèle d'intelligence artificielle. Le quatrième "
        "présente l'implémentation du backend et du frontend. Le cinquième expose les "
        "tests, les résultats et les limites du système."
    ),
]

# Replace paragraphs 67 to 71
for offset, new_text in enumerate(intro_replacements):
    idx = 67 + offset
    doc.paragraphs[idx].clear()
    doc.paragraphs[idx].add_run(new_text)

print("✓ Introduction générale body replaced")


# ── B) Insert "Contextualisation du projet" section ──
# Insert after paragraph 82 (last paragraph of 1.2.3 Maintenance prédictive)
# and before paragraph 83 (empty) / 84 (1.3 Problématique)

anchor = doc.paragraphs[82]  # Last para of section 1.2.3

contextualization_heading = "1.2.4 Contextualisation du projet"
contextualization_paragraphs = [
    (
        "Le présent projet de fin d'année s'inscrit dans le cadre de la formation "
        "en ingénierie informatique et intelligence artificielle. Il vise à concevoir "
        "et développer un système intelligent de maintenance prédictive capable "
        "d'estimer la durée de vie utile restante (Remaining Useful Life – RUL) "
        "des équipements industriels, en exploitant des données de capteurs et des "
        "algorithmes d'apprentissage automatique."
    ),
    (
        "Le projet s'appuie sur le jeu de données NASA C-MAPSS FD001 (Commercial "
        "Modular Aero-Propulsion System Simulation), un référentiel largement reconnu "
        "dans la communauté scientifique. Ce dataset contient les trajectoires de "
        "dégradation de 100 moteurs turbofan simulés, comprenant 3 paramètres "
        "opérationnels et 21 mesures de capteurs par cycle de fonctionnement. "
        "Le choix de ce jeu de données répond à un double objectif : disposer d'un "
        "matériau empirique rigoureux et reproductible, tout en permettant une "
        "comparaison directe avec les résultats de la littérature."
    ),
    (
        "La solution développée comprend un pipeline complet d'apprentissage "
        "automatique (préparation des données, ingénierie des variables, entraînement "
        "et évaluation de plusieurs modèles de régression), un backend REST développé "
        "avec FastAPI, une base de données relationnelle PostgreSQL et une interface "
        "web de supervision développée avec React et TypeScript. Le système retourne "
        "un RUL prédit, un score de santé, un RUL effectif après application d'une "
        "marge de sécurité et un statut de maintenance exploitable par les opérateurs."
    ),
    (
        "Une attention particulière a été accordée à la rigueur méthodologique, "
        "notamment à la détection et l'élimination d'une fuite de données "
        "(data leakage) liée à la variable relative_cycle. Cette variable, calculée "
        "à partir de la durée de vie totale du moteur, constituait une information "
        "future indisponible en conditions réelles d'exploitation. Son identification "
        "et sa suppression ont constitué un apprentissage méthodologique essentiel "
        "pour la validité du système."
    ),
]

# Insert in reverse order so positions remain stable
last = anchor
# First insert heading
h = insert_paragraph_after(last, contextualization_heading, 'Heading 3')
last = h
for para_text in contextualization_paragraphs:
    last = insert_paragraph_after(last, para_text, 'Normal')

print("✓ Contextualisation du projet section inserted")


# ── C) Replace Problématique paragraph ──
# Paragraph 85 = current short problématique text
# We need to find it again because insertion shifted indices
# Let's find it by content match
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("La problématique principale consiste"):
        prob_body_idx = i
        break

enriched_problematique = (
    "L'observation de la littérature et l'analyse du domaine révèlent un "
    "paradoxe : bien que les entreprises industrielles disposent de volumes "
    "croissants de données de capteurs, la transformation de ces données en "
    "décisions de maintenance exploitables reste un défi majeur. Les modèles "
    "prédictifs, lorsqu'ils ne font pas l'objet d'une validation rigoureuse, "
    "peuvent produire des résultats artificiellement performants en raison de "
    "fuites de données, de variables confondantes ou de protocoles d'évaluation "
    "inadaptés aux séries temporelles. Cette situation questionne la fiabilité "
    "réelle des systèmes de maintenance prédictive et leur capacité à fonctionner "
    "dans un environnement opérationnel réel."
)

enriched_problematique_2 = (
    "Dès lors, notre problématique de recherche est la suivante : comment "
    "concevoir un système intelligent de maintenance prédictive qui soit à la "
    "fois performant du point de vue statistique et fiable du point de vue "
    "opérationnel, en intégrant une démarche rigoureuse de détection des biais "
    "méthodologiques et en proposant une interface décisionnelle exploitable "
    "par les utilisateurs finaux ?"
)

doc.paragraphs[prob_body_idx].clear()
doc.paragraphs[prob_body_idx].add_run(enriched_problematique)

# Insert the second paragraph after it
insert_paragraph_after(doc.paragraphs[prob_body_idx], enriched_problematique_2, 'Normal')

print("✓ Problématique section enriched")


# ── Save ──
doc.save(OUTPUT_PATH)
print(f"\n✅ Saved to: {OUTPUT_PATH}")
