import pdfplumber
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Find the PDF file
folder = r'C:\Users\Chou\Desktop\recherche-fuite-gironde'
files = os.listdir(folder)
pdf_files = [f for f in files if f.lower().endswith('.pdf')]

for pdf_name in pdf_files:
    pdf_path = os.path.join(folder, pdf_name)
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"\n=== PAGE {i+1} ===")
            t = page.extract_text()
            if t:
                print(t)
