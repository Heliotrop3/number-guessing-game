#Author: Tyler Huffman
#Last Modified: 5/23/2020

import random
import time
import sys
import numbers
import os
import shelve
import ctypes
import webbrowser

# Define the top and bottom of the range of possible values
# to pick a random number from
MAX_RANGE = 100
MIN_RANGE = 1

def delayed_print(text):
    """
    A function to print the text character by character with a pause
    after each character sentence
    """
    # Define the characters that deserve a slight pause after them
    pause_chars = ['.','?','!', ',']
    
    for character in text:
        # Push the char into the output buffer
        sys.stdout.write(character)
        
        # Push the contents of the output buffer to the screen
        sys.stdout.flush()
        
        # If the character is one of the
        # pause chars, add an additional
        # slight pause for emphasis 
        if character in pause_chars:
            time.sleep(0.75)
            
        time.sleep(0.045)
    # Return an empty string otherwise print statements will
    # concatenate "None" when utilizing this method.
    return ""

def get_name():
    """
    Define the player's name.  If they don't provide a name we
    assign one to them
    """
    name = str(input(("What is your name? ")))
    if (len(name) == 0):
        return "John Doe"
    return name

def clear_screen():
    """
    Clear the cmd/terminal window
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    

def greetings(player_name, number_of_attempts):
    """
    Greet the user with their player_name
    and give them a rundown on the rules
    """
    # Store the intro messages in a list
    intro = [
            "Greetings {}!".format(player_name),
            ("You have {} attempts to guess the number "
             "I am thinking of."
            ).format(number_of_attempts),
            ("I am thinking of an integer between and including "
             "1 and 100."
             ),
            ("Entering a character, string, or floating point will "
             "incur a penalty..."
             ),
             "You have been warned."
            ]

    # Display each intro message
    for msg in intro:
        msg = msg + "\n"
        delayed_print(msg)
        time.sleep(1)
        
    # Effectively cause the messages to dissapear
    clear_screen()

def guessing_game(player_name, number_of_attempts):
    """
    This is the heart of the game.  This function generates and
    "interacts" with the player.  We use a while loop and i to
    enable control over punishing the player for entering
    non-numerical values or floating point numbers.  Yes this is
    harsh but if you're reading this that means you can tweak it
    to your preferences.
    """
    # Generate the random number
    num_to_guess = random.randint(MIN_RANGE,MAX_RANGE)
    # Initialize a counter for invalid attempts and another for guesses
    invalid_counter,i = 0,0
    
    # In an effort to make the game feel somewhat interactive I decided
    # to add a variety of responses to input that is higher, lower,
    # flat out the wrong type, and then the correct number
    too_high = [
                "Thats too large!",
                "The number I am thinking of is smaller than that.",
                "I am thinking of a smaller number.",
                ("The number I am thinking of is of a lower "
                "order of magnitude."
                 ), 
                "Try a smaller number.",
                "Let me think... Nope, thats too high!",
                "The number I am thinking of is less than that."
                ]

    too_low = [
               "My number is bigger than that!",
               "Too small!",
               "Not large enough!",
               "Let me think... No, thats too small to be my number.",
               "I am thinking of a larger number.",
               "My number is larger than that!",
               "My number is greater than that!"
               ]

    correct_guess = [
                     ("Let me think... Yes, that is in fact the number "
                      "I am thinking of!"
                      ),
                      "Good guess, it's correct!",
                      "Yep, thats my number!",
                      "Hmmmm... You are correct!",
                      "Spot on!",
                      ("Let me consult with Grand Master Hoyle....."
                      "{}, according to Hoyle, you are "
                      "correct!".format(player_name)
                      ),
                      ("Spot on old chum! {} is the number I was"
                      "thinking of!".format(num_to_guess)
                      ),
                      ("Righteous answer {}, you are "
                      "correct!".format(player_name)
                       ),
                     "{}, you are correct!".format(player_name)
                     ]
    
    # I realize I could shorten the number of responses for each key
    # and stretch them out.  I think, however, having 5 responses for
    # each of the five guesses gives the game a more intense breath of
    # life...  I also realize this may incentivise entering invalid
    # input.
    # 
    # Grabbing from invalid_answer does not scale with number of
    # guesses.  I'm sure theres a way to implement scaling punishment
    # using modular arithmetic.  I leave that exercise for the reader
    # to complete.  My solution was to catch the key error thrown and
    # terminate the game when asking the dictionary for a non-existent
    # key
    invalid_answer = {
        1: ("Am I a joke to you?",
            "Do you think I am kidding?",
            "Did you read the rules?",
            "I am warning you...",
            ("You caught the part about punishing "
             "for invalid input right?"
            )
            ),
        
        2: ("When will you learn that your actions have conseqeunces?",
            "Keep this up and you will run out of guesses!",
            "Fortune favors the bold... unfortunately for you I do not."
            ),
                      
        3: ("Listen here, play by the rules or else...",
            "If you continue to misbehave I'll have to punish you."
            ),
        
        # The sentence is duplicated because otherwise the random
        # choice will slice a random character from the sentence
        4: (("Right, if you enter another invalid input I'm putting an "
            "end to your shenanigans...\nTry me."
             ),
            ("\nRight, if you enter another invalid input I'm putting an "
            "end to your shenanigans...\nTry me."
             )
            )
        }

    while i < number_of_attempts:
        try:                                                            
            print("Attempts remaining: {}".format(number_of_attempts - i
                                                  )
                  )
            suc_msg = random.choice(correct_guess) + "\n"
            
            too_high_msg = random.choice(too_high) + "\n"
                           
            too_low_msg = random.choice(too_low) + "\n"
            
            num_guessed = int(input("Guess the number: "))
            
            # If they correctly guessed the number show one of the
            # victory messages and return the number of gueses taken
            if (num_guessed == num_to_guess):
                print(delayed_print())
                
                # If they got it on their first, make i reflect as much
                if (i == 0):
                    return i+1
                return i
            
            # If the number is greater then the max range print out a
            # generic "Out of range" message
            elif (num_guessed > MAX_RANGE):
                i += 1
                print(delayed_print(("Incorrect, the integer I am "
                                    "thinking of is no larger than {}\n"
                                     ).format(MAX_RANGE)
                                    )
                      )

            # If the number is lower then the min range print out a
            # generic "Out of range" message
            elif (num_guessed < MIN_RANGE):
                i += 1
                print(delayed_print(("Incorrect, the integer I am "
                                     "thinking of is no less than {}\n"
                                     ).format(MIN_RANGE)
                                    )
                      )
                
            # If they overshot the value increase the guess count and
            # show a random message from too_high
            elif (num_guessed > num_to_guess):
                i += 1
                
                print(delayed_print(too_high_msg))
            
            # If they undershot the value increase the guess count and
            # show a random message from too_low
            else:
                i+=1
                print(delayed_print(too_low_msg))
                
        except ValueError:
            # If the user gets cheeky and throws non-integer values
            # we catch the error and penalize them a guess
            # 
            # I want the program to have a certain degree of life to it.
            # That being said if someone changes the number of guesses a
            # user is allowed to anything other than 5 then this won't
            # work as intended.
            
            try:
                # Increase the number of times
                # they've entered invalid input.
                invalid_counter +=1

                # We give them 5 chances to enter
                # (This could be changed to number_of_attempts)
                if invalid_counter >= 5:
                    # If they push their luck too much we open their
                    # webrowser and rickroll them then game over
                    # them and exit the program
                    yt_link = ("https://www.youtube.com"
                               "/watch?v=dQw4w9WgXcQ")
                    troll_msg = "Get Rickrolled you troll"
                    (webbrowser.open(yt_link) |
                     ctypes.windll.user32.MessageBoxW(0,
                                                      # Message
                                                      troll_msg,
                                                      # Title
                                                      troll_msg,
                                                      0
                                                     )
                     )
                    time.sleep(1)  
                    print(delayed_print("-=Game Over=-"))
                    input(("Press any key to contemplate the "
                          "decisions you made..."
                           )
                          )
                    sys.exit(0)
                    
                # If they have yet to reach the great threshold of Rick
                # then print one of the warning mesages associated with
                # their number of invalid attempts     
                else:
                    inv_msg = str("\n"
                                  + random.choice(
                                      invalid_answer[invalid_counter]
                                      )
                                  + "\n"
                                  )
                    print(delayed_print(inv_msg)
                          )
                    
                    # Make the user pay the troll
                    # their dues and dock them a guess
                    i += 1
                    
            # Catch the case where someone decides
            # to alter the number of attempts
            except KeyError:
                print("Incorrect: Illegal value submitted") 
                print("You has been docked a guess\n")
                
                # The user still has to pay the
                # troll their dues times two
                i += 2

    # If the user runs out of attempts show them
    # game over text and the random number
    print(delayed_print("-=Game Over=-")
          )
    print("The number I was thinking of was {}".format(num_to_guess)
          )
    
    return i # Return the number of guesses taken

def keep_playing(player_name):
    """
    Ask the user if they want to play again
    """
    valid_input = False
    valid_chars = ["y","n"]
    while valid_input == False:
        try:
            keep_playing = str(input(("Do you wish to "
                                     "play again? (y/n) "
                                      )
                                     )
                               ).lower()
            
            if keep_playing not in valid_chars:
                print("Error: Expecting a \"y\" or \"n\", "
                      "recieved {}\n".format(keep_playing)
                      )

            elif keep_playing == "y":
                os.system('cls' if os.name == 'nt' else 'clear')
                return True
            
            else:
                print(delayed_print("Goodbye {}".format(player_name)
                                    )
                      )
                time.sleep(2.5)
                return False
        except ValueError:
            print(("Error: Expecting a \"y\" or \"n\", "
                  "recieved {}\n".format(keep_playing)
                   )
                  )

def update_session_score(score, list_of_player_scores):
    """
    Keep track of the session scores. This list wil die
    when the program is terminated.
    """
    # Add the most recent result to their score ledger
    list_of_player_scores.append(score)

    # If they've played more than once print out their previous results
    if len(list_of_player_scores) > 1:
        print("Ledger of Guesses: {}".format(list_of_player_scores))
        
    return list_of_player_scores

def check_persistent_score(player_name, player_score):
    """
    The only way to get onto the scoreboard is, and I cannot emphasize
    this enough, have a lower score. The player will not get onto the
    highscore list if they tie another user for a score.

    Keep track of the top 3 best scores using shelve. This dict will
    not die when the program is terminated.
    """
    scoreboard = shelve.open("scores.txt")
    # If the dict is empty theres nothing to check. Chuck the player's
    # name and score into the scoreboard
    if len(scoreboard) < 3:
        try:
            # If the player's highscore is a new personal best
            print(scoreboard[player_name])
            if scoreboard[player_name] > player_score:   
                scoreboard[player_name] = player_score
                print(delayed_print(("Congratulations {}, you've set "
                                     "a new personal highscore!"
                                     "".format(player_name)
                                     )
                                    )

                      )
                read_persistent_score()
                
        # Catch the case where this is the player's first time
        except KeyError:
            # Add their score to the highscore file
            scoreboard[player_name] = player_score
            
            print(delayed_print(("Congratulations {}, you've set a "
                                "new personal highscore!"
                                "".format(player_name)
                                 )
                                )
                  )
            read_persistent_score()
            
    # If the dict is not empty than we iterate through the highscores
    # in descending order and if f the player's score is better than
    # a pre-existing score replace the pre-existing score.  Smaller is
    # better in this instance.
    else:
        # Iterate through the highscores in descending order
        for existing_score in sorted(scoreboard.values()):
            if player_score < existing_score:
                print(delayed_print(("Congratulations {}, you've set a "
                                    "highscore!".format(player_name)
                                     )
                                    )
                      )
                
                # Find the user associated with the beaten score and
                # replace them
                for user in scoreboard:
                    if scoreboard[user] == existing_score: 
                        del scoreboard[user]
                        scoreboard[player_name] = player_score
                        break # Break out of loops
                break         # |      |   |   |
    scoreboard.close()

def read_persistent_score():
    """
    I vaugley remember an issue my professor had when trying to run this
    program that involed a pre-existing file interferring with correctly
    saving.  That was long enough ago that I don't remember enough about
    what the problem was to patch it.  So if the program crashes it's
    more than likely a problem with the filename.  The fix is either to
    change the filename or delete the existing file.
    """
    # Open the highscore file
    hi_scores = shelve.open("scores.txt")
    
    # If the file is empty then don't do anything
    if len(hi_scores) < 3:
        pass
    # If their are names and scores inside of the
    # file display a highscore scoreboard
    else:
        print("Highscores")                               
        print("="*20)

        # Iterate over the inhabitants of the highscores and write
        # their names and scores to the screen
        with shelve.open("scores.txt") as db:
            for player in db:
                print("%s : %i" %(player, db[player]))
        print("="*20)

'''
The Master Control Program (The Driver)
'''
def MCP(number_of_attempts):
    scores_for_session = []
    clear_screen()
    try:
        user = get_name()
        # Grab any pre-existing scores
        read_persistent_score()

        # Let the user know the rules
        greetings(user,number_of_attempts)
        cont_play = True
        
        # Throw the user into a while loop that will be broken
        # once they convey they no longer wish to play
        while (cont_play == True):
            # The guessing part of the game
            score = guessing_game(user, number_of_attempts)

            # Check if a highscore has been set
            check_persistent_score(user, score)

            # Update the player's scores based on the results
            scores_for_session = update_session_score(score, scores_for_session)

            # Check if they still want to play
            cont_play = keep_playing(user)
            
    # Catch the intterupt request
    except KeyboardInterrupt
        print("\nExiting the Matrix\n")
        time.sleep(1)
        sys.exit(0)
        
# Call the driver 
MCP(5)
