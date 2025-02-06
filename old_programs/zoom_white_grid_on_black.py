import sys
import math
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class OpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.grid_size = (10, 10)  # Grid dimensions (10x10)
        self.cell_size = 1.0       # Each cell is 1 unit in OpenGL space
        self.hover_cell = None     # Track the hovered cell
        self.toggled_cells = set() # Stores toggled cubes

        # Camera controls
        self.camera_angle_x = 30   # Camera rotation (X-axis)
        self.camera_angle_y = 30   # Camera rotation (Y-axis)
        self.zoom = -20            # Zoom distance
        self.last_mouse_pos = None

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Dark background

    def resizeGL(self, w, h):
        """Adjusts viewport and projection when window resizes."""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / max(1, h), 0.1, 100)  # 3D Perspective
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """Draw everything."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera setup (Rotate & Zoom)
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.camera_angle_x, 1, 0, 0)
        glRotatef(self.camera_angle_y, 0, 1, 0)

        # Draw the grid
        self.draw_grid()

        # Draw toggled cubes (blue)
        for cell in self.toggled_cells:
            self.draw_cube(cell[0], cell[1], color=(0, 0, 1))  # Blue cubes

        # Highlight hovered cell (pink)
        if self.hover_cell:
            self.draw_cube(self.hover_cell[0], self.hover_cell[1], color=(1, 0.5, 0.5))  # Pink highlight

        self.update()

    def draw_grid(self):
        """Draws the 10x10 grid on the XZ plane."""
        glColor3f(1, 1, 1)  # White grid lines
        glBegin(GL_LINES)
        for i in range(self.grid_size[0] + 1):
            glVertex3f(i * self.cell_size, 0, 0)
            glVertex3f(i * self.cell_size, 0, self.grid_size[1] * self.cell_size)
        for j in range(self.grid_size[1] + 1):
            glVertex3f(0, 0, j * self.cell_size)
            glVertex3f(self.grid_size[0] * self.cell_size, 0, j * self.cell_size)
        glEnd()

    def draw_cube(self, x, z, color):
        """Draws a filled cube at (x, z) on the grid."""
        glColor3f(*color)
        glPushMatrix()
        glTranslatef(x * self.cell_size + 0.5, 0.5, z * self.cell_size + 0.5)  # Centered on grid
        glutSolidCube(self.cell_size * 0.8)  # Cube size slightly smaller than grid cell
        glPopMatrix()

    def mouseMoveEvent(self, event):
        """Tracks mouse movement for hover and camera rotation."""
        if event.buttons() & Qt.LeftButton:
            # Rotate camera with left-click drag
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.camera_angle_x += dy * 0.5
            self.camera_angle_y += dx * 0.5
            self.update()
        else:
            # Detect hovered grid cell
            x, z = self.map_mouse_to_grid(event.x(), event.y())
            if x is not None and z is not None:
                if self.hover_cell != (x, z):
                    self.hover_cell = (x, z)
                    self.update()
            else:
                self.hover_cell = None
                self.update()

        self.last_mouse_pos = event

    def mousePressEvent(self, event):
        """Handles clicking to toggle cubes."""
        if event.button() == Qt.LeftButton and self.hover_cell:
            if self.hover_cell in self.toggled_cells:
                self.toggled_cells.remove(self.hover_cell)  # Toggle off
            else:
                self.toggled_cells.add(self.hover_cell)  # Toggle on
            self.update()
        self.last_mouse_pos = event

    def wheelEvent(self, event):
        """Zoom in/out with the scroll wheel."""
        delta = event.angleDelta().y()
        self.zoom += delta * 0.02  # Adjust zoom sensitivity
        self.update()

    def map_mouse_to_grid(self, x, y):
        """Converts screen coordinates to grid coordinates."""
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)

        winX, winY = x, viewport[3] - y  # Convert to OpenGL coordinates
        depth = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

        if depth == 1.0:
            return None, None  # No depth value means no intersection

        pos = gluUnProject(winX, winY, depth, modelview, projection, viewport)
        gridX = int(pos[0] // self.cell_size)
        gridZ = int(pos[2] // self.cell_size)

        if 0 <= gridX < self.grid_size[0] and 0 <= gridZ < self.grid_size[1]:
            return gridX, gridZ
        return None, None

# Run the application
app = QApplication(sys.argv)
window = OpenGLWidget()
window.resize(600, 600)
window.show()
sys.exit(app.exec_())
