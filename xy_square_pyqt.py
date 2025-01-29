from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QFrame, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# Constants
GRID_SIZE = 16
SQUARE_SIZE = 20
PADDING = 40
AXIS_EXTENSION = 20
AXIS_WIDTH = 5

class CubeGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CubeCAD 2D with PyQt")
        self.setGeometry(100, 100, GRID_SIZE * SQUARE_SIZE + 2 * PADDING, GRID_SIZE * SQUARE_SIZE + 2 * PADDING)

        # Main Layout
        main_layout = QVBoxLayout(self)

        # Create Grid Layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)
        self.grid_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)

        # Store grid colors
        self.colors = [["white" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.squares = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Create the grid
        self.create_grid()

        # Create axes
        self.create_axes()

        # Add grid layout to main layout
        main_layout.addLayout(self.grid_layout)

    def create_grid(self):
        """Creates a GRID_SIZE x GRID_SIZE grid of squares"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                square = QLabel()
                square.setFixedSize(SQUARE_SIZE, SQUARE_SIZE)
                square.setAutoFillBackground(True)
                self.update_square_color(square, "white")

                # Store square reference
                self.squares[row][col] = square

                # Add events
                square.mousePressEvent = lambda event, r=row, c=col: self.toggle_square(r, c)
                square.enterEvent = lambda event, r=row, c=col: self.on_hover(r, c)
                square.leaveEvent = lambda event, r=row, c=col: self.on_leave(r, c)

                # Add to layout
                self.grid_layout.addWidget(square, row, col)

    def create_axes(self):
        """Creates X and Y axes"""
        # X-axis (horizontal red line)
        x_axis = QFrame(self)
        x_axis.setGeometry(PADDING, PADDING + GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE + AXIS_EXTENSION, AXIS_WIDTH)
        x_axis.setStyleSheet("background-color: red;")

        # Y-axis (vertical blue line)
        y_axis = QFrame(self)
        y_axis.setGeometry(PADDING - AXIS_WIDTH, PADDING - 40, AXIS_WIDTH, GRID_SIZE * SQUARE_SIZE + 2 * PADDING + AXIS_EXTENSION - 60)
        y_axis.setStyleSheet("background-color: blue;")

        x_axis.show()
        y_axis.show()

    def update_square_color(self, square, color):
        """Updates QLabel background color"""
        palette = square.palette()
        palette.setColor(QPalette.Window, QColor(color))
        square.setPalette(palette)

    def on_hover(self, row, col):
        """Highlights square when hovered"""
        if self.colors[row][col] == "white":
            self.update_square_color(self.squares[row][col], "pink")

    def on_leave(self, row, col):
        """Reverts hover effect"""
        if self.colors[row][col] == "white":
            self.update_square_color(self.squares[row][col], "white")

    def toggle_square(self, row, col):
        """Toggles black/white on click"""
        if self.colors[row][col] == "black":
            self.colors[row][col] = "white"
            self.update_square_color(self.squares[row][col], "white")
        else:
            self.colors[row][col] = "black"
            self.update_square_color(self.squares[row][col], "black")


if __name__ == "__main__":
    app = QApplication([])
    window = CubeGrid()
    window.show()
    app.exec_()
