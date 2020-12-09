"""This module uses the elevation API to get altitude of certain locations.
"""
from typing import List, Tuple, Dict
import json
import requests
from map_setup import MapImage, Midpoint
from PIL import Image


def split_into_grid(n: int, map: MapImage) -> Tuple[List[float], List[float]]:
    """Split the map into a grids size of n * n, and return the location coordinates that mark the grid.

    The output will be a tuple, where the first element is a list of longitude coords and the second
    is a list of latitude coords.


    Preconditions:
        - (map.latitude[1] - map.latitude[0) % n == 0.0
        - (map.longitude[1] - map.longitude[0]) % n == 0.0

    >>> m = MapImage((40, 84), (-50, -146), 'Canada.png')
    >>> split_into_grid(4, m)
    ([40.0, 44.0, 48.0, 52.0, 56.0, 60.0, 64.0, 68.0, 72.0, 76.0, 80.0, 84.0], [-50.0, -54.0, -58.0, -62.0, -66.0,
    -70.0, -74.0, -78.0, -82.0, -86.0, -90.0, -94.0, -98.0, -102.0, -106.0, -110.0, -114.0, -118.0, -122.0, -126.0,
    -130.0, -134.0, -138.0, -142.0, -146.0])
    """
    coords = (map.latitude, map.longitude)
    # coords = ((40,  84), (-50, -146))

    num_latitude = int((coords[0][1] - coords[0][0]) / n)  # Finding the number of latitude lines
    num_longitude = abs(int((coords[1][1] - coords[1][0]) / n))  # Finding the number of longitude lines

    latitude_start = coords[0][0]  # Marker for where the latitude starts (e.g. 40 - the smallest lat value)
    longitude_start = coords[1][0]  # Marker for where the longitude starts (e.g. 50 - the smallest lon value)

    # Comprehensions to find the line values
    lat_so_far = [latitude_start + i * n for i in range(num_latitude + 1)]
    lon_so_far = [longitude_start - i * n for i in range(num_longitude + 1)]

    return (lat_so_far, lon_so_far)


def get_midpoints(grid: Tuple[List[float], List[float]], map: MapImage) -> List[Midpoint]:
    """Return the midpoints of the grid squares

    The grid input is the same as the format for the split_into_grid functions output
    (The *input* will be a tuple, where the first element is a list of longitude coords and the second
    is a list of latitude coords.)

    >>> m = MapImage((40, 84), (-50, -146), 'Canada.png')
    >>> grids = split_into_grid(4, m)
    >>> midpoints = get_midpoints(grids, m)
    >>> midpoints[0].coords
    (42.0, -52.0)
    >>> midpoints[1].coords
    (44.0, -52.0)
    """
    # Finds the difference between latitude and longitude lines for the midpoint
    lat_delta = (grid[0][1] - grid[0][0])
    lon_delta = (grid[1][1] - grid[1][0])

    # Markers for where the latitude and longitude grid starts
    lat_start = grid[0][0] + (lat_delta / 2)
    lon_start = grid[1][0] + (lon_delta / 2)

    # ACCUMULATOR: Keeps track of the midpoints so far
    points_so_far = []

    for lon in range(0, len(grid[1])):  # The loop iterates row by row through the map
        for lat in range(0, len(grid[0])):
            points_so_far.append(Midpoint((lat_start + lat_delta * lat, lon_start + lon_delta * lon), map))

    return points_so_far


def get_altitude(mid_point: Midpoint) -> float:
    """Return the altitude of a give point, using Canada Gov elevation api

    The tuple values should containt (latitude, longitude) in given order
    >>> m = MapImage((40, 84), (-50, -146), 'Canada.png')
    >>> mid_point1 = Midpoint((56.0, -101.0), m)
    >>> mid_point2 = Midpoint((45.5, -71.5), m)
    >>> get_altitude(mid_point1)
    327.0
    >>> get_altitude(mid_point2)
    326.0
    """
    coords = mid_point.coords

    # request urls are essentially the same each request, but only with the lat and lon points having different values
    begin = 'http://geogratis.gc.ca/services/elevation/cdem/altitude?'
    # converts the latitude and longitude points into a string
    lat = 'lat=' + str(coords[0])
    lon = 'lon=' + str(coords[1])

    # combines all elements to have the final url
    url = begin + lat + '&' + lon

    r = requests.get(url)  # sends a request to url and stores data in variable r
    data = r.json()  # converts the json information into a python readable datatype (dictionary)

    return data['altitude']  # returns only the elevation variable from nested dictionary

