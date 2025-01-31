
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Call this before any OpenGL drawing
glutInit()

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = (10, 10)  # 10x10 grid
        self.cube_positions = set()  # Store placed cubes
        self.hover_cell = None

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
        gluLookAt(5, -15, 10, 5, 5, 0, 0, 0, 1)
        
        self.draw_grid()
        for pos in self.cube_positions:
            self.draw_cube(pos[0], pos[1])
        
        if self.hover_cell:
            self.draw_highlight(self.hover_cell[0], self.hover_cell[1])
        
        #self.swapBuffers()
    
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
        glColor3f(0.0, 0.0, 1.0)
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
        x, y = event.x(), event.y()
        
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        
        winX = x
        winY = viewport[3] - y
        
        objX, objY, objZ = gluUnProject(winX, winY, 0, modelview, projection, viewport)
        gridX, gridY = int(objX), int(objY)
        
        if 0 <= gridX < self.grid_size[0] and 0 <= gridY < self.grid_size[1]:
            self.hover_cell = (gridX, gridY)
        else:
            self.hover_cell = None
        
        self.update()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.hover_cell:
            self.cube_positions.add(self.hover_cell)
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Grid of Cubes")
        self.setGeometry(100, 100, 800, 600)
        self.glWidget = OpenGLWidget(self)
        self.setCentralWidget(self.glWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
