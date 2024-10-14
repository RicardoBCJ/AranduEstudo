# arandu/ui.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QPushButton, QFileDialog, QSplitter
from PyQt5.QtGui import QIcon 
from PyQt5.QtCore import QSize, Qt
import os
from converter import convert_pdf_to_epub, validate_epub, ensure_library_folder
from library import load_library_books

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arandu - Study Helper")
        self.setGeometry(200, 100, 1200, 800)

        # Create main layout and sidebar
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # Sidebar with navigation
        self.sidebar_widget = self.create_sidebar()
        splitter.addWidget(self.sidebar_widget)

        # Content area (Library and Converter)
        self.content_widget = self.create_content_widget()
        splitter.addWidget(self.content_widget)

        layout.addWidget(splitter)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Path to the library folder
        self.library_path = os.path.join(os.path.dirname(__file__), "library")
        ensure_library_folder(self.library_path)  # Ensure library folder exists

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Icons (absolute paths)
        icon_path_library = os.path.join(os.path.dirname(__file__), "assets/icons/library.svg")
        icon_path_converter = os.path.join(os.path.dirname(__file__), "assets/icons/converter.svg")

        # Menu toggle button
        toggle_button = QPushButton("≡ Menu")
        toggle_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(toggle_button)

        # Library button
        self.library_button = QPushButton("Library")
        self.library_button.setIcon(QIcon(icon_path_library))
        self.library_button.clicked.connect(lambda: self.switch_section(0))
        sidebar_layout.addWidget(self.library_button)

        # Converter button
        self.converter_button = QPushButton("Converter")
        self.converter_button.setIcon(QIcon(icon_path_converter))
        self.converter_button.clicked.connect(lambda: self.switch_section(1))
        sidebar_layout.addWidget(self.converter_button)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)

        return sidebar

    def create_content_widget(self):
        self.stacked_widget = QStackedWidget()

        # Create Library view (QListWidget to display books)
        self.library_view = QListWidget()
        self.load_library_books()  # Load the books from the library folder
        self.library_view.itemClicked.connect(self.open_book)
        self.stacked_widget.addWidget(self.library_view)

        # Create Converter view
        converter_widget = QWidget()
        converter_layout = QVBoxLayout()
        convert_button = QPushButton("Select PDF to Convert")
        convert_button.clicked.connect(self.open_pdf_dialog)
        converter_layout.addWidget(convert_button)
        converter_widget.setLayout(converter_layout)
        self.stacked_widget.addWidget(converter_widget)

        return self.stacked_widget

    def load_library_books(self):
        # Load the books from the library folder into the QListWidget
        load_library_books(self.library_view, self.library_path)

    def open_pdf_dialog(self):
        # Open file dialog to select a PDF or EPUB file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF or EPUB", "", "PDF Files (*.pdf);;EPUB Files (*.epub);;All Files (*)", options=options)

        if file_name:
            if file_name.endswith('.pdf'):
                epub_path = convert_pdf_to_epub(file_name, self.library_path)
                if epub_path:
                    print(f"PDF converted to EPUB: {epub_path}")
                    self.load_library_books()  # Reload library after conversion
            elif file_name.endswith('.epub'):
                if validate_epub(file_name):
                    print(f"Valid EPUB: {file_name}")
                    self.load_library_books()  # Add the EPUB to the library

    def open_book(self, item):
        epub_file = item.text()
        epub_path = os.path.join(self.library_path, epub_file)
        print(f"Opening book: {epub_path}")
        # Implement reader functionality here

    def switch_section(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def toggle_sidebar(self):
        # Simple sidebar toggle without animation for now
        if self.sidebar_widget.width() == 200:
            self.sidebar_widget.setFixedWidth(50)  # Collapse to 50px
        else:
            self.sidebar_widget.setFixedWidth(200)  # Expand to 200px
