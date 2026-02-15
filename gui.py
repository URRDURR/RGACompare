import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QGroupBox
from graph import RGAPlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.create_linear_log_buttons())

        center_layout = QHBoxLayout()
        center_layout.addLayout(sidebar_layout)
        center_layout.addWidget(self.create_RGA_plot())

        layout.addLayout(center_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_linear_log_buttons(self):
        """Generates the box for the Linear and Logarithmic radio buttons for the plot"""
        group_box = QGroupBox("Linear or Logarithmic")
        
        self.lin_button = QRadioButton("Linear")
        self.log_button = QRadioButton("Log")

        self.lin_button.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.lin_button)
        layout.addWidget(self.log_button)

        group_box.setLayout(layout)

        return group_box
    
    def create_RGA_plot(self):
        """Generates the Plot for the RGA data (mostly here for organization)"""
        group_box = QGroupBox("RGA Plot")
        self.rga_plot_widget = RGAPlot()

        layout = QVBoxLayout()
        layout.addWidget(self.rga_plot_widget)

        group_box.setLayout(layout)

        return group_box
    
    # def create_
    
