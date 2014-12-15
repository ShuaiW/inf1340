#!/usr/bin/env python3

"""
    INF 1340 (Fall 2014) Assignment 1, Exercise 3

    Purpose of Assignment: to create a table that determines the result of an imaginary rock, paper, scissors game.
    There are two participants in the game: Player1 and Player2. Each player is able to input
    rock, paper and scissors.  The program tabulates the winner, and returns 0 if the game is a tie,
    1 if Player1 wins the round, and a 2 if Player2 wins the round.

    The program contains only one function: decide_rock_paper_scissors. The program decides the winner based on
    a matrix. In the matrix, "rock" is equal to 0, "paper" is equal to 1, and "scissors" is equal to 2. The program
    subtracts Player1's choice from Player2' choice. If the result is 0 (a tie), a 0 is returned. If the
    result is 1 (Player1 wins), a 1 is returned. If the result is 2 (Player2 wins), a 2 is returned.


"""

__author__ = 'Shuai Wang, Magdalene Schifferer'
__email__ = "info.shuai@gmail.com, magdaleneschifferer@outlook.com"

__copyright__ = "2014 Shuai Wang, Magdalene Schifferer"
__license__ = "MIT License"

__status__ = "Complete"


def decide_rps(player1, player2):
    """
    :param: choices(string type) made by player1 and player2.
        There are three possible choices: rock, paper and scissors.
        
    :return: int
        0: if Player1 and Player2 tie
        1: if Player1 wins
        2: if Player2 wins
        
    :raise:
        ValueError if any other value other than rock, paper or scissors is entered
    
    
    matrix:
        player1  player2  return  player1 - player2
        ---------------------------------------------
           0        0        0            0 
           0        1        2           -1    
           0        2        1           -2    -> player1 wins
        ---------------------------------------------
           1        0        1            1    -> player1 wins
           1        1        0            0
           1        2        2           -1    
        ---------------------------------------------    
           2        0        2            2    
           2        1        1            1    -> player1 wins
           2        2        0            0
        ---------------------------------------------  
    
    conclusion: 
        as long as player1 - player2 == 1 or -2, player1 wins.
  
    """
    choices = {"Rock": 0, "Paper": 1, "Scissors": 2}
    
    if player1 in choices and player2 in choices:
        if choices[player1] == choices[player2]:
            return 0
        elif (choices[player1] - choices[player2]) in[1, -2]:
            return 1
        else:
            return 2        
    else:
        raise ValueError("Invalid value was entered. Please enter only the terms 'Rock',\
            'Paper' or 'Scissors'.")
        