"""
Script de génération de présentation PPTX pour le rapport d'avancement de thèse.
Design institutionnel : gris/blanc, ton académique, français.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# Couleurs institutionnelles (gris/blanc)
COLOR_BG = RGBColor(250, 250, 250)  # Blanc cassé
COLOR_TITLE = RGBColor(51, 51, 51)  # Gris foncé
COLOR_TEXT = RGBColor(80, 80, 80)   # Gris moyen
COLOR_ACCENT = RGBColor(30, 80, 160)  # Bleu institutionnel discret
COLOR_LIGHT_GRAY = RGBColor(200, 200, 200)
COLOR_BOX_BG = RGBColor(245, 245, 245)

def set_slide_bg(slide, color=COLOR_BG):
    """Définir le fond de la slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_title(slide, text, left=Inches(0.5), top=Inches(0.3), width=Inches(9), height=Inches(0.8)):
    """Ajouter un titre à la slide."""
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE
    p.alignment = PP_ALIGN.LEFT
    return title_box

def add_subtitle(slide, text, left=Inches(0.5), top=Inches(1.0), width=Inches(9), height=Inches(0.4)):
    """Ajouter un sous-titre."""
    subtitle_box = slide.shapes.add_textbox(left, top, width, height)
    tf = subtitle_box.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.LEFT
    return subtitle_box

def add_content_box(slide, text, left=Inches(0.5), top=Inches(1.5), width=Inches(9), height=Inches(5.5), font_size=14):
    """Ajouter une zone de contenu texte."""
    content_box = slide.shapes.add_textbox(left, top, width, height)
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = COLOR_TEXT
    p.line_spacing = 1.5
    return content_box

def add_bullet_list(slide, items, left=Inches(0.5), top=Inches(1.8), width=Inches(9), height=Inches(5), font_size=14):
    """Ajouter une liste à puces."""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(font_size)
        p.font.color.rgb = COLOR_TEXT
        p.space_after = Pt(8)
    return box

def add_horizontal_line(slide, top=Inches(1.2), left=Inches(0.5), width=Inches(9)):
    """Ajouter une ligne horizontale décorative."""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_LIGHT_GRAY
    line.line.fill.background()
    return line

# Créer la présentation
prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9
prs.slide_height = Inches(7.5)

# Layout vierge pour toutes les slides
blank_layout = prs.slide_layouts[6]  # Blank layout

# ============================================================
# SLIDE 1 : Titre
# ============================================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide1)

# Titre principal
title_box = slide1.shapes.add_textbox(Inches(1), Inches(2), Inches(11.333), Inches(1.5))
tf = title_box.text_frame
p = tf.paragraphs[0]
p.text = "Federated Time Series Foundation Models"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "pour la Maintenance Prédictive Industrielle Multi-Domaine"
p2.font.size = Pt(28)
p2.font.color.rgb = COLOR_ACCENT
p2.alignment = PP_ALIGN.CENTER
p2.space_before = Pt(12)

# Sous-titre
subtitle = slide1.shapes.add_textbox(Inches(1), Inches(4), Inches(11.333), Inches(0.8))
tf = subtitle.text_frame
p = tf.paragraphs[0]
p.text = "Rapport d'avancement de thèse — Première année de doctorat"
p.font.size = Pt(18)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

# Informations doctorant
info = slide1.shapes.add_textbox(Inches(1), Inches(5.2), Inches(11.333), Inches(1.5))
tf = info.text_frame
tf.word_wrap = True

lines = [
    "Yassire AMMOURI",
    "Directeur de thèse : Pr. Younes Karfa Bakali  |  Encadrant : Mme Rajaa SAIDI",
    "Université Mohammed V — LRIT (Laboratoire de Recherche en Informatique et Télécommunications)",
    "31 mars 2026"
]

for i, line in enumerate(lines):
    if i == 0:
        p = tf.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(16)
    else:
        p = tf.add_paragraph()
        p.font.size = Pt(12)
    p.text = line
    p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(4)

print("Slide 1: Titre ✓")

# ============================================================
# SLIDE 2 : Vue d'ensemble — 3 piliers
# ============================================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide2)
add_title(slide2, "Vue d'ensemble : Les trois piliers de la thèse")
add_horizontal_line(slide2, top=Inches(1.1))

# Diagramme triangulaire simple avec 3 boxs
box_width = Inches(3.5)
box_height = Inches(2)
box_y = Inches(2.2)

# Box 1 : FL (gauche)
box1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), box_y, box_width, box_height)
box1.fill.solid()
box1.fill.fore_color.rgb = RGBColor(230, 240, 250)
box1.line.color.rgb = COLOR_ACCENT
box1.line.width = Pt(2)

box1_tf = box1.text_frame
box1_tf.word_wrap = True
p = box1_tf.paragraphs[0]
p.text = "Apprentissage Fédéré"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = box1_tf.add_paragraph()
p2.text = "\nEntraînement collaboratif sans partage de données"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

# Box 2 : TS FMs (droite)
box2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.9), box_y, box_width, box_height)
box2.fill.solid()
box2.fill.fore_color.rgb = RGBColor(230, 250, 240)
box2.line.color.rgb = RGBColor(40, 120, 80)
box2.line.width = Pt(2)

box2_tf = box2.text_frame
box2_tf.word_wrap = True
p = box2_tf.paragraphs[0]
p.text = "Foundation Models"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = box2_tf.add_paragraph()
p2.text = "\nModèles pré-entraînés pour séries temporelles"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

# Box 3 : Maintenance (bas)
box3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.85), Inches(4.5), box_width, box_height)
box3.fill.solid()
box3.fill.fore_color.rgb = RGBColor(250, 240, 230)
box3.line.color.rgb = RGBColor(180, 100, 40)
box3.line.width = Pt(2)

box3_tf = box3.text_frame
box3_tf.word_wrap = True
p = box3_tf.paragraphs[0]
p.text = "Maintenance Prédictive"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = box3_tf.add_paragraph()
p2.text = "\nAnticipation des pannes sur équipements industriels"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

# Centre : Intersection
center_box = slide2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.5), Inches(3.2), Inches(2.3), Inches(1.1))
center_box.fill.solid()
center_box.fill.fore_color.rgb = COLOR_ACCENT
center_box.line.fill.background()

center_tf = center_box.text_frame
p = center_tf.paragraphs[0]
p.text = "Cette thèse"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

# Timeline 3 ans
timeline = slide2.shapes.add_textbox(Inches(8.5), Inches(2), Inches(4.5), Inches(4.5))
tf = timeline.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Timeline 3 ans"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_TITLE

years = [
    "Année 1 : Article Master + SLR + Prototypage",
    "Année 2 : Benchmark + Architecture FedTSFM",
    "Année 3 : Validation industrielle multi-domaine"
]

for year in years:
    p = tf.add_paragraph()
    p.text = "• " + year
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

print("Slide 2: Vue d'ensemble ✓")

# ============================================================
# SLIDE 3 : Formations
# ============================================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide3)
add_title(slide3, "Formations et certifications suivies")
add_horizontal_line(slide3, top=Inches(1.1))

formations = [
    ("WIPO — DL101", "Propriété intellectuelle (brevets, droits d'auteur, marques)"),
    ("Scopus & Web of Science", "Maîtrise des bases bibliographiques et analyse de citations"),
    ("Wiley, Springer, Taylor & Francis", "Formation à la publication scientifique et processus éditoriaux"),
    ("Clarivate", "Indicateurs bibliométriques et facteurs d'impact")
]

y_pos = Inches(1.6)
for org, desc in formations:
    # Box pour chaque formation
    box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(1.1))
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_BOX_BG
    box.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = org
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.25)

# Infobox
infobox = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.8))
infobox.fill.solid()
infobox.fill.fore_color.rgb = RGBColor(240, 248, 255)
infobox.line.color.rgb = COLOR_ACCENT

infotf = infobox.text_frame
p = infotf.paragraphs[0]
p.text = "Apport concret : capacité à conduire une revue de littérature rigoureuse et identifier les journaux pertinents"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 3: Formations ✓")

# ============================================================
# SLIDE 4 : Avancement articles
# ============================================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide4)
add_title(slide4, "Avancement de la rédaction scientifique")
add_horizontal_line(slide4, top=Inches(1.1))

# Article Master
box_master = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(6), Inches(2.8))
box_master.fill.solid()
box_master.fill.fore_color.rgb = RGBColor(255, 245, 240)
box_master.line.color.rgb = RGBColor(200, 100, 50)

m_tf = box_master.text_frame
m_tf.word_wrap = True
p = m_tf.paragraphs[0]
p.text = "P0 — Article issu du Master"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_TITLE

p2 = m_tf.add_paragraph()
p2.text = "\nData-Centric FL for Wind Turbine PdM"
p2.font.size = Pt(13)
p2.font.color.rgb = COLOR_ACCENT
p2.font.italic = True

p3 = m_tf.add_paragraph()
p3.text = "\nStatut : Résultats bloqués (pipeline SCADA à déboguer)"
p3.font.size = Pt(11)
p3.font.color.rgb = RGBColor(180, 60, 60)

p4 = m_tf.add_paragraph()
p4.text = "\nCible : IEEE TII ou Renewable Energy"
p4.font.size = Pt(11)
p4.font.color.rgb = COLOR_TEXT

# SLR PRISMA
box_slr = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(6), Inches(2.8))
box_slr.fill.solid()
box_slr.fill.fore_color.rgb = RGBColor(240, 248, 255)
box_slr.line.color.rgb = COLOR_ACCENT

s_tf = box_slr.text_frame
s_tf.word_wrap = True
p = s_tf.paragraphs[0]
p.text = "P1 — Revue systématique (SLR)"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_TITLE

p2 = s_tf.add_paragraph()
p2.text = "\nFL + TS Foundation Models + Maintenance"
p2.font.size = Pt(13)
p2.font.color.rgb = COLOR_ACCENT
p2.font.italic = True

p3 = s_tf.add_paragraph()
p3.text = "\nEntonnoir PRISMA : 3,000 → 1,700 → 361 → 181 articles"
p3.font.size = Pt(11)
p3.font.color.rgb = COLOR_TEXT

# Entonnoir PRISMA simplifié
funnel_data = [
    ("Identification", "3,000", Inches(10), RGBColor(200, 200, 200)),
    ("Dédoublonnage", "1,700", Inches(8.5), RGBColor(180, 180, 180)),
    ("Criblage titres", "361", Inches(7), RGBColor(150, 150, 150)),
    ("Éligibilité", "181", Inches(5.5), RGBColor(100, 100, 100))
]

y_funnel = Inches(4.6)
for label, count, width, color in funnel_data:
    # Barre
    bar = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4), y_funnel, width, Inches(0.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    
    # Texte
    txt = slide4.shapes.add_textbox(Inches(0.5), y_funnel, Inches(3.3), Inches(0.6))
    tf = txt.text_frame
    p = tf.paragraphs[0]
    p.text = f"{label}: {count}"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT
    
    y_funnel += Inches(0.7)

print("Slide 4: Avancement articles ✓")

# ============================================================
# SLIDE 5 : Évolution maintenance
# ============================================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide5)
add_title(slide5, "L'évolution de la maintenance industrielle")
add_horizontal_line(slide5, top=Inches(1.1))

maintenance_types = [
    ("Corrective", "On répare après la panne", "Arrêts non planifiés, coûts élevés", RGBColor(200, 80, 80)),
    ("Préventive", "Interventions à intervalles fixes", "Gaspillage, interventions inutiles", RGBColor(200, 160, 80)),
    ("Prédictive", "Anticipation via les données", "Nécessite données et modèles IA", RGBColor(80, 160, 80)),
    ("Prescriptive", "IA recommande l'action", "Niveau de maturité encore faible", RGBColor(80, 120, 160))
]

y_pos = Inches(1.6)
for name, principe, limite, color in maintenance_types:
    box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(1.2))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    box.line.color.rgb = color
    box.line.width = Pt(3)
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = name
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = f"Principe : {principe}  |  Limite : {limite}"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.35)

# Statistiques
stats = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.7))
stats.fill.solid()
stats.fill.fore_color.rgb = COLOR_BOX_BG
stats.line.color.rgb = COLOR_LIGHT_GRAY

tf = stats.text_frame
p = tf.paragraphs[0]
p.text = "Impact : 70% des pannes sont précédées de signaux détectables | Marché mondial > $630 milliards d'ici 2028"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 5: Évolution maintenance ✓")

# ============================================================
# SLIDE 6 : Paradoxe des données
# ============================================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide6)
add_title(slide6, "Le paradoxe des données industrielles")
add_subtitle(slide6, "Données utiles mais inaccessibles")
add_horizontal_line(slide6, top=Inches(1.5))

obstacles = [
    ("Confidentialité", "Données de production stratégiquement sensibles — aucun opérateur ne partage avec ses concurrents"),
    ("Réglementations", "RGPD et réglementations sectorielles encadrent strictement les transferts de données"),
    ("Volume", "Parc d'éoliennes = dizaines de GO/jour — centralisation impraticable et coûteuse"),
    ("Hétérogénéité", "SCADA éolien ≠ données HVAC ≠ acoustique production — formats et patterns différents")
]

y_pos = Inches(1.9)
for title, desc in obstacles:
    # Numéro
    num = slide6.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.6), y_pos + Inches(0.1), Inches(0.5), Inches(0.5))
    num.fill.solid()
    num.fill.fore_color.rgb = COLOR_ACCENT
    num.line.fill.background()
    
    num_tf = num.text_frame
    p = num_tf.paragraphs[0]
    p.text = str(obstacles.index((title, desc)) + 1)
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Contenu
    box = slide6.shapes.add_textbox(Inches(1.3), y_pos, Inches(11.5), Inches(1))
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.15)

# Question centrale
q_box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.9))
q_box.fill.solid()
q_box.fill.fore_color.rgb = RGBColor(240, 248, 255)
q_box.line.color.rgb = COLOR_ACCENT
q_box.line.width = Pt(2)

tf = q_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Question centrale : Comment entraîner de bons modèles sans jamais voir les données brutes des autres ?"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_ACCENT
p.alignment = PP_ALIGN.CENTER

print("Slide 6: Paradoxe données ✓")

# Continue with remaining slides...
print("\nGénération des slides 7-22 en cours...")

# ============================================================
# SLIDE 7 : Positionnement
# ============================================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide7)
add_title(slide7, "Positionnement de la thèse")
add_horizontal_line(slide7, top=Inches(1.1))

# Schéma central
props = [
    ("Federated Learning", "Entraînement collectif sans centralisation", Inches(0.5), Inches(2), RGBColor(230, 240, 250)),
    ("Foundation Models TS", "Modèles pré-entraînés zero-shot/few-shot", Inches(9.5), Inches(2), RGBColor(230, 250, 240)),
    ("Maintenance Prédictive", "Multi-domaine : éolien, HVAC, manufacture", Inches(5), Inches(5.5), RGBColor(250, 240, 230))
]

for title, desc, x, y, color in props:
    box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.5), Inches(1.8))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.color.rgb = COLOR_ACCENT
    box.line.width = Pt(2)
    
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_TITLE
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT
    p2.alignment = PP_ALIGN.CENTER

# Centre : Intersection (thèse)
center = slide7.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5), Inches(3), Inches(3.3), Inches(1.6))
center.fill.solid()
center.fill.fore_color.rgb = COLOR_ACCENT
center.line.fill.background()

tf = center.text_frame
p = tf.paragraphs[0]
p.text = "CETTE THÈSE"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\nFL + TS FMs + Maintenance"
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(255, 255, 255)
p2.alignment = PP_ALIGN.CENTER

# Proposition centrale en bas
prop_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6), Inches(12.3), Inches(1.2))
prop_box.fill.solid()
prop_box.fill.fore_color.rgb = RGBColor(250, 250, 250)
prop_box.line.color.rgb = COLOR_ACCENT

tf = prop_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Proposition centrale"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_ACCENT

p2 = tf.add_paragraph()
p2.text = "Un Foundation Model de séries temporelles, entraînable de façon fédérée sur des données industrielles hétérogènes, capable de s'adapter à plusieurs domaines sans que les données brutes ne quittent les sites locaux."
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT

print("Slide 7: Positionnement ✓")

# ============================================================
# SLIDE 8 : Federated Learning
# ============================================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide8)
add_title(slide8, "Concepts de base : Apprentissage Fédéré")
add_horizontal_line(slide8, top=Inches(1.1))

# Schéma client-serveur
clients = [
    ("Client 1\n(Données locales)", Inches(0.5), Inches(2)),
    ("Client 2\n(Données locales)", Inches(0.5), Inches(3.5)),
    ("Client 3\n(Données locales)", Inches(0.5), Inches(5))
]

for label, x, y in clients:
    box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.5), Inches(1.2))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(230, 240, 250)
    box.line.color.rgb = COLOR_ACCENT
    
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.CENTER

# Flèches vers serveur
for i in range(3):
    y_arrow = Inches(2.6) + i * Inches(1.5)
    arrow = slide8.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.2), y_arrow, Inches(1.5), Inches(0.4))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = COLOR_ACCENT
    arrow.line.fill.background()
    
    # Mises à jour
    txt = slide8.shapes.add_textbox(Inches(3.2), y_arrow - Inches(0.3), Inches(1.5), Inches(0.3))
    tf = txt.text_frame
    p = tf.paragraphs[0]
    p.text = "MàJ modèle"
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.CENTER

# Serveur
server = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5), Inches(3), Inches(3), Inches(1.5))
server.fill.solid()
server.fill.fore_color.rgb = COLOR_ACCENT
server.line.fill.background()

tf = server.text_frame
p = tf.paragraphs[0]
p.text = "SERVEUR"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\nAgrégation\n(FedAvg / FedProx)"
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(255, 255, 255)
p2.alignment = PP_ALIGN.CENTER

# Flèches retour
for i in range(3):
    y_arrow = Inches(2.6) + i * Inches(1.5)
    arrow = slide8.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(4.7), y_arrow, Inches(1.5), Inches(0.4))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = RGBColor(100, 140, 180)
    arrow.line.fill.background()

# Points clés
points = slide8.shapes.add_textbox(Inches(8.5), Inches(2), Inches(4.5), Inches(4.5))
tf = points.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Points clés du FL"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE

bullet_points = [
    "Données restent locales",
    "Partage des mises à jour (gradients/poids)",
    "Agrégation périodique sur serveur",
    "Robustesse aux données non-IID (FedProx)",
    "Préservation de la confidentialité"
]

for bp in bullet_points:
    p = tf.add_paragraph()
    p.text = "• " + bp
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

print("Slide 8: Federated Learning ✓")

# ============================================================
# SLIDE 9 : Foundation Models
# ============================================================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide9)
add_title(slide9, "Concepts de base : Foundation Models pour séries temporelles")
add_horizontal_line(slide9, top=Inches(1.1))

# Tableau comparatif
models = [
    ("TimesFM", "2024", "100Mds points", "Prévision", "200M"),
    ("Moirai", "2024", "320M points", "Prév. + Anomalie", "32-480M"),
    ("MOMENT", "2024", "Time-Series Pile", "Prév. + Classif.", "385M"),
    ("Lag-Llama", "2023", "Features lagged", "Prévision", "~100M")
]

# Header
headers = ["Modèle", "Année", "Entraînement", "Tâches", "Params"]
x_positions = [Inches(0.5), Inches(2.5), Inches(4.3), Inches(6.8), Inches(9.5)]
col_widths = [Inches(1.8), Inches(1.6), Inches(2.3), Inches(2.5), Inches(1.5)]

for i, (header, x, w) in enumerate(zip(headers, x_positions, col_widths)):
    cell = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_ACCENT
    cell.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = cell.text_frame
    p = tf.paragraphs[0]
    p.text = header
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

# Data rows
for row_idx, model in enumerate(models):
    y = Inches(2.2) + row_idx * Inches(0.7)
    bg_color = RGBColor(245, 245, 245) if row_idx % 2 == 0 else RGBColor(250, 250, 250)
    
    for col_idx, (value, x, w) in enumerate(zip(model, x_positions, col_widths)):
        cell = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.65))
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
        cell.line.color.rgb = COLOR_LIGHT_GRAY
        
        tf = cell.text_frame
        p = tf.paragraphs[0]
        p.text = value
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT
        p.alignment = PP_ALIGN.CENTER

# Caractéristiques
chars = slide9.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(12.3), Inches(2))
tf = chars.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Caractéristiques clés des TS FMs"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE

features = [
    "Pré-entraînement sur corpus massif de données publiques",
    "Capacité zero-shot et few-shot (adaptation avec peu d'exemples)",
    "Architecture Transformer (attention temporelle)",
    "Révolution : un modèle unique pour nombreux équipements industriels"
]

for f in features:
    p = tf.add_paragraph()
    p.text = "• " + f
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(4)

print("Slide 9: Foundation Models ✓")

# ============================================================
# SLIDE 10 : Maintenance prédictive
# ============================================================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide10)
add_title(slide10, "Concepts de base : Maintenance Prédictive")
add_horizontal_line(slide10, top=Inches(1.1))

tasks = [
    ("Détection d'anomalies", "Identifier un comportement anormal dans les signaux"),
    ("Classification de défaillances", "Reconnaître le type de panne (tâche principale de la thèse)"),
    ("Estimation RUL", "Prédire la durée de vie résiduelle avant panne"),
    ("Prévision de l'état de santé", "Suivre l'évolution globale de l'équipement")
]

y_pos = Inches(1.6)
for title, desc in tasks:
    box = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(1))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    box.line.color.rgb = COLOR_ACCENT
    box.line.width = Pt(2)
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.15)

# Difficultés spécifiques
bottom = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.8), Inches(12.3), Inches(1.4))
bottom.fill.solid()
bottom.fill.fore_color.rgb = RGBColor(255, 245, 240)
bottom.line.color.rgb = RGBColor(180, 100, 50)

tf = bottom.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Difficultés spécifiques aux données industrielles"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(150, 80, 50)

issues = "Multivariées • Non-stationnaires • Classes déséquilibrées • Bruit de capteurs • Fréquences d'échantillonnage hétérogènes"
p2 = tf.add_paragraph()
p2.text = issues
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT

print("Slide 10: Maintenance prédictive ✓")

# ============================================================
# SLIDE 11 : Cartographie domaines
# ============================================================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide11)
add_title(slide11, "État de l'art : Cartographie du domaine de recherche")
add_horizontal_line(slide11, top=Inches(1.1))

# Tableau maturité
domains = [
    ("FL général", "Algorithmes FedAvg/FedProx, hétérogénéité, privacy", "Mature", "1000+", RGBColor(200, 220, 240)),
    ("TS FMs centralisés", "TimesFM, Moirai, MOMENT, Lag-Llama", "Émergent", "~8 modèles", RGBColor(240, 230, 200)),
    ("FL pour NLP/Vision", "LoRA fédéré, adapters, split learning", "Émergent", "~50 travaux", RGBColor(240, 230, 200)),
    ("FL pour maintenance", "Pruckovskaja et al., OASEES, turbofan", "Initial", "~10 travaux", RGBColor(240, 210, 200)),
    ("FL + TS FMs", "Time-FFM, Ali et al., FedForecaster", "Quasi vide", "3 travaux", RGBColor(240, 180, 180)),
    ("FL + TS FMs + Maintenance", "———", "VIERGE", "0", RGBColor(220, 150, 150))
]

# Headers
headers = ["Domaine", "Description", "Maturité", "Nb. travaux"]
x_pos = [Inches(0.5), Inches(3.2), Inches(8.5), Inches(10.8)]
widths = [Inches(2.5), Inches(5), Inches(2), Inches(1.8)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_ACCENT
    cell.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = cell.text_frame
    p = tf.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

# Rows
for idx, (domain, desc, maturity, count, color) in enumerate(domains):
    y = Inches(2.2) + idx * Inches(0.7)
    
    data = [domain, desc, maturity, count]
    for value, x, w in zip(data, x_pos, widths):
        cell = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.65))
        cell.fill.solid()
        cell.fill.fore_color.rgb = color
        cell.line.color.rgb = COLOR_LIGHT_GRAY
        
        tf = cell.text_frame
        p = tf.paragraphs[0]
        p.text = value
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT
        if value == "VIERGE" or value == "0":
            p.font.bold = True
            p.font.color.rgb = RGBColor(180, 60, 60)

print("Slide 11: Cartographie domaines ✓")

# ============================================================
# SLIDE 12 : Les 3 travaux existants
# ============================================================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide12)
add_title(slide12, "Les trois seuls travaux à l'intersection FL + TS FMs")
add_horizontal_line(slide12, top=Inches(1.1))

works = [
    {
        "name": "Time-FFM",
        "authors": "Liu et al. (2024) — NeurIPS",
        "approach": "FM fédéré natif avec LLM reprogrammé",
        "models": "Tokenization texte des séries",
        "domain": "Données génériques uniquement",
        "limits": "Pas de maintenance, pas de LoRA/PEFT"
    },
    {
        "name": "Ali et al.",
        "authors": "Ali et al. (2025) — arXiv",
        "approach": "Fine-tuning fédéré de modèles pré-entraînés",
        "models": "Chronos, TimesFM",
        "domain": "Médical (ECG) uniquement",
        "limits": "FedAvg standard, pas de solution non-IID"
    },
    {
        "name": "FedForecaster",
        "authors": "Maher et al. (2025) — EDBT",
        "approach": "AutoML fédéré avec méta-modèle",
        "models": "Méta-modèle de recommandation",
        "domain": "Générique",
        "limits": "Pas un vrai FM, pas de transfert cross-domaine"
    }
]

y_pos = Inches(1.5)
for work in works:
    box = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(1.6))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    box.line.color.rgb = COLOR_ACCENT
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = work["name"] + " — " + work["authors"]
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_ACCENT
    
    details = [
        f"Approche : {work['approach']}",
        f"Modèles : {work['models']}  |  Domaine : {work['domain']}",
        f"Limite : {work['limits']}"
    ]
    
    for detail in details:
        p = tf.add_paragraph()
        p.text = detail
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.8)

print("Slide 12: 3 travaux existants ✓")

# ============================================================
# SLIDE 13 : Les 4 problématiques
# ============================================================
slide13 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide13)
add_title(slide13, "Problématiques identifiées : les quatre verrous")
add_horizontal_line(slide13, top=Inches(1.1))

problems = [
    ("P1 — Personnalisation fédérée", 
     "Comment adapter un TS FM global à des clients aux données très hétérogènes (non-IID) ?",
     "Manque : mécanisme LoRA + prompts domaine en FL",
     RGBColor(240, 200, 200)),
    
    ("P2 — Absence de benchmark", 
     "Aucun protocole standardisé pour évaluer les TS FMs en FL",
     "Manque : partitions non-IID réalistes, métriques maintenance",
     RGBColor(240, 220, 200)),
    
    ("P3 — Incompatibilité architecturale", 
     "Les TS FMs actuels non conçus pour les contraintes FL",
     "Manque : patching adaptatif, MoE sparse, mises à jour low-rank",
     RGBColor(200, 220, 240)),
    
    ("P4 — Inadéquation aux données industrielles", 
     "TS FMs pré-entraînés sur données publiques (météo, finance), jamais testés sur SCADA/vibration",
     "Manque : corpus industriel et évaluation zero-shot réelle",
     RGBColor(220, 240, 220))
]

y_pos = Inches(1.5)
for title, problem, gap, color in problems:
    box = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(1.25))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.color.rgb = COLOR_ACCENT
    box.line.width = Pt(2)
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = problem + " → " + gap
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.35)

print("Slide 13: 4 problématiques ✓")

# ============================================================
# SLIDE 14 : RQ1 & RQ2
# ============================================================
slide14 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide14)
add_title(slide14, "Questions de recherche : RQ1 & RQ2")
add_horizontal_line(slide14, top=Inches(1.1))

# RQ1
rq1_box = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(12.3), Inches(2.3))
rq1_box.fill.solid()
rq1_box.fill.fore_color.rgb = RGBColor(240, 248, 255)
rq1_box.line.color.rgb = COLOR_ACCENT
rq1_box.line.width = Pt(3)

tf = rq1_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "RQ1 — Personnalisation fédérée"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_ACCENT

p2 = tf.add_paragraph()
p2.text = "\nComment concevoir un mécanisme de personnalisation fédérée, combinant prompts domaine-spécifiques et LoRA, permettant à un TS FM de s'adapter aux distributions locales hétérogènes ?"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT

p3 = tf.add_paragraph()
p3.text = "\n→ Approche : LoRA dual (global agrégé + local personnel) + prompts de domaine"
p3.font.size = Pt(11)
p3.font.italic = True
p3.font.color.rgb = COLOR_ACCENT

# RQ2
rq2_box = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(4.1), Inches(12.3), Inches(2.3))
rq2_box.fill.solid()
rq2_box.fill.fore_color.rgb = RGBColor(255, 250, 240)
rq2_box.line.color.rgb = RGBColor(180, 120, 50)
rq2_box.line.width = Pt(3)

tf = rq2_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "RQ2 — Benchmark fédéré"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(150, 100, 40)

p2 = tf.add_paragraph()
p2.text = "\nQuels protocoles d'évaluation et benchmarks fédérés permettent de mesurer fidèlement les capacités de généralisation cross-domaine d'un TS FM en maintenance industrielle ?"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT

p3 = tf.add_paragraph()
p3.text = "\n→ Approche : FedTS-Bench avec partitions non-IID, métriques F1/AUC-PR"
p3.font.size = Pt(11)
p3.font.italic = True
p3.font.color.rgb = RGBColor(150, 100, 40)

print("Slide 14: RQ1 & RQ2 ✓")

# ============================================================
# SLIDE 15 : RQ3 & RQ4
# ============================================================
slide15 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide15)
add_title(slide15, "Questions de recherche : RQ3 & RQ4")
add_horizontal_line(slide15, top=Inches(1.1))

# RQ3
rq3_box = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(12.3), Inches(2.3))
rq3_box.fill.solid()
rq3_box.fill.fore_color.rgb = RGBColor(240, 255, 250)
rq3_box.line.color.rgb = RGBColor(50, 140, 100)
rq3_box.line.width = Pt(3)

tf = rq3_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "RQ3 — Architecture native FL"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(40, 120, 80)

p2 = tf.add_paragraph()
p2.text = "\nQuelles propriétés architecturales d'un TS FM — tokenisation, attention, mise à jour — maximisent son efficacité de communication et sa convergence en FL hétérogène ?"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT

p3 = tf.add_paragraph()
p3.text = "\n→ Approche : FedTSFM-Arch avec patching hiérarchique, MoE sparse, LoRA query/key"
p3.font.size = Pt(11)
p3.font.italic = True
p3.font.color.rgb = RGBColor(40, 120, 80)

# RQ4
rq4_box = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(4.1), Inches(12.3), Inches(2.3))
rq4_box.fill.solid()
rq4_box.fill.fore_color.rgb = RGBColor(255, 245, 250)
rq4_box.line.color.rgb = RGBColor(140, 80, 120)
rq4_box.line.width = Pt(3)

tf = rq4_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "RQ4 — Données industrielles réelles"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(120, 60, 90)

p2 = tf.add_paragraph()
p2.text = "\nDans quelle mesure les TS FMs actuels peuvent-ils se généraliser aux signaux industriels (SCADA, vibration, acoustique) en zero-shot ou few-shot ?"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT

p3 = tf.add_paragraph()
p3.text = "\n→ Approche : IndusFedFM — validation sur éolien, HVAC, manufacture"
p3.font.size = Pt(11)
p3.font.italic = True
p3.font.color.rgb = RGBColor(120, 60, 90)

print("Slide 15: RQ3 & RQ4 ✓")

# ============================================================
# SLIDE 16 : Contribution C1
# ============================================================
slide16 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide16)
add_title(slide16, "Contribution C1 : FedPEFT-TS")
add_subtitle(slide16, "Personnalisation fédérée par LoRA + prompts de domaine")
add_horizontal_line(slide16, top=Inches(1.5))

# Architecture schéma
box_left = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(2), Inches(3.5), Inches(1.5))
box_left.fill.solid()
box_left.fill.fore_color.rgb = RGBColor(230, 240, 250)
box_left.line.color.rgb = COLOR_ACCENT

tf = box_left.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "TS FM Backbone"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\n(Moirai / TimesFM)\nGelé — partagé"
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

# Flèche droite
arrow = slide16.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.2), Inches(2.5), Inches(1.5), Inches(0.5))
arrow.fill.solid()
arrow.fill.fore_color.rgb = COLOR_ACCENT

# LoRA box
lora_box = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6), Inches(1.8), Inches(3), Inches(2))
lora_box.fill.solid()
lora_box.fill.fore_color.rgb = RGBColor(250, 240, 230)
lora_box.line.color.rgb = RGBColor(180, 120, 60)

tf = lora_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "LoRA Layers"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\nGlobal (agrégé)\n+ Local (client)"
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

# Prompts
prompt_box = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6), Inches(4.2), Inches(3), Inches(1.2))
prompt_box.fill.solid()
prompt_box.fill.fore_color.rgb = RGBColor(230, 250, 240)
prompt_box.line.color.rgb = RGBColor(60, 140, 100)

tf = prompt_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Domain Prompts"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

# Client box
client_box = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.5), Inches(2.2), Inches(3.3), Inches(2.5))
client_box.fill.solid()
client_box.fill.fore_color.rgb = RGBColor(255, 245, 240)
client_box.line.color.rgb = RGBColor(160, 100, 60)

tf = client_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Client i"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\nDonnées locales\n+ LoRA local\n+ Prompt domaine"
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

# Innovation
innov = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.5), Inches(12.3), Inches(1.5))
innov.fill.solid()
innov.fill.fore_color.rgb = RGBColor(240, 248, 255)
innov.line.color.rgb = COLOR_ACCENT

tf = innov.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Innovation : Première combinaison LoRA dual (global + local) + prompts de domaine en FL pour séries temporelles"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_ACCENT
p.alignment = PP_ALIGN.CENTER

print("Slide 16: C1 FedPEFT-TS ✓")

# ============================================================
# SLIDE 17 : Contribution C2
# ============================================================
slide17 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide17)
add_title(slide17, "Contribution C2 : FedTS-Bench")
add_subtitle(slide17, "Benchmark fédéré pour la maintenance industrielle")
add_horizontal_line(slide17, top=Inches(1.5))

# Datasets
datasets = [
    ("NASA C-MAPSS", "Moteurs turbofan", RGBColor(230, 240, 250)),
    ("CWRU", "Roulements (bearing)", RGBColor(230, 250, 240)),
    ("FEMTO-ST", "Dégradation PRONOSTIA", RGBColor(250, 240, 230)),
    ("SCADA Éoliennes", "Données EDP Renewables", RGBColor(255, 245, 240))
]

x_pos = Inches(0.5)
for name, desc, color in datasets:
    box = slide17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(2), Inches(2.9), Inches(1.5))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.color.rgb = COLOR_ACCENT
    
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = name
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TITLE
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT
    p2.alignment = PP_ALIGN.CENTER
    
    x_pos += Inches(3.1)

# Caractéristiques
middle = slide17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(3.8), Inches(12.3), Inches(2))
middle.fill.solid()
middle.fill.fore_color.rgb = RGBColor(250, 250, 250)
middle.line.color.rgb = COLOR_LIGHT_GRAY

tf = middle.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Propriétés du benchmark"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE

props = [
    "Partitions non-IID réalistes simulant N clients industriels hétérogènes",
    "Métriques adaptées : F1 pondéré, AUC-PR (classes déséquilibrées), variance de dérive, rounds à convergence"
]

for prop in props:
    p = tf.add_paragraph()
    p.text = "• " + prop
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT

# Livrable
bottom = slide17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6), Inches(12.3), Inches(1))
bottom.fill.solid()
bottom.fill.fore_color.rgb = RGBColor(240, 248, 255)
bottom.line.color.rgb = COLOR_ACCENT

tf = bottom.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Livrable : Splits de datasets + code d'évaluation open-source — première ressource communautaire de ce type"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_ACCENT
p.alignment = PP_ALIGN.CENTER

print("Slide 17: C2 FedTS-Bench ✓")

# ============================================================
# SLIDE 18 : Contributions C3 & C4
# ============================================================
slide18 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide18)
add_title(slide18, "Contributions C3 & C4 : Architecture et Validation")
add_horizontal_line(slide18, top=Inches(1.1))

# C3
c3_box = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(6), Inches(3.5))
c3_box.fill.solid()
c3_box.fill.fore_color.rgb = RGBColor(240, 248, 255)
c3_box.line.color.rgb = COLOR_ACCENT
c3_box.line.width = Pt(3)

tf = c3_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "C3 — FedTSFM-Arch"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = COLOR_ACCENT

props_c3 = [
    ("Patching hiérarchique", "Découpage adaptatif selon fréquence locale → réduction communication"),
    ("MoE sparse client-guidé", "Experts activés par domaine client → spécialisation sans partage"),
    ("Mises à jour low-rank", "LoRA sur query/key uniquement → réduction ×50 du volume")
]

for title, desc in props_c3:
    p = tf.add_paragraph()
    p.text = f"• {title} : {desc}"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT

# C4
c4_box = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(6), Inches(3.5))
c4_box.fill.solid()
c4_box.fill.fore_color.rgb = RGBColor(255, 250, 240)
c4_box.line.color.rgb = RGBColor(180, 120, 50)
c4_box.line.width = Pt(3)

tf = c4_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "C4 — IndusFedFM"
p.font.bold = True
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(150, 100, 40)

scenarios = [
    "Intra-domaine : N clients éoliens hétérogènes",
    "Cross-domaine : Éolien + HVAC + Manufacture",
    "Cold-start : Nouveau client sans historique"
]

p2 = tf.add_paragraph()
p2.text = "\nValidation sur 3 scénarios :"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TITLE

for scen in scenarios:
    p = tf.add_paragraph()
    p.text = "→ " + scen
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT

# Vision
vision = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.3), Inches(12.3), Inches(1.7))
vision.fill.solid()
vision.fill.fore_color.rgb = RGBColor(245, 245, 245)
vision.line.color.rgb = COLOR_ACCENT
vision.line.width = Pt(2)

tf = vision.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Vision d'ensemble — FedTSFM"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\nC1 (méthode) + C2 (benchmark) + C3 (architecture) + C4 (validation)"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

p3 = tf.add_paragraph()
p3.text = "\nUn Foundation Model de séries temporelles entraînable de façon fédérée pour la maintenance prédictive multi-domaine"
p3.font.size = Pt(11)
p3.font.italic = True
p3.font.color.rgb = COLOR_ACCENT
p3.alignment = PP_ALIGN.CENTER

print("Slide 18: C3 & C4 ✓")

# ============================================================
# SLIDE 19 : Plan de publication
# ============================================================
slide19 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide19)
add_title(slide19, "Plan de publication : 5 publications sur 3 ans")
add_horizontal_line(slide19, top=Inches(1.1))

# Tableau publications
pubs = [
    ("P0", "Data-Centric FL for Wind Turbine PdM", "Master", "Journal", "2025", RGBColor(230, 240, 250)),
    ("P1", "Literature Review FL+TS FMs for Industrial Maintenance", "SLR (C1-C2)", "Journal", "An 1-2", RGBColor(240, 250, 245)),
    ("P2", "FedTS-Bench: A Federated Benchmark for Industrial PM", "C2", "Conférence", "An 2", RGBColor(250, 245, 240)),
    ("P3", "FedTSFM-Arch: A Federation-Native TS FM Architecture", "C3", "Journal Q1", "An 2-3", RGBColor(255, 240, 245)),
    ("P4", "IndusFedFM: Multi-Domain Federated TS FMs for PM", "C4", "Journal Q1", "An 3", RGBColor(255, 245, 240))
]

# Headers
headers = ["#", "Titre", "Contribution", "Type", "Année"]
x_pos = [Inches(0.5), Inches(1.3), Inches(8.5), Inches(10.5), Inches(11.8)]
widths = [Inches(0.7), Inches(7), Inches(1.8), Inches(1.2), Inches(1.2)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide19.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_ACCENT
    cell.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = cell.text_frame
    p = tf.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

# Data
for idx, (num, title, contrib, type_pub, year, color) in enumerate(pubs):
    y = Inches(2.2) + idx * Inches(0.9)
    
    data = [num, title, contrib, type_pub, year]
    for value, x, w in zip(data, x_pos, widths):
        cell = slide19.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.8))
        cell.fill.solid()
        cell.fill.fore_color.rgb = color
        cell.line.color.rgb = COLOR_LIGHT_GRAY
        
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = value
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT
        if num in ["P3", "P4"]:
            p.font.bold = True

# Stratégie
strategy = slide19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.7))
strategy.fill.solid()
strategy.fill.fore_color.rgb = COLOR_BOX_BG
strategy.line.color.rgb = COLOR_LIGHT_GRAY

tf = strategy.text_frame
p = tf.paragraphs[0]
p.text = "Stratégie : P0 (Master) + P1 (SLR) dès que possible → P2 (conférence) → P3/P4 (journaux Q1 majeurs)"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 19: Plan publication ✓")

# ============================================================
# SLIDE 20 : Fil narratif
# ============================================================
slide20 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide20)
add_title(slide20, "Fil narratif de la thèse")
add_horizontal_line(slide20, top=Inches(1.1))

# Flowchart vertical
pubs_flow = [
    ("P0 (Master)", "Data-Centric FL for Wind Turbine", "Année 1", "Master", RGBColor(200, 200, 200)),
    ("P1 (SLR)", "Literature Review — Identifier les gaps", "Années 1-2", "C1-C2", RGBColor(180, 200, 220)),
    ("P2 (Benchmark)", "FedTS-Bench — Verrou expérimental", "Année 2", "C2", RGBColor(200, 220, 200)),
    ("P3 (Architecture)", "FedTSFM-Arch — Verrou architectural", "Années 2-3", "C3", RGBColor(220, 200, 180)),
    ("P4 (Validation)", "IndusFedFM — Preuve industrielle", "Année 3", "C4", RGBColor(220, 180, 180))
]

y_pos = Inches(1.5)
for name, desc, year, contrib, color in pubs_flow:
    # Box
    box = slide20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2), y_pos, Inches(8), Inches(0.9))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.color.rgb = COLOR_ACCENT
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"{name} — {desc}"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT
    
    # Année (droite)
    year_box = slide20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.3), y_pos + Inches(0.2), Inches(2), Inches(0.5))
    year_box.fill.solid()
    year_box.fill.fore_color.rgb = RGBColor(240, 240, 240)
    year_box.line.color.rgb = COLOR_LIGHT_GRAY
    
    y_tf = year_box.text_frame
    p = y_tf.paragraphs[0]
    p.text = year
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.CENTER
    
    # Contribution (gauche)
    c_box = slide20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), y_pos + Inches(0.2), Inches(1.5), Inches(0.5))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = RGBColor(240, 240, 240)
    c_box.line.color.rgb = COLOR_LIGHT_GRAY
    
    c_tf = c_box.text_frame
    p = c_tf.paragraphs[0]
    p.text = contrib
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.CENTER
    
    # Flèche vers bas (sauf dernier)
    if pubs_flow.index((name, desc, year, contrib, color)) < len(pubs_flow) - 1:
        arrow = slide20.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(5.7), y_pos + Inches(0.9), Inches(0.6), Inches(0.3))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = COLOR_ACCENT
    
    y_pos += Inches(1.1)

print("Slide 20: Fil narratif ✓")

# ============================================================
# SLIDE 21 : Cibles de publication
# ============================================================
slide21 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide21)
add_title(slide21, "Conférences et journaux ciblés")
add_horizontal_line(slide21, top=Inches(1.1))

# Conférences (gauche)
conf_box = slide21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(6), Inches(3.5))
conf_box.fill.solid()
conf_box.fill.fore_color.rgb = RGBColor(240, 248, 255)
conf_box.line.color.rgb = COLOR_ACCENT

tf = conf_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Conférences A* (soumissions rapides)"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_ACCENT

confs = [
    "NeurIPS — TS FMs + méthodes FL",
    "ICML — Architecture + PEFT fédéré",
    "ICLR — FL + Foundation Models",
    "KDD — Benchmark + application industrielle",
    "AAAI — FL personnalisé séries temporelles"
]

for c in confs:
    p = tf.add_paragraph()
    p.text = "• " + c
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT

# Journaux (droite)
journal_box = slide21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(6), Inches(3.5))
journal_box.fill.solid()
journal_box.fill.fore_color.rgb = RGBColor(255, 250, 240)
journal_box.line.color.rgb = RGBColor(180, 120, 50)

tf = journal_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Journaux Q1 (contributions majeures)"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(150, 100, 40)

journals = [
    "Neurocomputing — Gratuit, Q1, 28% acc.",
    "IEEE Trans. Industrial Electronics — Q1, 28% acc.",
    "Machine Learning (Springer) — Gratuit, Q1",
    "JMLR — Diamond OA, Q1",
    "Pattern Recognition Letters — Q2, rapide"
]

for j in journals:
    p = tf.add_paragraph()
    p.text = "• " + j
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT

# Stratégie matching
match = slide21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.3), Inches(12.3), Inches(1.5))
match.fill.solid()
match.fill.fore_color.rgb = RGBColor(250, 250, 250)
match.line.color.rgb = COLOR_LIGHT_GRAY

tf = match.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Stratégie de matching publications/cibles"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = COLOR_TITLE

matches = [
    "P1 (SLR) → Machine Learning / JMLR / Neurocomputing",
    "P2 (Benchmark) → Pattern Recognition Letters / Conférence KDD",
    "P3 (Architecture) → Neurocomputing / JMLR",
    "P4 (Industriel) → IEEE Trans. Industrial Electronics / IEEE T-ASE"
]

for m in matches:
    p = tf.add_paragraph()
    p.text = "• " + m
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT

print("Slide 21: Cibles publication ✓")

# ============================================================
# SLIDE 22 : Calendrier 3 ans
# ============================================================
slide22 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide22)
add_title(slide22, "Calendrier prévisionnel et priorités immédiates")
add_horizontal_line(slide22, top=Inches(1.1))

# Priorités immédiates
priority_box = slide22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.5))
priority_box.fill.solid()
priority_box.fill.fore_color.rgb = RGBColor(255, 245, 240)
priority_box.line.color.rgb = RGBColor(180, 100, 50)
priority_box.line.width = Pt(2)

tf = priority_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Priorités immédiates (2025-2026)"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(150, 80, 50)

priorities = [
    "Débloquer article Master : correction pipeline SCADA, débogage FedProx",
    "Commencer SLR : formalisation PRISMA, structuration des 181 articles retenus"
]

for pr in priorities:
    p = tf.add_paragraph()
    p.text = "→ " + pr
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT

# Timeline semestres
semesters = [
    ("An 1, S1", "Finaliser P0 — SLR — Prototypage C1", "P0 soumis"),
    ("An 1, S2", "Expériences C1 — Construction C2", "P1 soumis"),
    ("An 2, S1", "Finaliser C2 — Début C3", "P2 soumis"),
    ("An 2, S2", "Expériences C3 — Rédaction P3", "P3 soumis"),
    ("An 3, S1", "Déploiement C4 — Multi-domaines", "Données C4"),
    ("An 3, S2", "Rédaction P4 — Thèse", "P4 + Soutenance")
]

y_pos = Inches(3.3)
for sem, acts, deliver in semesters:
    # Semestre
    s_box = slide22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(2.5), Inches(0.6))
    s_box.fill.solid()
    s_box.fill.fore_color.rgb = COLOR_ACCENT
    s_box.line.fill.background()
    
    s_tf = s_box.text_frame
    p = s_tf.paragraphs[0]
    p.text = sem
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Activités
    a_box = slide22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), y_pos, Inches(6.5), Inches(0.6))
    a_box.fill.solid()
    a_box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    a_box.line.color.rgb = COLOR_LIGHT_GRAY
    
    a_tf = a_box.text_frame
    p = a_tf.paragraphs[0]
    p.text = acts
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT
    
    # Livrable
    l_box = slide22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.9), y_pos, Inches(2.9), Inches(0.6))
    l_box.fill.solid()
    l_box.fill.fore_color.rgb = RGBColor(240, 248, 255)
    l_box.line.color.rgb = COLOR_ACCENT
    
    l_tf = l_box.text_frame
    p = l_tf.paragraphs[0]
    p.text = deliver
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_ACCENT
    p.alignment = PP_ALIGN.CENTER
    
    y_pos += Inches(0.7)

# Note bottom
note = slide22.shapes.add_textbox(Inches(0.5), Inches(6.8), Inches(12.3), Inches(0.5))
tf = note.text_frame
p = tf.paragraphs[0]
p.text = "Points d'attention : article Master bloqué sur résultats — calendrier réaliste si focus maintenu sur recherche"
p.font.size = Pt(11)
p.font.italic = True
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 22: Calendrier ✓")

# ============================================================
# SAUVEGARDE
# ============================================================
output_path = "presentation_rapport_avancement.pptx"
prs.save(output_path)
print(f"\n{'='*60}")
print(f"Présentation générée avec succès !")
print(f"Fichier : {output_path}")
print(f"Nombre de slides : {len(prs.slides)}")
print(f"{'='*60}")
