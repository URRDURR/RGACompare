import pyqtgraph as pg
import numpy as np
from PySide6 import QtWidgets, QtCore
from rgaScanClass import RgaScan, RgaScanList


class RGAPlot(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.scans_objects = []

        self.getPlotItem().setClipToView(True)  # Stops rendering points that are off-screen
        self.getPlotItem().setDownsampling(mode="peak", auto=True)  # Reduce points when zoomed out

        self.log_mode = False  # Set to False since plot is made to begin in Linear mode
        self.x_lim_upper = None
        self.x_lim_lower = None
        self.y_lim_upper = None
        self.y_lim_lower = None

        self.set_plot_theme()

    def replot(self, scans: RgaScanList):

        # Aspect representing the characteristics of the viewbox/viewable area
        view_box = self.getPlotItem().getViewBox()

        # set up the variable for limits, apply constants so that they are always initially overwritten
        x_lim_upper = -1
        x_lim_lower = float("inf")
        y_lim_upper = -1
        y_lim_lower = float("inf")

        # Clear and replot
        self.clear()

        # sets the view back to default conditions when all plots are removed
        if len(scans) == 0:
            self.setLimits(xMin=-100, xMax=100, yMin=-100, yMax=100)
            view_box.setRange(xRange=(0, 1), yRange=(0, 1))
            return

        # Plots every scan in the RgaScanList
        for i in range(len(scans)):
            scan = scans.get_scan(i)
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

        self.x_lim_upper = x_lim_upper
        self.x_lim_lower = x_lim_lower
        self.y_lim_upper = y_lim_upper
        self.y_lim_lower = y_lim_lower

        self.set_axis_limits()

    def set_axis_limits(self):

        view_box = self.getPlotItem().getViewBox()

        # Creates the padding space for sides of plot so the viewbox is less cramped
        padding_x = (self.x_lim_upper - self.x_lim_lower) * 0.02  # 2% padding
        padding_y = (self.y_lim_upper - self.y_lim_lower) * 0.02

        # Sets x axis limits
        view_box.setLimits(
            xMin=(self.x_lim_lower - padding_x),
            xMax=(self.x_lim_upper + padding_x),
        )

        if self.log_mode:
            # Sets log y axis limits (accounts for the fact the Pyqtgraph takes the 10^x of limits given)
            y_min = np.log10(self.y_lim_lower)
            y_max = np.log10(self.y_lim_upper)
            view_box.setLimits(yMin=y_min, yMax=y_max)
        else:
            # Sets linear y axis limits
            view_box.setLimits(yMin=self.y_lim_lower - padding_y, yMax=self.y_lim_upper + padding_y)

    def change_axis_scale(self, log_mode: bool):

        self.log_mode = log_mode
        if len([item for item in self.listDataItems() if isinstance(item, pg.PlotDataItem)]) != 0:
            self.set_axis_limits()
        self.getPlotItem().setLogMode(y=log_mode)

    def set_plot_theme(self, title="System Telemetry"):
        """
        Main styling method to be called on initialization or reset.
        """

        self.setBackground("#1e1e2e")
        self.plotItem.getAxis("bottom").setPen("#cdd6f4")
        self.plotItem.getAxis("left").setPen("#cdd6f4")
        self.plotItem.showGrid(x=True, y=True, alpha=0.1)

        # 1. Store multiple curves in a list
        self.curves = []
        self.colors = ["#89b4fa", "#a6e3a1", "#f38ba8", "#fab387", "#cba6f7"]

        # # 2. Add n plots (Example: 3 plots)
        # for i in range(3):
        #     x_data = np.arange(10)
        #     y_data = np.random.randint(1, 25, 10)
        #     color = self.colors[i % len(self.colors)]

        #     # Create curve
        #     curve = self.plot(x_data, y_data,
        #                       pen=pg.mkPen(color, width=2),
        #                       symbol='o', symbolSize=6,
        #                       symbolBrush=color, name=f"Sensor {i+1}")

        #     # Store data inside the curve object for easy retrieval in hover
        #     curve.x_values = x_data
        #     curve.y_values = y_data
        #     self.curves.append(curve)

        # # 3. Enhanced Interactivity
        # self.vLine = pg.InfiniteLine(angle=90, movable=False, pen='#f5e0dc')
        # self.addItem(self.vLine, ignoreBounds=True)

        # # Tracking Label (HTML allows for multiple lines of data)
        # self.label = pg.TextItem(anchor=(0, 1), color='#cdd6f4')
        # self.addItem(self.label)

        # self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=280, slot=self.update_hover)

    def update_hover(self, event):
        pos = event[0]
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
            x = mousePoint.x()

            # 1. Update the vertical line position
            self.vLine.setPos(x)

            # 2. Build the HTML string for the label
            # We can loop through the curves you stored in self.curves
            label_html = f"<div style='background-color: rgba(30, 30, 46, 150); padding: 5px; border: 1px solid #cdd6f4;'>"
            label_html += f"<b style='color: #f5e0dc;'>Time: {x:.2f}</b><br>"

            found_data = False
            for i, curve in enumerate(self.curves):
                # Simple logic: find the y-value closest to the current mouse x
                # This assumes x_data is sorted
                idx = np.searchsorted(curve.x_values, x)
                if 0 <= idx < len(curve.y_values):
                    y_val = curve.y_values[idx]
                    color = self.colors[i % len(self.colors)]
                    label_html += f"<span style='color: {color};'>Sensor {i+1}: {y_val:.2f}</span><br>"
                    found_data = True

            label_html += "</div>"

            # 3. Update label text and position
            if found_data:
                self.label.setHtml(label_html)
                # Position the label slightly offset from the mouse
                self.label.setPos(mousePoint.x(), mousePoint.y())


# class TempPlot(pg.PlotWidget):
#     def __init__(self):
#         super().__init__()
#         pg.setConfigOptions(antialias=True, useOpenGL=True)

#         # Modern Palette
#         self.setBackground('#1e1e2e')
#         self.getAxis('bottom').setPen('#cdd6f4')
#         self.getAxis('left').setPen('#cdd6f4')
#         self.showGrid(x=True, y=True, alpha=0.1)

#         # 1. Store multiple curves in a list
#         self.curves = []
#         self.colors = ['#89b4fa', '#a6e3a1', '#f38ba8', '#fab387', '#cba6f7']

#         # 2. Add n plots (Example: 3 plots)
#         for i in range(3):
#             x_data = np.arange(10)
#             y_data = np.random.randint(1, 25, 10)
#             color = self.colors[i % len(self.colors)]

#             # Create curve
#             curve = self.plot(x_data, y_data,
#                               pen=pg.mkPen(color, width=2),
#                               symbol='o', symbolSize=6,
#                               symbolBrush=color, name=f"Sensor {i+1}")

#             # Store data inside the curve object for easy retrieval in hover
#             curve.x_values = x_data
#             curve.y_values = y_data
#             self.curves.append(curve)

#         # 3. Enhanced Interactivity
#         self.vLine = pg.InfiniteLine(angle=90, movable=False, pen='#f5e0dc')
#         self.addItem(self.vLine, ignoreBounds=True)

#         # Tracking Label (HTML allows for multiple lines of data)
#         self.label = pg.TextItem(anchor=(0, 1), color='#cdd6f4')
#         self.addItem(self.label)

#         self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self.update_hover)

#     def update_hover(self, event):
#         pos = event[0]
#         if self.sceneBoundingRect().contains(pos):
#             mousePoint = self.plotItem.vb.mapSceneToView(pos)
#             x_mouse = mousePoint.x()

#             # Build an HTML string for all plots
#             html_content = "<div style='background-color: #313244; padding: 8px; border: 1px solid #cdd6f4; border-radius: 5px;'>"
#             html_content += f"<b style='color: #f5e0dc;'>X: {x_mouse:.2f}</b><br>"

#             found_data = False
#             for i, curve in enumerate(self.curves):
#                 # Find nearest index
#                 idx = np.searchsorted(curve.x_values, x_mouse)
#                 if 0 <= idx < len(curve.x_values):
#                     x_val = curve.x_values[idx]
#                     y_val = curve.y_values[idx]
#                     color = self.colors[i % len(self.colors)]

#                     html_content += f"<span style='color: {color};'>Plot {i+1}: {y_val:.2f}</span><br>"
#                     found_data = True

#             html_content += "</div>"

#             if found_data:
#                 self.vLine.setPos(x_mouse)
#                 self.label.setHtml(html_content)
#                 self.label.setPos(x_mouse, mousePoint.y())
#                 self.label.show()
#             else:
#                 self.label.hide()
