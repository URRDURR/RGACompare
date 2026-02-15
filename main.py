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

print(file.spectra)
print(file.number_of_cycles)
print(file.single_cycle_data_size)
print(file.number_of_active_scan_steps)
print(file.step_data_sizes)

print(file.pointsPerAmu)
print(file.scanRate)
print(file.startMass)
print(file.stopMass)

print("HIIIIIIIIIIII")