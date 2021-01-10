import ctypes
import json
import os
import random
import sys
import time
import webbrowser

import utility

MAX_RANGE = 100
MIN_RANGE = 1

def is_valid_number(number : int) -> bool:
    """Return a boolean indicating whether number is within the range."""
    valid = True
    if (number > MAX_RANGE):
        msg = f"No, the number I am thinking of is no larger than {MAX_RANGE}"
        utility.delayed_print(msg)
        valid = False

    if (number < MIN_RANGE):
        msg = f"No, the number I am thinking of is no less than {MIN_RANGE}"
        utility.delayed_print(msg)
        valid = False

    return valid

def keep_playing(player_name) -> bool:
    """Determines whether the player wants to continue playing.
    
    Args:
        player_name: 
            A string representing the name of the player

    Returns:
        A boolean indicating whether to reset the game state or exit
    """
    valid_chars = ["y","n"]
    while True:

        answer = str(input("Do you wish to play again? (y/n): ")).lower()

        if answer not in valid_chars:
            print(f"Error: Expecting a \"y\" or \"n\" recieved {answer}\n")

        elif answer == "y":
            utility.clear_screen()
            return True
        
        else:
            utility.delayed_print(f"Goodbye {player_name}")
            time.sleep(2.5)
            utility.clear_screen()
            return False

def penalty_msg(msg : str, 
                invalid_counter : int) -> None:
    """Output penalty messages to the console.
    
    Args:
        msg:
           The string to 

        invalid_counter:
            An integer representing the number of times the player has entered
            an invalid input
    
    Returns:
        None
    """
    if invalid_counter <= 3:
        utility.delayed_print(msg)

    elif invalid_counter == 4:
        msg = ("Right, if you enter another invalid input I'm putting an "
               "end to your shenanigans...\nTry me.")
        utility.delayed_print(msg)
        
    else:
        # If they push their luck too much we open their webrowser, rickroll,
        # game over, and finally exit the program
        rick_roll()
        time.sleep(1)
        input("Press any key and contemplate your life choices...")
        sys.exit(0)

def greetings(player_name :str, 
              num_attempts : int) -> None:
    """Greet the user with their chosen name and provide the rules.
    
    Args:
        player_name:
            A string representing the user's chosen handle
        
        num_attempts:
            A positive, non-zero integer representing the number of attempts
            the player has before the game state is forcibly terminated

    Returns:
        None
    """

    # Store the intro messages in a list
    intro = [
                f"Greetings {player_name}!",

                (f"You have {num_attempts} attempts to guess the number "
                "I am thinking of."),

                "I am thinking of an integer between and including 1 and 100.",
                
                ("Entering a character, string, or floating point will incur "
                 "a penalty..."),

                "You have been warned.",
            ]
    
    utility.clear_screen()
    # Display each intro message
    for msg in intro:
        utility.delayed_print(msg)
        time.sleep(1)
        
    # Effectively cause the messages to dissapear
    utility.clear_screen()

def update_session_score(score : int, session_scores : list) -> list:
    """Return a list of scores across the given session.
    
    Args:
        score:
            The integer representing the number of guesses taken before
            the game state was terminated

        session_scores:
            A list containing the player's historical scores

    Returns:
        A list 
    """
    # Add the most recent result to their score ledger
    session_scores.append(score)

    # If they've played more than once print out their previous results
    if len(session_scores) > 1:
        print(f"Session Scores: {session_scores}")
        
    return session_scores

def load_responses(json_path : str=None) -> dict:
    """Return a dict containing responses to the player's guesses.
    
    Args:
        json_path: Optional; Filepath to json file containing responses. If
            no path is provided, defaults to looking in working folder. If file
            is not found, creates and returns a bare-metal dict representing
            the json object.
    
    Returns:
        A dict mapping keys to their corresponding responses. The responses are
        strings stored in a list. For example:

        { 
            "Invalid" : ["Wait, thats illegal!"],
            "Over"    : ["That number is too large!"],
            "Under"   : ["That number is too small!"],
            "Correct" : ["You got it!"]
        }

        Returned keys are always strings and returned values are always strings
        in lists. If the json file is not found then a dict like the example is
        returned.
        
    Raises:
        FileNotFoundError: Occurs when json_path does not exists.
        AttributeError: Occurs when attempting to load a json file that isn't
            of the correct format.
    """
    if json_path is None:
        json_path = "responses.json"

    try:
        with open("responses.json", 'r') as f:
            responses = json.loads(f.read())

    except (FileNotFoundError, AttributeError):
        responses = {
            "Invalid" : ["Invalid"],
            "Over" : ["Too High!"],
            "Under" : ["Too Low!"],
            "Correct" : ["You got it!"]
        }

    finally:
        return responses

def guessing_game(num_attempts : int) -> int:
    """Give the player a finite number of attempts to guess a random number.
    
    Args:
        num_attempts: A positive, non-zero integer representing the number of
            attempts the player has until forcibly terminating the game
    
    Returns:
        A positive, non-zero integer representing the number of guesses
        taken between initializing the game state and terminating the game
        state
    """
    # Load the systems responses
    responses = load_responses()

    # Generate the random number
    num_to_guess = random.randint(MIN_RANGE,MAX_RANGE)
    
    # Initialize a counter for invalid attempts and another for guesses
    invalid_counter, guess_counter = 0,0
    
    while  num_attempts > guess_counter:
        try:                                                            
            print(f"Attempts remaining: {num_attempts - guess_counter}")
            
            num_guessed = int(input("Guess the number: "))
            guess_counter += 1

            if not is_valid_number(num_guessed):
                continue
            
            # Show a message corresponding to the accuracy of the guess.
            if (num_guessed == num_to_guess):
                utility.delayed_print(random.choice(responses['Correct']))
                return guess_counter
            
            elif (num_guessed > num_to_guess):
                utility.delayed_print(random.choice(responses['Over']))
            
            else:
                utility.delayed_print(random.choice(responses['Under']))
            
        # If the user gets cheeky and throws non-integer values we catch the
        # error and penalize them a guess and increment the invalid counter
        except ValueError:
            guess_counter += 1
            invalid_counter +=1
            msg = random.choice(responses['Invalid'])
            
            penalty_msg(msg,invalid_counter)
            
    # If the user runs out of attempts show them
    # game over text and the random number
    utility.delayed_print("-=Game Over=-")
    print(f"The number I was thinking of was {num_to_guess}") 

    return guess_counter # Return the number of guesses taken

def rick_roll() -> None:
    """If you know, you know."""

    msg = "Get Rickrolled you troll"
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    ctypes.windll.user32.MessageBoxW(0,
                                     msg, # Message
                                     msg, # Title
                                     0
                                   )

