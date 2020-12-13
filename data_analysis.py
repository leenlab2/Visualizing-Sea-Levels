"""This module contains functions that analyze the datasets to predict future sea levels.
We will use a the semi-empirical sea level projection model outlined here:
https://www-jstor-org.myaccess.library.utoronto.ca/stable/20035254?pq-origsite=summon&seq=1#metadata_info_tab_contents
We will also use the regression methods from sci-kit learn to get our predictions
"""
from typing import Dict
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from dataset_cleaner import read_sea_level_data, read_temperature_data
import numpy as np


#  This function runs a polynomial regression on temperature versus year based on the dataset
#  containing the prediction values of temperature from 2006 to 2100
def temp_year_regression(year: float, temp: Dict[int, float]) -> float:
    """Return the predicted temperature of the given point in the given year.
    """
    #  Polynomial regression:
    temperature_data = temp
    x = np.array([[year] for year in temperature_data])
    y = np.array([temperature_data[year] for year in temperature_data])
    poly_reg = PolynomialFeatures(degree=6)
    x_poly = poly_reg.fit_transform(x)
    poly_reg.fit(x_poly, y)
    lin_reg = LinearRegression()
    lin_reg.fit(x_poly, y)

    #  Value prediction:
    year_value = np.array([[year]])
    year_poly = poly_reg.fit_transform(year_value)
    prediction = lin_reg.predict(year_poly)

    return float(prediction)


# Based on the semi-empirical sea level projection model, there is a proportionality constant
# between sea level and integration of temperature minus equilibrium temperature, this function
# runs a riemann sum integration to get an approximation of the integration.
# detailed information is in https://www-jstor-org.myaccess.library.utoronto.ca/stable/
# 20035254?pq-origsite=summon&seq=1#metadata_info_tab_contents
def integration_approximation(year: int, temp: Dict[int, float]) -> float:
    """Return the integrations of temperature minus t0 from 2006 to the given year.
    """
    sum_so_far = 0
    n = 100
    y0 = 2012
    t0 = temp_year_regression(y0, temp)
    dx = (year - y0) / n

    for i in range(n):
        y = y0 + dx / 2 + i * dx
        sum_so_far += temp_year_regression(y, temp) - t0
    integration = dx * sum_so_far
    return integration


#  This function runs a linear regression on the sea level and the integration to find the slope
#  to represent the proportionality constant.
def finding_constant(temp: Dict[int, float]) -> float:
    """Return the proportionality constant between sea level and integration of temperature"""
    x = np.array([[integration_approximation(i, temp)] for i in range(2006, 2019)])
    y = np.array([read_sea_level_data()[i] for i in range(2006, 2019)])
    model = LinearRegression()
    model.fit(x, y)

    return float(model.coef_)


#  This function returns the predicted value of sea level based on the formula in
#  semi-empirical sea level projection model
def sea_level_prediction(year: int, temp: Dict[int, float]) -> float:
    """Return the predicted sea level of the given point in a given year"""
    a = finding_constant(temp)
    ht = a * integration_approximation(year, temp)

    return ht
