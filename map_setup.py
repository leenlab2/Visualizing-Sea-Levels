"""This module contains the MapArea and Midpoint classes.
Together they represent the points of the map that we are working with.
"""
from typing import Tuple
from dataclasses import dataclass


@dataclass
class MapArea:
    """A map of a certain area.

    Instance Attributes:
        - latitude: the range of the map in latitude
        - longitude: the range of the map in longitude

    Representation Invariants:
        - all(-90 <= l <= 90 for l in self.latitude)
        - self.latitude[0] < self.latitude[1]
        - all(-180 <= l <= 180 for l in self.longitude)
        - self.longitude[0] < self.longitude[1]
    """
    latitude: Tuple[float, float]
    longitude: Tuple[float, float]


@dataclass
class Midpoint:
    """A midpoint in a grid.

    Instance Attributes:
        - coords: the coordinates of this point (latitude, longitude)
        - map: the MapArea that this midpoint is on

    Representation Invariants:
        - self.map_area.latitude[1] <= self.coords[0] <= self.map_area.latitude[1]
        - self.map_area.longitude[1] <= self.coords[1] <= self.map_area.longitude[1]
    """
    coords: Tuple[float, float]
    map_area: MapArea
