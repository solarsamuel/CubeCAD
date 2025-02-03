import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *


class OpenGLGrid(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 16
        self.cell_size = 1.0
        self.zoom = -20
        self.rotation_x = 90  # Start with an overhead view
        self.rotation_y = 0
        self.last_mouse_pos = None
        self.cubes = set()
        self.hover_cell = None

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glClearColor(1, 1, 1, 1)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h else 1, 0.1, 50)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        self.draw_grid()
        self.draw_cubes()

    def draw_grid(self):
        glColor3f(0, 0, 0)
        for i in range(self.grid_size + 1):
            offset = i * self.cell_size - (self.grid_size * self.cell_size) / 2
            glBegin(GL_LINES)
            glVertex3f(offset, -self.grid_size / 2, 0)
            glVertex3f(offset, self.grid_size / 2, 0)
            glVertex3f(-self.grid_size / 2, offset, 0)
            glVertex3f(self.grid_size / 2, offset, 0)
            glEnd()
        
        if self.hover_cell:
            glColor3f(1, 0.75, 0.8)
            self.draw_square(*self.hover_cell)

    def draw_cubes(self):
        glColor3f(0, 0, 0)
        for cell in self.cubes:
            self.draw_cube(*cell)

    def draw_square(self, x, y):
        size = self.cell_size
        x, y = x * size - (self.grid_size / 2) * size, y * size - (self.grid_size / 2) * size
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0.01)
        glVertex3f(x + size, y, 0.01)
        glVertex3f(x + size, y + size, 0.01)
        glVertex3f(x, y + size, 0.01)
        glEnd()

    def draw_cube(self, x, y):
        size = self.cell_size
        x, y = x * size - (self.grid_size / 2) * size, y * size - (self.grid_size / 2) * size
        glPushMatrix()
        glTranslatef(x + size / 2, y + size / 2, size / 2)
        glutSolidCube(size)
        glPopMatrix()

    def mouseMoveEvent(self, event):
        ray_x, ray_y = self.map_to_grid(event.pos())
        if 0 <= ray_x < self.grid_size and 0 <= ray_y < self.grid_size:
            self.hover_cell = (ray_x, ray_y)
        else:
            self.hover_cell = None
        
        if event.buttons() == Qt.RightButton and self.last_mouse_pos:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.rotation_x += dy * 0.5
            self.rotation_y += dx * 0.5
        
        self.last_mouse_pos = event.pos()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.hover_cell:
            if self.hover_cell in self.cubes:
                self.cubes.remove(self.hover_cell)
            else:
                self.cubes.add(self.hover_cell)
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom += delta * 1.2
        self.update()

    def map_to_grid(self, pos):
        w, h = self.width(), self.height()
        x, y = (pos.x() - w / 2) / (self.cell_size * self.grid_size / 2), (h / 2 - pos.y()) / (self.cell_size * self.grid_size / 2)
        return int((x + 0.5) * self.grid_size), int((y + 0.5) * self.grid_size)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenGL 3D Grid")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = OpenGLGrid()
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
