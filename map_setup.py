"""This module contains functions that classify land as sea, land, and coastal land.

We assume that the map has already been divided into grids, and the locations we are working with
in this module are the midpoints of these grid squares.
"""
from typing import Tuple, Dict, Set
# TODO somehow import a map and save it
# Maybe instead of this outline, make a class for the points, and have attributes for
# geographical coords, pixel coords, coastal/etc


def convert_location_to_pixels(location: Tuple[float, float]) -> Tuple[int, int]:
    """Return the pixel coordinates on our map image of the given location.

    The location is a tuple in the form of (longitude, latitude)
    """
    # TODO


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


def change_to_sea() -> :
    """Change the color of the given pixel to blue, so that it is "underwater".

    You may use the putpixel method from PIL
    """
    # TODO
