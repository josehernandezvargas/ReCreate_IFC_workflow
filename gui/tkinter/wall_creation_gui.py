import sys
import os

# Add the parent directory of 'ifc_library' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import tkinter as tk
from tkinter import ttk
from ifc_library.ifc_manager import IFCManager
from ifc_library.elements.ifc_wall import IFCWall

class WallCreationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IFC Wall Creation Tool")

        # Variables for wall parameters
        self.length = tk.DoubleVar()
        self.height = tk.DoubleVar()
        self.thickness = tk.DoubleVar()
        self.element_data = {
            'Element_ID': tk.StringVar(),
            'Wall_ID': tk.StringVar(),
            'Local_ID': tk.StringVar(),
            'Building_ID': tk.StringVar(),
            'Product_ID': tk.StringVar(),
            'Reinf_ID': tk.StringVar(),
            'Wall_Type': tk.StringVar(),
            'Wing': tk.StringVar(),
            'Floor_Num': tk.StringVar(),
            'Orientation': tk.StringVar(),
            'Grid_Pos': tk.StringVar(),
            'Status': tk.StringVar(),
            'Storage_Loc': tk.StringVar(),
            'Links': tk.StringVar(),
            'Notes': tk.StringVar()
        }

        self.geometry_data = {
            'Product_ID': tk.StringVar(),
            'Reinf_Type': tk.StringVar(),
            'Mirrored': tk.BooleanVar(value=False),  # Default value
            'Count': tk.IntVar(value=1),  # Default value
            'FootprintPolyline': tk.StringVar(),
            'Height': tk.DoubleVar(),
            'Length': tk.DoubleVar(),
            'Thickness': tk.DoubleVar(),
            'Strength_Class': tk.StringVar(),
            'Agg_Size': tk.StringVar(),
            'Drawing': tk.StringVar(),
            'Geometry_Notes': tk.StringVar(),
            'Has_Void': tk.BooleanVar(value=False),  # Default value
            'Has_ExtPanels': tk.BooleanVar(value=False),  # Default value
            'Has_Connections': tk.BooleanVar(value=False),  # Default value
            'Has_Corbel': tk.BooleanVar(value=False)  # Default value
        }

        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Length, Height, Thickness Inputs (Compulsory Inputs)
        compulsory_frame = ttk.LabelFrame(frame, text="Basic Wall Dimensions (Compulsory)", padding="10")
        compulsory_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        ttk.Label(compulsory_frame, text="Wall Length (mm)*:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(compulsory_frame, textvariable=self.length).grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(compulsory_frame, text="Wall Height (mm)*:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(compulsory_frame, textvariable=self.height).grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(compulsory_frame, text="Wall Thickness (mm)*:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(compulsory_frame, textvariable=self.thickness).grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Element Data Inputs
        element_frame = ttk.LabelFrame(frame, text="Element Data", padding="10")
        element_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        row = 0
        for key, var in self.element_data.items():
            ttk.Label(element_frame, text=f"{key.replace('_', ' ')}:").grid(row=row, column=0, sticky=tk.W)
            ttk.Entry(element_frame, textvariable=var).grid(row=row, column=1, sticky=(tk.W, tk.E))
            row += 1

        # Geometry Data Inputs
        geometry_frame = ttk.LabelFrame(frame, text="Geometry Data", padding="10")
        geometry_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        row = 0
        for key, var in self.geometry_data.items():
            ttk.Label(geometry_frame, text=f"{key.replace('_', ' ')}:").grid(row=row, column=0, sticky=tk.W)
            ttk.Entry(geometry_frame, textvariable=var).grid(row=row, column=1, sticky=(tk.W, tk.E))
            row += 1

        # Create Wall Button
        ttk.Button(frame, text="Create Wall", command=self.create_wall).grid(row=5, column=0, columnspan=2, pady=10)

        # Feedback Label
        self.feedback_label = ttk.Label(frame, text="", foreground="green")
        self.feedback_label.grid(row=6, column=0, columnspan=2)

    def create_wall(self):
        # Create an IFC Manager and Wall Element
        manager = IFCManager("wall_demo.ifc")
        wall = IFCWall(manager, name="Demo Wall")
        wall.add_wall_representation(
            length=self.length.get(),
            height=self.height.get(),
            thickness=self.thickness.get()
        )

        # Add element data
        element_data = {key: var.get() for key, var in self.element_data.items()}
        wall.add_element_data(element_data)

        # Add geometry data
        geometry_data = {key: var.get() for key, var in self.geometry_data.items()}
        wall.add_geometry_data(geometry_data)

        manager.save()

        # Update feedback
        self.feedback_label.config(text=f"Wall created and saved to 'wall_demo.ifc'")

if __name__ == "__main__":
    root = tk.Tk()
    app = WallCreationGUI(root)
    root.mainloop()