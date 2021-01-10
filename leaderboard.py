import shelve
import random

import player
from utility import delayed_print


def check_personal_best(leaderboard, name, score):
    """Returns a message based on a player's existing leaderboard score. 
    
    Returns a string indicating whether the player tied, beat, or missed their
    score which landed them on the leaderboard.

    Args:
        leaderboard:
            A text file in the form of a shelve.DBfilenameShelve representing
            the leaderboard.
        name:
            A string representing the name of the player
        score:
            An integer representing the number of attempts taken in guessing
    
    Returns:
        A string if the player has an exisiting score.
   """
    existing_score = leaderboard.get(name, -1)

    if existing_score != -1:
        
        if score == existing_score:
            msg = f"{name}, you tied your personal best. Keep trying!"

        elif score > existing_score:
            msg = f"{name}, you did not beat your personal best of {existing_score}"

        else:
            _update_player_score(leaderboard, name, score)
            msg = f"{name}, you achieved a personal best!"
        return msg

def update(name : str, score : int) -> None:
    with shelve.open("scores.txt") as leaderboard:

        if name in leaderboard.keys():
            msg = check_personal_best(leaderboard, name, score)
        
        # Equivalent to saying "if name not in leaderboard"
        else:
       
            # Grab the scores to compare the users score against
            score_to_beat = max(set(leaderboard.values()))

            # Check the score can at least match the worst score on the leaderboard
            if score <= score_to_beat: 
                # List of players whose score is tied with the player
                in_jeporady = [p_name for p_name in leaderboard.keys() 
                               if leaderboard[p_name] == score_to_beat]
                # Shake it up
                random.shuffle(in_jeporady)
                    
                # From the shuffled list, choose a random player
                to_replace = random.choice(in_jeporady)

                msg = (f"Congrats! You beat out {to_replace} for their "
                        "position on the leaderboard")

                del leaderboard[to_replace]
                _update_player_score(leaderboard, 
                                     name, 
                                     score)
            else:
                msg = ("Unlucky, you didn't manage to break into the "
                       "leaderboard. Better luck next time!")
        print(msg)


def _update_player_score(leaderboard : shelve.DbfilenameShelf, 
                         name : str, 
                         new_score : int): 
    leaderboard[name] = new_score

def _create_scoreboard_header(title, frill, amount_of_frills) -> str:
    """Returns the scoreboards leading text.
    
    Args:
        title:
            A string used to indicate what the collection of highscores
            is called
        frill:
            A string used to encase the title.
        amount_of_frills:
            An integer indicating the number of frills to encase the title with

    Returns:
        A string representing the scoreboards header

    Example:
        title = "Scores", frill = "+", amount_of_frills = 5 ->

        \"+++++
        Scores
        +++++
        \"
    """ 
    frills = frill * amount_of_frills
    title = title.center(amount_of_frills)  
    return "\n".join([frills, title, frills])
    

def read_scores():
    """Print the leaderboard to the console.


    I vaugley remember an issue my professor had when trying to run this
    program that involed a pre-exisiting file crashing the game. The shelve
    file can't be deleted (kinda defeats the whole purpose of persistent
    storage :P) but I'm also not going to try and replicate the issue for a
    one-off college project. Just know, if the game crashes, it's more than
    likely a problem with the filename.  The fix is either to change the 
    filename or delete the existing file.
    """
    
    num_frills = 20
    header_frill = "="
    title = "Highscores"

    with shelve.open("scores.txt") as leaderboard:
        # If the file is empty then don't do anything
        if len(leaderboard) > 0:

            print(_create_scoreboard_header(title, header_frill, num_frills))
            
            # Use the score as the key
            sorted_lboard = sorted(leaderboard.items(), key=lambda x: x[1])

            name_padding = max([len(name[0]) for name in sorted_lboard])
            
            for record in sorted_lboard:
                name, score = record[0],record[1]
                name = name.rjust(name_padding)

                result = " : ".join([name, str(score)]).center(num_frills)
                print(result)

            print(header_frill * num_frills)
