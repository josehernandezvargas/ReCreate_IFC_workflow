import sqlite3
from ifc_library.ifc_manager import IFCManager
from ifc_library.elements.ifc_wall import IFCWall
from ifc_library.db_toolkit import DatabaseToIFCToolkit

# Set up a small temporary SQLite database
DB_PATH = "sample.sqlite"
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE Element (id INTEGER PRIMARY KEY, Name TEXT, Status TEXT)")
    cur.execute("CREATE TABLE Manufacturer (id INTEGER PRIMARY KEY, Company TEXT)")
    cur.execute("CREATE TABLE Geometry (id INTEGER PRIMARY KEY, Length REAL, Height REAL, Thickness REAL)")
    cur.executemany("INSERT INTO Element VALUES (?, ?, ?)", [(1, 'Wall_001', 'Active')])
    cur.executemany("INSERT INTO Manufacturer VALUES (?, ?)", [(1, 'ACME')])
    cur.executemany("INSERT INTO Geometry VALUES (?, ?, ?, ?)", [(1, 1000.0, 3000.0, 200.0)])
    conn.commit()

# Create IFC element and populate from the tables
manager = IFCManager("test_db_toolkit.ifc")
wall = IFCWall(manager, name="Wall_001")
kit = DatabaseToIFCToolkit(DB_PATH)
kit.populate_element(wall, tables=["Element", "Manufacturer"], geom_table="Geometry", key=1)
wall.assign_to_container(manager.storey)
manager.save()
print("IFC file created using database toolkit.")
