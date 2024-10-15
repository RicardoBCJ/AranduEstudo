import os
import json
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QProgressBar, QWidget, QGridLayout
from PyQt5.QtCore import Qt  # Import Qt for alignment

# Path to store reading progress
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), 'progress.json')

# Load or initialize the progress data
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save the progress data
def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(progress, file)

# Load the book cover and metadata (dummy function for now)
def load_book_cover(book_path):
    # Placeholder for actual EPUB cover loading
    return QPixmap('assets/icons/book_placeholder.png')  # Replace with actual cover extraction

# Load books into the grid layout
def load_library_grid(grid_layout, library_path):
    progress_data = load_progress()  # Load reading progress data
    books = [f for f in os.listdir(library_path) if f.endswith('.epub')]

    row, col = 0, 0
    for book in books:
        book_path = os.path.join(library_path, book)
        book_cover = load_book_cover(book_path)

        # Create QLabel for book cover
        cover_label = QLabel()
        cover_label.setPixmap(book_cover)
        cover_label.setScaledContents(True)
        cover_label.setFixedSize(150, 200)  # Uniform book cover size

        # Create QLabel for book title
        title_label = QLabel(book)
        title_label.setStyleSheet("color: white; font-size: 12px; font-family: 'Open Sans';")
        title_label.setAlignment(Qt.AlignCenter)

        # Progress bar styling (light blue, no edges)
        progress = progress_data.get(book, 0)  # Get saved progress or default to 0
        progress_bar = QProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setTextVisible(False)  # Hide percentage text
        progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: grey;
                border: none;
                height: 15px;
            }
            QProgressBar::chunk {
                background-color: lightblue;
            }
        """)
        progress_bar.setFixedHeight(15)

        # Book layout
        book_layout = QVBoxLayout()
        book_layout.addWidget(cover_label)
        book_layout.addWidget(title_label)
        book_layout.addWidget(progress_bar)

        # Encapsulate book layout into a QWidget
        book_widget = QWidget()
        book_widget.setLayout(book_layout)
        book_widget.setStyleSheet("background-color: matte black; border-radius: 10px;")

        # Add book widget to the grid
        grid_layout.addWidget(book_widget, row, col)
        col += 1
        if col > 4:  # 5 books per row
            col = 0
            row += 1
