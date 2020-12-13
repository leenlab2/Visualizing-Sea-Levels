"""This module contains functions that compare the altitude at a point to the current sea level.
"""
from typing import Dict, Tuple, List
from datasets.Altitudes import *
from datasets.Temperatures import *
from data_analysis import sea_level_prediction

def compare_altitude_to_sea_level(altitudes: Dict) -> Dict:
    """Calculates the difference between each location's predicted sea level and altitude
    throughout each decade of 2020-2100 and returns a dictionary 
    mapped as {'year': [], 'lat': [], 'lon': [], 'diff': []}.
    Prerequisites:
    - alitudes in Altitudes.py
    """
    full_data = {'year': [], 'lat': [], 'lon': [], 'diff': []}
    predictions = prediction_creator()
    for location in altitudes:
        category = categorize(location, predictions)
        altitude = altitudes[location]
        for i in range(2020, 2101, 10):
            full_data['year'].append(i)
            full_data['lat'].append(location[0])
            full_data['lon'].append(location[1])
            sea_level = category[int((i - 2020) / 10)]
            full_data['diff'].append(altitude - sea_level)

    return full_data


def prediction_creator() -> Tuple:
    """Returns a tuple containing lists of predicted sea level rises
        each decade from 2020-2100 in 4 different geographical points
    """
    p1 = []
    p2 = []
    p3 = []
    p4 = []

    for i in range(2020, 2101, 10):
        p1.append(sea_level_prediction(i, temp1))
        p2.append(sea_level_prediction(i, temp2))
        p3.append(sea_level_prediction(i, temp3))
        p4.append(sea_level_prediction(i, temp4))
    return (p1, p2, p3, p4)


def categorize(location: Tuple[float], predictions: Tuple[List[float]]) -> List:
    """Categorizes a geographical point onto the differing
       temperature coordinate dictionaries
    """
    prediction = []
    if location[0] < 62 and location[1] < -102:
        prediction = predictions[0]
    elif location[0] < 62 and location[1] > -102:
        prediction = predictions[1]
    elif location[0] > 62 and location[1] > -102:
        prediction = predictions[2]
    elif location[0] > 62 and location[1] < -102:
        prediction = predictions[3]
    return prediction


def flooding_map(year: int) -> :
    """Return the image of what the map would look like at a given year.
    """
    # TODO

def slider() -> :
    """Using the Bokeh library, build an interactive slider, where each "frame" is the image for a
    certain year
    """
    # TODO
