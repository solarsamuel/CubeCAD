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
GRID_SIZE = 4
SQUARE_SIZE = 20

# Initialize Tkinter window
root = tk.Tk()
root.title("Grid View")

# Create a frame for the grid
grid_canvas = tk.Frame(root)
grid_canvas.pack(pady=10)

# Initialize grid data structures
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
colors = [["white" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Create the grid
create_grid()

# Start the main loop
root.mainloop()
