"""This module contains functions that will process the datasets into variable types we can use.

There are two main datasets we are working with:
    - Global Average Surface Temperates by Year (includes predicted values)
    - Global Average Sea Level
"""
from typing import Dict


###################################################################################################
# Cleanup Temperature data
###################################################################################################
def read_temperature_data() -> Dict[int, float]:
    """Return a dictionary where the key is a certain year and the value is the average temperature
    for that year.
    """
    # TODO implement this (you may add helper functions)


###################################################################################################
# Cleanup Sea level data
###################################################################################################
def read_sea_level_data() -> Dict[int, float]:
    """Return a dictionary where the key is a certain year and the value is the average sea level
    for that year.
    """
    # TODO implement this (you may add helper functions)
