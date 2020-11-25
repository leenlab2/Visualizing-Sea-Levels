"""This module uses the elevation API to get altitude of certain locations.
"""
from typing import List, Tuple
import json
import requests


def split_into_grid(n: int, coords: List[Tuple[float, float]]) -> Tuple[List[float], List[float]]:
    """Split the map into n * n grid, and return the location coordinates that mark the grid.

    The output will be a tuple, where the first element is a list of longitude coords and the second
    is a list of latitude coords.

    Preconditions:
        - coords == [(88.0, -146.0), (88.0, -50.0), (40.0, -146.0), (40.0, -50.0)]
        - (coords[0][0] - coords[2][0]) % n == 0.0
        - (coords[0][1] - coords[1][1]) % n == 0.0

    >>> split_into_grid(48, [(88.0, -146.0), (88.0, -50.0), (40.0, -146.0), (40.0, -50.0)])
    ([40.0, 88.0], [-50.0, -98.0, -146.0])
    >>> split_into_grid(12, [(88.0, -146.0), (88.0, -50.0), (40.0, -146.0), (40.0, -50.0)])
    ([40.0, 52.0, 64.0, 76.0, 88.0], [-50.0, -62.0, -74.0, -86.0, -98.0, -110.0, -122.0, -134.0, -146.0])
    >>> split_into_grid(2, [(88.0, -146.0), (88.0, -50.0), (40.0, -146.0), (40.0, -50.0)])
    ([40.0, 44.0, 48.0, 52.0, 56.0, 60.0, 64.0, 68.0, 72.0, 76.0, 80.0, 84.0, 88.0], [-50.0, -54.0, -58.0, -62.0,
    -66.0, -70.0, -74.0, -78.0, -82.0, -86.0, -90.0, -94.0, -98.0, -102.0, -106.0, -110.0, -114.0, -118.0, -122.0,
    -126.0, -130.0, -134.0, -138.0, -142.0, -146.0])
    """

    num_latitude = int((coords[0][0] - coords[2][0]) / n)  # Finding the number of latitude lines
    num_longitude = abs(int((coords[0][1] - coords[1][1]) / n))  # Finding the number of longitude lines

    latitude_start = coords[2][0]  # Marker for where the latitude starts (e.g. 40 - the smallest lat value)
    longitude_start = coords[1][1]  # Marker for where the longitude starts (e.g. 50 - the smallest lon value)

    # Comprehensions to find the line values
    lat_so_far = [latitude_start + i * n for i in range(num_latitude + 1)]
    lon_so_far = [longitude_start - i * n for i in range(num_longitude + 1)]

    return (lat_so_far, lon_so_far)


def get_midpoints(grid: Tuple[List[float], List[float]]) -> List[Tuple[float, float]]:
    """Return the midpoints of the grid squares

    The grid input is the same as the format for the split_into_grid functions output
    (The *input* will be a tuple, where the first element is a list of longitude coords and the second
    is a list of latitude coords.)

    >>> grids = split_into_grid(48, [(88.0, -146.0), (88.0, -50.0), (40.0, -146.0), (40.0, -50.0)])
    >>> get_midpoints(grids)
    [(64.0, -74.0), (64.0, -98.0)]
    >>> grids = split_into_grid(12, [(88.0, -146.0), (88.0, -50.0), (40.0, -146.0), (40.0, -50.0)])
    >>> get_midpoints(grids)
    [(46.0, -56.0), (52.0, -56.0), (58.0, -56.0), (64.0, -56.0), (46.0, -62.0), (52.0, -62.0), (58.0, -62.0), (64.0, -62.0),
    (46.0, -68.0), (52.0, -68.0), (58.0, -68.0), (64.0, -68.0), (46.0, -74.0), (52.0, -74.0), (58.0, -74.0), (64.0, -74.0),
    (46.0, -80.0), (52.0, -80.0), (58.0, -80.0), (64.0, -80.0), (46.0, -86.0), (52.0, -86.0), (58.0, -86.0), (64.0, -86.0),
    (46.0, -92.0), (52.0, -92.0), (58.0, -92.0), (64.0, -92.0), (46.0, -98.0), (52.0, -98.0), (58.0, -98.0), (64.0, -98.0)]
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
    """Return the altitude of a give point, using Canada Gov elevation api

    The tuple values should containt (latitude, longitude) in given order

    >>> get_altitude((56.0, -101.0))
    327.0
    >>> get_altitude((45.5, -71.5))
    326.0
    """

    # request urls are essentially the same each request, but only with the lat and lon points having different values
    begin = 'http://geogratis.gc.ca/services/elevation/cdem/altitude?'
    # converts the latitude and longitude points into a string
    lat = 'lat=' + str(point[0])
    lon = 'lon=' + str(point[1])

    # combines all elements to have the final url
    url = begin + lat + '&' + lon

    r = requests.get(url)  # sends a request to url and stores data in variable r
    data = r.json()  # converts the json information into a python readable datatype (dictionary)

    return data['altitude']  # returns only the elevation variable from nested dictionary
