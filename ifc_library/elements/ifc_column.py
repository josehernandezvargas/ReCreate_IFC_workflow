from ifc_library.ifc_manager import IFCElement
from ifcopenshell.api import run

class IFCColumn(IFCElement):
    """Represents an IFC Column element."""

    def __init__(self, ifc_manager, name="Column"):
        super().__init__(ifc_manager, ifc_class="IfcColumn", name=name)

    def add_geometry_from_coordinates(self, points, height):
        """Create column geometry from a cross-section ``points`` list.

        The polyline defines the column profile in the XY plane and is
        extruded by ``height`` along the vertical axis.
        """
        super().add_geometry_from_coordinates(points, height)

    def add_column_representation(self, width, depth, height):
        """Add a simple rectangular column representation.

        Parameters
        ----------
        width: float
            Width of the column cross section.
        depth: float
            Depth (or thickness) of the column cross section.
        height: float
            Height of the column.
        """
        representation_data = {
            "length": width,
            "height": height,
            "thickness": depth,
        }
        representation = run(
            "geometry.add_wall_representation",
            self.ifc_manager.model,
            context=self.ifc_manager.body,
            **representation_data,
        )
        run(
            "geometry.assign_representation",
            self.ifc_manager.model,
            product=self.element,
            representation=representation,
        )

    def add_element_data(self, element_data):
        """Attach element specific information as a property set."""
        properties = {
            "Column_ID": element_data["Column_ID"],
            "Product_ID": element_data["Product_ID"],
            "Type": element_data.get("Type"),
            "Status": element_data.get("Status"),
        }
        self.add_property_set({"ReC_Pset_ColumnElementData": properties})

    def add_geometry_data(self, geometry_data):
        """Attach basic geometric parameters as a property set."""
        properties = {
            "Product_ID": geometry_data["Product_ID"],
            "Width": geometry_data.get("Width"),
            "Depth": geometry_data.get("Depth"),
            "Height": geometry_data.get("Height"),
        }
        self.add_property_set({"ReC_Pset_ColumnGeometryData": properties})
