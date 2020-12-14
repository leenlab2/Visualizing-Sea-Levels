"""This module contains functions that compare the altitude at a point to the current sea level.
"""
from typing import Dict, Tuple, List
from datasets.Temperatures import temp1, temp2, temp3, temp4
from data_analysis import sea_level_prediction
from altitudes import split_into_grid
from map_setup import MapArea


def compare_altitude_to_sea_level(altitudes: Dict) -> Dict:
    """Returns a dictionary with keys 'year', 'lat', 'lon', 'diff'.
    The values in diff are the differences between each location's predicted sea level and
    altitude throughout each decade of 2020-2100.

    The values in the returned dictionary will only contain those below sea level (negative
    difference).

    Preconditions:
        - all(-90 <= location[0] <= 90 for location in altitudes)
        - all(-180 <= location[1] <= 180 for location in altitudes)
        - altitudes is formatted in the same way as the values in AltitudeData
    """
    # ACCUMULATOR
    full_data = {'year': [], 'lat': [], 'lon': [], 'diff': []}

    # create map of canada
    map_area = MapArea((40.0, 84.0), (-146.0, -50.0))

    # get sea level predictions for 4 locations
    predictions = prediction_creator()

    for location in altitudes:
        # select corresponding sea level prediction list
        category = categorize(location, map_area, predictions)
        # get the altitude of that point
        altitude = altitudes[location]

        # loop through decades from 2020 to 2100
        for i in range(2020, 2101, 10):
            sea_level = category[(i - 2020) // 10]  # get sea level for this year
            difference = sea_level - altitude

            # if difference is positive, add to accumulator
            if difference >= 0:
                full_data['year'].append(i)
                full_data['lat'].append(location[0])
                full_data['lon'].append(location[1])
                full_data['diff'].append(difference)

    return full_data


def prediction_creator() -> Tuple[List[float], List[float], List[float], List[float]]:
    """Returns a tuple containing lists of predicted sea level rises for each decade from 2020-2100
    in 4 different geographical points.
    """
    # ACCUMULATOR
    p1 = []
    p2 = []
    p3 = []
    p4 = []

    # get sea level predictions for these years
    for i in range(2020, 2101, 10):
        p1.append(sea_level_prediction(i, temp1))
        p2.append(sea_level_prediction(i, temp2))
        p3.append(sea_level_prediction(i, temp3))
        p4.append(sea_level_prediction(i, temp4))

    return (p1, p2, p3, p4)


def categorize(location: Tuple[float, float], my_map: MapArea,
               predictions: Tuple[List[float], List[float], List[float], List[float]]) \
        -> List[float]:
    """Returns the appropriate prediction list for the given location.

    Each sea level prediction list in predictions corresponds to the midpoint of a quadrant of the
    map. If the point lies within the corresponding quadrant, that prediction list is returned.

    Preconditions:
        - lists in predictions are ordered as bottom-left, bottom-right, top-left, top-right
    """
    prediction = []  # default

    # split map into quadrants (2*2 grid)
    grid = split_into_grid(2, 2, my_map)
    latitude_limit = grid[0][1]
    longitude_limit = grid[1][1]

    # select corresponding prediction
    if location[0] < latitude_limit and location[1] < longitude_limit:  # bottom-left
        prediction = predictions[0]
    elif location[0] < latitude_limit and location[1] > longitude_limit:  # bottom-right
        prediction = predictions[1]
    elif location[0] > latitude_limit and location[1] < longitude_limit:  # top-left
        prediction = predictions[2]
    elif location[0] > latitude_limit and location[1] > longitude_limit:  # top-right
        prediction = predictions[3]

    return prediction
