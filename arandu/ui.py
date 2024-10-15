from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QPushButton, QFileDialog, QSplitter, QMessageBox, QGridLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon  # Import QIcon
from conversion_thread import ConversionThread  # Import the thread class
import os
from converter import convert_pdf_to_epub, ensure_library_folder, validate_epub
from library import load_library_grid


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arandu - Study Helper")
        self.setGeometry(200, 100, 1200, 800)

        # Path to the library folder
        self.library_path = os.path.join(os.path.dirname(__file__), "library")
        ensure_library_folder(self.library_path)

        # Create main splitter
        splitter = QSplitter(Qt.Horizontal)

        # Disable handle interaction
        splitter.setHandleWidth(0)  # Hide the grey bar (handle)
        splitter.setChildrenCollapsible(False)  # Disable collapsing by dragging

        # Sidebar with navigation
        self.sidebar_widget = self.create_sidebar()
        splitter.addWidget(self.sidebar_widget)

        # Content area (Library and Converter)
        self.content_widget = self.create_content_widget()
        splitter.addWidget(self.content_widget)

        # Set stretch factor so content uses more space
        splitter.setStretchFactor(1, 4)

        # Main layout
        layout = QHBoxLayout()
        layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.apply_stylesheet()

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Set spacing to control the vertical space
        sidebar_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        sidebar_layout.setSpacing(10)  # Adjust the spacing between buttons

        # Set the menu icon
        icon_path_menu = os.path.join(os.path.dirname(__file__), "assets/icons/menu.svg")
        icon_path_library = os.path.join(os.path.dirname(__file__), "assets/icons/library.svg")
        icon_path_converter = os.path.join(os.path.dirname(__file__), "assets/icons/converter.svg")

        # Menu toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon(icon_path_menu))
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.toggle_button)

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

    def toggle_sidebar(self):
        if self.sidebar_widget.width() == 200:
            # Collapse the sidebar
            self.sidebar_widget.setFixedWidth(50)

            # Hide text, show only icons
            self.library_button.setText("")
            self.converter_button.setText("")
            self.toggle_button.setText("")
        else:
            # Expand the sidebar
            self.sidebar_widget.setFixedWidth(200)

            # Show text with icons
            self.toggle_button.setText("Menu")
            self.library_button.setText("Library")
            self.converter_button.setText("Converter")

    def create_content_widget(self):
        self.stacked_widget = QStackedWidget()

        # Create a grid layout for the library view
        library_widget = QWidget()
        library_layout = QVBoxLayout()
        
        grid_layout = QGridLayout()  # Grid layout for books
        load_library_grid(grid_layout, self.library_path)  # Load books into the grid

        library_layout.addLayout(grid_layout)
        library_widget.setLayout(library_layout)
        
        self.stacked_widget.addWidget(library_widget)

        # Converter section (unchanged)
        converter_widget = QWidget()
        converter_layout = QVBoxLayout()
        convert_button = QPushButton("Select PDF to Convert")
        convert_button.clicked.connect(self.open_pdf_dialog)
        converter_layout.addWidget(convert_button)
        converter_widget.setLayout(converter_layout)
        self.stacked_widget.addWidget(converter_widget)

        return self.stacked_widget

    def open_book(self, item):
        epub_file = item.text()
        epub_path = os.path.join(self.library_path, epub_file)
        print(f"Opening book: {epub_path}")

    def open_pdf_dialog(self):
        convert_button = self.sender()
        convert_button.setEnabled(False)

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF or EPUB", "", "PDF Files (*.pdf);;EPUB Files (*.epub);;All Files (*)", options=options)

        if file_name:
            self.message_box = QMessageBox(self)
            self.message_box.setIcon(QMessageBox.Information)
            self.message_box.setWindowTitle("Converting File")
            self.message_box.setText("Converting file, please wait...")
            self.message_box.setStandardButtons(QMessageBox.NoButton)
            self.message_box.show()

            # Run the conversion in the background
            self.thread = ConversionThread(file_name, self.library_path)
            self.thread.conversion_done.connect(self.conversion_success)
            self.thread.conversion_failed.connect(self.conversion_failed)
            self.thread.start()

        convert_button.setEnabled(True)

    def conversion_success(self, epub_path):
        self.message_box.setText(f"Conversion successful: {epub_path}")
        self.message_box.setStandardButtons(QMessageBox.Ok)
        # self.load_library_books()

    def conversion_failed(self):
        self.message_box.setText("Conversion failed.")
        self.message_box.setStandardButtons(QMessageBox.Ok)

    def switch_section(self, index):
        self.stacked_widget.setCurrentIndex(index)

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
            QPushButton:hover {
                background-color: #3e3e3e;
            }
            QLabel {
                color: white;
            }
            QListWidget {
                background-color: white;
            }
            QWidget {
                background-color: #2c2c2c;  # Ensure consistent background color
            }
        """
        self.setStyleSheet(style_sheet)
