import pyqtgraph as pg
import numpy as np
from PySide6 import QtWidgets, QtCore
from rgaScanClass import RgaScan

class RGAPlot(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.scans_objects = []

        # self.plot_colours = ['#ff5454','#428bca','#f37735','#5cb85c']
        # self.available_plot_colours = self.plot_colours

        self.x_test_data = np.array([1,2,3,4,5,6,7,8,9,10])
        self.y_test_data = np.array([2,4,6,8,10,12,14,16,18,20])


    def add_plot(self, scan: RgaScan):

        self.scans_objects.append(scan)
        self.plot(scan.amu_vector(), scan.spectra[1], pen = pg.mkPen(scan.colour, width = 2))

    def remove_plot(self, scan: RgaScan):
            
            pass
    
    def change_axis_scale(self, log_mode: bool):
         
         self.getPlotItem().setLogMode(y = log_mode)































































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
