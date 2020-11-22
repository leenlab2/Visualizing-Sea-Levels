"""This module uses the elevation API to get altitude of certain locations.
"""
from typing import List, Tuple


def split_into_grid(n: int) -> Tuple[List[float], List[float]]:
    """Split the map into n * n grid, and return the location coordinates that mark the grid.

    The output will be a tuple, where the first element is a list of longitude coords and the second
    is a list of latitude coords.
    """
    # TODO


def get_midpoints(grid: Tuple[List[float], List[float]]) -> List[Tuple[float, float]]:
    """Return the midpoints of the grid squares
    """
    # TODO


def get_altitude(point: Tuple[float, float]) -> float:
    """Return the altitude of a give point, using an elevation API"""
    # TODO
