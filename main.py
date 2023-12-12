import math

import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import colorchooser
from tkinter import messagebox

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

    def get_obj_pos(self):
        return getattr(self, 'x', 0), getattr(self, 'y', 0)
    
    def get_obj_id(self):
        return getattr(self, 'id', 0)
    
    def get_obj_color(self):
        return getattr(self, 'color', 0)
    
    def get_obj_center(self):
        c_x = getattr(self,'x',0) + getattr(self,'width',0)*0.5
        c_y = getattr(self,'y', 0) + getattr(self,'height',0)*0.5
        return c_x,c_y
    
    def set_obj_pos(self, x, y):
        self.x = x
        self.y = y
        self.draw()


class RectangleObject(GraphicObject):

    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.type = 'Rectangle'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect_id = None
        self.id = self.generate_obj_id()
        self.draw()

    def draw(self):
        if self.rect_id is not None:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline=self.color, tags="graphic_object")

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
        self.selected_objects = []

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

        select_button = tk.Button(self.bottom_frame, text="Select", command=lambda: self.set_mode("select"))
        select_button.pack(side=tk.LEFT)

        multiselect_button = tk.Button(self.bottom_frame, text="Multiselect", command=lambda: self.set_mode("multiselect"))
        multiselect_button.pack(side=tk.LEFT)

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

        spacer2 = tk.Frame(self.right_column_frame, height=20, bg='lightgray')
        spacer2.pack(side=tk.TOP, fill=tk.X)
        self.select_object_color_frame = tk.Label(self.right_column_frame, text=f"Object Color: \nNone", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.select_object_color_frame.pack(side=tk.TOP, fill=tk.X)

        spacer3 = tk.Frame(self.right_column_frame, height=20, bg='lightgray')
        spacer3.pack(side=tk.TOP, fill=tk.X)
        self.select_object_pos_frame = tk.Label(self.right_column_frame, text=f"Object Position: \nNone", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.select_object_pos_frame.pack(side=tk.TOP, fill=tk.X)

        # Selected object color modifier
        spacer4 = tk.Frame(self.right_column_frame, height=20, bg='lightgray')
        spacer4.pack(side=tk.TOP, fill=tk.X)
        self.color_button = tk.Button(self.right_column_frame, text="Change objects color", command=self.choose_color)
        self.color_button.pack(side=tk.TOP)

        # Create a button that opens the number input window
        spacer4 = tk.Frame(self.right_column_frame, height=20, bg='lightgray')
        spacer4.pack(side=tk.TOP, fill=tk.X)
        self.number_button = tk.Button(self.right_column_frame, text="Change the position", command=self.open_number_input)
        self.number_button.pack()

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
        
        if self.mode == 'rectangle' or self.mode == 'ellipse':
            self.current_object = self.canvas.create_rectangle(
                self.start_x, self.start_y, cur_x, cur_y, fill=self.color, outline=self.color
            )
        elif self.mode == 'multiselect':
            self.current_object = self.canvas.create_rectangle(
                self.start_x, self.start_y, cur_x, cur_y, outline='black',dash=(2, 2)
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

        if self.mode == 'select':
            self.select_object(event)
    
    def on_drag(self, event):
        if self.mode == 'rectangle' or self.mode == 'ellipse' or self.mode == 'multiselect':
            self.draw_object_drag(event)

    def on_release(self, event):
        if self.mode == 'rectangle' or self.mode == 'ellipse':
            self.draw_object_release(event)
        elif self.mode == 'multiselect':
            self.multiselect_object(event)

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

    ## Select one object
    def select_object(self, event=None):
        self.mode = 'select'
        x, y = event.x, event.y
        self.selected_objects = [self.find_closest(x, y)]
        self.update_select_object_frame()
        self.update_select_object_color_frame()
        self.update_select_object_pos_frame()

    def find_closest(self, x, y):
        closest_object = None
        min_distance = float('inf')

        for obj in self.objects:
            obj_x, obj_y = obj.get_obj_center()
            distance = math.sqrt((x - obj_x)**2 + (y - obj_y)**2)

            if distance < min_distance:
                min_distance = distance
                closest_object = obj

        return closest_object
    

    ## Multiselect objects
    def multiselect_object(self, event=None):
        cur_x, cur_y = event.x, event.y
        self.selected_objects = []
        min_x = min(cur_x, self.start_x)
        max_x = max(cur_x, self.start_x)
        min_y = min(cur_y, self.start_y)
        max_y = max(cur_y, self.start_y)

        if self.current_object: # Remove existing boundary box
            self.canvas.delete(self.current_object)

        for obj in self.objects :
            obj_x, obj_y = obj.get_obj_center()
            if obj_x >= min_x and obj_x <= max_x and obj_y >= min_y and obj_y <= max_y :
                self.selected_objects.append(obj)
        self.update_select_object_frame()
        self.update_select_object_color_frame()
        self.update_select_object_pos_frame()

    ## modifying the position of selected object 
    def open_number_input(self):
        # Create a new window for number input
        input_window = tk.Toplevel(self.root)
        input_window.title("Number Input")

        # Create two entry fields for entering numbers
        label1 = tk.Label(input_window, text="Enter the first number:")
        label1.pack()
        entry1 = tk.Entry(input_window)
        entry1.pack()

        label2 = tk.Label(input_window, text="Enter the second number:")
        label2.pack()
        entry2 = tk.Entry(input_window)
        entry2.pack()

        # Create a button to submit the numbers
        submit_button = tk.Button(input_window, text="Submit", command=lambda: self.close_on_submit(entry1.get(), entry2.get(), input_window))
        submit_button.pack()

    def close_on_submit(self, num1, num2, window):
        if self.get_numbers(num1, num2):
            window.destroy()

    def get_numbers(self, x, y):
        try:
            x = float(x)
            y = float(y)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers.")
            return False
        
        if len(self.objects) > 1 :
            messagebox.showwarning("The position can be changed when only one object is selected.")

        else:
            self.objects[0].set_obj_pos(x, y)
        return True
    

    ## Update View methods
    def update_mode_label(self):
        self.mode_label.config(text=f"Mode: {self.mode}")

    def update_select_object_frame(self):
        self.select_object_frame.config(text=f"Selected Object:\n" + "\n".join([obj.get_obj_id() for obj in self.selected_objects]))

    def update_select_object_color_frame(self):
        self.select_object_color_frame.config(text=f"Object Color:\n" + "\n".join([obj.get_obj_color() for obj in self.selected_objects]))

    def update_select_object_pos_frame(self):
        self.select_object_pos_frame.config(text=f"Object Position:\n" + "\n".join([str(obj.get_obj_pos()) for obj in self.selected_objects]))

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorGraphicEditor(root)
    root.mainloop()