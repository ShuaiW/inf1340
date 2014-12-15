#!/usr/bin/env python3

"""
    INF 1340 (Fall 2014) Assignment 1, Exercise 2

    Purpose of Assignment: Execute a checksum on the last digit of a 12 digit UPC-A barcode.
    If the checksum is correct, return True.
    If the checksum is incorrect, return False.

    The program contains only one function: checksum. The function parameter is twelve digits representative of a
    UPC-A barcode. Each digit is an integer. A TypeError will be raised if the input is not a string of single
    digit integers. A ValueError will be raised if the string is less or more than 12 digits.


"""

__author__ = 'Shuai Wang, Magdalene Schifferer'
__email__ = "info.shuai@gmail.com, magdaleneschifferer@outlook.com"

__copyright__ = "2014 Shuai Wang, Magdalene Schifferer"
__license__ = "MIT License"



def checksum (upc):
    """
    The function checksum is used to calculate the last digit of a 12 digit UPC-A barcode.
    In order to calculate the last digit, the function checksum performs the following steps:
    1. Adds the digits in the odd-number positions together, produces a sum and multiplies the sum by 3
    2. Adds the digits in the even-numbered positions together
    3. Adds the odd-numbered position sum with the even-numbered position sum and divides the result by 10
       to find the modulo.
    4. If the result from step 3 is not 0, the sum is subtracted from 10
       Eg. The resulting modulo is 7, so 10 - 7 must be performed. The result should be 3.


    :param: a twelve digit UPC-A barcode.
    :return:
        Boolean: If checksum is correct, True will be returned
        If the checksum is not correct, False will be returned.
    :raises:
        A TypeError will be raised if the input is not a string of single digit integers.
        A ValueError if string is the wrong length. An error message will be displayed stating how many digits
        the string is missing or has in excess to 12.
    """

    # raise TypeError if not string of single digit integers


    if type(upc) is not str:
        raise TypeError("UPC code is not correct. Please enter a 12 digit numerical UPC code.")
        
    upc_length = len(upc)
    
    # raise ValueError string length is incorrect
    if upc_length > 12:
        raise ValueError("The string has " + str(upc_length - 12) + 
            " extra digit(s) than is necessary.")
    elif upc_length < 12:
        raise ValueError("The string has " + str(12 - upc_length) +     
        " fewer digit(s) than is necessary.")
    # if the format and length of UPC-A barcode is correct, the program continues to the next step
    else:   
        last_digit = int(upc[-1])
        # 1. adds the digits in the odd-numbered positions together, produces a sum and multiplies the sum by 3
        odd = (int(upc[0]) + int(upc[2]) + int(upc[4]) + int(upc[6]) \
            + int(upc[8]) + int(upc[10])) * 3
        # 2. adds the digits in the even-numbered positions together
        even = int(upc[1]) + int(upc[3]) + int(upc[5]) + int(upc[7]) \
            + int(upc[9])
        # 3. adds the odd-numbered position sum with the even-numbered position sum and divides the result by 10 to find the modulo
        result = (odd + even) % 10
        if result != 0:
         # 4. if the result from step three is not 0, the sum is subtracted from 10
            result = 10 - result
        
        # check if our result equals to the last digit
        return result == last_digit



