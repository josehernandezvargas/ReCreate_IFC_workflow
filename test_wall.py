from ifc_library.ifc_manager import IFCManager
from ifc_library.elements.ifc_wall import IFCWall

def create_wall_from_data(ifc_manager, wall_data):
    """
    Creates an IFC wall element from provided data.

    Args:
        ifc_manager (IFCManager): The IFCManager instance managing the IFC file.
        wall_data (dict): Dictionary containing `element_data` and `geometry_data`.

    Returns:
        IFCWall: The created IFCWall instance.
    """
    # Extract element and geometry data from the input
    element_data = wall_data.get("element_data", {})
    geometry_data = wall_data.get("geometry_data", {})

    # Extract void data if available
    voids = geometry_data.get("Voids", [])

    # Create the wall element
    wall = IFCWall(ifc_manager, name=element_data.get("Wall_ID", "Default Wall"))
    
    # Set the placement (if applicable)
    wall.set_placement()

    # Add wall representation using geometry data, including voids
    wall.add_wall_representation(
        length=geometry_data.get("Length", 5000.0),
        height=geometry_data.get("Height", 3000.0),
        thickness=geometry_data.get("Thickness", 300.0),
        voids=voids
    )

    # Add element and geometry data to the wall
    wall.add_element_data(element_data)
    wall.add_geometry_data(geometry_data)

    # Assign the wall to a storey or other container
    wall.assign_to_container(ifc_manager.storey)

    return wall  # Optionally return the wall object for further manipulation

# Example usage in the script:
if __name__ == "__main__":
    # Create an IFC manager instance
    ifc_manager = IFCManager("test_wall_element.ifc")
    
    # Example wall data with voids
    wall_data = {
        "element_data": {
            "Element_ID": 1,
            "Wall_ID": "Wall_001",
            "Local_ID": "Local_001",
            "Building_ID": "Building_001",
            "Product_ID": "Product_001",
            "Reinf_ID": "Reinf_001",
            "Wall_Type": "Precast Concrete",
            "Wing": "Wing_A",
            "Floor_Num": 1,
            "Orientation": "North",
            "Grid_Pos": "A1",
            "Status": "Active",
            "Storage_Loc": "Location_A",
            "Links": "http://example.com",
            "Notes": "This is a sample wall."
        },
        "geometry_data": {
            "Product_ID": "Product_001",
            "Reinf_Type": "Type_A",
            "Mirrored": False,
            "Count": 1,
            "Height": 2600.0,
            "Length": 3200.0,
            "Thickness": 200.0,
            "Strength_Class": "C30/37",
            "Agg_Size": 20,
            "Drawing": "Drawing_001.png",
            "Geometry_Notes": "Geometry specific notes.",
            "Has_Void": False,
            "Voids": [
                {"X": 400.0, "Z": 0.0, "Width": 800.0, "Height": 2100.0},  # A door void
                {"X": 1800.0, "Z": 900.0, "Width": 1000.0, "Height": 1200.0}   # A window void
            ],
            "Has_ExtPanels": False,
            "Has_Connections": True,
            "Has_Corbel": False
        }
    }

    # Create the wall using the provided data
    create_wall_from_data(ifc_manager, wall_data)

    # Save the IFC file
    ifc_manager.save()
