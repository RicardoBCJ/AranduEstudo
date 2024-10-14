from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QToolBar, QAction, QFileDialog, QSplitter, QPushButton, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QPropertyAnimation, Qt
import os

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
        # Create sidebar widget and layout
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Toggle button
        toggle_button = QPushButton("≡ Menu")
        toggle_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(toggle_button)

        # Initialize buttons with icons
        self.library_button = QPushButton()
        self.converter_button = QPushButton()

        sidebar_layout.addWidget(self.library_button)
        sidebar_layout.addWidget(self.converter_button)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)

        # Initial button state (with text and icons)
        self.update_sidebar_buttons(show_text=True)

        return sidebar
    
    def open_pdf_dialog(self):
        # Open file dialog to select a PDF file for conversion
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF to Convert", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_name:
            # Call the conversion function (we will handle the conversion here)
            print(f"Selected PDF: {file_name}")

    def create_content_widget(self):
        # Create a stacked widget to switch between Library, Converter, and Reader sections
        self.stacked_widget = QStackedWidget()

        # Create the library view (placeholder for now)
        self.library_view = QTextEdit()
        self.library_view.setText("Library Section: Display your books here")
        self.stacked_widget.addWidget(self.library_view)

        # Create the converter view (placeholder for now)
        self.converter_view = QTextEdit()
        self.converter_view.setText("Converter Section: Drag and drop PDFs here to convert to EPUB")
        self.stacked_widget.addWidget(self.converter_view)

        return self.stacked_widget
    
    def switch_section(self, index):
        # Switch between different sections (Library, Converter, etc.)
        self.stacked_widget.setCurrentIndex(index)

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
