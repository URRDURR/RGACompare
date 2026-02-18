import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QRadioButton,
    QGroupBox,
    QFileDialog,
    QTableWidget,
    QSizePolicy,
    QSplitter,
    QTableWidgetItem,
    QHeaderView,
    QListWidget,
    QListWidgetItem,
    QMenuBar,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor, QPixmap
from rgaPlotClass import RGAPlot
from rgaScanClass import RgaScanList, RgaScan


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.rga_plot = RGAPlot()
        self.rga_scan_list = RgaScanList()

        self.setWindowTitle("RGA Compare")
        self.setWindowIcon(QIcon("./resources/icons/rga_compare.ico"))

        file_button = QPushButton("Open Scans")
        file_button.clicked.connect(self.open_rga_scan)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.create_linear_log_buttons())
        sidebar_layout.addWidget(self.create_scan_table())
        sidebar_layout.addWidget(file_button)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(self.create_RGA_plot(self.rga_plot))
        splitter.setSizes([200, 600])

        self.menu_bar = self.menuBar()
        self.setMenuBar(self.menu_bar)
        file_menu = self.menu_bar.addMenu("File")
        recent_menu = file_menu.addMenu("Recent Files")
        recent_menu.addAction("Document 1")
        recent_menu.addAction("Document 2")
        recent_menu.addAction("Document 3")

        layout = QVBoxLayout()
        layout.addWidget(splitter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.rga_scan_list.scan_added.connect(self.on_scan_added)
        self.rga_scan_list.scan_removed.connect(self.on_scan_removed)

    def create_linear_log_buttons(self):
        """Generates the box for the Linear and Logarithmic radio buttons for the plot"""

        lin_button = QRadioButton("Linear")
        log_button = QRadioButton("Log")
        lin_button.setChecked(True)
        log_button.toggled.connect(self.rga_plot.set_axis_scale)

        layout = QHBoxLayout()
        layout.addWidget(lin_button)
        layout.addWidget(log_button)

        group_box = QGroupBox("Linear or Logarithmic")
        group_box.setLayout(layout)

        return group_box

    def create_RGA_plot(self, rga_plot):
        """Generates the Plot for the RGA data (mostly here for organization)"""

        layout = QVBoxLayout()
        layout.addWidget(rga_plot)

        group_box = QGroupBox("RGA Plot")
        group_box.setLayout(layout)

        return group_box

    def create_scan_table(self):

        self.list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.list)

        group_box = QGroupBox("Scans")
        group_box.setLayout(layout)

        return group_box

    def create_scan_widget(self, scan_name: str, scan_colour: str, scan_added: RgaScan):
        """Generates a listWidgetItem to the sidebar when a scan/plot is added containing quick info and
        options for the added plot (e.g. name, plot colour, remove scan button)

        Args:
            scan_name (str): The filename of the scan added (currently bugged)
            scan_colour (str): The plot colour assigned to the scan
            scan_added (RgaScan): the RgaScan object of the newly added scan
        """
        name = QLabel(scan_name)

        colour_icon = QWidget()
        colour_icon.setFixedSize(15, 15)
        colour_icon.setStyleSheet(f"background-color: {scan_colour}; border: 1.4px solid black;")

        remove_plot_button = QPushButton("remove")
        remove_plot_button.clicked.connect(lambda: self.rga_scan_list.remove_scan(scan_added))
        remove_plot_button.clicked.connect(lambda: self.list.takeItem(self.list.row(list_item)))

        toggle_visibility_button = QPushButton("Toggle_Visibility")
        toggle_visibility_button.setCheckable(True)
        # toggle_visibility_button.clicked.connect(lambda: list_widget.setWindowOpacity(0.5))
        # toggle_visibility_button.toggled.connect(lambda checked: 
        #                                          toggle_visibility_button.clicked.connect(lambda: self.rga_plot.add_plot(scan_added)) if checked
        #                                          else toggle_visibility_button.clicked.connect(lambda: self.rga_plot.remove_plot(scan_added))
        #                                             )

        top_layout = QHBoxLayout()
        top_layout.addWidget(colour_icon)
        top_layout.addWidget(name)

        bottom_layout = QHBoxLayout()
        # bottom_layout.addWidget(toggle_visibility_button)
        bottom_layout.addWidget(remove_plot_button)

        total_layout = QVBoxLayout()
        total_layout.addLayout(top_layout)
        total_layout.addLayout(bottom_layout)

        list_widget = QWidget()
        list_widget.setLayout(total_layout)
        list_item = QListWidgetItem()
        list_item.setSizeHint(list_widget.sizeHint())
        self.list.addItem(list_item)
        self.list.setItemWidget(list_item, list_widget)

    def open_rga_scan(self):
        """Opens a file dialog to select .rgadata scan files to plot"""
        files, _ = QFileDialog().getOpenFileNames(self, "Select file(s) to open", "", "RGASoft Scans (*.rgadata)")
        for file in files:
            scan = RgaScan(file)
            self.rga_scan_list.add_scan(scan)

    def on_scan_added(self, scan_added: RgaScan):
        """Runs various plot and GUI updates when a scan is added

        Args:
            scan_added (RgaScan): The RgaScan object of the newly added scan
        """
        self.rga_plot.add_plot(scan_added)

        scan_name = scan_added.file_identifier
        scan_colour = scan_added.colour
        self.create_scan_widget(scan_name, scan_colour, scan_added)

    def on_scan_removed(self, scan_removed: RgaScan):
        """Runs various plot and GUI updates when a scan is removed

        Args:
            scan_removed (_type_): The RgaScan object of the newly added scan
        """
        self.rga_plot.remove_plot(scan_removed)
