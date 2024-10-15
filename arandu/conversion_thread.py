# arandu/conversion_thread.py
from PyQt5.QtCore import QThread, pyqtSignal
from converter import convert_pdf_to_epub

class ConversionThread(QThread):
    conversion_done = pyqtSignal(str)  # Signal emitted when conversion is done
    conversion_failed = pyqtSignal()  # Signal emitted if conversion fails

    def __init__(self, pdf_file, output_dir):
        super().__init__()
        self.pdf_file = pdf_file
        self.output_dir = output_dir

    def run(self):
        # Perform the conversion in the background
        epub_path = convert_pdf_to_epub(self.pdf_file, self.output_dir)
        if epub_path:
            self.conversion_done.emit(epub_path)
        else:
            self.conversion_failed.emit()
