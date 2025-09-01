from fpdf import FPDF

from pdf2image import convert_from_path

import os
# Input/Output folders
input_dir = "O"
output_dir = "OO"
os.makedirs(output_dir, exist_ok=True)
# Loop over all PDF files in the folder
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        Testimages = convert_from_path(pdf_path, dpi=200)

    for i, page in enumerate(Testimages):
        output_file = os.path.join(output_dir, f"{filename.replace('.pdf','')}_page{i+1}.jpg")
        page.convert("RGB").save(output_file, "JPEG")
        print(f"✅ Converted: {filename} → {output_file}")