'''
LIMITED LICENSE (ZERO-FIVE LICENSE) – Material contained are free for individual use, commercial use subject to royalty:  Free use of this material is allowed for personal use only.  Credit must be provided to the License owner, Sam Wechsler.  Any commercial use of this material is subject to a 5% royalty on gross income on any sale or transaction which utilizes this material. 
If you download or copy this material then you agree to this. If you remix, transform, or build upon the material, you may not distribute the modified material. Exemptions may be made with Sam Wechsler's consent on a signed waiver. Contact Sam Wechsler with any questions: info@wexventures.net
'''
import sys
import math
import datetime
#from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QAction, QToolBar, QToolButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QAction, QToolBar, QToolButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QFileDialog

from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

glutInit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CubeCAD V1.0")
        self.setGeometry(100, 100, 1000, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.opengl_grid = OpenGLGrid(self)
        self.event_log_widget = QTextEdit()
        self.event_log_widget.setStyleSheet("background-color: #f0f0f0;")        
        # Project log label
        self.event_log_label = QLabel("Project Log")
        #self.event_log_label.setStyleSheet("font-weight: bold;")
        self.event_log_widget.setReadOnly(True)
    
        # Layout
        layout = QVBoxLayout()
        #layout.addWidget(self.event_log_label)
        #layout.addWidget(self.event_log_widget)
        layout.addWidget(self.event_log_label)
        layout.addWidget(self.event_log_widget, 1)        
        container = QWidget()
        container.setLayout(layout)

        # Add to central widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.opengl_grid, 10)
        main_layout.addWidget(container)
        self.central_widget.setLayout(main_layout)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Save Button
        save_button = QToolButton()
        save_button.setText("Save Project Log")
        save_button.clicked.connect(self.save_event_log)
        toolbar.addWidget(save_button)
        
        # Add Upload Project Log Button
        upload_button = QToolButton()
        upload_button.setText("Upload Project Log")
        upload_button.clicked.connect(self.upload_project_log)
        toolbar.addWidget(upload_button)

        self.initUI()

    def initUI(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        self.place_action = QAction("Place Cube", self)
        self.place_action.triggered.connect(self.set_placing_mode)
        toolbar.addAction(self.place_action)

        self.erase_action = QAction("Erase Cube", self)
        self.erase_action.triggered.connect(self.set_erasing_mode)
        toolbar.addAction(self.erase_action)

        # Store action buttons
        self.place_button = toolbar.widgetForAction(self.place_action)
        self.erase_button = toolbar.widgetForAction(self.erase_action)

        self.update_button_styles()

    def set_placing_mode(self):
        self.opengl_grid.set_placing_mode()  # Fix here
        self.update_button_styles()

    def set_erasing_mode(self):
        self.opengl_grid.set_erasing_mode()  # Fix here
        self.update_button_styles()

    

    def update_button_styles(self):
        if self.opengl_grid.placing_mode:
            self.place_button.setStyleSheet("background-color: lightblue;")
            self.erase_button.setStyleSheet("")
        else:
            self.erase_button.setStyleSheet("background-color: lightblue;")
            self.place_button.setStyleSheet("")
    

    def update_event_log(self, text):
        self.event_log_widget.setPlainText(text)
        
    def save_event_log(self):
        """Save the event log to a text file with date and time as filename."""
        filename = datetime.datetime.now().strftime("project_log_%Y-%m-%d_%H-%M-%S.txt")
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Project Log", filename, "Text Files (*.txt);;All Files (*)", options=options)
        if filepath:
            with open(filepath, "w") as file:
                file.write(self.event_log_widget.toPlainText()) 
   

    #UPLOAD PROJECT LOG FILE DIALOG           
    def upload_project_log(self):
        """Upload a Project Log file and update the scene accordingly."""
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Project Log", "", "Text Files (*.txt);;All Files (*)", options=options)
    
        if filepath:
            self.opengl_grid.load_project_log(filepath)

    

    
                
                
                
                   

class OpenGLGrid(QOpenGLWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to MainWindow
        self.grid_size = (16, 16)
        self.cube_positions = set()
        self.hover_cell = None
        self.hover_face = None
        self.zoom = 1.3 #grid zoom
        self.pan_x = -5.0  #x grid offset
        self.pan_y = -8.0  #y grid offset
        self.rot_x = 0
        self.rot_y = 0
        self.last_mouse_pos = QPoint()
        self.panning = False
        self.tilting = False
        self.setMouseTracking(True)
        self.placing_mode = True  # True for placing, False for erasing
        self.event_log = []  # Store event logs


    def set_placing_mode(self):
        self.placing_mode = True

    def set_erasing_mode(self):
        self.placing_mode = False

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
        if event.button() == Qt.LeftButton and self.hover_cell:
            if self.placing_mode:
                if self.hover_cell not in self.cube_positions:  # Avoid duplicate logs
                    self.cube_positions.add(self.hover_cell)
                    self.log_event(f"P({self.hover_cell[0]},{self.hover_cell[1]})")
            else:
                if self.hover_cell in self.cube_positions:  # Only log if it was present
                    self.cube_positions.discard(self.hover_cell)
                    self.log_event(f"E({self.hover_cell[0]},{self.hover_cell[1]})")
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

    def log_event(self, event_str):
        """Log the event and update the event log display"""
        self.event_log.append(f"{len(self.event_log) + 1}: {event_str}")
        #if self.parent():
        #    self.parent().update_event_log("\n".join(self.event_log))
        if self.main_window:  # Ensure reference exists
            self.main_window.update_event_log("\n".join(self.event_log))


    #UPLOAD PROJECT LOG IN GRID
    def load_project_log(self, filepath):
        """Load a project log file, clear the scene, and process commands."""
        self.cube_positions.clear()  # Clear all cubes
        self.event_log.clear()  # Clear the event log

        try:
            with open(filepath, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        self.process_log_entry(line)
            self.update()
        except Exception as e:
            print(f"Error reading file: {e}")


    def process_log_entry(self, entry):
        """Process a log entry to place or erase a cube."""
        parts = entry.split(":")
        if len(parts) == 2:
            action, position = parts
            coords = position.strip("P()").split(",")
        
            if len(coords) == 2:
                try:
                    x, y = map(int, coords)
                    if action == "1":  # Place cube
                        self.cube_positions.add((x, y))
                    elif action == "0":  # Erase cube
                        self.cube_positions.discard((x, y))
                except ValueError:
                    print(f"Invalid coordinates in log: {entry}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    #Q29weXJpZ2h0IFNhbSBXZWNoc2xlcg==
