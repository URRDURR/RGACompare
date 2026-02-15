import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor
from gui import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

print("HIIIIIIIIIIII")