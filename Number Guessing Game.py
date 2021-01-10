import random
import time
import sys
import numbers
import os
import shelve
import ctypes
import webbrowser

# Program packages
import leaderboard
import game
import utility

from player import Player

'''
The Master Control Program
'''
def MCP(number_of_attempts):

    scores_for_session = []
    utility.clear_screen()
   
    name = str(input("Enter your name: "))
    try:
        player = Player(name)
        # Let the user know the rules
        game.greetings(player.name, number_of_attempts)
        cont_play = True
        
        # Throw the user into a while loop that will be broken
        # once they convey they no longer wish to play
        while (cont_play == True):

            # The guessing part of the game
            player.score = game.guessing_game(number_of_attempts)

            leaderboard.update(player.name, player.score)

            # Display any pre-existing scores
            leaderboard.read_scores()

            # Update the player's scores based on the results
            scores_for_session = game.update_session_score(player.score, 
                                                           scores_for_session)
            # Check if they still want to play
            cont_play = game.keep_playing(player.name)
            
    # Catch the intterupt request
    except KeyboardInterrupt:
        print("\nExiting the Matrix\n")
        time.sleep(1)
        sys.exit(0)
        
# Call the driver 
MCP(5)
