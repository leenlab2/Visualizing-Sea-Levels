"""This module contains functions that will process the datasets into variable types we can use.

There are two main datasets we are working with:
    - Global Average Surface Temperates by Year (includes predicted values)
    - Global Average Sea Level
"""
from typing import Dict
import netCDF4 as nc
import numpy.ma as ma


###################################################################################################
# Cleanup Temperature data
###################################################################################################
def read_temperature_data(lat: float, lon: float) -> Dict[int, float]:
    """Return a dictionary where the key is a certain year and the value is the average temperature in Kelvin
    for that year. 
    
    Prerequisites
    - -90 <= lat <= 89.5
    - 0 <= lon <= 359.5
    """
    fn = 'temp.nc'
    fn2 = 'temp46-65.nc'
    fn3 = 'temp81-100.nc'
    
    ds = nc.Dataset(fn)
    ds2 = nc.Dataset(fn2)
    ds3 = nc.Dataset(fn3)
    
    temp = ds['tas']
    temp2 = ds2['tas']
    temp3 = ds3['tas']
    
    temperatures = {i + 1: float('%7.4f' % (temp[12 * i, 0, 0])) for i in range(0, 20)}
    dict2 = {i + 46: float('%7.4f' % (temp2[12 * i, 0, 0])) for i in range(0, 20)}
    dict3 = {i + 81: float('%7.4f' % (temp3[12 * i, 0, 0])) for i in range(0, 20)}
    
    temperatures.update(dict2)
    temperatures.update(dict3)
    return temperatures


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
    
