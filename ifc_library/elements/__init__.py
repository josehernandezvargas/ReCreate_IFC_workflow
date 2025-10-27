"""Convenience imports for available IFC element classes."""

from .ifc_wall import IFCWall
from .ifc_slab import IFCSlab
from .ifc_column import IFCColumn
from .ifc_beam import IFCBeam

__all__ = [
    "IFCWall",
    "IFCSlab",
    "IFCColumn",
    "IFCBeam",
]
