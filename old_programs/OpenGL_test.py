import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

class OpenGLWindow(QOpenGLWidget):
    def initializeGL(self):
        """Initialize OpenGL settings."""
        #self.qglClearColor(0.0, 0.0, 0.0, 1.0)  # Black background

    def paintGL(self):
        """Render the scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def resizeGL(self, w, h):
        """Resize the OpenGL viewport."""
        #glViewport(0, 0, w, h)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(OpenGLWindow())
        self.setWindowTitle("OpenGL with PyQt5")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
