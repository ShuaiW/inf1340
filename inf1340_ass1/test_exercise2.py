#!/usr/bin/env python3

""" Module to test exercise2.py """

__author__ = 'Shuai Wang'
__email__ = "info.shuai@gmail.com"

__copyright__ = "2014 Shuai Wang"
__license__ = "MIT License"

__status__ = "Prototype"


import pytest
from exercise2 import checksum


def test_checksum():
    """
    Inputs that are the correct format and length
    """
    assert checksum("786936224306") is True
    assert checksum("085392132225") is True
    assert checksum("717951000841") is False    # should be 2


def test_input():
    """
    Inputs that are the incorrect format and length
    """
    # type error test
    with pytest.raises(TypeError):
        checksum(1.0)               # float
        checksum(786936224306)      # int
        checksum(True)              # boolean
    
    # value error test
    with pytest.raises(ValueError):
        checksum("1")               # len 1
        checksum("1234567890")      # len 10
        checksum("1234567890123")   # len 13


def run_test():
    """
    Test function that runs all tests above.
    """
    test_checksum()
    test_input()
    
run_test()   
