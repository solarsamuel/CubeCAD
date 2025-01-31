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

        # Label for displaying mouse state
        self.mouse_state_label = tk.Label(root, text="Mouse State: None", font=("Arial", 12))
        self.mouse_state_label.pack()

        # Initial camera settings
        self.camera = {"zoom": 1.0, "pan_x": 0, "pan_y": 0, "tilt_x": 0, "tilt_y": 0}
        self.last_mouse_pos = None
        self.right_mouse_down = False
        self.mouse_wheel_pressed = False
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonPress-3>", self.on_right_mouse_press)
        self.canvas.bind("<B3-Motion>", self.on_right_mouse_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_mouse_release)
        self.canvas.bind("<ButtonPress-2>", self.on_middle_mouse_press)
        self.canvas.bind("<B2-Motion>", self.on_middle_mouse_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_middle_mouse_release)

        # Draw the initial scene
        self.draw_scene()

    def draw_scene(self):
        self.canvas.delete("all")
        self.draw_axes()
        self.draw_xy_plane()

    def project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates into 2D for drawing."""
        tilt_x = math.radians(self.camera["tilt_x"])
        tilt_y = math.radians(self.camera["tilt_y"])

        # Rotate around the X axis (tilt_y)
        x_rot = x
        y_rot = y * math.cos(tilt_y) - z * math.sin(tilt_y)
        z_rot = y * math.sin(tilt_y) + z * math.cos(tilt_y)

        # Rotate around the Y axis (tilt_x)
        x_proj = x_rot * math.cos(tilt_x) + z_rot * math.sin(tilt_x)
        z_proj = -x_rot * math.sin(tilt_x) + z_rot * math.cos(tilt_x)

        # Apply zoom and pan
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
        """Draw the X-Y plane."""
        size = 320  # Plane size
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

    def on_mouse_press(self, event):
        self.last_mouse_pos = (event.x, event.y)

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

    def on_canvas_click(self, event):
        if self.add_cube:
            # Snap to grid
            grid_size = 20
            x = round((event.x - 250) / grid_size) * grid_size
            y = round((250 - event.y) / grid_size) * grid_size
            self.cubes.append((x, y))
            self.draw_scene()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateSystem3D(root)
    root.mainloop()
