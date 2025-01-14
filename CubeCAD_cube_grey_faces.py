import tkinter as tk
import math


class CubeRenderer3D:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Cube Renderer")

        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Camera settings
        self.camera = {"zoom": 1.0, "pan_x": 0, "pan_y": 0, "tilt_x": 0, "tilt_y": 0}
        self.last_mouse_pos = None
        self.right_mouse_down = False
        self.middle_mouse_down = False

        # Cube vertices
        self.cube_size = 20
        self.cube_vertices = [
            (-10, -10, -10), (10, -10, -10), (10, 10, -10), (-10, 10, -10),
            (-10, -10, 10), (10, -10, 10), (10, 10, 10), (-10, 10, 10)
        ]

        self.cube_faces = [
            (0, 1, 2, 3),  # Back face
            (4, 5, 6, 7),  # Front face
            (0, 4, 7, 3),  # Left face
            (1, 5, 6, 2),  # Right face
            (0, 1, 5, 4),  # Bottom face
            (3, 2, 6, 7),  # Top face
        ]

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_left_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_left_mouse_drag)
        self.canvas.bind("<ButtonPress-2>", self.on_middle_mouse_press)
        self.canvas.bind("<B2-Motion>", self.on_middle_mouse_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_middle_mouse_release)
        self.canvas.bind("<ButtonPress-3>", self.on_right_mouse_press)
        self.canvas.bind("<B3-Motion>", self.on_right_mouse_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_mouse_release)

        # Draw the initial scene
        self.draw_scene()

    def project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates into 2D for drawing."""
        tilt_x = math.radians(self.camera["tilt_x"])
        tilt_y = math.radians(self.camera["tilt_y"])

        # Rotate around the X-axis (tilt_y)
        x_rot = x
        y_rot = y * math.cos(tilt_y) - z * math.sin(tilt_y)
        z_rot = y * math.sin(tilt_y) + z * math.cos(tilt_y)

        # Rotate around the Y-axis (tilt_x)
        x_proj = x_rot * math.cos(tilt_x) + z_rot * math.sin(tilt_x)
        z_proj = -x_rot * math.sin(tilt_x) + z_rot * math.cos(tilt_x)

        # Apply zoom and pan
        x_screen = x_proj * self.camera["zoom"] + 250 + self.camera["pan_x"]
        y_screen = -y_rot * self.camera["zoom"] + 250 + self.camera["pan_y"]

        return x_screen, y_screen

    def draw_scene(self):
        self.canvas.delete("all")
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

    def on_left_mouse_press(self, event):
        self.last_mouse_pos = (event.x, event.y)

    def on_left_mouse_drag(self, event):
        if self.last_mouse_pos:
            dx = event.x - self.last_mouse_pos[0]
            dy = event.y - self.last_mouse_pos[1]

            # Update tilt
            self.camera["tilt_x"] += dx / 2
            self.camera["tilt_y"] += dy / 2

            self.draw_scene()
            self.last_mouse_pos = (event.x, event.y)

    def on_middle_mouse_press(self, event):
        self.middle_mouse_down = True
        self.last_mouse_pos = (event.x, event.y)

    def on_middle_mouse_drag(self, event):
        if self.middle_mouse_down and self.last_mouse_pos:
            dy = event.y - self.last_mouse_pos[1]

            # Update zoom
            self.camera["zoom"] += -dy / 200
            self.camera["zoom"] = max(0.1, self.camera["zoom"])  # Prevent negative zoom

            self.draw_scene()
            self.last_mouse_pos = (event.x, event.y)

    def on_middle_mouse_release(self, event):
        self.middle_mouse_down = False

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

            self.draw_scene()
            self.last_mouse_pos = (event.x, event.y)

    def on_right_mouse_release(self, event):
        self.right_mouse_down = False


if __name__ == "__main__":
    root = tk.Tk()
    app = CubeRenderer3D(root)
    root.mainloop()
