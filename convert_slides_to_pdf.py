#!/usr/bin/env python3
"""Convert HTML slides to a single PDF presentation using WeasyPrint."""
import os
import sys
import subprocess

slides_dir = "/mnt/c/Users/DEll/Desktop/Master IT/S4/PFE/Articals/My Artical/phd_presentation/slides"
output_path = "/mnt/c/Users/DEll/Desktop/Master IT/S4/PFE/Articals/My Artical/phd_presentation/presentation_avancement_these_updated.pdf"
temp_dir = "/tmp/slides_pdf"

os.makedirs(temp_dir, exist_ok=True)

# Get sorted slide files
slide_files = sorted(
    [f for f in os.listdir(slides_dir) if f.endswith('.html')],
    key=lambda x: int(x.replace('slide', '').replace('.html', ''))
)

print(f"Found {len(slide_files)} slides")

# Convert each slide to individual PDF
pdf_files = []
for slide_file in slide_files:
    slide_num = slide_file.replace('slide', '').replace('.html', '')
    pdf_file = os.path.join(temp_dir, f"slide_{slide_num}.pdf")
    slide_path = os.path.join(slides_dir, slide_file)
    print(f"  Converting {slide_file} -> slide_{slide_num}.pdf")
    
    from weasyprint import HTML
    doc = HTML(filename=slide_path)
    doc.write_pdf(pdf_file)
    pdf_files.append(pdf_file)

# Merge all PDFs using pdfunite (from poppler-utils) or pdftk
print(f"\nMerging {len(pdf_files)} PDF pages...")

# Try pdfunite first
try:
    subprocess.run(['pdfunite'] + pdf_files + [output_path], check=True)
    print(f"✅ PDF saved to: {output_path}")
except (subprocess.CalledProcessError, FileNotFoundError):
    # Fallback: use Python to merge
    print("pdfunite not found, using PyPDF2...")
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    merger.write(output_path)
    merger.close()
    print(f"✅ PDF saved to: {output_path}")
