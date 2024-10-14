# arandu/converter.py
import os
import subprocess

# Full path to the Calibre ebook-convert executable
calibre_path = r"C:\Program Files\Calibre2\ebook-convert.exe"

# Function to convert PDF to EPUB
def convert_pdf_to_epub(pdf_file, output_dir):
    epub_filename = os.path.splitext(os.path.basename(pdf_file))[0] + ".epub"
    epub_path = os.path.join(output_dir, epub_filename)

    try:
        # Print debug information about paths and command
        print(f"Converting PDF to EPUB...")
        print(f"PDF Path: {pdf_file}")
        print(f"EPUB Path: {epub_path}")
        print(f"Calibre Path: {calibre_path}")

        # Run the Calibre ebook-convert command with full path
        result = subprocess.run(
            [calibre_path, pdf_file, epub_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Check for any errors in stdout/stderr
        if result.stderr:
            print(f"Calibre Error: {result.stderr.decode()}")
        else:
            print(f"Conversion successful: {epub_path}")
        return epub_path  # Return the path of the converted file

    except Exception as e:
        print(f"Conversion failed: {e}")
        return None

# Function to validate whether an EPUB file is valid
def validate_epub(epub_file):
    # Validate that the file exists and has the .epub extension
    if os.path.exists(epub_file) and epub_file.endswith(".epub"):
        print(f"Valid EPUB file: {epub_file}")
        return True
    else:
        print(f"Invalid EPUB file: {epub_file}")
        return False

# Function to ensure the library folder exists
def ensure_library_folder(library_path):
    if not os.path.exists(library_path):
        os.makedirs(library_path)
        print(f"Library folder created: {library_path}")
    else:
        print(f"Library folder already exists: {library_path}")
