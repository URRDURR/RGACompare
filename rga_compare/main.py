import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow
import qt_themes

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qt_themes.set_theme("catppuccin_latte")

    window = MainWindow()
    window.show()

    app.exec()
