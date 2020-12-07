"""This module contains functions that classify land as sea, land, and coastal land.

We assume that the map has already been divided into grids, and the locations we are working with
in this module are the midpoints of these grid squares.
"""
from typing import Tuple, Dict, Set, List
from PIL import Image
# TODO somehow save it


class MapImage:
    """An image of a map of a certain area.

    Instance Attributes:
        - latitude: the range of the map in latitude
        - longitude: the range of the map in longitude
        - map: an Image object containing the actual map image
        - land: set of pixel points that represent land
        - sea: set of pixel points that represent sea

    Representation Invariants:
        - all(-90 <= l <= 90 for l in self.latitude)
        - self.latitude[0] < self.latitude[1]
        - all(-180 <= l <= 180 for l in self.longitude)
        - self.longitude[0] < self.longitude[1]
    """
    latitude: Tuple[float, float]
    longitude: Tuple[float, float]
    map_image: Image
    land: Set[Tuple[int, int]]
    sea: Set[Tuple[int, int]]

    def __init__(self,
                 latitude: Tuple[float, float],
                 longitude: Tuple[float, float], file: str) -> None:
        """Initialize a MapImage object"""
        self.latitude = latitude
        self.longitude = longitude
        self.map_image = Image.open(file)

    def change_to_sea(self, point: Tuple[int, int]) -> None:
        """Change the color of the given pixel to blue, so that it is "underwater".
        """
        blue = (76, 96, 155)
        self.map_image.putpixel(point, blue)
        self.land.remove(point)
        self.sea.add(point)


class Midpoint:
    """A midpoint in the grid.

    Instance Attributes:
        - coords: the coordinates of this point (latitude, longitude)
        - pixels: the pixel location of this point (x, y)
        - map: the MapImage that this midpoint is on

    Representation Invariants:
        - self.map_image.latitude[1] <= self.coords[0] <= self.map_image.latitude[1]
        - self.map_image.longitude[1] <= self.coords[1] <= self.map_image.longitude[1]
    """
    coords: Tuple[float, float]
    pixels: Tuple[int, int]
    map_image: MapImage

    def __init__(self, coords: Tuple[float, float], map_image: MapImage) -> None:
        """Initialize a Midpoint object"""
        self.coords = coords
        self.pixels = convert_location_to_pixels(coords)
        self.map_image = map_image


def convert_location_to_pixels(my_map: MapImage,
                               location: Tuple[float, float]) -> Tuple[int, int]:
    """Return the pixel coordinates on our map image of the given location.

    The location is a tuple in the form of (latitude, longitude)

    >>> map1 = MapImage((40, 84), (-146, -50), 'Canada.png')
    >>> convert_location_to_pixels(map1, (84, -146))
    (0, 0)
    >>> convert_location_to_pixels(map1, (40, -50))
    (684, 894)
    """
    # get the maximum values of the pixel coordinates using the size of the image
    x_max, y_max = my_map.map_image.size
    # this adjustment since the size is actually one more than the coordinates
    x_max -= 1
    y_max -= 1

    # calculate the range in degrees latitude, longitude of the map edges
    latitude_range = my_map.latitude[1] - my_map.latitude[0]
    longitude_range = my_map.longitude[1] - my_map.longitude[0]

    # conversion factors
    x_conversion = x_max / longitude_range
    y_conversion = y_max / latitude_range

    # shift to account for the fact that the top left corner is the origin
    x_shift = my_map.longitude[0] * x_conversion
    y_shift = my_map.latitude[1] * y_conversion

    # implement formula
    x = location[1] * x_conversion - x_shift
    y = y_shift - location[0] * y_conversion

    # must round into integers
    return (round(x), round(y))


def convert_pixels_to_location(pixels: Tuple[int, int]) -> Tuple[float, float]:
    """Return the location of the given pixel coordinates.
    """
    # TODO


def classify_land() -> Dict[Tuple[int, int], str]:
    """Return a dictionary that classifies location points as either land or sea.

    You may use PIL.ImageColor.getrgb()

    This is done by comparing the color of the pixels:
        - blue implies sea
        - brown implies land
    """
    # TODO


def classify_coastal(points: Dict[Tuple[int, int], str]) -> Set[Tuple[int]]:
    """Return a set of coastal location points.

    A point is coastal when it is next to sea.
    """
    # TODO
