import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QTransform
import math

class GridWidget(QWidget):
    def __init__(self, size=20, parent=None):
        super().__init__(parent)
        self.size = size  # Grid cell size
        self.cols, self.rows = 20, 20  # Grid dimensions
        self.grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.hover_pos = None
        self.zoom = 1.0
        self.pan_offset = QPointF(0, 0)
        self.rotation_x = 0
        self.rotation_y = 0
        self.last_mouse_pos = None
        
        self.setMouseTracking(True)

    def getTransform(self):
        """Returns the current transformation matrix."""
        transform = QTransform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.scale(self.zoom, self.zoom)
        transform.translate(self.pan_offset.x(), self.pan_offset.y())
        transform.rotate(self.rotation_y, Qt.YAxis)  # Side rotation
        transform.rotate(self.rotation_x, Qt.XAxis)  # Up/down tilt
        return transform

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setTransform(self.getTransform(), True)

        for i in range(self.rows):
            for j in range(self.cols):
                x, y = j * self.size, i * self.size
                if self.grid[i][j]:
                    painter.fillRect(x, y, self.size, self.size, QColor('black'))
                elif self.hover_pos == (i, j):
                    painter.fillRect(x, y, self.size, self.size, QColor('pink'))
                painter.drawRect(x, y, self.size, self.size)

    def mouseMoveEvent(self, event):
        # Get inverse transformation to map screen coordinates back to grid coordinates
        inverse_transform = self.getTransform().inverted()[0]
        mouse_pos = inverse_transform.map(QPointF(event.x(), event.y()))

        row, col = int(mouse_pos.y() // self.size), int(mouse_pos.x() // self.size)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.hover_pos = (row, col)
        else:
            self.hover_pos = None

        # Handle rotation
        if event.buttons() == Qt.RightButton and self.last_mouse_pos:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.rotation_x += dy * 0.5  # Up/down tilt
            self.rotation_y += dx * 0.5  # Left/right rotation

        # Handle panning
        if event.buttons() == Qt.MidButton and self.last_mouse_pos:
            self.pan_offset += event.pos() - self.last_mouse_pos

        self.last_mouse_pos = event.pos()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.hover_pos:
            row, col = self.hover_pos
            self.grid[row][col] = not self.grid[row][col]
        self.last_mouse_pos = event.pos()
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom *= math.pow(1.2, delta)
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive 3D-Like Grid")
        self.setGeometry(100, 100, 600, 600)
        self.central_widget = GridWidget()
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
