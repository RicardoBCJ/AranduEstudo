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

    print("Books found:", books)  # Add this line to check if books are being detected

    row, col = 0, 0
    for book in books:
        print(f"Loading book: {book}")  # Add this to confirm each book is being processed
        
    for book in books:
        book_path = os.path.join(library_path, book)
        book_cover = load_book_cover(book_path)
        
        # Create a QLabel for the book cover
        cover_label = QLabel()
        cover_label.setPixmap(book_cover)
        cover_label.setScaledContents(True)
        cover_label.setFixedSize(150, 200)  # Larger size for book covers

        # Create a QLabel for the book title
        title_label = QLabel(book)
        title_label.setStyleSheet("color: white; font-size: 14px;")
        title_label.setAlignment(Qt.AlignCenter)

        # Create a progress bar to show reading progress
        progress = progress_data.get(book, 0)  # Get the saved progress or default to 0
        progress_bar = QProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setTextVisible(True)
        progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: grey;
                color: white;
                height: 15px;
            }
            QProgressBar::chunk {
                background-color: #3e9f3e;
            }
        """)
        progress_bar.setFixedHeight(15)

        # Create a layout for each book item
        book_layout = QVBoxLayout()
        book_layout.addWidget(cover_label)
        book_layout.addWidget(title_label)
        book_layout.addWidget(progress_bar)

        # Create a widget to encapsulate each book layout
        book_widget = QWidget()
        book_widget.setLayout(book_layout)

        # Add the book widget to the grid layout
        grid_layout.addWidget(book_widget, row, col)

        # Increment the grid position
        col += 1
        if col > 4:  # 5 books per row
            col = 0
            row += 1