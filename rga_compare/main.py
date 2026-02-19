import sys
import os
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
from gui import MainWindow
import qt_themes

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

pg.setConfigOptions(antialias=True, useOpenGL=True, enableExperimental=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qt_themes.set_theme("catppuccin_latte")

    window = MainWindow()
    window.show()

    app.exec()
