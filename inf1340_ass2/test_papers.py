#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = "Shuai Wang"
__email__ = "info.shuai@gmail.com"


# imports one per line
import pytest
from papers import decide


def test_complete_info():
    """
    Test if required info is complete
    """
    # 8 entries: 1st is complete, and the rest 7 miss one of the required info
    assert decide("json_test/test_complete_info.json", "watchlist.json",
                  "countries.json") == ["Accept", "Reject", "Reject", "Reject",
                                        "Reject", "Reject", "Reject", "Reject"]


def test_basic():
    """
    Some basic tests
    """
    # "Accept": returning citizens, no other conditions
    assert decide("json_test/test_returning_citizen.json", "watchlist.json",
                  "countries.json") == ["Accept", "Accept"]

    # "Secondary": name or passport on watchlist
    assert decide("json_test/test_watchlist.json", "watchlist.json",
                  "countries.json") == ["Secondary", "Secondary"]

    # "Quarantine": from/via a country that has medical advisory
    assert decide("json_test/test_quarantine.json", "watchlist.json",
                  "countries.json") == ["Quarantine", "Quarantine"]


def test_visit():
    """
    Some tests on visit visa
    """
    # 1. "Accept": visit but visa not required
    # 2. "Accept": visit and visa required, visa valid
    # 3. "Reject": visit and visa required, visa invalid
    assert decide("json_test/test_visit.json", "watchlist.json",
                  "countries.json") == ["Accept", "Accept", "Reject"]


def test_transit():
    """
    Some tests on transit visa
    """
    # 1. "Accept": transit but visa not required
    # 2. "Accept": transit and visa required, visa valid
    # 3. "Reject": transit and visa required, visa invalid
    assert decide("json_test/test_transit.json", "watchlist.json",
                  "countries.json") == ["Accept", "Accept", "Reject"]


def test_valid_format():
    """
    Test if passport and date (visa date and birth date) formats are valid
    """
    # one entry with all valid format and three with each of the invalid
    assert decide("json_test/test_valid_format.json", "watchlist.json",
                  "countries.json") == ["Accept", "Reject", "Reject", "Reject"]


def test_files():
    """
    Test for files
    """
    # all files are found
    assert decide("example_entries.json", "watchlist.json", "countries.json")

    # one or more files not found
    with pytest.raises(FileNotFoundError):
        decide("", "watchlist.json", "countries.json")
        decide("", "", "countries.json")
        decide("", "", "")


def run_tests():
    """
    Runs all tests above
    """
    test_complete_info()
    test_basic()
    test_visit()
    test_transit()
    test_valid_format()
    test_files()


run_tests()
