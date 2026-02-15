import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor
from gui import MainWindow
from rgaScanClass import RgaScan

# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()

# .\sample_scans\2026-06-17 - RGA120.rgadata

file = RgaScan(".\\sample_scans\\2026-06-17 - RGA120.rgadata")

print(len(file.spectra[1]))
print(len(file.AMU_linspace()))

print("HIIIIIIIIIIII")