import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

glutInit()

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = (10, 10)
        self.cube_positions = set()
        self.hover_cell = None
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rot_x = -45
        self.rot_y = 0
        self.last_mouse_pos = QPoint()
        self.panning = False
        self.tilting = False
        self.mouse_position_label = None

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.2, 0.2, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, -20 * self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        
        self.draw_grid()
        for pos in self.cube_positions:
            self.draw_cube(pos[0], pos[1])
        if self.hover_cell:
            self.draw_highlight(self.hover_cell[0], self.hover_cell[1])

    def draw_grid(self):
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)
        for i in range(self.grid_size[0] + 1):
            glVertex3f(i, 0, 0)
            glVertex3f(i, self.grid_size[1], 0)
        for j in range(self.grid_size[1] + 1):
            glVertex3f(0, j, 0)
            glVertex3f(self.grid_size[0], j, 0)
        glEnd()

    def draw_cube(self, x, y):
        glPushMatrix()
        glTranslatef(x + 0.5, y + 0.5, 0.5)
        glColor3f(0.5, 0.5, 0.5)
        glutSolidCube(1)
        glPopMatrix()

    def draw_highlight(self, x, y):
        glColor4f(1.0, 0.4, 0.7, 0.5)
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0.01)
        glVertex3f(x + 1, y, 0.01)
        glVertex3f(x + 1, y + 1, 0.01)
        glVertex3f(x, y + 1, 0.01)
        glEnd()

    def mouseMoveEvent(self, event):
        if self.tilting:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.rot_x += dy * 0.5
            self.rot_y += dx * 0.5
        elif self.panning:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.pan_x += dx * 0.05
            self.pan_y -= dy * 0.05
        else:
            x, y = event.x() // 40, (self.height() - event.y()) // 40  # Corrected grid position
            if 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]:
                self.hover_cell = (x, y)
                if self.mouse_position_label:
                    self.mouse_position_label.setText(f"Mouse Grid Position: ({x}, {y})")
            else:
                self.hover_cell = None
        
        self.last_mouse_pos = event.pos()
        self.update()

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()
        if event.button() == Qt.MiddleButton:
            self.panning = True
        elif event.button() == Qt.RightButton:
            self.tilting = True
        elif event.button() == Qt.LeftButton and self.hover_cell:
            if self.hover_cell in self.cube_positions:
                self.cube_positions.remove(self.hover_cell)
            else:
                self.cube_positions.add(self.hover_cell)
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.panning = False
        elif event.button() == Qt.RightButton:
            self.tilting = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom *= math.pow(1.1, delta)
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Grid of Cubes")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.glWidget = OpenGLWidget(self)
        self.layout.addWidget(self.glWidget)
        
        self.mouse_position_label = QLabel("Mouse Grid Position: (-, -)")
        self.layout.addWidget(self.mouse_position_label)
        
        self.glWidget.mouse_position_label = self.mouse_position_label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
