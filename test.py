import pyqtgraph as pg

# 1. Global Antialiasing (Makes lines smooth, not jagged)
pg.setConfigOptions(antialias=True, useOpenGL=True)

plot = pg.PlotWidget()

# 2. Modern Palette
# Use "Flat UI" colors instead of standard Red/Green
# Background: #1e1e2e (Mocha), Line: #89b4fa (Sky Blue)
plot.setBackground('#1e1e2e')
plot.getAxis('bottom').setPen('#cdd6f4')
plot.getAxis('left').setPen('#cdd6f4')

# 3. Add a fill under the curve for a modern "Area Chart" look
curve = plot.plot([1, 4, 2, 3, 5], pen=pg.mkPen('#89b4fa', width=3))
brush = pg.mkBrush(137, 180, 250, 50) # Transparent blue
curve.setFillBrush(brush)
curve.setFillLevel(0)