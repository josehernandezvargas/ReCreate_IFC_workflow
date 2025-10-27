# ReCreate_IFC_workflow
IFC workflow for reused precast elements based on IfcOpenShell.

## Database toolkit

The repository now includes a small helper class for turning database
records into IFC property sets.  The `DatabaseToIFCToolkit` loads rows
from multiple tables and attaches their column/value pairs to an
`IFCElement` instance as property sets (psets).  A dedicated geometry
row can also be interpreted in order to build the geometric
representation of the element.

The basic usage pattern is::

```python
from ifc_library.ifc_manager import IFCManager
from ifc_library.elements import IFCWall, IFCSlab, IFCColumn, IFCBeam
from ifc_library.db_toolkit import DatabaseToIFCToolkit

manager = IFCManager("demo.ifc")
wall = IFCWall(manager)

# extract information for element id 1 from three tables and a geometry table
kit = DatabaseToIFCToolkit("my_database.sqlite")
kit.populate_element(wall,
                     tables=["Element", "Manufacturer", "Logistics"],
                     geom_table="Geometry",
                     key=1)
```

Each table is stored as its own pset while the geometry table is used to
generate the representation.  This removes the need for monolithic
parsers that read the whole database at once and allows selective access
to the tables relevant for a particular element.

## Coordinate based geometry

In addition to the simple length/width/height helpers, all element classes
now expose ``add_geometry_from_coordinates``.  The method accepts a list
of 2D Cartesian points describing a projection in one of the principal
planes and extrudes it along the remaining axis.  This makes it possible
to create walls, slabs, columns and beams from arbitrary polylines, in
line with the project's data collection guidelines.
