# arandu/main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Use showMaximized instead of showFullScreen to retain window controls
    window.showMaximized()  
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
