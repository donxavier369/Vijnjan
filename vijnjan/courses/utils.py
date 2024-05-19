import os
import subprocess
from django.core.files.base import ContentFile
import tempfile


def convert_ppt_to_pdf(ppt_file):
    # Save the PPT file to a temporary location
    temp_ppt_file = tempfile.NamedTemporaryFile(delete=False)
    for chunk in ppt_file.chunks():
        temp_ppt_file.write(chunk)
    temp_ppt_file.close()

    # Convert PPT to PDF using LibreOffice
    temp_pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', temp_ppt_file.name, '--outdir', os.path.dirname(temp_pdf_file.name)])

    # Read the converted PDF file
    with open(temp_pdf_file.name, 'rb') as f:
        pdf_content = f.read()

    # Create a Django ContentFile from the PDF content
    pdf_file = ContentFile(pdf_content, name=os.path.basename(temp_pdf_file.name))

    # Clean up temporary files
    os.remove(temp_ppt_file.name)
    os.remove(temp_pdf_file.name)

    return pdf_file