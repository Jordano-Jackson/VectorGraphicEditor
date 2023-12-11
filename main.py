import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import colorchooser

class GraphicObject(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self, dx, dy):
        pass

class RectangleObject(GraphicObject):
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.rect_id = self.canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline=color, tags="graphic_object")

    def draw(self):
        pass  # No additional drawing logic for a basic rectangle

    def move(self, dx, dy):
        self.canvas.move(self.rect_id, dx, dy)

class EllipseObject(GraphicObject):
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.ellipse_id = self.canvas.create_oval(x, y, x + width, y + height, fill=color, tags="graphic_object")

    def draw(self):
        pass  # No additional drawing logic for a basic ellipse

    def move(self, dx, dy):
        self.canvas.move(self.ellipse_id, dx, dy)

class VectorGraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Vector Graphic Editor")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.drawing_mode = "rectangle"  # Initial drawing mode
        self.start_x = None
        self.start_y = None
        self.current_object = None

        self.color='black'

        rectangle_button = tk.Button(root, text="Rectangle Mode", command=lambda: self.set_drawing_mode("rectangle"))
        rectangle_button.pack(side=tk.LEFT)


        ellipse_button = tk.Button(root, text="Ellipse Mode", command=lambda: self.set_drawing_mode("ellipse"))
        ellipse_button.pack(side=tk.LEFT)

        rectangle_color_button = tk.Button(root, text="Color", command=self.choose_color)
        rectangle_color_button.pack(side=tk.LEFT)

        self.objects = []  # List to store drawn objects

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)


    def draw_object_drag(self, event, complete=False):
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
        if self.drawing_mode == 'rectangle' :
            self.current_object = self.create_rectangle(
                self.start_x, self.start_y, cur_x, cur_y
            )
        print(self.objects)



    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
    
    def on_drag(self, event):
        self.draw_object_drag(event)

    def on_release(self, event):
        self.draw_object_release(event)

    def set_drawing_mode(self, mode):
        self.drawing_mode = mode
    

    def create_rectangle(self, start_x, start_y, cur_x, cur_y):
        rect = RectangleObject(self.canvas,start_x, start_y, cur_x-start_x, cur_y-start_y, self.color)
        self.objects.append(rect)

    def create_ellipse(self):
        ellipse = EllipseObject(self.canvas, 200, 200, 40, 40, "red")
        self.objects.append(ellipse)
    """
    
    def paint(self, event):
        if self.selected_object:
            x, y = event.x, event.y
            self.selected_object.move(x - self.start_x, y - self.start_y)
            self.start_x, self.start_y = x, y
    

    def select_object(self, event):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y, tags="graphic_object")
        if item:
            self.selected_object = self.get_object_by_id(item[0])
            print("Selected object:", self.selected_object)
            # Add logic to update property window with object properties

    def get_object_by_id(self, obj_id):
        for obj in self.objects:
            if hasattr(obj, "rect_id") and obj.rect_id == obj_id:
                return obj
            elif hasattr(obj, "ellipse_id") and obj.ellipse_id == obj_id:
                return obj
        return None
    """

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]
        

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorGraphicEditor(root)
    root.mainloop()