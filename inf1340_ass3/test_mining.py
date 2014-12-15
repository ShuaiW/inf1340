#!/usr/bin/env python3

""" Module to test mining.py """

__author__ = 'Joanna Kolbe, Shuai Wang'
__email__ = "joannakolbe@gmail.com, info.shuai@gmail.com"
__copyright__ = "2014 Joanna Kolbe, Shuai Wang"
__status__ = "Prototype"

# imports one per line
from mining import *
import pytest


def test_google():
    """
    Test for correct google output
    """
    google = Stock("GOOG", "data/GOOG.json")
    assert google.six_best_months() == [('2007/12', 693.76),
                                        ('2007/11', 676.55),
                                        ('2007/10', 637.38),
                                        ('2008/01', 599.42),
                                        ('2008/05', 576.29),
                                        ('2008/06', 555.34)]
    assert google.six_worst_months() == [('2004/08', 104.66),
                                         ('2004/09', 116.38),
                                         ('2004/10', 164.52),
                                         ('2004/11', 177.09),
                                         ('2004/12', 181.01),
                                         ('2005/03', 181.18)]
    assert google.name() == "GOOG"
    assert google.span() == 50


def test_tseso():
    """
    Test for correct tse-so output
    """
    tse = Stock("Tse-So", "data/TSE-SO.json")
    assert tse.six_best_months() == [('2007/12', 20.98), ('2007/11', 20.89),
                                     ('2013/05', 19.96), ('2013/06', 19.94),
                                     ('2013/04', 19.65), ('2007/10', 19.11)]
    assert tse.six_worst_months() == [('2009/03', 1.74), ('2008/11', 2.08),
                                      ('2008/12', 2.25), ('2009/02', 2.41),
                                      ('2009/04', 2.75), ('2009/01', 3.14)]
    assert tse.name() == "Tse-So"
    assert tse.span() == 104


def test_parameters():
    """
    Test for missing arguments or non-existing files
    """
    with pytest.raises(TypeError):
        google = Stock("data/GOOG.json")
    with pytest.raises(TypeError):
        google = Stock("Google")
    with pytest.raises(FileNotFoundError):
        google = Stock("Google", "data/non-existing.json")


def test_file():
    """
    Check if the json file is properly formatted and
    contains correct data
    """
    # File that does not contains a list of stocks
    with pytest.raises(TypeError):
        google = Stock("Goog", "data/not_a_list.json")
    # Stock is not an object
    with pytest.raises(TypeError):
        google = Stock("Goog", "data/stock_not_object.json")
    # Date is incorrectly formatted YYYY:MM:DD
    with pytest.raises(ValueError):
        google = Stock("Goog", "data/invalid_date.json")
    # Date missing
    with pytest.raises(ValueError):
        google = Stock("Goog", "data/missing_date.json")
    # "Close" is missing
    with pytest.raises(ValueError):
        google = Stock("Goog", "data/close_missing.json")
    # "Volume" is not a number
    with pytest.raises(TypeError):
        google = Stock("Goog", "data/volume_type.json")
    # Less than 6 monts
    test = Stock("Test", "data/less_6.json")
    with pytest.raises(ValueError):
        test.six_worst_months()


def test_math_errors():
    """
    Test for data that would cause mathematical errors
    """
    # all Volumes are 0 so sum of Volumes as denominator has no meaning
    with pytest.raises(ZeroDivisionError):
        google = Stock("Goog", "data/volume_zero.json")
    # monthly averages list is empty; can't compute standard deviation
    with pytest.raises(ValueError):
        stdev([])
    # monthly averages list contains negative stock price
    with pytest.raises(ValueError):
        stdev([5, 12, -2, 25, 56])


def test_compare():
    """
    Test for function that compares the standard deviation of the two stocks
    """
    google = Stock("Goog", "data/GOOG.json")
    tse = Stock("Tse-So", "data/TSE-SO.json")
    assert compare_stocks(tse, google) == ("Goog stock has a higher standard"
                                           " deviation in monthly averages"
                                           " than that of Tse-So")
    assert compare_stocks(google, tse) == ("Goog stock has a higher standard"
                                           " deviation in monthly averages"
                                           " than that of Tse-So")
    assert compare_stocks(google, google) == ("Goog and Goog stocks have the"
                                              " same standard deviation in"
                                              " monthly averages")
    assert compare_stocks(tse, tse) == ("Tse-So and Tse-So stocks have the"
                                        " same standard deviation in monthly"
                                        " averages")


def run_tests():
    """
    Run all tests above.
    """
    test_google()
    test_tseso()
    test_parameters()
    test_file()
    test_math_errors()
    test_compare()

run_tests()
