import tkinter as tk
import math

class CoordinateSystem3D:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Coordinate System")

        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Button and status labels
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.add_cube_button = tk.Button(self.button_frame, text="Add Cube", command=self.toggle_add_cube)
        self.add_cube_button.pack(side=tk.LEFT, padx=5)

        self.delete_cube_button = tk.Button(self.button_frame, text="Delete Cube", command=self.toggle_delete_cube)
        self.delete_cube_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(root, text="Add Cube: OFF | Delete Cube: OFF", font=("Arial", 12))
        self.status_label.pack()

        # Label for displaying mouse state
        self.mouse_state_label = tk.Label(root, text="Mouse State: None", font=("Arial", 12))
        self.mouse_state_label.pack()

        # Initial camera settings
        self.camera = {"zoom": 1.0, "pan_x": 0, "pan_y": 0, "tilt_x": 0, "tilt_y": 0}
        self.last_mouse_pos = None
        self.right_mouse_down = False
        self.mouse_wheel_pressed = False
        
        # Cube vertices
        self.cube_size = 20
        self.cube_vertices = [
            (0, 0, 0), (20, 0, 0), (20, 20, 0), (0, 20, 0),
            (0, 0, 20), (20, 0, 20), (20, 20, 20), (0, 20, 20)
        ]

        self.cube_faces = [
            (0, 1, 2, 3),  # Back face
            (4, 5, 6, 7),  # Front face
            (0, 4, 7, 3),  # Left face
            (1, 5, 6, 2),  # Right face
            (0, 1, 5, 4),  # Bottom face
            (3, 2, 6, 7),  # Top face
        ]
        
        # Cube placement state
        self.add_cube = False
        self.delete_cube = False
        self.cubes = []  # List to store cube positions

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonPress-3>", self.on_right_mouse_press)
        self.canvas.bind("<B3-Motion>", self.on_right_mouse_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_mouse_release)
        self.canvas.bind("<ButtonPress-2>", self.on_middle_mouse_press)
        self.canvas.bind("<B2-Motion>", self.on_middle_mouse_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_middle_mouse_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)  # Track mouse movement

        # Draw the initial scene
        self.draw_scene()

    def draw_scene(self):
        self.canvas.delete("all")
        self.draw_axes()
        self.draw_xy_plane()
        #self.draw_cubes()
        self.draw_cube()

    def draw_cube(self):
        """Draw the cube."""
        # Project all vertices to 2D
        projected_vertices = [self.project_3d_to_2d(*v) for v in self.cube_vertices]

        # Draw each face as a filled polygon
        for face in self.cube_faces:
            face_coords = [projected_vertices[i] for i in face]
            flat_coords = [coord for vertex in face_coords for coord in vertex]
            self.canvas.create_polygon(
                flat_coords, fill="gray", outline="black", width=2
            )

    def project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates into 2D for drawing."""
        tilt_x = math.radians(self.camera["tilt_x"])
        tilt_y = math.radians(self.camera["tilt_y"])

        # Rotate around the X axis (tilt_y)
        x_rot = x
        #y_rot = 2 * y * math.cos(tilt_y) - z * math.sin(tilt_y)
        #y_rot = y * math.cos(tilt_y) - 2 * z * math.sin(tilt_y)
        y_rot = y * math.cos(tilt_y) - z * math.sin(tilt_y)
        #z_rot = 2*y * math.sin(tilt_y) + z * math.cos(tilt_y)
        z_rot = y * math.sin(tilt_y) + z * math.cos(tilt_y)

        # Rotate around the Y axis (tilt_x)
        #x_proj = x_rot * 2* math.cos(tilt_x) + z_rot * math.sin(tilt_x)
        x_proj = x_rot *  math.cos(tilt_x) + z_rot * math.sin(tilt_x)
        z_proj = -x_rot * math.sin(tilt_x) + z_rot * math.cos(tilt_x)

        # Apply zoom and pan to the projected coordinates, making sure tiles stay flat
        x_screen = x_proj * self.camera["zoom"] + 250 + self.camera["pan_x"]
        y_screen = -y_rot * self.camera["zoom"] + 250 + self.camera["pan_y"]


        return x_screen, y_screen

    def draw_axes(self):
        """Draw X, Y, and Z axes."""
        axes = [
            ((0, 0, 0), (100, 0, 0), "red"),  # X-axis
            ((0, 0, 0), (0, 100, 0), "green"),  # Y-axis
            ((0, 0, 0), (0, 0, 100), "blue"),  # Z-axis
        ]

        for start, end, color in axes:
            x1, y1 = self.project_3d_to_2d(*start)
            x2, y2 = self.project_3d_to_2d(*end)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def draw_xy_plane(self):
        """Draw the X-Y plane with tiles."""
        size = 160  # Plane size
        step = 20   # Grid step size
        color = "lightgrey"

        # Draw grid lines on the X-Y plane
        for x in range(-size // 2, size // 2 + 1, step):
            x1, y1 = self.project_3d_to_2d(x, -size // 2, 0)
            x2, y2 = self.project_3d_to_2d(x, size // 2, 0)
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

        for y in range(-size // 2, size // 2 + 1, step):
            x1, y1 = self.project_3d_to_2d(-size // 2, y, 0)
            x2, y2 = self.project_3d_to_2d(size // 2, y, 0)
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

        # Draw the grid tiles (20x20 pixels) in a flat orientation
        for x in range(-size // 2, size // 2, step):
            for y in range(-size // 2, size // 2, step):
                x1, y1 = self.project_3d_to_2d(x, y, 0)
                x2, y2 = self.project_3d_to_2d(x + step, y + step, 0)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white", tags="tile")

    
    
    def on_middle_mouse_press(self, event):
        self.mouse_wheel_pressed = True
        self.last_mouse_pos = (event.x, event.y)
        self.mouse_state_label.config(text="Mouse State: Button Pressed")

    def on_middle_mouse_drag(self, event):
        if self.mouse_wheel_pressed and self.last_mouse_pos:
            dy = event.y - self.last_mouse_pos[1]

            # Zoom in or out based on mouse movement
            zoom_direction = "In" if dy < 0 else "Out"
            self.camera["zoom"] += -dy / 200
            self.camera["zoom"] = max(0.1, self.camera["zoom"])  # Prevent negative zoom

            # Update the label
            self.mouse_state_label.config(text=f"Mouse State: Button Pressed, Zoom {zoom_direction}")

            # Redraw the scene
            self.draw_scene()

            # Update last mouse position
            self.last_mouse_pos = (event.x, event.y)

    def on_middle_mouse_release(self, event):
        self.mouse_wheel_pressed = False
        self.mouse_state_label.config(text="Mouse State: Button Released")
    
    def on_mouse_move(self, event):
        """Highlight tile under mouse cursor."""
        # Get the mouse position
        mouse_x, mouse_y = event.x, event.y

        # Adjust the mouse position relative to the center (250, 250)
        mouse_x -= 90
        mouse_y -= 410

        # Tile size and grid size
        tile_size = 20
        grid_size = 320  # Adjust this size as necessary

        # Calculate the row and column based on the mouse position
        row = mouse_x // tile_size
        col = -mouse_y // tile_size  # Invert Y to align with the correct direction

        # Highlight the tile in pink
        self.canvas.delete("highlight")
    
        # Calculate the 2D coordinates for the tile
        x1, y1 = self.project_3d_to_2d(row * tile_size - grid_size // 2, col * tile_size - grid_size // 2, 0)
        x2, y2 = self.project_3d_to_2d((row + 1) * tile_size - grid_size // 2, (col + 1) * tile_size - grid_size // 2, 0)
    
        # Draw the highlighted tile
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="pink", tags="highlight", state="normal")

    def on_mouse_press(self, event):
        """Handle mouse click on a tile."""
        #if not self.add_cube:
        #    return  # Do nothing if add_cube is off

        # Get the mouse position
        mouse_x, mouse_y = event.x, event.y

        # Adjust the mouse position relative to the center (250, 250)
        mouse_x -= 90
        mouse_y -= 410

        # Tile size and grid size
        tile_size = 20
        grid_size = 320  # Adjust this size as necessary

        # Calculate the row and column based on the mouse position
        row = mouse_x // tile_size
        col = -mouse_y // tile_size  # Invert Y to align with the correct direction

        # Check if the tile is highlighted (pink)
        if self.canvas.itemcget("highlight", "fill") == "pink":
            # Calculate the 2D coordinates for the tile
            x1, y1 = self.project_3d_to_2d(row * tile_size - grid_size // 2, col * tile_size - grid_size // 2, 0)
            x2, y2 = self.project_3d_to_2d((row + 1) * tile_size - grid_size // 2, (col + 1) * tile_size - grid_size // 2, 0)

            # Change the color to black
            #self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", tags="tile")

        # Determine the fill color based on the state
        if self.add_cube:
            fill_color = "black"
        elif self.delete_cube:
            fill_color = "white"
        else:
            return  # Exit if neither state is active

        # Change the color of the tile
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=fill_color, fill=fill_color, tags="tile")

        
    def on_right_mouse_press(self, event):
        self.right_mouse_down = True
        self.last_mouse_pos = (event.x, event.y)
        
    def on_right_mouse_drag(self, event):
        if self.right_mouse_down and self.last_mouse_pos:
            dx = event.x - self.last_mouse_pos[0]
            dy = event.y - self.last_mouse_pos[1]

            # Update pan
            self.camera["pan_x"] += dx
            self.camera["pan_y"] += dy

            # Redraw the scene
            self.draw_scene()

            # Update last mouse position
            self.last_mouse_pos = (event.x, event.y)
            
    def on_right_mouse_release(self, event):
        self.right_mouse_down = False

    def on_mouse_drag(self, event):
        if self.last_mouse_pos:
            dx = event.x - self.last_mouse_pos[0]
            dy = event.y - self.last_mouse_pos[1]

            # Update tilt and pan
            self.camera["tilt_x"] += dx / 2
            self.camera["tilt_y"] += dy / 2

            # Redraw the scene
            self.draw_scene()

            # Update last mouse position
            self.last_mouse_pos = (event.x, event.y)

    def toggle_add_cube(self):
        self.add_cube = not self.add_cube
        if self.add_cube:
            self.delete_cube = False  # Turn off Delete Cube
        self.update_status_label()

    def toggle_delete_cube(self):
        self.delete_cube = not self.delete_cube
        if self.delete_cube:
            self.add_cube = False  # Turn off Add Cube
        self.update_status_label()

    def update_status_label(self):
        add_cube_status = "ON" if self.add_cube else "OFF"
        delete_cube_status = "ON" if self.delete_cube else "OFF"
        self.status_label.config(text=f"Add Cube: {add_cube_status} | Delete Cube: {delete_cube_status}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateSystem3D(root)
    root.mainloop()
