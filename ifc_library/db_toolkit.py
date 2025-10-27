import sqlite3
import json
from typing import Any, Dict, Iterable, Optional

from .ifc_manager import IFCElement

class DatabaseToIFCToolkit:
    """Utility class for pulling data from database tables and
    attaching them to :class:`~ifc_library.ifc_manager.IFCElement` instances.

    Each database table is converted into an IFC property set (pset). The
    toolkit also tries to add geometric information to the element by
    calling element specific representation methods if the required
    parameters are present in the fetched table.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    # ------------------------------------------------------------------
    # Database helpers
    def _fetch_row(self, table: str, key: Any, key_column: str) -> Dict[str, Any]:
        """Fetch a single row from *table* identified by *key*.

        Parameters
        ----------
        table: str
            Name of the table to query.
        key: Any
            Value that identifies the desired row.
        key_column: str
            Name of the column that stores the *key*.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table} WHERE {key_column}=?", (key,))
            row = cur.fetchone()
        return dict(row) if row else {}

    # ------------------------------------------------------------------
    def add_psets(self, element: IFCElement, tables: Iterable[str], key: Any,
                  key_column: str = "id") -> None:
        """Add data from multiple *tables* to *element* as property sets.

        Each table is queried for the row identified by ``key`` and the
        resulting column/value pairs are attached as a pset whose name is
        the table name.
        """
        for table in tables:
            data = self._fetch_row(table, key, key_column)
            if data:
                element.add_property_set({table: data})

    # ------------------------------------------------------------------
    def add_geometry(self, element: IFCElement, table: str, key: Any,
                     key_column: str = "id") -> None:
        """Attempt to add geometric representation from a table.

        The method looks for common geometric attributes (``Length``,
        ``Width``, ``Height``, ``Thickness`` and void information). If the
        ``element`` provides a matching representation method (e.g.
        ``add_wall_representation`` or ``add_slab_representation``) it is
        invoked with the retrieved parameters.
        """
        geom_data = self._fetch_row(table, key, key_column)
        if not geom_data:
            return

        length = geom_data.get("Length")
        height = geom_data.get("Height")
        width = geom_data.get("Width")
        thickness = geom_data.get("Thickness")
        voids = geom_data.get("Voids")

        if isinstance(voids, str):
            try:
                voids = json.loads(voids)
            except json.JSONDecodeError:
                voids = None

        # Prefer wall representation when available
        if hasattr(element, "add_wall_representation") and length and height and thickness:
            element.add_wall_representation(length, height, thickness, voids=voids)
        elif hasattr(element, "add_slab_representation") and length and width and height:
            void_count = geom_data.get("Void_Count", 0)
            void_diameter = geom_data.get("Void_Diameter", 0)
            element.add_slab_representation(
                length,
                width,
                height,
                void_count=void_count,
                void_diameter=void_diameter,
            )
        elif hasattr(element, "add_column_representation") and width and thickness and height:
            element.add_column_representation(width, thickness, height)
        elif hasattr(element, "add_beam_representation") and length and width and height:
            element.add_beam_representation(length, width, height)

    # ------------------------------------------------------------------
    def populate_element(self, element: IFCElement, tables: Iterable[str],
                         geom_table: Optional[str], key: Any,
                         key_column: str = "id") -> None:
        """Fetch information from *tables* and attach them to *element*.

        Parameters
        ----------
        element: IFCElement
            The IFC element to populate.
        tables: iterable of str
            Names of data tables to convert into property sets.
        geom_table: str or None
            Name of the table containing geometric data. If ``None`` no
            geometry is added.
        key: Any
            Value that identifies the row to fetch in every table.
        key_column: str, optional
            Name of the identifying column. Defaults to ``"id"``.
        """
        self.add_psets(element, tables, key, key_column)
        if geom_table:
            self.add_geometry(element, geom_table, key, key_column)
