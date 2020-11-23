"""This module uses the elevation API to get altitude of certain locations.
"""
from typing import List, Tuple


def split_into_grid(n: int, coords: List[Tuple[float, float]]) -> Tuple[List[float], List[float]]:
    """Split the map into n * n grid, and return the location coordinates that mark the grid.

    The output will be a tuple, where the first element is a list of longitude coords and the second
    is a list of latitude coords.

    Preconditions:
        - coords == [(88.0, 146.0), (88.0, 50.0), (40.0, 146.0), (40.0, 50.0)]
        - (coords[0][0] - coords[2][0]) % n == 0.0
        - (coords[0][1] - coords[1][1]) % n == 0.0

    >>> split_into_grid(48, [(88.0, 146.0), (88.0, 50.0), (40.0, 146.0), (40.0, 50.0)])
    ([40, 88], [50, 98, 146])
    >>> split_into_grid(12, [(88.0, 146.0), (88.0, 50.0), (40.0, 146.0), (40.0, 50.0)])
    ([40, 52, 64, 76, 88], [50, 62, 74, 86, 98, 110, 122, 134, 146])
    >>> split_into_grid(2, [(88.0, 146.0), (88.0, 50.0), (40.0, 146.0), (40.0, 50.0)])
    ([40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88],
    [50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102,
    104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146])
    """

    num_latitude = int((coords[0][0] - coords[2][0]) / n)  # Finding the number of latitude lines
    num_longitude = int((coords[0][1] - coords[1][1]) / n)  # Finding the number of longitude lines

    latitude_start = coords[2][0]  # Marker for where the latitude starts (e.g. 40 - the smallest lat value)
    longitude_start = coords[1][1]  # Marker for where the longitude starts (e.g. 50 - the smallest lon value)

    # Comprehensions to find the line values
    lat_so_far = [latitude_start + i * n for i in range(num_latitude + 1)]
    lon_so_far = [longitude_start + i * n for i in range(num_longitude + 1)]

    return (lat_so_far, lon_so_far)


def get_midpoints(grid: Tuple[List[float], List[float]]) -> List[Tuple[float, float]]:
    """Return the midpoints of the grid squares

    The grid input is the same as the format for the split_into_grid functions output
    (The *input* will be a tuple, where the first element is a list of longitude coords and the second
    is a list of latitude coords.)

    >>> grids = split_into_grid(48, [(88.0, 146.0), (88.0, 50.0), (40.0, 146.0), (40.0, 50.0)])
    >>> get_midpoints(grids)
    [(64.0, 74.0), (64.0, 98.0)]
    >>> grids = split_into_grid(12, [(88.0, 146.0), (88.0, 50.0), (40.0, 146.0), (40.0, 50.0)])
    >>> get_midpoints(grids)
    [(46.0, 56.0), (52.0, 56.0), (58.0, 56.0), (64.0, 56.0), (46.0, 62.0), (52.0, 62.0), (58.0, 62.0), (64.0, 62.0),
    (46.0, 68.0), (52.0, 68.0), (58.0, 68.0), (64.0, 68.0), (46.0, 74.0), (52.0, 74.0), (58.0, 74.0), (64.0, 74.0),
    (46.0, 80.0), (52.0, 80.0), (58.0, 80.0), (64.0, 80.0), (46.0, 86.0), (52.0, 86.0), (58.0, 86.0), (64.0, 86.0),
    (46.0, 92.0), (52.0, 92.0), (58.0, 92.0), (64.0, 92.0), (46.0, 98.0), (52.0, 98.0), (58.0, 98.0), (64.0, 98.0)]
    """
    # Finds the difference between latitude and longitude lines for the midpoint
    lat_difference = (grid[0][1] - grid[0][0]) / 2
    lon_difference = (grid[1][1] - grid[1][0]) / 2

    # Markers for where the latitude and longitude grid starts
    lat_start = grid[0][0]
    lon_start = grid[1][0]

    # ACCUMULATOR: Keeps track of the midpoints so far
    points_so_far = []

    for lon in range(1, len(grid[1])):  # The loop iterates row by row through the map
        for lat in range(1, len(grid[0])):
            points_so_far.append((lat_start + lat_difference * lat, lon_start + lon_difference * lon))

    return points_so_far


def get_altitude(point: Tuple[float, float]) -> float:
    """Return the altitude of a give point, using an elevation API"""
    # TODO


    # AAGGHHHGHH APIIIIII skajdksjdkja
