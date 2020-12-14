"""This is the main file of the project and will run all the other modules.
"""
from AltitudeData import altitude_data
from bubble import draw_map
from flooding import compare_altitude_to_sea_level

if __name__ == "__main__":
    data = compare_altitude_to_sea_level(altitude_data)
    draw_map(data)
