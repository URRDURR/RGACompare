import sys
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
from gui import MainWindow
import qt_themes

pg.setConfigOptions(antialias=True, useOpenGL=True, enableExperimental=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qt_themes.set_theme("catppuccin_latte")

    window = MainWindow()
    window.show()

    app.exec()
