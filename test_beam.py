from ifc_library.ifc_manager import IFCManager
from ifc_library.elements.ifc_beam import IFCBeam


def create_beam_from_data(ifc_manager, beam_data):
    element_data = beam_data.get("element_data", {})
    geometry_data = beam_data.get("geometry_data", {})

    beam = IFCBeam(ifc_manager, name=element_data.get("Beam_ID", "Default Beam"))
    beam.set_placement()
    beam.add_beam_representation(
        length=geometry_data.get("Length", 4000.0),
        width=geometry_data.get("Width", 200.0),
        height=geometry_data.get("Height", 300.0),
    )

    # Demonstrate coordinate based geometry using the beam profile
    profile = [
        (0.0, 0.0),
        (geometry_data.get("Width", 0.0), 0.0),
        (
            geometry_data.get("Width", 0.0),
            geometry_data.get("Height", 0.0),
        ),
        (0.0, geometry_data.get("Height", 0.0)),
    ]
    beam.add_geometry_from_coordinates(profile, geometry_data.get("Length", 0.0))
    beam.add_element_data(element_data)
    beam.add_geometry_data(geometry_data)
    beam.assign_to_container(ifc_manager.storey)
    return beam


if __name__ == "__main__":
    ifc_manager = IFCManager("test_beam.ifc")
    beam_data = {
        "element_data": {
            "Beam_ID": "Beam_001",
            "Product_ID": "Product_001",
            "Type": "Rectangular",
            "Status": "Active",
        },
        "geometry_data": {
            "Product_ID": "Product_001",
            "Length": 4000.0,
            "Width": 200.0,
            "Height": 300.0,
        },
    }
    create_beam_from_data(ifc_manager, beam_data)
    ifc_manager.save()
