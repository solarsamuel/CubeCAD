from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF
import sys
import math

class CoordinateSystem3D(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Coordinate System")
        self.setFixedSize(500, 500)
        
        self.camera = {"zoom": 1.0, "pan_x": 0, "pan_y": 0, "tilt_x": 0, "tilt_y": 0}
        self.last_mouse_pos = None
        self.right_mouse_down = False
        self.middle_mouse_down = False
        
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

        x_screen = x_proj * self.camera["zoom"] + 250 + self.camera["pan_x"]
        y_screen = -y_rot * self.camera["zoom"] + 250 + self.camera["pan_y"]

        return QPointF(x_screen, y_screen)
    
    def draw_axes(self, painter):
        axes = [
            ((0, 0, 0), (100, 0, 0), Qt.red),  
            ((0, 0, 0), (0, 100, 0), Qt.green),  
            ((0, 0, 0), (0, 0, 100), Qt.blue),  
        ]

        pen = QPen()
        pen.setWidth(2)
        
        for start, end, color in axes:
            pen.setColor(color)
            painter.setPen(pen)
            p1 = self.project_3d_to_2d(*start)
            p2 = self.project_3d_to_2d(*end)
            painter.drawLine(p1, p2)
    
    def draw_xy_plane(self, painter):
        size = 160
        step = 20
        color = Qt.lightGray

        pen = QPen(color)
        painter.setPen(pen)
        
        for x in range(-size // 2, size // 2 + 1, step):
            p1 = self.project_3d_to_2d(x, -size // 2, 0)
            p2 = self.project_3d_to_2d(x, size // 2, 0)
            painter.drawLine(p1, p2)

        for y in range(-size // 2, size // 2 + 1, step):
            p1 = self.project_3d_to_2d(-size // 2, y, 0)
            p2 = self.project_3d_to_2d(size // 2, y, 0)
            painter.drawLine(p1, p2)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.right_mouse_down = True
        elif event.button() == Qt.MiddleButton:
            self.middle_mouse_down = True
        self.last_mouse_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()

            if self.right_mouse_down:
                self.camera["tilt_x"] += dx / 2
                self.camera["tilt_y"] += dy / 2
            elif self.middle_mouse_down:
                self.camera["pan_x"] += dx
                self.camera["pan_y"] += dy
            
            self.last_mouse_pos = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.right_mouse_down = False
        elif event.button() == Qt.MiddleButton:
            self.middle_mouse_down = False
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.camera["zoom"] *= 1.1 ** delta
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Coordinate System")
        self.setCentralWidget(CoordinateSystem3D())
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
