from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QToolBar, QAction, QFileDialog, QSplitter, QPushButton, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QPropertyAnimation, Qt
import os
import subprocess
from converter import convert_pdf_to_epub, validate_epub  # Import from the new module

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arandu - Study Helper")
        self.setGeometry(200, 100, 1200, 800)

        # Initialize state variable
        self.sidebar_expanded = True

        # Create main layout with sidebar and content area
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # Sidebar (Library/Navigation Menu)
        self.sidebar_widget = self.create_sidebar()
        splitter.addWidget(self.sidebar_widget)

        # Main content area
        self.content_widget = self.create_content_widget()
        splitter.addWidget(self.content_widget)

        layout.addWidget(splitter)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Apply stylesheet for appearance
        self.apply_stylesheet()

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Menu toggle button
        toggle_button = QPushButton("≡ Menu")
        toggle_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(toggle_button)

        # Only two buttons: Library and Converter
        self.library_button = QPushButton("Library")
        self.library_button.setIcon(QIcon("assets/icons/library.svg"))
        self.library_button.clicked.connect(lambda: self.switch_section(0))
        sidebar_layout.addWidget(self.library_button)

        self.converter_button = QPushButton("Converter")
        self.converter_button.setIcon(QIcon("assets/icons/converter.svg"))
        self.converter_button.clicked.connect(lambda: self.switch_section(1))
        sidebar_layout.addWidget(self.converter_button)

        # Spacer to push buttons to the top
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)

        return sidebar
    
    def open_pdf_dialog(self):
        # Open file dialog to select PDF or EPUB file for conversion
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF or EPUB", "", "PDF Files (*.pdf);;EPUB Files (*.epub);;All Files (*)", options=options)

        if file_name:
            # If it's a PDF, convert it to EPUB
            if file_name.endswith('.pdf'):
                output_dir = "path/to/library"  # The directory where EPUBs will be saved
                epub_path = convert_pdf_to_epub(file_name, output_dir)
                if epub_path:
                    print(f"PDF converted to EPUB: {epub_path}")
                    # Add to library here
            elif file_name.endswith('.epub'):
                # Validate the EPUB and add it to the library
                if validate_epub(file_name):
                    print(f"Valid EPUB: {file_name}")
                    # Add to library here
                else:
                    print(f"Invalid EPUB file: {file_name}")

    def create_content_widget(self):
        # Create a stacked widget to handle multiple views (Library, Converter)
        self.stacked_widget = QStackedWidget()

        # Library view (Placeholder for now)
        self.library_view = QTextEdit()
        self.library_view.setText("Library Section: Display your books here")
        self.stacked_widget.addWidget(self.library_view)

        # Converter view (New section)
        converter_widget = QWidget()  # Main widget for Converter view
        converter_layout = QVBoxLayout()  # Layout for Converter view
        convert_button = QPushButton("Select PDF to Convert")  # Button to open file dialog
        convert_button.clicked.connect(self.open_pdf_dialog)  # Connect button to file dialog function
        converter_layout.addWidget(convert_button)

        # Set the layout for the converter widget
        converter_widget.setLayout(converter_layout)
        self.stacked_widget.addWidget(converter_widget)

        return self.stacked_widget
    
    def open_pdf_dialog(self):
            # Open a file dialog to select a PDF file for conversion
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF to Convert", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_name:
            # Call the conversion function here or handle the selected PDF
            print(f"Selected PDF: {file_name}")
    
# Inside ui.py
    def switch_section(self, index):
        self.stacked_widget.setCurrentIndex(index)  # Switch the view in the stacked widget

    def convert_pdf_to_epub(self, pdf_file):
        epub_filename = pdf_file.replace('.pdf', '.epub')
    
        try:
            # Run the calibre ebook-convert command
            subprocess.run(['ebook-convert', pdf_file, epub_filename], check=True)
            print(f"Conversion successful: {epub_filename}")
            # You would then save the converted EPUB to the library folder
        except Exception as e:
            print(f"Conversion failed: {e}")


    def toggle_sidebar(self):
        # Directly set the fixed width of the sidebar (no animation)
        if self.sidebar_expanded:
            self.sidebar_widget.setFixedWidth(50)  # Retract to 50px
            self.sidebar_expanded = False
            self.update_sidebar_buttons(show_text=False)  # Show only icons
        else:
            self.sidebar_widget.setFixedWidth(200)  # Expand to 200px
            self.sidebar_expanded = True
            self.update_sidebar_buttons(show_text=True)  # Show text and icons

    def update_sidebar_buttons(self, show_text):
        icon_size = QSize(24, 24)

        # Use absolute paths to the icons
        icon_path_library = os.path.join(os.path.dirname(__file__), "assets/icons/library.svg")
        icon_path_converter = os.path.join(os.path.dirname(__file__), "assets/icons/converter.svg")

        self.library_button.setIcon(QIcon(icon_path_library))
        self.library_button.setIconSize(icon_size)

        self.converter_button.setIcon(QIcon(icon_path_converter))
        self.converter_button.setIconSize(icon_size)

        # Set text visibility based on sidebar state
        if show_text:
            self.library_button.setText("Library")
            self.converter_button.setText("Converter")
        else:
            self.library_button.setText("")
            self.converter_button.setText("")

    def apply_stylesheet(self):
        style_sheet = """
            QMainWindow {
                background-color: #2c2c2c;
            }
            QPushButton {
                background-color: #2c2c2c;
                color: #f0f0f0;
                border: 1px solid #3e3e3e;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton#menuButton {
                border: none;
                font-size: 16px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
            }
            QTextEdit {
                background-color: #3e3e3e;
                border: 1px solid #d3d3d3;
                padding: 10px;
                font-size: 16px;
                color: #ffffff;
            }
        """
        self.setStyleSheet(style_sheet)
