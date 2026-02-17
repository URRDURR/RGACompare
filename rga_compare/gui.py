import sys
import os
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
QWidget, QRadioButton, QGroupBox, QFileDialog, QTableWidget, QSizePolicy, QSplitter, QTableWidgetItem, QHeaderView, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from rgaPlotClass import RGAPlot
from rgaScanClass import RgaScanArray, RgaScan

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.rga_plot_widget = RGAPlot()
        self.rga_scans = RgaScanArray()
        self.table = None

        self.setWindowTitle("RGA Compare")
        self.setWindowIcon(QIcon("./resources/icons/rga_compare.ico"))

        layout = QVBoxLayout()

        file_button = QPushButton()

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.create_linear_log_buttons())
        sidebar_layout.addWidget(self.create_scan_table())
        sidebar_layout.addWidget(file_button)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(self.create_RGA_plot(self.rga_plot_widget))
        splitter.setSizes([200, 600])

        # center_layout = QHBoxLayout()
        # center_layout.addLayout(sidebar_layout)
        # center_layout.addWidget(self.create_RGA_plot(self.rga_plot_widget))
        # center_layout.setStretch(1, 3)  

        layout.addWidget(splitter)

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

    def create_scan_table(self):
        
        group_box = QGroupBox("Scans")

        self.list = QListWidget()

        button = QPushButton()

        self.list.addItem(QListWidgetItem("Geeks"))
        self.list.setItemWidget(QListWidgetItem("Geeks"), button)

        # self.table = QTableWidget()
        # self.table.setColumnCount(3)
        # self.table.setRowCount(1)
        # self.table.setHorizontalHeaderLabels(["Colour","Name","Range"])
        # self.table.setItem(0,0,QTableWidgetItem('#ffffff'))
        # self.table.setItem(0,1,QTableWidgetItem("White"))
        # self.table.setItem(0,2,QTableWidgetItem("12-14"))

        # header = self.table.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        # header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.list)

        group_box.setLayout(layout)

        return group_box
        

    def open_rga_scan(self):

        files, _ = QFileDialog().getOpenFileNames(self, "Select file(s) to open")

        for file in files:
            scan = RgaScan(file)
            self.rga_scans.add_scan(scan)

    def on_scan_added(self, scans: RgaScanArray):
        
        self.rga_plot_widget.replot(self.rga_scans)

    
