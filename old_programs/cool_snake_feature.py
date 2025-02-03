import tkinter as tk
import math

class CoordinateSystem3D:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Coordinate System")

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.mouse_state_label = tk.Label(root, text="Mouse State: None", font=("Arial", 12))
        self.mouse_state_label.pack()

        self.camera = {"zoom": 1.0, "pan_x": 0, "pan_y": 0, "tilt_x": 0, "tilt_y": 0}
        self.last_mouse_pos = None
        self.right_mouse_down = False
        self.mouse_wheel_pressed = False
    
        self.hovered_square = None  # Track the currently hovered square

        # Bind mouse events
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonPress-3>", self.on_right_mouse_press)
        self.canvas.bind("<B3-Motion>", self.on_right_mouse_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_mouse_release)
        self.canvas.bind("<ButtonPress-2>", self.on_middle_mouse_press)
        self.canvas.bind("<B2-Motion>", self.on_middle_mouse_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_middle_mouse_release)
        
        
        self.draw_scene()

    def draw_scene(self):
        self.canvas.delete("all")
        self.draw_axes()
        self.draw_xy_plane()

    def project_3d_to_2d(self, x, y, z):
        tilt_x = math.radians(self.camera["tilt_x"])
        tilt_y = math.radians(self.camera["tilt_y"])

        x_rot = x
        y_rot = y * math.cos(tilt_y) - z * math.sin(tilt_y)
        z_rot = y * math.sin(tilt_y) + z * math.cos(tilt_y)

        x_proj = x_rot * math.cos(tilt_x) + z_rot * math.sin(tilt_x)
        z_proj = -x_rot * math.sin(tilt_x) + z_rot * math.cos(tilt_x)

        x_screen = x_proj * self.camera["zoom"] + 250 + self.camera["pan_x"]
        y_screen = -y_rot * self.camera["zoom"] + 250 + self.camera["pan_y"]

        return x_screen, y_screen

    def draw_axes(self):
        axes = [
            ((0, 0, 0), (100, 0, 0), "red"),
            ((0, 0, 0), (0, 100, 0), "green"),
            ((0, 0, 0), (0, 0, 100), "blue"),
        ]

        for start, end, color in axes:
            x1, y1 = self.project_3d_to_2d(*start)
            x2, y2 = self.project_3d_to_2d(*end)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def draw_xy_plane(self):
        size = 160
        step = 20
        self.grid_rectangles = []  # Store rectangles for hover detection

        for x in range(-size // 2, size // 2 + 1, step):
            for y in range(-size // 2, size // 2 + 1, step):
                x1, y1 = self.project_3d_to_2d(x, y, 0)
                x2, y2 = self.project_3d_to_2d(x + step, y + step, 0)
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.grid_rectangles.append((rect, x, y))

    def on_mouse_move(self, event):
        hovered = None
        for rect, x, y in self.grid_rectangles:
            coords = self.canvas.coords(rect)
            if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                hovered = rect
                break

        if hovered != self.hovered_square:
            if self.hovered_square:
                self.canvas.itemconfig(self.hovered_square, fill="lightgrey")
            if hovered:
                self.canvas.itemconfig(hovered, fill="pink")
            self.hovered_square = hovered
            
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
            

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateSystem3D(root)
    root.mainloop()
