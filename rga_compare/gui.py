import sys
import os
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
QWidget, QRadioButton, QGroupBox, QFileDialog, QTableWidget, QSizePolicy, QSplitter, QTableWidgetItem, 
QHeaderView, QListWidget, QListWidgetItem, QMenuBar)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor, QPixmap
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

        self.menu_bar = self.menuBar()
        self.setMenuBar(self.menu_bar)
        file_menu = self.menu_bar.addMenu("File")
        recent_menu = file_menu.addMenu("Recent Files")
        recent_menu.addAction("Document 1")
        recent_menu.addAction("Document 2")
        recent_menu.addAction("Document 3")

        layout.addWidget(splitter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



        file_button.clicked.connect(self.open_rga_scan)
        self.rga_scans.scan_added.connect(self.on_scan_added)
        self.rga_scans.scan_removed.connect(self.on_scan_removed)

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

        # item1 = QListWidgetItem()
        # self.list.addItem(item1)
        # item1.setSizeHint(QSize(300, 50))
        # self.list.setItemWidget(item1, self.create_scan_widget())

        layout = QVBoxLayout()
        layout.addWidget(self.list)

        group_box.setLayout(layout)

        return group_box
        
    def create_scan_widget(self, scan_name: str, scan_colour: str, scan_added: RgaScan):
        
        total_layout = QVBoxLayout()

        name = QLabel(scan_name)

        colour = QWidget()
        colour.setFixedSize(15, 15)
        colour.setStyleSheet(f"""
            background-color: {scan_colour};
            border: 1.4px solid black;
        """)

        top_layout = QHBoxLayout()

        top_layout.addWidget(colour)
        top_layout.addWidget(name)

        button = QPushButton("remove")
        button.clicked.connect(lambda: self.rga_scans.remove_scan(scan_added))

        total_layout.addLayout(top_layout)
        total_layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(total_layout)

        item1 = QListWidgetItem()
        # item1.setSizeHint(QSize(300, 50))
        item1.setSizeHint(widget.sizeHint())    
        self.list.addItem(item1)
        self.list.setItemWidget(item1, widget)

        button.clicked.connect(lambda: self.list.takeItem(self.list.row(item1)))

    def open_rga_scan(self):

        files, _ = QFileDialog().getOpenFileNames(self, "Select file(s) to open")

        for file in files:
            scan = RgaScan(file)
            self.rga_scans.add_scan(scan)

    def on_scan_added(self, scan_added: RgaScan):
        
        self.rga_plot_widget.replot(self.rga_scans)
        
        scan_name = scan_added.file_identifier
        scan_colour = scan_added.colour

        self.create_scan_widget(scan_name, scan_colour, scan_added)

    def on_scan_removed(self, scan_added):
        
        self.rga_plot_widget.replot(self.rga_scans)

    
