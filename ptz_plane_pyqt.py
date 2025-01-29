from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import sys
import math

class CoordinateSystem3D(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Coordinate System")
        self.setGeometry(100, 100, 500, 500)
        
        self.camera = {"zoom": 1.0, "pan_x": 0, "pan_y": 0, "tilt_x": 0, "tilt_y": 0}
        self.last_mouse_pos = None
        
        self.label = QLabel("Use mouse to pan/tilt, scroll to zoom", self)
        self.label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addStretch()
        self.setLayout(layout)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        self.draw_axes(painter)
        self.draw_xy_plane(painter)
        
    def project_3d_to_2d(self, x, y, z):
        tilt_x = math.radians(self.camera["tilt_x"])
        tilt_y = math.radians(self.camera["tilt_y"])
        
        x_rot = x
        y_rot = y * math.cos(tilt_y) - z * math.sin(tilt_y)
        z_rot = y * math.sin(tilt_y) + z * math.cos(tilt_y)
        
        x_proj = x_rot * math.cos(tilt_x) + z_rot * math.sin(tilt_x)
        z_proj = -x_rot * math.sin(tilt_x) + z_rot * math.cos(tilt_x)
        
        x_screen = x_proj * self.camera["zoom"] + self.width() // 2 + self.camera["pan_x"]
        y_screen = -y_rot * self.camera["zoom"] + self.height() // 2 + self.camera["pan_y"]
        
        return int(x_screen), int(y_screen)
    
    def draw_axes(self, painter):
        axes = [
            ((0, 0, 0), (100, 0, 0), Qt.red),
            ((0, 0, 0), (0, 100, 0), Qt.green),
            ((0, 0, 0), (0, 0, 100), Qt.blue),
        ]
        
        for start, end, color in axes:
            x1, y1 = self.project_3d_to_2d(*start)
            x2, y2 = self.project_3d_to_2d(*end)
            painter.setPen(QPen(color, 2))
            painter.drawLine(x1, y1, x2, y2)
    
    def draw_xy_plane(self, painter):
        size, step, color = 160, 20, Qt.lightGray
        painter.setPen(QPen(color, 1))
        
        for x in range(-size // 2, size // 2 + 1, step):
            x1, y1 = self.project_3d_to_2d(x, -size // 2, 0)
            x2, y2 = self.project_3d_to_2d(x, size // 2, 0)
            painter.drawLine(x1, y1, x2, y2)
        
        for y in range(-size // 2, size // 2 + 1, step):
            x1, y1 = self.project_3d_to_2d(-size // 2, y, 0)
            x2, y2 = self.project_3d_to_2d(size // 2, y, 0)
            painter.drawLine(x1, y1, x2, y2)
    
    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.camera["tilt_x"] += dx / 2
            self.camera["tilt_y"] += dy / 2
            self.last_mouse_pos = event.pos()
            self.update()
    
    def wheelEvent(self, event):
        self.camera["zoom"] += event.angleDelta().y() / 1200
        self.camera["zoom"] = max(0.1, self.camera["zoom"])
        self.update()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoordinateSystem3D()
    window.show()
    sys.exit(app.exec_())
