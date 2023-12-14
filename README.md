# VectorGraphicEditor

## Description
VectorGraphicEditor is a straightforward vector graphics editor, crafted as a coursework project for COSE457. It's built in Python using Tkinter for the graphical user interface and Pillow for image processing. The editor is a showcase of software design patterns and fundamental graphic manipulation techniques.

## Features
- **Shape Drawing**: Users can draw basic geometric shapes such as rectangles, ellipses, and lines.
- **Text Insertion**: Allows adding text to the canvas.
- **Image Handling**: Supports importing images into the canvas for mixed media creations.
- **Object Manipulation**: Provides functionality to move, resize, and change the colors of objects.
- **Multiselect Capability**: Enables the selection and modification of multiple objects simultaneously.
- **Z-Order Adjustment**: Users can change the stacking order of objects on the canvas.

## Design Patterns
- **Factory Pattern**: Utilized for creating various types of graphic objects.
- **Singleton Pattern**: Ensures a single, consistent state across the application.
- **Command Pattern**: (Planned for future implementation) to allow undo/redo actions.

## Usage

1. **Install Pillow**: The Pillow library is necessary for image processing capabilities. Install it using pip:

   ```bash
   pip install Pillow
   ```

2. **Run the Application**: In the directory containing `main.py`, run the following command:

   ```bash
   python main.py
   ```

3. **Using the GUI**: The graphical interface is intuitive, allowing users to easily create and edit vector graphics. Utilize the toolset to draw shapes, insert text and images, and modify or multiselect various objects for manipulation.

## Developers
