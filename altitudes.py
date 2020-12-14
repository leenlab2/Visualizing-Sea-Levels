"""This module uses the elevation API to get altitude of certain locations.
"""
from typing import List, Tuple, Dict
import requests
from map_setup import MapArea, Midpoint


def split_into_grid(n: int, m: int, my_map: MapArea) -> Tuple[List[float], List[float]]:
    """Return the location of the grid lines for a grid of size n * n.

    The output will be a tuple, whose first element is a list of latitude coords and the second
    is a list of longitude coords.

    Preconditions:
        - n >= 1
        - m >= 1

    >>> map1 = MapArea((40.0, 84.0), (-146.0, -50.0))
    >>> split_into_grid(4, 4, map1)
    ([40.0, 51.0, 62.0, 73.0, 84.0], [-146.0, -122.0, -98.0, -74.0, -50.0])
    """
    # retrieve the latitude and longitude coordinates of the map
    latitude = my_map.latitude
    longitude = my_map.longitude

    # ACCUMULATORS: keep track of grid lines
    lat_so_far = [latitude[0]]
    long_so_far = [longitude[0]]

    # get the range of how many degrees latitude/longitude the map spans
    latitude_range = abs(latitude[1] - latitude[0])
    longitude_range = abs(longitude[1] - longitude[0])

    # the "step" is equivalent to the width of the grid squares
    latitude_step = latitude_range / n
    longitude_step = longitude_range / m

    for i in range(1, n + 1):
        lat_so_far.append(lat_so_far[i - 1] + latitude_step)

    for j in range(1, m + 1):
        long_so_far.append(long_so_far[j - 1] + longitude_step)

    return (lat_so_far, long_so_far)


def get_midpoints(grid: Tuple[List[float], List[float]], my_map: MapArea) -> List[Midpoint]:
    """Return the midpoints of the grid squares.
    The grid input is the same as the format for the split_into_grid functions output.

    Preconditions:
        - grid[0] is a list of latitude coordinates
        - grid[1] is a list of longitude coordinates
        - grid[0] != []
        - grid[1] != []

    >>> map1 = MapArea((40.0, 84.0), (-146.0, -50.0))
    >>> grids = split_into_grid(2, 2, map1)
    >>> midpoints = get_midpoints(grids, map1)
    >>> midpoints[0].coords
    (51.0, -122.0)
    >>> midpoints[1].coords
    (51.0, -74.0)
    """
    # retrieve coordinates of grid lines
    latitudes = grid[0]
    longitudes = grid[1]

    # ACCUMULATORS: keep track of midpoint coordinates
    lat_midpoints = []
    lon_midpoints = []

    # midpoint coordinates for latitude
    for i in range(len(latitudes) - 1):
        lat_mp = (latitudes[i] + latitudes[i + 1]) / 2
        lat_midpoints.append(lat_mp)

    # midpoint coordinates for longitudes
    for i in range(len(longitudes) - 1):
        lon_mp = (longitudes[i] + longitudes[i + 1]) / 2
        lon_midpoints.append(lon_mp)

    return [Midpoint((lat, lon), my_map) for lat in lat_midpoints for lon in lon_midpoints]


def get_altitude(mid_point: Midpoint) -> float:
    """Return the altitude of a give point, using Canada Gov elevation API.
    The tuple values should containt (latitude, longitude) in given order.

    >>> m = MapArea((40, 84), (-50, -146))
    >>> mid_point1 = Midpoint((56.0, -101.0), m)
    >>> mid_point2 = Midpoint((45.5, -71.5), m)
    >>> get_altitude(mid_point1)
    327.0
    >>> get_altitude(mid_point2)
    326.0
    """
    # coordinates of the midpoint
    latitude, longitude = mid_point.coords

    # request urls are essentially the same each request
    # but only with the lat and lon points having different values
    begin = 'http://geogratis.gc.ca/services/elevation/cdem/altitude?'
    # converts the latitude and longitude points into a string
    lat = 'lat=' + str(latitude)
    lon = 'lon=' + str(longitude)

    # combines all elements to have the final url
    url = begin + lat + '&' + lon

    r = requests.get(url)  # sends a request to url and stores data in variable r
    data = r.json()  # converts the json information into a python readable datatype (dictionary)

    return data['altitude']  # returns only the elevation variable from nested dictionary


def get_altitude_data(my_map: MapArea) -> Dict[Tuple[float, float], float]:
    """Return a dictionary with a tuple containing (latitude, longitude) mapping to the altitude of
    that point.

    The grid size for the data will be fixed at 50*50.
    """
    # get grid and midpoints
    grid = split_into_grid(50, 50, my_map)
    midpoints = get_midpoints(grid, my_map)

    # ACCUMULATOR: keeps track of dictionary mapping location to altitude
    data = {}

    for point in midpoints:
        altitude = get_altitude(point)

        if altitude is not None:  # if the point lies outside Canada, altitude is None
            data[point.coords] = altitude

    return data
