# arandu/converter.py
import os
import subprocess

# Function to convert PDF to EPUB
def convert_pdf_to_epub(pdf_file, output_dir):
    epub_filename = os.path.splitext(os.path.basename(pdf_file))[0] + ".epub"
    epub_path = os.path.join(output_dir, epub_filename)
    
    try:
        # Run the Calibre command to convert the PDF to EPUB
        subprocess.run(['ebook-convert', pdf_file, epub_path], check=True)
        return epub_path  # Return the path of the converted file
    except Exception as e:
        print(f"Conversion failed: {e}")
        return None

# Function to validate whether an EPUB file is valid
def validate_epub(epub_file):
    return os.path.exists(epub_file) and epub_file.endswith(".epub")

# Function to ensure the library folder exists
def ensure_library_folder(library_path):
    if not os.path.exists(library_path):
        os.makedirs(library_path)
