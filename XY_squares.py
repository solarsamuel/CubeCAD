import tkinter as tk

def create_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            square = tk.Frame(
                grid_canvas, 
                width=SQUARE_SIZE, 
                height=SQUARE_SIZE, 
                bg="white", 
                highlightbackground="black", 
                highlightthickness=1
            )
            square.grid(row=row, column=col)
            
            square.bind("<Enter>", lambda e, r=row, c=col: on_hover(r, c))
            square.bind("<Leave>", lambda e, r=row, c=col: on_leave(r, c))
            square.bind("<Button-1>", lambda e, r=row, c=col: toggle_square(r, c))
            
            grid[row][col] = square

def create_axes():
    # Create the X-axis
    x_axis = tk.Frame(root, width=GRID_SIZE * SQUARE_SIZE + AXIS_EXTENSION, height=AXIS_WIDTH, bg="red")
    x_axis.place(x=PADDING, y=PADDING + GRID_SIZE * SQUARE_SIZE)
    
    # Create the Y-axis
    #y_axis = tk.Frame(root, width=AXIS_WIDTH, height=GRID_SIZE * SQUARE_SIZE + 2 * PADDING + AXIS_EXTENSION, bg="blue")
    #y_axis = tk.Frame(root, width=GRID_SIZE * SQUARE_SIZE + AXIS_EXTENSION, height=AXIS_WIDTH, bg="red")
    #y_axis.place(x=PADDING - AXIS_WIDTH, y=PADDING)
    # Create the Y-axis, shifted up by 80 pixels
    #y_axis = tk.Frame(root, width=AXIS_WIDTH, height=GRID_SIZE * SQUARE_SIZE + 2 * PADDING + AXIS_EXTENSION, bg="blue")
    #y_axis.place(x=PADDING - AXIS_WIDTH, y=PADDING - 100)
    
        # Create the Y-axis, shortened by 40 pixels
    y_axis = tk.Frame(root, width=AXIS_WIDTH, height=GRID_SIZE * SQUARE_SIZE + 2 * PADDING + AXIS_EXTENSION - 40, bg="blue")
    y_axis.place(x=PADDING - AXIS_WIDTH, y=PADDING - 60)

def on_hover(row, col):
    if colors[row][col] == "white":
        grid[row][col].configure(bg="pink")

def on_leave(row, col):
    if colors[row][col] == "white":
        grid[row][col].configure(bg="white")

def toggle_square(row, col):
    if colors[row][col] == "black":
        colors[row][col] = "white"
        grid[row][col].configure(bg="white")
    else:
        colors[row][col] = "black"
        grid[row][col].configure(bg="black")

# Constants
GRID_SIZE = 16
SQUARE_SIZE = 20
PADDING = 40
AXIS_EXTENSION = 20
AXIS_WIDTH = 5

# Initialize Tkinter window
root = tk.Tk()
root.title("CubeCAD 2D")
root.geometry(f"{GRID_SIZE * SQUARE_SIZE + 2 * PADDING}x{GRID_SIZE * SQUARE_SIZE + 2 * PADDING}")

# Create a frame for the grid
grid_canvas = tk.Frame(root, width=GRID_SIZE * SQUARE_SIZE, height=GRID_SIZE * SQUARE_SIZE)
grid_canvas.place(x=PADDING, y=PADDING)

# Initialize grid data structures
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
colors = [["white" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Create the grid
create_grid()
# Create the axes
create_axes()

# Start the main loop
root.mainloop()
