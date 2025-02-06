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

    '''

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Apply transformations
        glTranslatef(self.pan_x, self.pan_y, 0.0)
        glScalef(self.zoom, self.zoom, 1.0)
        #glRotatef(self.rotation, 0, 0, 1)
        
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
        '''

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
    '''
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
    '''
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

    # Store mouse position
        self.mouse_pos = event.pos()

    # Convert mouse position to grid coordinates
        x = (event.x() / self.width()) * self.grid_size[0]
        y = ((self.height() - event.y()) / self.height()) * self.grid_size[1]
    
        self.hover_cell = (int(x), int(y))
    
        self.last_mouse_pos = event.pos()
        self.update()


    def mousePressEvent(self, event): #this change disables pan and tilt
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
    '''
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
    '''
    def display_mouse_info(self):
        glColor3f(1.0, 1.0, 1.0)
    
    # Display mouse position
        glWindowPos2f(10, 10)
        text = f"Mouse: {self.mouse_pos.x()}, {self.mouse_pos.y()}"
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    # Display grid cell coordinates
        glWindowPos2f(10, 25)
        grid_text = f"Grid Cell: {self.hover_cell}" if self.hover_cell else "Grid Cell: None"
        for char in grid_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    def display_mouse_info(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width(), 0, self.height())  # Set up a 2D projection
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
    
        glDisable(GL_DEPTH_TEST)  # Ensure text is not occluded
        glColor3f(1.0, 1.0, 1.0)  # White text

    # Display mouse position
        glRasterPos2f(10, self.height() - 20)
        text = f"Mouse: {self.last_mouse_pos.x()}, {self.last_mouse_pos.y()}"
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    # Display grid cell coordinates
        glRasterPos2f(10, self.height() - 40)
        grid_text = f"Grid Cell: {self.hover_cell}" if self.hover_cell else "Grid Cell: None"
        for char in grid_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

        glEnable(GL_DEPTH_TEST)  # Re-enable depth testing

    # Restore original projection matrix
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    
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
