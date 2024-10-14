# arandu/library.py
import os
from PyQt5.QtWidgets import QListWidgetItem

# Load EPUB files from the library directory
def load_library_books(library_widget, library_path):
    # Ensure the library folder exists
    if not os.path.exists(library_path):
        os.makedirs(library_path)

    # Clear the widget before loading
    library_widget.clear()

    # Add EPUB files to the QListWidget
    for file_name in os.listdir(library_path):
        if file_name.endswith(".epub"):
            item = QListWidgetItem(file_name)
            library_widget.addItem(item)
