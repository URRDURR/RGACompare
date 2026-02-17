import pyqtgraph as pg
import numpy as np
from PySide6 import QtWidgets, QtCore
from rgaScanClass import RgaScan, RgaScanArray

class RGAPlot(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        # self.scans_objects = []

        self.log_mode = False
        self.x_lim_upper = None
        self.x_lim_lower = None
        self.y_lim_upper = None
        self.y_lim_lower = None

        # self.set_plot_theme()

        # self.plot_colours = ['#ff5454','#428bca','#f37735','#5cb85c']
        # self.available_plot_colours = self.plot_colours

        # self.x_test_data = np.array([1,2,3,4,5,6,7,8,9,10])
        # self.y_test_data = np.array([2,4,6,8,10,12,14,16,18,20])


    def replot(self, scans: RgaScanArray):

        # for i, scan in enumerate(scans.scan_files):

        view_box = self.getPlotItem().getViewBox()
        current_range = view_box.viewRange()  # [[xmin, xmax], [ymin, ymax]]

        # set up the variable for limits, apply constants so that they are always initially overwritten
        x_lim_upper = -1
        x_lim_lower = float('inf')
        y_lim_upper = -1
        y_lim_lower = float('inf')
        
        # Clear and replot
        self.clear()

        for i in range(scans.return_scan_file_length()):
            # self.scans_objects.append(scan)
            scan = scans.return_scan_file(i)
            cycle = scan.spectra[len(scan.spectra) - 1]
            self.getPlotItem().plot(scan.amu_vector(), cycle, pen = pg.mkPen(scan.colour, width = 2))

            y_max = np.max(cycle)
            y_min = np.min(cycle, where=(cycle > 0), initial=np.inf)

            if x_lim_upper < scan.stopMass: x_lim_upper = scan.stopMass
            if x_lim_lower > scan.startMass: x_lim_lower = scan.startMass
            if y_lim_upper < y_max: y_lim_upper = y_max
            if y_lim_lower > y_min and y_min > 0:  y_lim_lower = y_min

        self.x_lim_upper = x_lim_upper
        self.x_lim_lower = x_lim_lower
        self.y_lim_upper = y_lim_upper
        self.y_lim_lower = y_lim_lower

        self.set_axis_limits()

        # view_box.setRange(xRange=current_range[0], yRange=current_range[1])
    
    # def add_plot(self, scan: RgaScan):

    #     self.scans_objects.append(scan)
    #     self.getPlotItem().plot(scan.amu_vector(), scan.spectra[1], pen = pg.mkPen(scan.colour, width = 2))

    # def remove_plot(self, scan: RgaScan):
            
    #         pass

    def set_axis_limits(self):
        
        view_box = self.getPlotItem().getViewBox()

        padding_x = (self.x_lim_upper - self.x_lim_lower) * 0.02  # 2% padding
        padding_y = (self.y_lim_upper - self.y_lim_lower) *  0.02

        view_box.setLimits(
            xMin = (self.x_lim_lower - padding_x),
            xMax = (self.x_lim_upper + padding_x),
        )

        print("y_lim_upper:", self.y_lim_upper)
        print("y_lim_lower:", self.y_lim_lower)

        if self.log_mode:
            # For log scale: minimum must be > 0
            # Use 1% of the current max as the minimum
            y_min = (np.log10(self.y_lim_lower))
            y_max = (np.log10(self.y_lim_upper))
            print("y_min:", y_min)
            print("y_max:", y_max)
            
            # Update limits for log scale
            view_box.setLimits(yMin=y_min, yMax=y_max) 
        else:
            # For linear scale: can use 0
            view_box.setLimits(yMin = 0, yMax = self.y_lim_upper + padding_y)

        # self.getPlotItem().autoRange()
    
    def change_axis_scale(self, log_mode: bool):
         
         self.log_mode = log_mode
         if len([item for item in self.listDataItems() if isinstance(item, pg.PlotDataItem)]) != 0:
             self.set_axis_limits()
         self.getPlotItem().setLogMode(y = log_mode)

    def set_plot_theme(self, title="System Telemetry"):
        """
        Main styling method to be called on initialization or reset.
        """

        pg.setConfigOptions(antialias=True, useOpenGL=True)

        self.setBackground('#1e1e2e')
        self.getAxis('bottom').setPen('#cdd6f4')
        self.getAxis('left').setPen('#cdd6f4')
        self.showGrid(x=True, y=True, alpha=0.1)

        # 1. Store multiple curves in a list
        self.curves = []
        self.colors = ['#89b4fa', '#a6e3a1', '#f38ba8', '#fab387', '#cba6f7']
        
        # 2. Add n plots (Example: 3 plots)
        for i in range(3):
            x_data = np.arange(10)
            y_data = np.random.randint(1, 25, 10)
            color = self.colors[i % len(self.colors)]
            
            # Create curve
            curve = self.plot(x_data, y_data, 
                              pen=pg.mkPen(color, width=2),
                              symbol='o', symbolSize=6, 
                              symbolBrush=color, name=f"Sensor {i+1}")
            
            # Store data inside the curve object for easy retrieval in hover
            curve.x_values = x_data
            curve.y_values = y_data
            self.curves.append(curve)

        # 3. Enhanced Interactivity
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen='#f5e0dc')
        self.addItem(self.vLine, ignoreBounds=True)
        
        # Tracking Label (HTML allows for multiple lines of data)
        self.label = pg.TextItem(anchor=(0, 1), color='#cdd6f4')
        self.addItem(self.label)

        self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self.update_hover)








        # # 1. Background and Canvas
        # self.setBackground('#1e1e1e') # Dark Charcoal
        # self.plotItem.showGrid(x=True, y=True, alpha=0.2)
        
        # # 2. Title & Axis Labels
        # # We use HTML-style strings for PyQtGraph labels
        # self.plotItem.setTitle(title, color="#00d4ff", size="14pt", bold=True)
        
        # label_style = {'color': '#999999', 'font-size': '11pt'}
        # self.plotItem.setLabel('left', 'Amplitude', **label_style)
        # self.plotItem.setLabel('bottom', 'Time', **label_style)

        # # 3. Axis Aesthetics
        # # Define a clean pen for the axis lines
        # axis_pen = pg.mkPen(color='#555555', width=1)
        
        # for axis_name in ['left', 'bottom']:
        #     ax = self.getAxis(axis_name)
        #     ax.setPen(axis_pen)
        #     # To change the color of the numbers (ticks), we set the text color 
        #     # via the AxisItem's text pen properties implicitly through setPen
        #     # or explicitly using the following for the labels:
        #     ax.setTextPen('#bbbbbb')

        # # 4. Legend Handling
        # # This creates a hoverable, styled legend box
        # self.plotItem.addLegend(offset=(10, 10), labelTextColor='#eeeeee')


    def update_hover(self, event):
            """
            This is the slot that gets called when the mouse moves.
            'event' is usually a tuple containing the position.
            """
            pos = event[0]
            if self.sceneBoundingRect().contains(pos):
                mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
                # You can now use mousePoint.x() and mousePoint.y()
                print(f"Coordinates: x={mousePoint.x()}, y={mousePoint.y()}")
























































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
