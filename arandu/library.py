import os
import json
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QSize, Qt

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
    # For now, return a dummy cover (replace with actual EPUB cover loading)
    return QPixmap('assets/icons/book_placeholder.png')  # Replace with actual cover extraction

# Load books into the grid layout
def load_library_grid(grid_layout, library_path):
    progress_data = load_progress()  # Load reading progress data

    books = [f for f in os.listdir(library_path) if f.endswith('.epub')]
    row, col = 0, 0
    for book in books:
        book_path = os.path.join(library_path, book)
        book_cover = load_book_cover(book_path)
        
        # Create a QLabel for the book cover
        cover_label = QLabel()
        cover_label.setPixmap(book_cover)
        cover_label.setScaledContents(True)
        cover_label.setFixedSize(100, 150)  # Fixed size for book covers

        # Create a QLabel for the book title
        title_label = QLabel(book)
        title_label.setStyleSheet("color: white; font-size: 14px;")
        title_label.setAlignment(Qt.AlignCenter)

        # Create a progress bar to show reading progress
        progress = progress_data.get(book, 0)  # Get the saved progress or default to 0
        progress_bar = QProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setTextVisible(True)
        progress_bar.setStyleSheet("QProgressBar { background-color: grey; color: white; }")
        
        # Create a layout for each book item
        book_layout = QVBoxLayout()
        book_layout.addWidget(cover_label)
        book_layout.addWidget(title_label)
        book_layout.addWidget(progress_bar)

        # Add the book layout to the grid
        grid_layout.addLayout(book_layout, row, col)
        col += 1
        if col > 3:  # 4 books per row
            col = 0
            row += 1
