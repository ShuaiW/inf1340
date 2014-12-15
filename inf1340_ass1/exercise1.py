#!/usr/bin/env python3

"""
    INF 1340 (Fall 2014) Assignment 1, Exercise 1

    Purpose of Assignment: to create a program that converts letter and numerical grades to corresponding GPA according
    to the University of Toronto Graduate Student grading scheme

    The program contains only one function: grade_to_gpa. The function parameters can either be a
    letter grade (A+, A, A-, B+, B, B-, or FZ) or an integer (0-100). An error message will be given for any other types
    of inputs.

"""

__author__ = 'Shuai Wang, Magdalene Schifferer'
__email__ = "info.shuai@gmail.com, magdaleneschifferer@outlook.com"

__copyright__ = "2014 Shuai Wang, Magdalene Schifferer"
__license__ = "MIT License"

__status__ = "Complete"


def grade_to_gpa(grade):
    """
    The function grade_to_gpa will return the University of Toronto Graduate GPA for grades entered in
    alphabetical (A+, A, A-, B+, B, B-, or FZ) or numerical (0-100) form.

    :param:
        grade (integer or string): Grade to be converted
            If grade entered is an integer, the accepted value range is 0-100.
            If grade entered is a string,the only accepted values are A+, A, A-, B+, B, B-, FZ.

    :return:
        float: The corresponding GPA to the integer (0-100) or string (A+, A, A-, B+, B, B-, FZ) entered.
            The returned GPA will be a float with a value range of 0.0-4.0.

    :raises:
       A TypeError will be raised if the parameter entered is not a string.
       A ValueError will be raised if the parameter entered is out of alphabetical(A+, A, A-, B+, B, B-, FZ)
       and numerical (0-100) range.
    """

    if type(grade) is str:
        alphabetical_grade_gpa_dict = {"A+": 4.0,
                                       "A" : 4.0,
                                       "A-": 3.7,
                                       "B+": 3.3,
                                       "B" : 3.0,
                                       "B-": 2.7,
                                       "FZ": 0.0}         
        if grade in alphabetical_grade_gpa_dict:
            gpa = alphabetical_grade_gpa_dict[grade]
        else:
            raise ValueError("Please enter a valid University of Toronto Graduate School letter grade")

    elif type(grade) is int:
        if 85 <= grade <= 100:
            gpa = 4.0
        elif 80 <= grade <= 84:
            gpa = 3.7
        elif 77 <= grade <= 79:
            gpa = 3.3
        elif 73 <= grade <= 76:
            gpa = 3.0
        elif 70 <= grade <= 72:
            gpa = 2.7
        elif 0 <= grade <= 69:
            gpa = 0.0
        else:
            raise ValueError("Please enter a valid University of Toronto Graduate School numerical grade")
            
    else:
        raise TypeError("Please enter a valid University of Toronto Graduate School grade (string or integer)")

    return gpa
