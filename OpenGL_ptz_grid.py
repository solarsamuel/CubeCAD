'''
LIMITED LICENSE (ZERO-FIVE LICENSE) – Material contained are free for individual use, commercial use subject to royalty:  Free use of this material is allowed for personal use only.  Credit must be provided to the License owner, Sam Wechsler.  Any commercial use of this material is subject to a 5% royalty on gross income on any sale or transaction which utilizes this material. 
If you download or copy this material then you agree to this. If you remix, transform, or build upon the material, you may not distribute the modified material. Exemptions may be made with Sam Wechsler's consent on a signed waiver. Contact Sam Wechsler with any questions: info@wexventures.net
'''
import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

glutInit()


class OpenGLGrid(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = (16, 16)
        self.cube_positions = set()
        self.hover_cell = None
        self.hover_face = None
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rot_x = 0
        self.rot_y = 0
        self.last_mouse_pos = QPoint()
        self.panning = False
        self.tilting = False
        self.setMouseTracking(True)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 1.0, 200.0)
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
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            self.draw_highlight(self.hover_cell[0], self.hover_cell[1])
            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)

    def draw_grid(self):
        glColor3f(0.0, 0.0, 0.0)
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

        # Draw solid cube (gray)
        glColor3f(0.5, 0.5, 0.5)
        glutSolidCube(1)

        # Draw black edges
        glColor3f(0.0, 0.0, 0.0)
        glutWireCube(1.02)

        glPopMatrix()

    def draw_highlight(self, x, y):
        glPushMatrix()
        glTranslatef(x + 0.5, y + 0.5, 0.01)
        glDisable(GL_DEPTH_TEST)
        glColor4f(1.0, 0.75, 0.8, 0.6)  # Pink with transparency

        glBegin(GL_QUADS)
        glVertex3f(-0.5, -0.5, 0)
        glVertex3f(0.5, -0.5, 0)
        glVertex3f(0.5, 0.5, 0)
        glVertex3f(-0.5, 0.5, 0)
        glEnd()

        glEnable(GL_DEPTH_TEST)
        glPopMatrix()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()

        if self.tilting:
            self.rot_x += dy * 0.5
            self.rot_y += dx * 0.5
        elif self.panning:
            self.pan_x += dx * 0.01
            self.pan_y += -dy * 0.01

        self.makeCurrent()

        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)

        x = event.x()
        y = viewport[3] - event.y()

        near_x, near_y, near_z = gluUnProject(x, y, 0, modelview, projection, viewport)
        far_x, far_y, far_z = gluUnProject(x, y, 1, modelview, projection, viewport)

        t = -near_z / (far_z - near_z) if (far_z - near_z) != 0 else 0
        world_x = near_x + t * (far_x - near_x)
        world_y = near_y + t * (far_y - near_y)

        grid_x = int(math.floor(world_x))
        grid_y = int(math.floor(world_y))

        if 0 <= grid_x < self.grid_size[0] and 0 <= grid_y < self.grid_size[1]:
            self.hover_cell = (grid_x, grid_y)
        else:
            self.hover_cell = None

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
        self.zoom = max(0.1, min(self.zoom * math.pow(1.2, delta), 50.0))
        self.update()

    def display_mouse_info(self):
        glColor3f(1.0, 1.0, 1.0)
        glWindowPos2f(10, 10)
        text = f"Mouse: {self.mouse_pos.x()}, {self.mouse_pos.y()}"
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

        glWindowPos2f(10, 25)
        grid_text = f"Grid Cell: {self.hover_cell}" if self.hover_cell else "Grid Cell: None"
        for char in grid_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))


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
    #Q29weXJpZ2h0IFNhbSBXZWNoc2xlcg==
