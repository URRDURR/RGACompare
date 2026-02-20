from abc import ABC, abstractmethod
import pyqtgraph as pg
import numpy as np
from PySide6 import QtWidgets, QtCore
from rgaScanClass import RgaScan, RgaScanList

class Plot(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.getPlotItem().setClipToView(True)  # Stops rendering points that are off-screen
        self.getPlotItem().setDownsampling(mode="peak", auto=True)  # Reduce points when zoomed out

        self.scan_list = []
        # self.log_mode = False  # Set to False since plot is made to begin in Linear mode
        # self.x_value_max = -1
        # self.x_value_min = float("inf")
        # self.y_value_max = -1
        # self.y_value_min = float("inf")

        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.addItem(self.vLine, ignoreBounds=True)
        self.label = pg.TextItem(anchor=(0, 1)) # Tracking Label (HTML allows for multiple lines of data)
        self.addItem(self.label)

        self.set_plot_theme()
        self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self.update_hover)

    @abstractmethod
    def replot(self):
            pass

    # @abstractmethod
    # def replot(self):

    #     # Aspect representing the characteristics of the viewbox/viewable area
    #     view_box = self.getPlotItem().getViewBox()

    #     # set up the variable for limits, apply constants so that they are always initially overwritten
    #     x_lim_upper = -1
    #     x_lim_lower = float("inf")
    #     y_lim_upper = -1
    #     y_lim_lower = float("inf")

    #     # # Clear and replot
    #     # for item in self.getPlotItem().listDataItems():
    #     #     self.getPlotItem().removeItem(item)

    #     view_box.clear()

    #     # sets the view back to default conditions when all plots are removed
    #     if len(self.scan_list) == 0:
    #         view_box.setLimits(xMin=-100, xMax=100, yMin=-100, yMax=100)
    #         view_box.setRange(xRange=(0, 1), yRange=(0, 1))
    #         return

    #     # Plots every scan in the RgaScanList
    #     for i in range(len(self.scan_list)):
    #         scan = self.scan_list[i]
    #         cycle = scan.get_cycle(scan.number_of_cyles() - 1)
    #         self.getPlotItem().plot(scan.amu_axis(), cycle, pen=pg.mkPen(scan.colour, width=2))

    #         y_max = np.max(cycle)
    #         y_min = np.min(cycle, where=(cycle > 0), initial=np.inf)

    #         # Measures the range of values for setting view range limits
    #         if x_lim_upper < scan.stopMass:
    #             x_lim_upper = scan.stopMass
    #         if x_lim_lower > scan.startMass:
    #             x_lim_lower = scan.startMass
    #         if y_lim_upper < y_max:
    #             y_lim_upper = y_max
    #         if y_lim_lower > y_min and y_min > 0:
    #             y_lim_lower = y_min

    #     self.x_lim_upper = x_lim_upper
    #     self.x_lim_lower = x_lim_lower
    #     self.y_lim_upper = y_lim_upper
    #     self.y_lim_lower = y_lim_lower

    #     self.set_axis_limits()

    #     view_box.addItem(self.vLine)
    #     view_box.addItem(self.label)

    def add_plot(self, scan: RgaScan):

        self.scan_list.append(scan)
        self.replot()

    def remove_plot(self, scan: RgaScan):
        self.scan_list.remove(scan)
        self.replot()

    def set_axis_limits(self, x_value_max, x_value_min, y_value_max, y_value_min):

        view_box = self.getPlotItem().getViewBox()
        y_axis_log_state = view_box.state['logMode'][1]

        # Creates the padding space for sides of plot so the viewbox is less cramped
        padding_x = (x_value_max - x_value_min) * 0.02  # 2% padding
        padding_y = (y_value_max - y_value_min) * 0.02

        # Sets x axis limits
        view_box.setLimits(
            xMin=(x_value_min - padding_x),
            xMax=(x_value_max + padding_x),
        )

        # print(self.log_mode)
        # print(y_axis_log_state)

        if y_axis_log_state:
            # Sets log y axis limits (accounts for the fact the Pyqtgraph takes the 10^x of limits given)
            y_min = np.log10(y_value_min)
            y_max = np.log10(y_value_max)
            view_box.setLimits(yMin=y_min, yMax=y_max)
        else:
            # Sets linear y axis limits
            view_box.setLimits(yMin=y_value_min - padding_y, yMax=y_value_max + padding_y)

    def set_axis_scale(self, log_mode: bool):

        # self.log_mode = log_mode
        self.getPlotItem().setLogMode(y=log_mode)
        if len([item for item in self.listDataItems() if isinstance(item, pg.PlotDataItem)]) != 0:
            self.set_axis_limits()


    def set_plot_theme(self):
        """
        Main styling method to be called on initialization or reset.
        """

        self.setBackground("#1e1e2e")
        self.plotItem.getAxis("bottom").setPen("#cdd6f4")
        self.plotItem.getAxis("left").setPen("#cdd6f4")
        self.plotItem.showGrid(x=True, y=True, alpha=0.1)

        self.vLine.setPen(pg.mkPen("#f5e0dc"))
        self.label.setColor("#cdd6f4")

    # def update_hover(self, event):
    #     pos = event[0]
    #     if self.sceneBoundingRect().contains(pos):
    #         mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
    #         x = mousePoint.x()

    #         if not self.scan_list:
    #             pass
    #         elif x < self.x_lim_lower:
    #             x = self.x_lim_lower
    #         elif x > self.x_lim_upper:
    #             x = self.x_lim_upper

    #         # 2. Build the HTML string for the label
    #         # We can loop through the curves you stored in self.curves
    #         label_html = f"<div style='background-color: rgba(30, 30, 46, 150); padding: 5px; border: 1px solid #cdd6f4;'>"
    #         label_html += f"<b style='color: #f5e0dc;'>AMU: {x:.2f}</b><br>"

    #         found_data = False
    #         for i, scan in enumerate(self.scan_list):
    #             cycle = scan.get_cycle(scan.number_of_cyles() - 1)
    #             # Simple logic: find the y-value closest to the current mouse x
    #             # This assumes x_data is sorted
    #             scan_x = scan.amu_axis()
    #             index = np.argmin(np.abs(scan_x - x))
    #             if 0 <= index < len(cycle):
    #                 y_val = cycle[index]
    #                 label_html += f"<span style='color: {scan.colour};'>Scan {i+1}: {y_val:.3e}</span><br>"
    #                 found_data = True
    #                 # print(f"x: {x}, y:{y_val}")

    #         label_html += "</div>"

    #         self.vLine.setPos(x)
    #         # 3. Update label text and position
    #         if found_data:
    #             # snap_x_pos = scan_x[index]
    #             # self.vLine.setPos(snap_x_pos)
    #             self.label.setHtml(label_html)
    #             # Position the label slightly offset from the mouse
    #             self.label.setPos(x, mousePoint.y())

class RGAPlot(Plot):
    def __init__(self):
        super().__init__()

        self.scan_list: list[RgaScan] = []

    def replot(self):

        # Aspect representing the characteristics of the viewbox/viewable area
        view_box = self.getPlotItem().getViewBox()

        # set up the variable for limits, apply constants so that they are always initially overwritten
        x_lim_upper = -1
        x_lim_lower = float("inf")
        y_lim_upper = -1
        y_lim_lower = float("inf")

        # # Clear and replot
        # for item in self.getPlotItem().listDataItems():
        #     self.getPlotItem().removeItem(item)

        view_box.clear()

        # sets the view back to default conditions when all plots are removed
        if len(self.scan_list) == 0:
            view_box.setLimits(xMin=-100, xMax=100, yMin=-100, yMax=100)
            view_box.setRange(xRange=(0, 1), yRange=(0, 1))
            return

        # Plots every scan in the RgaScanList
        for i in range(len(self.scan_list)):
            scan = self.scan_list[i]
            cycle = scan.get_cycle(scan.number_of_cyles() - 1)
            self.getPlotItem().plot(scan.amu_axis(), cycle, pen=pg.mkPen(scan.colour, width=2))

            y_max = np.max(cycle)
            y_min = np.min(cycle, where=(cycle > 0), initial=np.inf)

            # Measures the range of values for setting view range limits
            if x_lim_upper < scan.stopMass:
                x_lim_upper = scan.stopMass
            if x_lim_lower > scan.startMass:
                x_lim_lower = scan.startMass
            if y_lim_upper < y_max:
                y_lim_upper = y_max
            if y_lim_lower > y_min and y_min > 0:
                y_lim_lower = y_min

        self.x_value_max = x_lim_upper
        self.x_value_min = x_lim_lower
        self.y_value_max = y_lim_upper
        self.y_value_min = y_lim_lower

        self.set_axis_limits(self.x_value_max, self.x_value_min, self.y_value_max, self.y_value_min)

        view_box.addItem(self.vLine)
        view_box.addItem(self.label)

    def update_hover(self, event):
        pos = event[0]
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
            x = mousePoint.x()

            if not self.scan_list:
                pass
            elif x < self.x_value_min:
                x = self.x_value_min
            elif x > self.x_value_max:
                x = self.x_value_max

            # 2. Build the HTML string for the label
            # We can loop through the curves you stored in self.curves
            label_html = f"<div style='background-color: rgba(30, 30, 46, 150); padding: 5px; border: 1px solid #cdd6f4;'>"
            label_html += f"<b style='color: #f5e0dc;'>AMU: {x:.2f}</b><br>"

            found_data = False
            for i, scan in enumerate(self.scan_list):
                cycle = scan.get_cycle(scan.number_of_cyles() - 1)
                # Simple logic: find the y-value closest to the current mouse x
                # This assumes x_data is sorted
                scan_x = scan.amu_axis()
                index = np.argmin(np.abs(scan_x - x))
                if 0 <= index < len(cycle):
                    y_val = cycle[index]
                    label_html += f"<span style='color: {scan.colour};'>Scan {i+1}: {y_val:.3e}</span><br>"
                    found_data = True
                    # print(f"x: {x}, y:{y_val}")

            label_html += "</div>"

            self.vLine.setPos(x)
            # 3. Update label text and position
            if found_data:
                # snap_x_pos = scan_x[index]
                # self.vLine.setPos(snap_x_pos)
                self.label.setHtml(label_html)
                # Position the label slightly offset from the mouse
                self.label.setPos(x, mousePoint.y())