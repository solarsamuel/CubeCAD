import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QMouseEvent
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

glutInit()

class GridOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.grid_size = 10  # Number of rows and columns
        self.cell_size = 0.2  # Size of each grid cell
        self.mouse_pos = QPointF(0, 0)
        self.hovered_cell = None
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.rotation = 0.0
        self.setMouseTracking(True)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Apply transformations
        glTranslatef(self.pan_x, self.pan_y, 0.0)
        glScalef(self.zoom, self.zoom, 1.0)
        glRotatef(self.rotation, 0, 0, 1)
        
        # Draw the grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = (i - self.grid_size / 2) * self.cell_size
                y = (j - self.grid_size / 2) * self.cell_size
                
                if self.hovered_cell == (i, j):
                    glColor3f(1.0, 0.75, 0.8)  # Highlight color
                else:
                    glColor3f(1.0, 1.0, 1.0)  # Default color
                
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + self.cell_size, y)
                glVertex2f(x + self.cell_size, y + self.cell_size)
                glVertex2f(x, y + self.cell_size)
                glEnd()
        
        self.display_mouse_info()
        self.update()
    
    def display_mouse_info(self):
        # Set text color and position
        #glColor3f(1.0, 1.0, 1.0)
        glColor3f(0.0, 0.0, 0.0)
        glWindowPos2f(10, 10)
        text = f"Mouse: {self.mouse_pos.x():.2f}, {self.mouse_pos.y():.2f}"
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
        
        glWindowPos2f(10, 25)
        grid_text = "Grid Cell: " + (f"{self.hovered_cell}" if self.hovered_cell else "None")
        for char in grid_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    def mouseMoveEvent(self, event: QMouseEvent):
        self.mouse_pos = event.localPos()
        self.update_hovered_cell()
        self.update()
    
    def update_hovered_cell(self):
        x = (self.mouse_pos.x() / self.width()) * 2 - 1
        y = 1 - (self.mouse_pos.y() / self.height()) * 2
        
        grid_x = int((x + self.grid_size * self.cell_size / 2) / self.cell_size)
        grid_y = int((y + self.grid_size * self.cell_size / 2) / self.cell_size)
        
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            self.hovered_cell = (grid_x, grid_y)
        else:
            self.hovered_cell = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GridOpenGLWidget()
    window.show()
    sys.exit(app.exec_())
