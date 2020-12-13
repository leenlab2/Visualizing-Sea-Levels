"""This module contains functions that analyze the datasets to predict future sea levels.

We will use the semi-empirical sea level projection model outlined here:
https://www-jstor-org.myaccess.library.utoronto.ca/stable/20035254?pq-origsite=summon&seq=1#metadata_info_tab_contents

We will also use the regression methods from sci-kit learn to get our predictions
"""
from typing import Dict
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
from dataset_cleaner import read_sea_level_data


def temp_year_regression(year: float, temp: Dict[int, float]) -> float:
    """Return an estimated value of the temperature for a certain year.
    This is done by running a polynomial regression on the values in temp (temperature vs year).

    Preconditions:
        - 2006 <= year <= 2100
        - all(2006 <= year <= 2100 for year in temp)
    """
    # Polynomial regression:
    # retrieve x and y values as numpy arrays
    x = np.array([[yr] for yr in temp])  # years
    y = np.array([temp[yr] for yr in temp])  # temperatures

    # run a polynomial regression of degree 6
    poly_reg = PolynomialFeatures(degree=6)
    x_poly = poly_reg.fit_transform(x)
    poly_reg.fit(x_poly, y)
    lin_reg = LinearRegression()
    lin_reg.fit(x_poly, y)

    # Value prediction:
    year_value = np.array([[year]])
    year_poly = poly_reg.fit_transform(year_value)
    prediction = lin_reg.predict(year_poly)

    return float(prediction)


def integration_approximation(year: int, temp: Dict[int, float]) -> float:
    """Return the midpoint Riemann sum approximation of the integral from 2012 to year of the
    temperature in year - temperature in 2012 (T(year) - T0)
    """
    sum_so_far = 0
    n = 100  # number of sub-intervals taken
    y0 = 2012
    t0 = temp_year_regression(y0, temp)  # temperature at 2012
    dx = (year - y0) / n  # length of the intervals

    for i in range(n):
        y = y0 + dx / 2 + i * dx  # gets midpoint of interval
        sum_so_far += temp_year_regression(y, temp) - t0

    return dx * sum_so_far


def finding_constant(temp: Dict[int, float]) -> float:
    """Return the proportionality constant between sea level and integral of temperature from 2012
    to a certain year. The slope of the linear regression (sea level vs temperature) is the constant

    This proportionality is based on the semi-empirical model detailed here:
    https://www-jstor-org.myaccess.library.utoronto.ca/stable/20035254?pq-origsite=summon&seq=1#metadata_info_tab_contents
    """
    # retrieve the x and y axes for our linear regression as numpy arrays
    x = np.array([[integration_approximation(i, temp)] for i in range(2006, 2019)])  # integral
    y = np.array([read_sea_level_data('datasets/global_timeseries_measures.nc.nc4')[i]
                  for i in range(2006, 2019)])  # sea level

    # run linear regression
    model = LinearRegression()
    model.fit(x, y)

    return float(model.coef_)


def sea_level_prediction(year: int, temp: Dict[int, float]) -> float:
    """Return the predicted sea level in the given year. The choice of temp is affected by the
    location we need.

    This calculation is based on the semi-empirical projection model.
    """
    a = finding_constant(temp)
    return a * integration_approximation(year, temp)
