"""
Script de mise à jour de la présentation PPTX pour correspondre au rapport actuel.
Ajoute les sections manquantes : formations, enseignement, PRISMA détaillé, table des journaux.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Couleurs institutionnelles (gris/blanc)
COLOR_BG = RGBColor(250, 250, 250)
COLOR_TITLE = RGBColor(45, 45, 45)  # #2D2D2D
COLOR_TEXT = RGBColor(107, 107, 107)  # #6B6B6B
COLOR_ACCENT = RGBColor(30, 80, 160)
COLOR_LIGHT_GRAY = RGBColor(224, 224, 224)
COLOR_BOX_BG = RGBColor(245, 245, 245)

def set_slide_bg(slide, color=COLOR_BG):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_title(slide, text, left=Inches(0.5), top=Inches(0.3), width=Inches(9), height=Inches(0.8)):
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE
    p.alignment = PP_ALIGN.LEFT
    return title_box

def add_section_num(slide, text, top=Inches(0.5)):
    box = slide.shapes.add_textbox(Inches(0.5), top, Inches(9), Inches(0.4))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(153, 153, 153)
    return box

def add_horizontal_line(slide, top=Inches(1.15), left=Inches(0.5), width=Inches(9)):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_LIGHT_GRAY
    line.line.fill.background()
    return line

# Créer la présentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

print("Génération de la présentation mise à jour...")

# ============================================================
# SLIDE 1 : Titre
# ============================================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide1)

accent = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.05))
accent.fill.solid()
accent.fill.fore_color.rgb = COLOR_TITLE
accent.line.fill.background()

title_box = slide1.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(12), Inches(1.5))
tf = title_box.text_frame
p = tf.paragraphs[0]
p.text = "Federated Time Series Foundation Models"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.LEFT

p2 = tf.add_paragraph()
p2.text = "pour la Maintenance Prédictive Industrielle Multi-Domaine"
p2.font.size = Pt(22)
p2.font.color.rgb = COLOR_TITLE
p2.alignment = PP_ALIGN.LEFT

subtitle = slide1.shapes.add_textbox(Inches(0.7), Inches(3.5), Inches(12), Inches(0.5))
tf = subtitle.text_frame
p = tf.paragraphs[0]
p.text = "Rapport d'avancement de thèse — Première année"
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TEXT

info = slide1.shapes.add_textbox(Inches(0.7), Inches(4.3), Inches(12), Inches(2))
tf = info.text_frame
tf.word_wrap = True

lines = [
    ("Doctorant :", "Yassire AMMOURI"),
    ("Directeur de thèse :", "Pr. Younes Karfa Bakali"),
    ("Encadrant :", "Mme Rajaa SAIDI"),
    ("Laboratoire :", "LRIT — Université Mohammed V, Rabat"),
    ("Date :", "Mars 2026")
]

for i, (label, value) in enumerate(lines):
    if i == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.text = f"{label}  {value}"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT if i > 0 else COLOR_TITLE
    p.space_after = Pt(6)

footer = slide1.shapes.add_textbox(Inches(0.7), Inches(6.8), Inches(12), Inches(0.4))
tf = footer.text_frame
p = tf.paragraphs[0]
p.text = "Université Mohammed V — Faculté des Sciences de Rabat — LRIT"
p.font.size = Pt(9)
p.font.color.rgb = RGBColor(153, 153, 153)
p.alignment = PP_ALIGN.LEFT

print("Slide 1: Titre ✓")

# ============================================================
# SLIDE 2 : Formations et certifications
# ============================================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide2)
add_section_num(slide2, "AVANT-PROPOS — Formations et certifications", Inches(0.4))
add_title(slide2, "Formations et certifications suivies", top=Inches(0.7))
add_horizontal_line(slide2, top=Inches(1.25))

formations = [
    ("WIPO — DL101", "Propriété intellectuelle (brevets, droits d'auteur, marques)", "complète"),
    ("Wiley", "Publication scientifique : processus de soumission, révision par les pairs", "1 Certif"),
    ("Scopus (Elsevier)", "Base bibliographique : recherche avancée, analyse de citations", "1 Certif"),
    ("Springer Nature", "Plateforme Springer : recherche et politiques open access", "1 Certif"),
    ("Taylor & Francis", "Outils de recherche et publication en ingénierie/informatique", "5 Certif"),
    ("Clarivate (WoS)", "Web of Science : facteurs d'impact, indicateurs bibliométriques", "10 Certif")
]

y_pos = Inches(1.5)
for org, desc, status in formations:
    box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(0.85))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    box.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"{org}  —  {desc}"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TITLE
    
    y_pos += Inches(0.95)

# Infobox
infobox = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.7))
infobox.fill.solid()
infobox.fill.fore_color.rgb = RGBColor(240, 248, 255)
infobox.line.color.rgb = COLOR_ACCENT

tf = infobox.text_frame
p = tf.paragraphs[0]
p.text = "Apport : capacité à conduire une revue de littérature rigoureuse et identifier les journaux pertinents"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 2: Formations ✓")

# ============================================================
# SLIDE 3 : Avancement articles + Enseignement
# ============================================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide3)
add_section_num(slide3, "AVANT-PROPOS — Avancement et activités", Inches(0.4))
add_title(slide3, "Avancement de la rédaction et activités pédagogiques", top=Inches(0.7))
add_horizontal_line(slide3, top=Inches(1.25))

# Article Master
box1 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(6), Inches(2.5))
box1.fill.solid()
box1.fill.fore_color.rgb = RGBColor(255, 245, 240)
box1.line.color.rgb = RGBColor(200, 100, 50)

tf = box1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "P0 — Article Master (Data-Centric FL)"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE

p2 = tf.add_paragraph()
p2.text = "\nStatut : Résultats BLOQUÉS"
p2.font.size = Pt(11)
p2.font.bold = True
p2.font.color.rgb = RGBColor(180, 60, 60)

p3 = tf.add_paragraph()
p3.text = "\n• Pipeline SCADA à déboguer\n• FedProx à refactoriser\n• Cible : IEEE TII ou Renewable Energy"
p3.font.size = Pt(10)
p3.font.color.rgb = COLOR_TEXT

# SLR PRISMA
box2 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(6), Inches(2.5))
box2.fill.solid()
box2.fill.fore_color.rgb = RGBColor(240, 248, 255)
box2.line.color.rgb = COLOR_ACCENT

tf = box2.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "P1 — Revue systématique (SLR)"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE

p2 = tf.add_paragraph()
p2.text = "\nPRISMA : 3,000 → 1,700 → 361 → 181 articles"
p2.font.size = Pt(12)
p2.font.bold = True
p2.font.color.rgb = COLOR_ACCENT

p3 = tf.add_paragraph()
p3.text = "\n181 articles retenus pour synthèse\nMéthodologie PRISMA formalisée"
p3.font.size = Pt(10)
p3.font.color.rgb = COLOR_TEXT

# Enseignement
enseignement = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(4.2), Inches(12.3), Inches(1.8))
enseignement.fill.solid()
enseignement.fill.fore_color.rgb = RGBColor(250, 250, 250)
enseignement.line.color.rgb = COLOR_LIGHT_GRAY

tf = enseignement.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Activités d'enseignement (2025-2026)"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = COLOR_TITLE

p2 = tf.add_paragraph()
p2.text = "\n• Traitement du Signal — TD (Licence 1ère année, branche AI)"
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT

p3 = tf.add_paragraph()
p3.text = "• Machine Learning — TP (Licence 1ère année, branche PC)"
p3.font.size = Pt(11)
p3.font.color.rgb = COLOR_TEXT

p4 = tf.add_paragraph()
p4.text = "\nApport : compétences de communication et pédagogie pour les conférences"
p4.font.size = Pt(10)
p4.font.italic = True
p4.font.color.rgb = COLOR_TEXT

print("Slide 3: Avancement + Enseignement ✓")

# ============================================================
# SLIDE 4 : Évolution maintenance
# ============================================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide4)
add_section_num(slide4, "SECTION 01 — Contexte général", Inches(0.4))
add_title(slide4, "L'évolution de la maintenance industrielle", top=Inches(0.7))
add_horizontal_line(slide4, top=Inches(1.25))

maintenance_types = [
    ("1", "Corrective", "On répare après la panne", "Arrêts non planifiés, coûts élevés", RGBColor(200, 80, 80)),
    ("2", "Préventive", "Interventions à intervalles fixes", "Gaspillage, interventions inutiles", RGBColor(200, 160, 80)),
    ("3", "Prédictive", "Anticipation via les données", "Nécessite données et modèles IA", RGBColor(80, 160, 80)),
    ("4", "Prescriptive", "L'IA recommande l'action", "Niveau de maturité encore faible", RGBColor(80, 120, 160))
]

y_pos = Inches(1.5)
for num, name, principe, limite, color in maintenance_types:
    # Numéro cercle
    circle = slide4.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.6), y_pos + Inches(0.15), Inches(0.4), Inches(0.4))
    circle.fill.solid()
    circle.fill.fore_color.rgb = color
    circle.line.fill.background()
    
    c_tf = circle.text_frame
    p = c_tf.paragraphs[0]
    p.text = num
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Contenu
    box = slide4.shapes.add_textbox(Inches(1.2), y_pos, Inches(11.5), Inches(0.7))
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"{name} — {principe}"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = f"Limite : {limite}"
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(0.9)

# Stats
stats = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.2), Inches(12.3), Inches(1.2))
stats.fill.solid()
stats.fill.fore_color.rgb = COLOR_BOX_BG
stats.line.color.rgb = COLOR_LIGHT_GRAY

tf = stats.text_frame
p = tf.paragraphs[0]
p.text = "Impact : 70% des pannes sont précédées de signaux détectables | Marché mondial > $630 milliards d'ici 2028"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 4: Évolution maintenance ✓")

# ============================================================
# SLIDE 5 : Paradoxe des données
# ============================================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide5)
add_section_num(slide5, "SECTION 01 — Contexte général", Inches(0.4))
add_title(slide5, "Le problème fondamental : des données utiles mais inaccessibles", top=Inches(0.7))
add_horizontal_line(slide5, top=Inches(1.35))

obstacles = [
    ("Confidentialité", "Données de production stratégiquement sensibles — aucun opérateur ne partage avec ses concurrents"),
    ("Réglementations", "RGPD et réglementations sectorielles encadrent strictement les transferts de données"),
    ("Volume", "Parc d'éoliennes = dizaines de GO/jour — centralisation impraticable et coûteuse"),
    ("Hétérogénéité", "SCADA éolien ≠ données HVAC ≠ acoustique production — formats et patterns différents")
]

y_pos = Inches(1.6)
for title, desc in obstacles:
    # Numéro
    num = slide5.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.6), y_pos + Inches(0.1), Inches(0.5), Inches(0.5))
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
    box = slide5.shapes.add_textbox(Inches(1.3), y_pos, Inches(11.5), Inches(1))
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
q_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.9))
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

print("Slide 5: Paradoxe données ✓")

# Continue with more slides...
print("\n... Génération des slides 6-22 en cours ...")

# ============================================================
# SLIDE 6 : Positionnement
# ============================================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide6)
add_section_num(slide6, "SECTION 01 — Contexte général", Inches(0.4))
add_title(slide6, "Positionnement de la thèse", top=Inches(0.7))
add_horizontal_line(slide6, top=Inches(1.25))

# 3 piliers
props = [
    ("Federated Learning", "Entraînement collectif\nsans centralisation", Inches(0.8), Inches(2), RGBColor(230, 240, 250)),
    ("Foundation Models TS", "Modèles pré-entraînés\nzero-shot/few-shot", Inches(9), Inches(2), RGBColor(230, 250, 240)),
    ("Maintenance Prédictive", "Multi-domaine :\néolien, HVAC, manufacture", Inches(4.8), Inches(5), RGBColor(250, 240, 230))
]

for title, desc, x, y, color in props:
    box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.5), Inches(1.8))
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

# Centre intersection
center = slide6.shapes.add_shape(MSO_SHAPE.OVAL, Inches(4.8), Inches(3), Inches(3.5), Inches(1.6))
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

# Proposition
prop_box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6), Inches(12.3), Inches(1.2))
prop_box.fill.solid()
prop_box.fill.fore_color.rgb = RGBColor(250, 250, 250)
prop_box.line.color.rgb = COLOR_ACCENT

tf = prop_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Proposition centrale : un Foundation Model entraînable de façon fédérée sur des données industrielles hétérogènes, adaptable à plusieurs domaines sans que les données brutes ne quittent les sites locaux."
p.font.size = Pt(12)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 6: Positionnement ✓")

# ============================================================
# SLIDE 7 : Concepts FL
# ============================================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide7)
add_section_num(slide7, "SECTION 02 — Concepts de base", Inches(0.4))
add_title(slide7, "Federated Learning", top=Inches(0.7))
add_horizontal_line(slide7, top=Inches(1.25))

# Schéma
clients = [("Client 1\n(Données locales)", Inches(0.5), Inches(2)), ("Client 2\n(Données locales)", Inches(0.5), Inches(3.5)), ("Client 3\n(Données locales)", Inches(0.5), Inches(5))]
for label, x, y in clients:
    box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.5), Inches(1.2))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(230, 240, 250)
    box.line.color.rgb = COLOR_ACCENT
    
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.CENTER

# Flèches
for i in range(3):
    y_arrow = Inches(2.6) + i * Inches(1.5)
    arrow = slide7.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.2), y_arrow, Inches(1.2), Inches(0.4))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = COLOR_ACCENT

# Serveur
server = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(3), Inches(3), Inches(1.5))
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
p2.text = "\nAgrégation FedAvg / FedProx"
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(255, 255, 255)
p2.alignment = PP_ALIGN.CENTER

# Points clés
points = slide7.shapes.add_textbox(Inches(8.2), Inches(2), Inches(4.8), Inches(4.5))
tf = points.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Points clés"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE

bullet_points = ["Données restent locales", "Partage des mises à jour (poids/gradients)", "Agrégation périodique", "Robustesse non-IID (FedProx)", "Préservation confidentialité"]
for bp in bullet_points:
    p = tf.add_paragraph()
    p.text = "• " + bp
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

print("Slide 7: FL ✓")

# ============================================================
# SLIDE 8 : Foundation Models
# ============================================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide8)
add_section_num(slide8, "SECTION 02 — Concepts de base", Inches(0.4))
add_title(slide8, "Foundation Models pour séries temporelles", top=Inches(0.7))
add_horizontal_line(slide8, top=Inches(1.25))

models = [
    ("TimesFM", "2024", "100Mds points", "Prévision", "200M"),
    ("Moirai", "2024", "320M points", "Prév. + Anomalie", "32-480M"),
    ("MOMENT", "2024", "Time-Series Pile", "Prév. + Classif.", "385M"),
    ("Lag-Llama", "2023", "Features lagged", "Prévision", "~100M"),
    ("UniTime", "2023", "Domain prompts", "Prévision", "ND")
]

# Tableau
headers = ["Modèle", "Année", "Entraînement", "Tâches", "Params"]
x_positions = [Inches(0.5), Inches(2.3), Inches(4), Inches(6.5), Inches(9)]
col_widths = [Inches(1.7), Inches(1.6), Inches(2.4), Inches(2.4), Inches(1.5)]

for i, (header, x, w) in enumerate(zip(headers, x_positions, col_widths)):
    cell = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
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

for row_idx, model in enumerate(models):
    y = Inches(2.2) + row_idx * Inches(0.7)
    bg_color = RGBColor(245, 245, 245) if row_idx % 2 == 0 else RGBColor(250, 250, 250)
    
    for col_idx, (value, x, w) in enumerate(zip(model, x_positions, col_widths)):
        cell = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.65))
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
        cell.line.color.rgb = COLOR_LIGHT_GRAY
        
        tf = cell.text_frame
        p = tf.paragraphs[0]
        p.text = value
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT
        p.alignment = PP_ALIGN.CENTER

# Insight
y_pos = Inches(5.8)
insight = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(0.8))
insight.fill.solid()
insight.fill.fore_color.rgb = RGBColor(240, 248, 255)
insight.line.color.rgb = COLOR_ACCENT

tf = insight.text_frame
p = tf.paragraphs[0]
p.text = "Capacité zero-shot / few-shot — un modèle unique pour nombreux équipements industriels"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_ACCENT
p.alignment = PP_ALIGN.CENTER

print("Slide 8: Foundation Models ✓")

# ============================================================
# SLIDE 9 : Maintenance prédictive
# ============================================================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide9)
add_section_num(slide9, "SECTION 02 — Concepts de base", Inches(0.4))
add_title(slide9, "Maintenance prédictive", top=Inches(0.7))
add_horizontal_line(slide9, top=Inches(1.25))

tasks = [
    ("Détection d'anomalies", "Identifier un comportement anormal dans les signaux"),
    ("Classification de défaillances", "Reconnaître le type de panne (tâche principale)"),
    ("Estimation RUL", "Prédire la durée de vie résiduelle avant panne"),
    ("Prévision état de santé", "Suivre l'évolution globale de l'équipement")
]

y_pos = Inches(1.6)
for title, desc in tasks:
    box = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(0.95))
    is_main = "Classification" in title
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    box.line.color.rgb = COLOR_ACCENT if is_main else COLOR_LIGHT_GRAY
    box.line.width = Pt(3) if is_main else Pt(1)
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title + (" ★" if is_main else "")
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_ACCENT if is_main else COLOR_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.1)

# Difficultés
bottom = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.8), Inches(12.3), Inches(1.3))
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

issues = "Multivariées • Non-stationnaires • Classes déséquilibrées • Bruit de capteurs • Fréquences hétérogènes"
p2 = tf.add_paragraph()
p2.text = issues
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT

print("Slide 9: Maintenance ✓")

# ============================================================
# SLIDE 10 : Cartographie maturité
# ============================================================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide10)
add_section_num(slide10, "SECTION 03 — État de l'art", Inches(0.4))
add_title(slide10, "Cartographie du domaine de recherche", top=Inches(0.7))
add_horizontal_line(slide10, top=Inches(1.25))

domains = [
    ("FL général", "FedAvg/FedProx, privacy", "Mature", "1000+", RGBColor(200, 220, 240)),
    ("TS FMs centr.", "TimesFM, Moirai, MOMENT", "Émergent", "~8 mod.", RGBColor(240, 230, 200)),
    ("FL NLP/Vision", "LoRA fédéré, adapters", "Émergent", "~50 trav.", RGBColor(240, 230, 200)),
    ("FL maintenance", "Pruckovskaja, OASEES", "Initial", "~10 trav.", RGBColor(240, 210, 200)),
    ("FL + TS FMs", "Time-FFM, Ali, FedForecaster", "Quasi vide", "3 travaux", RGBColor(240, 180, 180)),
    ("FL + TS FMs + Maint.", "———", "VIERGE", "0", RGBColor(220, 150, 150))
]

headers = ["Domaine", "Description", "Maturité", "Nb. travaux"]
x_pos = [Inches(0.5), Inches(3), Inches(8.2), Inches(10.5)]
widths = [Inches(2.4), Inches(5), Inches(2), Inches(2)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
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

for idx, (domain, desc, maturity, count, color) in enumerate(domains):
    y = Inches(2.2) + idx * Inches(0.75)
    
    data = [domain, desc, maturity, count]
    for value, x, w in zip(data, x_pos, widths):
        cell = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.7))
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

print("Slide 10: Cartographie ✓")

# ============================================================
# SLIDE 11 : Limitations TS FMs
# ============================================================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide11)
add_section_num(slide11, "SECTION 03 — État de l'art", Inches(0.4))
add_title(slide11, "Limitations des TS FMs pour l'industrie", top=Inches(0.7))
add_horizontal_line(slide11, top=Inches(1.25))

limitations = [
    ("01", "Distribution des données", "Pré-entraînement sur données publiques (météo, finance), pas industrielles"),
    ("02", "Support multivarié limité", "Conçus pour univariés, industrie = 100+ capteurs"),
    ("03", "Absence évaluation maintenance", "Pas de classification défaillances industrielle"),
    ("04", "Non-conception FL", "Pas de propriétés federation-friendly")
]

y_pos = Inches(1.6)
for num, title, desc in limitations:
    # Numéro
    num_box = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(0.8), Inches(0.8))
    num_box.fill.solid()
    num_box.fill.fore_color.rgb = COLOR_ACCENT
    num_box.line.fill.background()
    
    n_tf = num_box.text_frame
    p = n_tf.paragraphs[0]
    p.text = num
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Contenu
    box = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), y_pos, Inches(11.3), Inches(0.8))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    box.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(1.0)

# Gap performance
gap = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.7), Inches(12.3), Inches(1))
gap.fill.solid()
gap.fill.fore_color.rgb = COLOR_TITLE
gap.line.fill.background()

tf = gap.text_frame
p = tf.paragraphs[0]
p.text = "Écart de performance estimé : 25-50% de perte sans fine-tuning sur données industrielles"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

print("Slide 11: Limitations ✓")

# ============================================================
# SLIDE 12 : 3 travaux existants
# ============================================================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide12)
add_section_num(slide12, "SECTION 03 — État de l'art", Inches(0.4))
add_title(slide12, "Les 3 travaux FL + TS FMs existants", top=Inches(0.7))
add_horizontal_line(slide12, top=Inches(1.25))

works = [
    ("Time-FFM (Liu 2024)", "NeurIPS", "FM fédéré natif, LLM reprogrammé", "Générique", "Pas de maintenance, pas de LoRA"),
    ("Ali et al. (2025)", "arXiv", "Fine-tuning fédéré Chronos/TimesFM", "Médical ECG", "FedAvg standard, pas solution non-IID"),
    ("FedForecaster (Maher 2025)", "EDBT", "AutoML fédéré, méta-modèle", "Générique", "Pas un vrai FM, pas cross-domaine")
]

# Headers
headers = ["Travail", "Venue", "Approche", "Domaine", "Limite clé"]
x_pos = [Inches(0.5), Inches(2.8), Inches(4.3), Inches(7), Inches(9)]
widths = [Inches(2.2), Inches(1.4), Inches(2.6), Inches(1.9), Inches(3.2)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_ACCENT
    cell.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = cell.text_frame
    p = tf.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

for idx, (work, venue, approach, domain, limit) in enumerate(works):
    y = Inches(2.2) + idx * Inches(0.9)
    bg_color = RGBColor(250, 250, 250) if idx % 2 == 0 else RGBColor(245, 245, 245)
    
    data = [work, venue, approach, domain, limit]
    for value, x, w in zip(data, x_pos, widths):
        cell = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.85))
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
        cell.line.color.rgb = COLOR_LIGHT_GRAY
        
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = value
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT

# Conclusion
conc = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.5), Inches(12.3), Inches(0.9))
conc.fill.solid()
conc.fill.fore_color.rgb = RGBColor(255, 240, 240)
conc.line.color.rgb = RGBColor(180, 60, 60)
conc.line.width = Pt(2)

tf = conc.text_frame
p = tf.paragraphs[0]
p.text = "Conclusion : Aucun travail ne combine FL + TS FM + Maintenance industrielle"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(180, 60, 60)
p.alignment = PP_ALIGN.CENTER

print("Slide 12: 3 travaux ✓")

# ============================================================
# SLIDE 13 : PEFT strategies
# ============================================================
slide13 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide13)
add_section_num(slide13, "SECTION 03 — État de l'art", Inches(0.4))
add_title(slide13, "Stratégies PEFT fédérées (inspiration NLP/Vision)", top=Inches(0.7))
add_horizontal_line(slide13, top=Inches(1.25))

methods = [
    ("FedCLIP", "Wang 2023", "Adapters sur backbone gelé", "283× vitesse"),
    ("FedOPAL", "Tupper 2025", "Dual LoRA global + personnel", "Personnalisation"),
    ("FDLoRA", "Qi 2024", "Fusion adaptative post-agrégation", "Meilleure perf."),
    ("HeLoRA", "Fan 2025", "Rangs LoRA hétérogènes", "Flexibilité"),
    ("FedQLoRA", "Hu 2025", "Quantization-aware", "Robustesse")
]

headers = ["Méthode", "Année", "Approche", "Gain"]
x_pos = [Inches(0.5), Inches(2.5), Inches(4), Inches(8.5)]
widths = [Inches(1.9), Inches(1.4), Inches(4.4), Inches(2.9)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide13.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
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

for idx, (method, year, approach, gain) in enumerate(methods):
    y = Inches(2.2) + idx * Inches(0.75)
    bg_color = RGBColor(245, 245, 245) if idx % 2 == 0 else RGBColor(250, 250, 250)
    
    data = [method, year, approach, gain]
    for value, x, w in zip(data, x_pos, widths):
        cell = slide13.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.7))
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
        cell.line.color.rgb = COLOR_LIGHT_GRAY
        
        tf = cell.text_frame
        p = tf.paragraphs[0]
        p.text = value
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT

# Insight
insight = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.2), Inches(12.3), Inches(0.9))
insight.fill.solid()
insight.fill.fore_color.rgb = RGBColor(240, 248, 255)
insight.line.color.rgb = COLOR_ACCENT

tf = insight.text_frame
p = tf.paragraphs[0]
p.text = "Techniques PEFT (LoRA, adapters) transférables aux séries temporelles — première combinaison recherchée"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_ACCENT
p.alignment = PP_ALIGN.CENTER

print("Slide 13: PEFT strategies ✓")

# ============================================================
# SLIDE 14 : 4 problématiques
# ============================================================
slide14 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide14)
add_section_num(slide14, "SECTION 04 — Problématiques", Inches(0.4))
add_title(slide14, "Les quatre problématiques identifiées", top=Inches(0.7))
add_horizontal_line(slide14, top=Inches(1.25))

problems = [
    ("P1", "RQ1", "Personnalisation fédérée sur données hétérogènes", RGBColor(240, 200, 200)),
    ("P2", "RQ2", "Absence de benchmark fédéré standardisé", RGBColor(240, 220, 200)),
    ("P3", "RQ3", "Incompatibilité architecturale TS FMs avec FL", RGBColor(200, 220, 240)),
    ("P4", "RQ4", "Inadéquation aux données industrielles réelles", RGBColor(220, 240, 220))
]

y_pos = Inches(1.5)
for prob, rq, desc, color in problems:
    box = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(1.1))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.color.rgb = COLOR_ACCENT
    box.line.width = Pt(2)
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"{prob} ({rq}) — {desc}"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_TITLE
    
    y_pos += Inches(1.25)

print("Slide 14: 4 problématiques ✓")

# ============================================================
# SLIDE 15 : Synthèse gaps
# ============================================================
slide15 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide15)
add_section_num(slide15, "SECTION 04 — Problématiques", Inches(0.4))
add_title(slide15, "Synthèse : carte des gaps", top=Inches(0.7))
add_horizontal_line(slide15, top=Inches(1.25))

gaps = [
    ("Entraînement fédéré de TS FMs", "Critique", RGBColor(211, 47, 47)),
    ("TS FMs pour maintenance", "Critique", RGBColor(211, 47, 47)),
    ("TS FMs sur non-IID hétérogène", "Critique", RGBColor(211, 47, 47)),
    ("PEFT (LoRA/adapters) pour TS FMs", "Critique", RGBColor(211, 47, 47)),
    ("Généralisation cross-domaine fédérée", "Majeur", RGBColor(245, 124, 0)),
    ("Benchmark fédéré multi-domaine", "Majeur", RGBColor(245, 124, 0)),
    ("Privacy (DP + FL + TS FMs)", "Modéré", RGBColor(56, 142, 60))
]

headers = ["Gap identifié", "Sévérité"]
x_pos = [Inches(0.5), Inches(10)]
widths = [Inches(9.3), Inches(3)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
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

for idx, (gap, severity, color) in enumerate(gaps):
    y = Inches(2.2) + idx * Inches(0.65)
    
    # Gap name
    cell1 = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), y, Inches(9.3), Inches(0.6))
    cell1.fill.solid()
    cell1.fill.fore_color.rgb = RGBColor(250, 250, 250)
    cell1.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = cell1.text_frame
    p = tf.paragraphs[0]
    p.text = gap
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT
    
    # Severity badge
    cell2 = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.3), y + Inches(0.1), Inches(2.4), Inches(0.4))
    cell2.fill.solid()
    cell2.fill.fore_color.rgb = color
    cell2.line.fill.background()
    
    tf = cell2.text_frame
    p = tf.paragraphs[0]
    p.text = severity
    p.font.bold = True
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

print("Slide 15: Carte des gaps ✓")

# ============================================================
# SLIDE 16 : Contributions C1-C4
# ============================================================
slide16 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide16)
add_section_num(slide16, "SECTION 05 — Contributions", Inches(0.4))
add_title(slide16, "Contributions envisagées (C1-C4)", top=Inches(0.7))
add_horizontal_line(slide16, top=Inches(1.25))

contribs = [
    ("C1", "FedPEFT-TS", "Personnalisation fédérée (LoRA + prompts)", "RQ1", "An 1-2", RGBColor(230, 240, 250)),
    ("C2", "FedTS-Bench", "Benchmark fédéré maintenance", "RQ2", "An 1-2", RGBColor(240, 250, 245)),
    ("C3", "FedTSFM-Arch", "Architecture TS FM native FL", "RQ3", "An 2-3", RGBColor(255, 248, 225)),
    ("C4", "IndusFedFM", "Validation industrielle multi-domaines", "RQ4", "An 3", RGBColor(255, 235, 238))
]

headers = ["ID", "Contribution", "Description", "RQ", "Période"]
x_pos = [Inches(0.5), Inches(1.3), Inches(4.2), Inches(9.5), Inches(10.8)]
widths = [Inches(0.7), Inches(2.8), Inches(5.1), Inches(1), Inches(1.7)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
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

for idx, (cid, name, desc, rq, period, color) in enumerate(contribs):
    y = Inches(2.2) + idx * Inches(0.85)
    
    data = [cid, name, desc, rq, period]
    for value, x, w in zip(data, x_pos, widths):
        cell = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.8))
        cell.fill.solid()
        cell.fill.fore_color.rgb = color
        cell.line.color.rgb = COLOR_LIGHT_GRAY
        
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = value
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT
        if value in ["C1", "C2", "C3", "C4"]:
            p.font.bold = True

# Timeline
y_pos = Inches(6)
timeline = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(0.9))
timeline.fill.solid()
timeline.fill.fore_color.rgb = RGBColor(245, 245, 245)
timeline.line.color.rgb = COLOR_LIGHT_GRAY

tf = timeline.text_frame
p = tf.paragraphs[0]
p.text = "Fil conducteur : TS FM existant → Personnalisable FL (C1) → Benchmark (C2) → Architecture optimisée (C3) → Validation industrielle (C4)"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 16: Contributions C1-C4 ✓")

# ============================================================
# SLIDE 17 : C1 FedPEFT-TS
# ============================================================
slide17 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide17)
add_section_num(slide17, "SECTION 05 — C1 FedPEFT-TS", Inches(0.4))
add_title(slide17, "C1 : Personnalisation fédérée", top=Inches(0.7))
add_horizontal_line(slide17, top=Inches(1.25))

# Principe
principle = slide17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.5))
principle.fill.solid()
principle.fill.fore_color.rgb = RGBColor(240, 248, 255)
principle.line.color.rgb = COLOR_ACCENT

tf = principle.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Problème : RQ1 — Personnaliser un TS FM global pour clients hétérogènes"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = COLOR_TITLE

principles = [
    "• Partir d'un TS FM existant (Moirai ou TimesFM), geler le backbone",
    "• Attacher modules LoRA sur couches d'attention temporelle",
    "• Chaque client : LoRA personnel (local) + LoRA global (agrégé)",
    "• Prompts domaine-spécifiques (inspiration UniTime, Time-FFM)"
]

for pr in principles:
    p = tf.add_paragraph()
    p.text = pr
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT

# Détail
y_pos = Inches(3.2)
details = [
    ("Approche", "Federated Prompt Tuning + LoRA avec agrégation FedAvg"),
    ("Personnalisation", "LoRA spécifiques par client + prompts learnable"),
    ("Communication", "Transfert des matrices LoRA uniquement (très faible volume)")
]

for label, value in details:
    row = slide17.shapes.add_textbox(Inches(0.5), y_pos, Inches(12.3), Inches(0.5))
    tf = row.text_frame
    
    p = tf.paragraphs[0]
    p.text = f"{label} : {value}"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(0.5)

# Innovation
innov = slide17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.3), Inches(12.3), Inches(0.9))
innov.fill.solid()
innov.fill.fore_color.rgb = COLOR_TITLE
innov.line.fill.background()

tf = innov.text_frame
p = tf.paragraphs[0]
p.text = "✨ Première combinaison LoRA + prompts domaine + FL pour séries temporelles"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

print("Slide 17: C1 FedPEFT-TS ✓")

# ============================================================
# SLIDE 18 : C2 FedTS-Bench
# ============================================================
slide18 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide18)
add_section_num(slide18, "SECTION 05 — C2 FedTS-Bench", Inches(0.4))
add_title(slide18, "C2 : Benchmark fédéré", top=Inches(0.7))
add_horizontal_line(slide18, top=Inches(1.25))

# Principe
principle = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.2))
principle.fill.solid()
principle.fill.fore_color.rgb = RGBColor(255, 250, 240)
principle.line.color.rgb = RGBColor(180, 120, 50)

tf = principle.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Problème : RQ2 — Absence totale de benchmark standardisé"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(150, 100, 40)

p2 = tf.add_paragraph()
p2.text = "Datasets : NASA C-MAPSS (turbofan), CWRU (roulements), FEMTO-ST, SCADA éoliennes"
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT

# Datasets
y_pos = Inches(2.9)
datasets = [
    ("NASA C-MAPSS", "Turbofan"),
    ("CWRU", "Roulements"),
    ("FEMTO-ST", "Dégradation"),
    ("SCADA Éoliennes", "EDP Renewables")
]

x_start = Inches(0.5)
for name, dtype in datasets:
    box = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_start, y_pos, Inches(2.9), Inches(0.9))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(250, 250, 250)
    box.line.color.rgb = COLOR_LIGHT_GRAY
    
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = name
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TITLE
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = dtype
    p2.font.size = Pt(9)
    p2.font.color.rgb = COLOR_TEXT
    p2.alignment = PP_ALIGN.CENTER
    
    x_start += Inches(3.1)

# Métriques
y_pos = Inches(4.1)
metrics_title = slide18.shapes.add_textbox(Inches(0.5), y_pos, Inches(3), Inches(0.4))
tf = metrics_title.text_frame
p = tf.paragraphs[0]
p.text = "Métriques adaptées :"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = COLOR_TITLE

metrics = [
    ("F1 pondéré", "Équilibre classes déséquilibrées"),
    ("AUC-PR", "Précision-Rappel area under curve"),
    ("Variance dérive", "Stabilité inter-clients"),
    ("Rounds convergence", "Efficacité communication")
]

y_pos = Inches(4.6)
for metric, desc in metrics:
    row = slide18.shapes.add_textbox(Inches(0.5), y_pos, Inches(12), Inches(0.4))
    tf = row.text_frame
    
    p = tf.paragraphs[0]
    p.text = f"• {metric} : {desc}"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT
    
    y_pos += Inches(0.35)

# Livrable
livrable = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.7))
livrable.fill.solid()
livrable.fill.fore_color.rgb = RGBColor(240, 248, 255)
livrable.line.color.rgb = COLOR_ACCENT

tf = livrable.text_frame
p = tf.paragraphs[0]
p.text = "Livrable : Splits de datasets + code d'évaluation open-source — première ressource communautaire"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_ACCENT
p.alignment = PP_ALIGN.CENTER

print("Slide 18: C2 FedTS-Bench ✓")

# ============================================================
# SLIDE 19 : C3 + C4
# ============================================================
slide19 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide19)
add_section_num(slide19, "SECTION 05 — C3 + C4", Inches(0.4))
add_title(slide19, "Architecture native FL + Validation industrielle", top=Inches(0.7))
add_horizontal_line(slide19, top=Inches(1.25))

# C3
c3_box = slide19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(6), Inches(3.3))
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

p2 = tf.add_paragraph()
p2.text = "\nArchitecture TS FM native FL"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TITLE

props_c3 = [
    ("Patching hiérarchique", "Découpage adaptatif selon fréquence locale"),
    ("MoE sparse client-guidé", "Experts activés par domaine client"),
    ("Mises à jour low-rank", "LoRA sur query/key uniquement (×50 réduction)")
]

for title, desc in props_c3:
    p = tf.add_paragraph()
    p.text = f"• {title} : {desc}"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT

# C4
c4_box = slide19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(6), Inches(3.3))
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

p2 = tf.add_paragraph()
p2.text = "\nValidation industrielle multi-domaines"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TITLE

scenarios = [
    "Intra-domaine : N clients éoliens hétérogènes",
    "Cross-domaine : Éolien + HVAC + Manufacture",
    "Cold-start : Nouveau client sans historique (zero-shot)"
]

for scen in scenarios:
    p = tf.add_paragraph()
    p.text = f"→ {scen}"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT

# Vision
vision = slide19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.1), Inches(12.3), Inches(1.7))
vision.fill.solid()
vision.fill.fore_color.rgb = COLOR_TITLE
vision.line.fill.background()

tf = vision.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "🎯 Vision d'ensemble — FedTSFM"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\nC1 (méthode) + C2 (benchmark) + C3 (architecture) + C4 (validation)"
p2.font.size = Pt(12)
p2.font.color.rgb = RGBColor(220, 220, 220)
p2.alignment = PP_ALIGN.CENTER

p3 = tf.add_paragraph()
p3.text = "\nUn Foundation Model de Séries Temporelles entraînable de façon fédérée"
p3.font.size = Pt(11)
p3.font.italic = True
p3.font.color.rgb = RGBColor(255, 255, 255)
p3.alignment = PP_ALIGN.CENTER

print("Slide 19: C3 + C4 ✓")

# ============================================================
# SLIDE 20 : Plan de publication
# ============================================================
slide20 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide20)
add_section_num(slide20, "SECTION 06 — Publications", Inches(0.4))
add_title(slide20, "Plan de publication : 5 publications sur 3 ans", top=Inches(0.7))
add_horizontal_line(slide20, top=Inches(1.25))

pubs = [
    ("P0", "Data-Centric FL for Wind Turbine PdM", "Master → Journal", "2025", RGBColor(230, 240, 250)),
    ("P1", "Literature Review FL+TS FMs for Ind. Maint.", "SLR, Journal", "An 1-2", RGBColor(240, 250, 245)),
    ("P2", "FedTS-Bench: A Federated Benchmark", "Conférence", "An 2", RGBColor(250, 245, 240)),
    ("P3", "FedTSFM-Arch: Architecture native FL", "Journal Q1", "An 2-3", RGBColor(255, 240, 245)),
    ("P4", "IndusFedFM: Multi-Domain Validation", "Journal Q1", "An 3", RGBColor(255, 245, 240))
]

headers = ["#", "Titre", "Type", "Année"]
x_pos = [Inches(0.5), Inches(1.3), Inches(10), Inches(11.5)]
widths = [Inches(0.7), Inches(8.5), Inches(1.6), Inches(1.3)]

for h, x, w in zip(headers, x_pos, widths):
    cell = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.6), w, Inches(0.5))
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

for idx, (num, title, type_pub, year, color) in enumerate(pubs):
    y = Inches(2.2) + idx * Inches(0.8)
    
    data = [num, title, type_pub, year]
    for value, x, w in zip(data, x_pos, widths):
        cell = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.75))
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

# Fil narratif
y_pos = Inches(6.4)
narrative = slide20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(0.8))
narrative.fill.solid()
narrative.fill.fore_color.rgb = RGBColor(245, 245, 245)
narrative.line.color.rgb = COLOR_LIGHT_GRAY

tf = narrative.text_frame
p = tf.paragraphs[0]
p.text = "Fil narratif : Master → SLR (identifier gaps) → Benchmark (verrou expérimental) → Architecture (verrou archi) → Validation industrielle"
p.font.size = Pt(10)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

print("Slide 20: Plan publication ✓")

# ============================================================
# SLIDE 21 : Journaux et conférences ciblés
# ============================================================
slide21 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide21)
add_section_num(slide21, "SECTION 06 — Stratégie de publication", Inches(0.4))
add_title(slide21, "Conférences et journaux ciblés", top=Inches(0.7))
add_horizontal_line(slide21, top=Inches(1.25))

# Conférences (gauche)
conf_box = slide21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(6), Inches(3.2))
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
journal_box = slide21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(6), Inches(3.2))
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
    "Neurocomputing — Q1, 28% acc., ~63 jours",
    "IEEE Trans. Industrial Electronics — Q1, 28%",
    "Machine Learning (Springer) — Q1, gratuit",
    "JMLR — Diamond OA, Q1",
    "Pattern Recognition Letters — Q2, rapide"
]

for j in journals:
    p = tf.add_paragraph()
    p.text = "• " + j
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT

# Stratégie matching
y_pos = Inches(4.9)
match = slide21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y_pos, Inches(12.3), Inches(1.6))
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
    "P0 (Master) → IEEE TII / Renewable Energy",
    "P1 (SLR) → Machine Learning / JMLR / Neurocomputing",
    "P2 (Benchmark) → Pattern Recognition Letters / KDD",
    "P3 (Architecture) → Neurocomputing / JMLR",
    "P4 (Industriel) → IEEE Trans. Industrial Electronics"
]

for m in matches:
    p = tf.add_paragraph()
    p.text = "• " + m
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT

print("Slide 21: Cibles publication ✓")

# ============================================================
# SLIDE 22 : Conclusion
# ============================================================
slide22 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide22)

accent = slide22.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.05))
accent.fill.solid()
accent.fill.fore_color.rgb = COLOR_TITLE
accent.line.fill.background()

# Titre merci
thanks = slide22.shapes.add_textbox(Inches(0), Inches(2), Inches(13.333), Inches(1))
tf = thanks.text_frame
p = tf.paragraphs[0]
p.text = "Merci"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

subtitle = slide22.shapes.add_textbox(Inches(0), Inches(3.2), Inches(13.333), Inches(0.5))
tf = subtitle.text_frame
p = tf.paragraphs[0]
p.text = "Questions et suggestions"
p.font.size = Pt(18)
p.font.color.rgb = COLOR_TEXT
p.alignment = PP_ALIGN.CENTER

# Contact
contact = slide22.shapes.add_textbox(Inches(0), Inches(4.2), Inches(13.333), Inches(1.5))
tf = contact.text_frame
p = tf.paragraphs[0]
p.text = "Yassire AMMOURI"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "\nPr. Younes Karfa Bakali, Mme Rajaa SAIDI"
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

# Université
univ = slide22.shapes.add_textbox(Inches(0), Inches(6), Inches(13.333), Inches(0.8))
tf = univ.text_frame
p = tf.paragraphs[0]
p.text = "Université Mohammed V, Faculté des Sciences de Rabat"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "LRIT - Laboratoire de Recherche en Informatique et Télécommunications"
p2.font.size = Pt(10)
p2.font.color.rgb = COLOR_TEXT
p2.alignment = PP_ALIGN.CENTER

footer = slide22.shapes.add_textbox(Inches(0), Inches(6.9), Inches(13.333), Inches(0.4))
tf = footer.text_frame
p = tf.paragraphs[0]
p.text = "Rapport d'avancement de thèse — Mars 2026"
p.font.size = Pt(9)
p.font.color.rgb = RGBColor(153, 153, 153)
p.alignment = PP_ALIGN.CENTER

print("Slide 22: Conclusion ✓")

# ============================================================
# SAUVEGARDE
# ============================================================
output_path = "presentation_rapport_AVANCEE_mars2026.pptx"
prs.save(output_path)
print(f"\n{'='*60}")
print(f"Présentation mise à jour générée avec succès !")
print(f"Fichier : {output_path}")
print(f"Nombre de slides : {len(prs.slides)}")
print(f"{'='*60}")
