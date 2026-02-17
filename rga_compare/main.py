import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor
from gui import MainWindow
from rgaScanClass import RgaScan, RgaScanArray
import qt_themes
import os

# Force software to use the desktop's native hardware acceleration
# os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1" 
# os.environ["QT_OPENGL"] = "desktop"

# print(np.log(0))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qt_themes.set_theme('catppuccin_latte')

    window = MainWindow()
    window.show()

    app.exec()

# file = RgaScan(".\\sample_scans\\2026-06-17 - RGA120.rgadata")

# print(len(file.spectra[1]))
# print(len(file.amu_vector()))

print("Program has finished running")