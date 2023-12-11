import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import colorchooser
import math

class GraphicObject(ABC):
    object_count = 0 # Class-level counter for generating unique names

    @classmethod
    def generate_obj_id(cls):
        cls.object_count += 1
        return f"{cls.__name__}{cls.object_count:03d}"

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self, dx, dy):
        pass

    def get_pos(self):
        return getattr(self, 'x', 0), getattr(self, 'y', 0)
    
    def get_obj_id(self):
        return getattr(self, 'id', 0)


class RectangleObject(GraphicObject):

    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.type = 'Rectangle'
        self.x = x
        self.y = y
        self.rect_id = self.canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline=color, tags="graphic_object")
        self.id = self.generate_obj_id()

    def draw(self):
        pass  # No additional drawing logic for a basic rectangle

    def move(self, dx, dy):
        self.canvas.move(self.rect_id, dx, dy)

class EllipseObject(GraphicObject):
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.ellipse_id = self.canvas.create_oval(x, y, x + width, y + height, fill=color, tags="graphic_object")

    def draw(self):
        pass  # No additional drawing logic for a basic ellipse

    def move(self, dx, dy):
        self.canvas.move(self.ellipse_id, dx, dy)

class VectorGraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Vector Graphic Editor")

        #self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        #self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.mode = "rectangle"  # Initial mode
        self.start_x = None
        self.start_y = None
        self.current_object = None
        self.selected_object = None

        self.color='black'

        # Create a Frame as a container for the bottom buttons
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Mode buttons
        rectangle_button = tk.Button(self.bottom_frame, text="Rectangle Mode", command=lambda: self.set_mode("rectangle"))
        rectangle_button.pack(side=tk.LEFT)

        ellipse_button = tk.Button(self.bottom_frame, text="Ellipse Mode", command=lambda: self.set_mode("ellipse"))
        ellipse_button.pack(side=tk.LEFT)

        rectangle_color_button = tk.Button(self.bottom_frame, text="Color", command=self.choose_color)
        rectangle_color_button.pack(side=tk.LEFT)

        select_button = tk.Button(self.bottom_frame, text="Select", command=lambda: self.set_mode("Select"))
        select_button.pack(side=tk.LEFT)

        # Mode label at the bottom-right
        self.mode_label = tk.Label(self.bottom_frame, text=f"Mode: {self.mode}", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.mode_label.pack(side=tk.RIGHT, fill=tk.X)

        # Create a Frame as a container for the right column
        self.right_column_frame = tk.Frame(root, bg="lightgray", relief=tk.SOLID)
        self.right_column_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Mode label at the bottom-right
        spacer = tk.Frame(self.right_column_frame, height=80, bg='lightgray')
        spacer.pack(side=tk.TOP, fill=tk.X)

        self.select_object_frame = tk.Label(self.right_column_frame, text=f"Selected Object: \nNone", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.select_object_frame.pack(side=tk.TOP, fill=tk.X)


        # Canvas to represent the drawing area
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)


        self.objects = []  # List to store drawn objects

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def draw_object_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        if self.current_object:
            self.canvas.delete(self.current_object)

        self.current_object = self.canvas.create_rectangle(
            self.start_x, self.start_y, cur_x, cur_y, fill=self.color, outline=self.color
        )


    def draw_object_release(self,event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        if self.current_object:
            self.canvas.delete(self.current_object)
        
        # Draw an ellipse, rectangle, or line based on the starting and current points
        if self.mode == 'rectangle' :
            self.current_object = self.create_rectangle(
                self.start_x, self.start_y, cur_x, cur_y
            )

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if self.mode == 'Select':
            self.select_object(event)
    
    def on_drag(self, event):
        if self.mode == 'rectangle' or self.mode == 'ellipse':
            self.draw_object_drag(event)

    def on_release(self, event):
        self.draw_object_release(event)

    def set_mode(self, mode):
        self.mode = mode
        self.update_mode_label()
    
    def create_rectangle(self, start_x, start_y, cur_x, cur_y):
        rect = RectangleObject(self.canvas,start_x, start_y, cur_x-start_x, cur_y-start_y, self.color)
        self.objects.append(rect)

    def create_ellipse(self):
        ellipse = EllipseObject(self.canvas, 200, 200, 40, 40, "red")
        self.objects.append(ellipse)

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]

    def select_object(self, event=None):
        self.mode = 'Select'
        x, y = event.x, event.y
        self.selected_object = self.find_closest(x, y)
        self.update_select_object_frame()

    def find_closest(self, x, y):
        closest_object = None
        min_distance = float('inf')

        for obj in self.objects:
            obj_x, obj_y = obj.get_pos()
            distance = math.sqrt((x - obj_x)**2 + (y - obj_y)**2)

            if distance < min_distance:
                min_distance = distance
                closest_object = obj

        return closest_object


    def update_mode_label(self):
        self.mode_label.config(text=f"Mode: {self.mode}")

    def update_select_object_frame(self):
        self.select_object_frame.config(text=f"Selected Object: \n{self.selected_object.get_obj_id()}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VectorGraphicEditor(root)
    root.mainloop()