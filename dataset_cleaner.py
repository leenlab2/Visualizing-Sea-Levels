"""This module contains functions that will process the datasets into variable types we can use.

There are two main datasets we are working with:
    - Global Average Surface Temperates by Year (includes predicted values)
    - Global Average Sea Level
"""
from typing import Dict
import netCDF4 as nc


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
    """Return a dictionary where the key is a certain year and the value is the average sea level change
    for that year (from 2006 to 2119).
    """
    fn = 'global_timeseries_measures.nc.nc4'
    ds = nc.Dataset(fn)
    averages = ds['global_average_sea_level_change'][:]
    time_sea = ds['time'][:]
    sea_levels = {i + 1: averages[i] for i in range(len(time_sea))}
    return sea_levels
    
