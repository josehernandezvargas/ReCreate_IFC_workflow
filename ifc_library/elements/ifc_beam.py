from ifc_library.ifc_manager import IFCElement
from ifcopenshell.api import run

class IFCBeam(IFCElement):
    """Represents an IFC Beam element."""

    def __init__(self, ifc_manager, name="Beam"):
        super().__init__(ifc_manager, ifc_class="IfcBeam", name=name)

    def add_geometry_from_coordinates(self, points, length):
        """Create beam geometry from a cross-section ``points`` list.

        The polyline defines the beam profile in the XY plane and is
        extruded along the beam's axis by ``length``.
        """
        super().add_geometry_from_coordinates(points, length)

    def add_beam_representation(self, length, width, height):
        """Add a simple rectangular beam representation."""
        representation_data = {
            "length": length,
            "height": height,
            "thickness": width,
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
        properties = {
            "Beam_ID": element_data["Beam_ID"],
            "Product_ID": element_data["Product_ID"],
            "Type": element_data.get("Type"),
            "Status": element_data.get("Status"),
        }
        self.add_property_set({"ReC_Pset_BeamElementData": properties})

    def add_geometry_data(self, geometry_data):
        properties = {
            "Product_ID": geometry_data["Product_ID"],
            "Length": geometry_data.get("Length"),
            "Width": geometry_data.get("Width"),
            "Height": geometry_data.get("Height"),
        }
        self.add_property_set({"ReC_Pset_BeamGeometryData": properties})
