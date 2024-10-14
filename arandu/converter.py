# arandu/converter.py
import subprocess
import os

def convert_pdf_to_epub(pdf_file, output_dir):
    # Replace .pdf extension with .epub
    epub_filename = os.path.splitext(os.path.basename(pdf_file))[0] + ".epub"
    epub_path = os.path.join(output_dir, epub_filename)
    
    try:
        # Run the Calibre command to convert the PDF to EPUB
        subprocess.run(['ebook-convert', pdf_file, epub_path], check=True)
        return epub_path
    except Exception as e:
        print(f"Conversion failed: {e}")
        return None

def validate_epub(epub_file):
    # Simple check to see if the EPUB file exists and is valid
    return os.path.exists(epub_file) and epub_file.endswith('.epub')
