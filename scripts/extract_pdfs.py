import fitz 
import os
import json

pdf_dir = "../data/pdfs"
output = []

for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith(".pdf"):
        doc = fitz.open(os.path.join(pdf_dir, pdf_file))
        text = "\n".join([page.get_text() for page in doc])
        output.append({
            "source": pdf_file,
            "content": text
        })

with open("../data/insurance_pdfs.json", "w") as f:
    json.dump(output, f, indent=2)
