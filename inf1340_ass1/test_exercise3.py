#!/usr/bin/env python3

""" Module to test exercise3.py """

__author__ = 'Shuai Wang'
__email__ = "info.shuai@gmail.com"

__copyright__ = "2014 Shuai Wang"
__license__ = "MIT License"

__status__ = "Complete"


import pytest
from exercise3 import decide_rps


def test_rps():
    """
    Test function for decide_rps().
    """  
    # valid input test (all 9 possibilities)
    assert decide_rps("Rock", "Rock") == 0
    assert decide_rps("Rock", "Paper") == 2
    assert decide_rps("Rock", "Scissors") == 1
    
    assert decide_rps("Paper", "Rock") == 1
    assert decide_rps("Paper", "Paper") == 0
    assert decide_rps("Paper", "Scissors") == 2
    
    assert decide_rps("Scissors", "Rock") == 2
    assert decide_rps("Scissors", "Paper") == 1
    assert decide_rps("Scissors", "Scissors") == 0
    
    # invalid input test
    with pytest.raises(ValueError):
        decide_rps("R", "Paper")        # player1 invalid
        decide_rps("Rock", "P")         # player2 invalid
        decide_rps("R", "S")            # both invalid
        decide_rps(True, 12)            # both invalid - non-string type
    

test_rps()