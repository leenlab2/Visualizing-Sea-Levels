"""This module contains functions that will process the datasets into variable types we can use.

There are two main datasets we are working with:
    - Average Surface Temperates by Year and Location (includes predicted values)
    - Global Average Sea Level
"""
from typing import Dict
import netCDF4 as nc


###################################################################################################
# Cleanup Temperature data
###################################################################################################
def read_temperature_data(lat: float, lon: float, filename: str) -> Dict[int, float]:
    """Return a dictionary where the key is a certain year and the value is the
    average temperature in Kelvin for that year and inputted location.

    Preconditions:
        - -90 <= lat <= 89.5
        - -180 <= lon <= 179.5
        - filename != ''
    """
    # use the netCDF4 library to read the NetCDF file
    ds = nc.Dataset(filename)

    # 'tas' is a NetCDF variable representing temperature
    temp = ds['tas']

    # dictionary accessing the arrays within temp
    temperatures = {i + 2006: float('%7.4f' % (temp[12 * i, lat, lon])) for i in range(0, 95)}
    return temperatures


###################################################################################################
# Cleanup Sea level data
###################################################################################################
def read_sea_level_data(filename: str) -> Dict[int, float]:
    """Return a dictionary where the key is a year and the value is the average sea level change
    for that year (from 2006 to 2018).

    Preconditions:
        - filename != ''
    """
    # use the netCDF4 library to read the NetCDF file
    ds = nc.Dataset(filename)

    # 'global_average_sea_level_change' contains sea level values
    averages = ds['global_average_sea_level_change'][:]

    # dictionary mapping year to average sea level change
    sea_levels = {i + 2006: averages[i + 106] for i in range(0, 13)}
    return sea_levels
