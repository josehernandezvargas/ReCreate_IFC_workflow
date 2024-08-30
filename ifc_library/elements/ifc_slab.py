from ifc_library.ifc_manager import IFCElement
from ifcopenshell.api import run
import numpy as np

class IFCSlab(IFCElement):
    """
    Represents an IFC Slab element, capable of managing both solid and hollow-core slabs.
    """

    def __init__(self, ifc_manager, name="Slab"):
        super().__init__(ifc_manager, ifc_class="IfcSlab", name=name)

    def add_slab_representation(self, length, width, height, void_count=0, void_diameter=0):
        """
        Adds a geometric representation of the slab, choosing between a solid or hollow-core representation.

        Args:
            length (int): Length of the slab in mm.
            width (int): Width of the slab in mm.
            height (int): Height of the slab in mm.
            void_count (int): Number of voids (cores) in the slab. If 0, the slab is considered solid.
            void_diameter (float): Diameter of the voids in mm. Ignored if void_count is 0.
        """
        if void_count > 0:
            self.add_hollow_core_representation(length, width, height, void_count, void_diameter)
        else:
            self.add_solid_representation(length, width, height)

    def add_solid_representation(self, length, width, height):
        """
        Adds a solid slab geometric representation.

        Args:
            length (int): Length of the slab in mm.
            width (int): Width of the slab in mm.
            height (int): Height of the slab in mm.
        """
        representation_data = {
            'length': length,
            'height': height,
            'thickness': width  # Using "thickness" to represent width as per IFC standards
        }

        # Create and assign the geometric representation to the slab
        representation = run("geometry.add_wall_representation", self.ifc_manager.model, context=self.ifc_manager.body, **representation_data)
        run("geometry.assign_representation", self.ifc_manager.model, product=self.element, representation=representation)

    def add_hollow_core_representation(self, length, width, height, void_count, void_diameter):
        """
        Adds a hollow-core slab geometric representation.

        Args:
            length (int): Length of the slab in mm.
            width (int): Width of the slab in mm.
            height (int): Height of the slab in mm.
            void_count (int): Number of voids (cores) in the slab.
            void_diameter (float): Diameter of the voids in mm.
        """
        profile_polyline = self.create_hollow_core_profile(width, height, void_count, void_diameter)

        # Create and assign the profile-based representation to the slab
        profile_representation = run("geometry.add_profile_representation", self.ifc_manager.model, context=self.ifc_manager.body, profile=profile_polyline, length=length)
        run("geometry.assign_representation", self.ifc_manager.model, product=self.element, representation=profile_representation)

    def create_hollow_core_profile(self, width, height, void_count, void_diameter):
        """
        Creates a 2D profile for a hollow-core slab based on the void count and diameter.

        Args:
            width (int): Width of the slab in mm.
            height (int): Height of the slab in mm.
            void_count (int): Number of voids (cores) in the slab.
            void_diameter (float): Diameter of the voids in mm.

        Returns:
            IfcPolyline: A polyline representing the profile points.
        """
        external_web_thickness = (width - void_count * void_diameter) / (void_count + 1)
        points = []

        x_pos = 0.0
        y_pos = 0.0

        # Start from the bottom left corner
        points.append((x_pos, y_pos))
        y_pos = height

        # Move up to the top left corner
        points.append((x_pos, y_pos))
        x_pos += external_web_thickness

        # Add the arcs representing the voids
        for _ in range(void_count):
            points.append((x_pos, y_pos))
            x_pos += void_diameter + external_web_thickness

        # Complete the profile
        points.append((width, height))
        points.append((width, 0.0))
        points.append((0.0, 0.0))  # Closing the profile

        # Convert points to IfcCartesianPoints
        cartesian_points = [run("geometry.add_cartesian_point", self.ifc_manager.model, coordinates=point) for point in points]
        
        # Create the polyline representation
        profile_polyline = run("geometry.add_polyline", self.ifc_manager.model, points=cartesian_points)

        return profile_polyline


    def add_element_data(self, element_data):
        """
        Adds element-specific data as a property set.

        Args:
            element_data (dict): Dictionary containing element-specific properties.
        """
        properties = {
            "Product_ID": element_data['Product ID'],
            "Reinforcement_ID": element_data['Reinforcement ID'],
            "Count": element_data['Count'],
            "Height": element_data['Height'],
            "Length": element_data['Length'],
            "Width": element_data['Width'],
            "Void_Count": element_data.get('Void Count', 0),  # Default to 0 if not provided
            "Void_Diameter": element_data.get('Void Diameter', 0.0),  # Default to 0.0 if not provided
            "Concrete_Cover": element_data.get('Concrete Cover', 0.0),  # Default to 0.0 if not provided
            "External_Web_Thickness": element_data.get('External Web Thickness', 0.0),  # Default to 0.0 if not provided
            "Concrete_Strength_Class": element_data['Concrete Strength Class'],
            "Max_Aggregate_Size": element_data.get('Max Aggregate Size'),  # Optional, may not be present
            "Drawings": element_data.get('Drawings'),  # Optional, may not be present
            "Notes": element_data.get('Notes')  # Optional, may not be present
        }
        self.add_property_set({"ReC_Pset_SlabElementData": properties})

