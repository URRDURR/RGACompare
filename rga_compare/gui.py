import sys
import os
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QGroupBox, QFileDialog
from PySide6.QtGui import QIcon
from rgaPlotClass import RGAPlot
from rgaScanClass import RgaScanArray, RgaScan

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.rga_plot_widget = RGAPlot()
        self.rga_scans = RgaScanArray()

        self.setWindowTitle("RGA Compare")
        self.setWindowIcon(QIcon("./resources/icons/rga_compare.ico"))

        layout = QVBoxLayout()

        file_button = QPushButton()

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.create_linear_log_buttons())
        sidebar_layout.addWidget(file_button)

        center_layout = QHBoxLayout()
        center_layout.addLayout(sidebar_layout)
        center_layout.addWidget(self.create_RGA_plot(self.rga_plot_widget))

        layout.addLayout(center_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



        file_button.clicked.connect(self.open_rga_scan)
        self.rga_scans.scan_added.connect(self.on_scan_added)

    def create_linear_log_buttons(self):
        """Generates the box for the Linear and Logarithmic radio buttons for the plot"""
        group_box = QGroupBox("Linear or Logarithmic")
        
        self.lin_button = QRadioButton("Linear")
        self.log_button = QRadioButton("Log")

        self.lin_button.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.lin_button)
        layout.addWidget(self.log_button)

        # self.lin_button.toggled.connect(self.rga_plot_widget.change_axis_scale)
        self.log_button.toggled.connect(self.rga_plot_widget.change_axis_scale)

        group_box.setLayout(layout)

        return group_box
    
    def create_RGA_plot(self,rga_plot):
        """Generates the Plot for the RGA data (mostly here for organization)"""
        group_box = QGroupBox("RGA Plot")

        layout = QVBoxLayout()
        layout.addWidget(rga_plot)

        group_box.setLayout(layout)

        return group_box

    def create_scan_table():
        pass

    def open_rga_scan(self):

        files, _ = QFileDialog().getOpenFileNames(self, "Select file(s) to open")

        for file in files:
            scan = RgaScan(file)
            self.rga_scans.add_scan(scan)

    def on_scan_added(self, scan: RgaScan):
        
        self.rga_plot_widget.add_plot(scan)

    
