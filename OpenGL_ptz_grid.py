import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

glutInit()

class OpenGLGrid(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = (16, 16)
        self.cube_positions = set()
        self.hover_cell = None
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rot_x = 0
        self.rot_y = 0
        self.last_mouse_pos = QPoint()
        self.panning = False
        self.tilting = False

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
        glPushMatrix()
        glTranslatef(x + 0.5, y + 0.5, 0.01)
        glColor4f(1.0, 0.75, 0.8, 0.6)
        glBegin(GL_QUADS)
        glVertex3f(-0.5, -0.5, 0)
        glVertex3f(0.5, -0.5, 0)
        glVertex3f(0.5, 0.5, 0)
        glVertex3f(-0.5, 0.5, 0)
        glEnd()
        glPopMatrix()

    def mouseMoveEvent(self, event):
        if self.tilting:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.rot_x += dy * 0.5
            self.rot_y += dx * 0.5
        elif self.panning:
            dx = (event.x() - self.last_mouse_pos.x()) * 0.01
            dy = (event.y() - self.last_mouse_pos.y()) * -0.01
            self.pan_x += dx
            self.pan_y += dy
        
        self.last_mouse_pos = event.pos()
        self.update()

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()
        if event.button() == Qt.LeftButton and self.hover_cell:
            if self.hover_cell in self.cube_positions:
                self.cube_positions.remove(self.hover_cell)
            else:
                self.cube_positions.add(self.hover_cell)
        elif event.button() == Qt.RightButton:
            self.tilting = True
        elif event.button() == Qt.MidButton:
            self.panning = True
        self.update()

    def mouseReleaseEvent(self, event):
        self.tilting = False
        self.panning = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom *= math.pow(1.2, delta)
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive 3D Grid with Cubes")
        self.setGeometry(100, 100, 1000, 600)
        self.central_widget = OpenGLGrid()
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
