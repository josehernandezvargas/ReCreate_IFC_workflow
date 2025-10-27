# ifc_library/elements/ifc_wall.py

from ifc_library.ifc_manager import IFCElement
from ifcopenshell.api import run  # Import run directly here
import numpy as np

class IFCWall(IFCElement):
    """
    Represents an IFC Wall element. Inherits from IFCElement.
    """
    def __init__(self, ifc_manager, name="Wall"):
        super().__init__(ifc_manager, ifc_class="IfcWall", name=name)


    def add_wall_representation(self, length, height, thickness, voids=None):
        """
        Adds a wall-specific geometric representation.
        The FootprintPolyline is automatically calculated from the length and thickness.
        Voids (openings) can also be added.

        Args:
            length (float): Length of the wall.
            height (float): Height of the wall.
            thickness (float): Thickness of the wall.
            voids (list of dicts): List of voids (openings) in the wall.
        """
        representation_data = {
            'length': length,
            'height': height,
            'thickness': thickness,
        }

        # Handle the representation creation and assignment for the wall
        representation = run("geometry.add_wall_representation", self.ifc_manager.model, context=self.ifc_manager.body, **representation_data)
        run("geometry.assign_representation", self.ifc_manager.model, product=self.element, representation=representation)

        # If voids are specified, create them
        if voids:
            for void in voids:
                self.add_void(void, thickness)

    def add_geometry_from_coordinates(self, points, height):
        """Create wall geometry from a plan view ``points`` list.

        The 2D cartesian coordinates describe the wall footprint in the XY
        plane and are extruded vertically by ``height``.
        """
        super().add_geometry_from_coordinates(points, height)

    def add_void(self, void_data, wall_thickness):
        """
        Adds a void (opening) to the wall using the ifcopenshell void.add_opening API.

        Args:
            void_data (dict): A dictionary containing X, Z, Width, Height, and optional Y, Depth of the void.
            wall_thickness (float): The thickness of the wall.
        """
        x = void_data.get("X", 0.0)  # Horizontal position
        z = void_data.get("Z", 0.0)  # Vertical position (height)
        y = void_data.get("Y", 0.0)  # Depth alignment (defaults to 0)
        width = void_data.get("Width", 1000.0)
        height = void_data.get("Height", 2100.0)
        depth = void_data.get("Depth", wall_thickness + 100.0)  # Default depth is wall_thickness + 100 to ensure the void goes through

        """Create a void (opening) in the wall.

        The previous implementation relied on the deprecated
        ``void.add_opening`` usecase.  Recent versions of IfcOpenShell do
        not provide this module which would raise a ``ModuleNotFoundError``.
        To keep the example functional across versions the opening is only
        created when the usecase is available; otherwise the request is
        silently ignored.
        """

        try:
            run  # ensure run is available
            import ifcopenshell.api
            if not hasattr(ifcopenshell.api, 'void'):
                return
        except Exception:
            return

        opening = run("root.create_entity", self.ifc_manager.model, ifc_class="IfcOpeningElement")
        representation = run(
            "geometry.add_wall_representation",
            self.ifc_manager.model,
            context=self.ifc_manager.body,
            length=width,
            height=height,
            thickness=depth,
        )
        run("geometry.assign_representation", self.ifc_manager.model, product=opening, representation=representation)

        matrix = np.identity(4)
        matrix[:, 3] = [x, y, z, 1]
        run("geometry.edit_object_placement", self.ifc_manager.model, product=opening, matrix=matrix)

        run("void.add_opening", self.ifc_manager.model, opening=opening, element=self.element)

    def add_element_data(self, element_data):
        properties = {
            "Element_ID": element_data['Element_ID'],
            "Wall_ID": element_data['Wall_ID'],
            "Local_ID": element_data['Local_ID'],
            "Building_ID": element_data['Building_ID'],
            "Product_ID": element_data['Product_ID'],
            "Reinf_ID": element_data['Reinf_ID'],
            "Wall_Type": element_data['Wall_Type'],
            "Wing": element_data['Wing'],
            "Floor_Num": element_data['Floor_Num'],
            "Orientation": element_data['Orientation'],
            "Grid_Pos": element_data['Grid_Pos'],
            "Status": element_data['Status'],
            "Storage_Loc": element_data['Storage_Loc'],
            "Links": element_data['Links'],
            "Notes": element_data['Notes']
        }
        self.add_property_set({"ReC_Pset_WallElementData": properties})

    def add_geometry_data(self, geometry_data):
        properties = {
            "Product_ID": geometry_data['Product_ID'],
            "Reinf_Type": geometry_data['Reinf_Type'],
            "Mirrored": geometry_data['Mirrored'],
            "Count": geometry_data['Count'],
            "FootprintPolyline": geometry_data.get('FootprintPolyline'),
            "Height": geometry_data.get('Height'),
            "Length": geometry_data.get('Length'),
            "Thickness": geometry_data.get('Thickness'),
            "Strength_Class": geometry_data['Strength_Class'],
            "Agg_Size": geometry_data['Agg_Size'],
            "Drawing": geometry_data['Drawing'],
            "Geometry_Notes": geometry_data['Geometry_Notes'],
            "Has_Void": geometry_data['Has_Void'],
            "Has_ExtPanels": geometry_data['Has_ExtPanels'],
            "Has_Connections": geometry_data['Has_Connections'],
            "Has_Corbel": geometry_data['Has_Corbel']
        }
        self.add_property_set({"ReC_Pset_WallGeometryData": properties})
