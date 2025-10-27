from ifc_library.ifc_manager import IFCManager
from ifc_library.elements.ifc_column import IFCColumn


def create_column_from_data(ifc_manager, column_data):
    element_data = column_data.get("element_data", {})
    geometry_data = column_data.get("geometry_data", {})

    column = IFCColumn(ifc_manager, name=element_data.get("Column_ID", "Default Column"))
    column.set_placement()
    column.add_column_representation(
        width=geometry_data.get("Width", 300.0),
        depth=geometry_data.get("Depth", 300.0),
        height=geometry_data.get("Height", 3000.0),
    )

    # Demonstrate coordinate based geometry using the column profile
    profile = [
        (0.0, 0.0),
        (geometry_data.get("Width", 0.0), 0.0),
        (
            geometry_data.get("Width", 0.0),
            geometry_data.get("Depth", 0.0),
        ),
        (0.0, geometry_data.get("Depth", 0.0)),
    ]
    column.add_geometry_from_coordinates(profile, geometry_data.get("Height", 0.0))
    column.add_element_data(element_data)
    column.add_geometry_data(geometry_data)
    column.assign_to_container(ifc_manager.storey)
    return column


if __name__ == "__main__":
    ifc_manager = IFCManager("test_column.ifc")
    column_data = {
        "element_data": {
            "Column_ID": "Column_001",
            "Product_ID": "Product_001",
            "Type": "Rectangular",
            "Status": "Active",
        },
        "geometry_data": {
            "Product_ID": "Product_001",
            "Width": 300.0,
            "Depth": 300.0,
            "Height": 3000.0,
        },
    }
    create_column_from_data(ifc_manager, column_data)
    ifc_manager.save()
