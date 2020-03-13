#Author: Tyler Huffman
#Last Modified: 3/13/2020
import random, time, sys, numbers, os, shelve, ctypes   

MAX_RANGE = 100
MIN_RANGE = 1

'''
A function to print the text 
'''
def delayed_print(text):
    pause_chars = ['.','?','!', ','] # Define the characters that deserve a slight pause after them
    for character in text:           # Iterate across the text char by char
        sys.stdout.write(character)  # Push the char into the output buffer
        sys.stdout.flush()           # Push the contents of the output buffer to the screen
        if character in pause_chars: # If the character is one of the pause chars, add an additional slight pause for emphasis 
            time.sleep(0.75)
        time.sleep(0.045)
    return ""                        # Return an empty string otherwise print statements will concatenate "None" when utilizing this method.

'''
Grab the user's name
'''
def get_name():
    name = str(input(("What is your name? ")))
    if (len(name) == 0):                        # If they don't give us a character
        return "John Doe"                       # We give them a name
    return name

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
'''
Greet the user with their chosen player_name and give them the basic rules
'''
def greetings(player_name, number_of_attempts):
    # An array to hold the intro message to the user
    greetings = ["Greetings {}!".format(player_name),
                 "You have {} attempts to guess the number I am thinking of.".format(number_of_attempts),
                 "I am thinking of an integer between and including 1 and 100.",
                 "Entering a character, string, or floating point will incur a penalty...",
                 "You have been warned."]
    
    for msg in greetings:     # Display each message to the user using the delayed print function
        delayed_print(msg)
        print("")             # Add a new line and take a pause after each message
        time.sleep(1)
    clear_screen()            # Clear the screen

'''
This is the heart of the game. This function generates and "interacts" with the player.
We use a while loop and i to enable control over punishing the player for entering
non-numerical values or floating point numbers. Yes this is harsh but if you're reading
this that means you can tweak it to your preferences.
'''
def guessing_game(player_name, number_of_attempts):
    num_to_guess = random.randint(MIN_RANGE,MAX_RANGE) # Generate the random number
    invalid_counter,i = 0,0                            # Initialize a counter for invalid attempts and guesses
    ###Debugging Purposes
    ###print(num_to_guess)

    '''
    In an effort to make the game feel somewhat interactive I decided to add a variety of responses to
    input that is higher, lower, flat out the wrong type, and then the correct number
    '''
    too_high = ["Thats too large!",
                "The number I am thinking of is smaller than that.",
                "I am thinking of a smaller number.",
                "The number I am thinking of is of a lower order of magnitude.", 
                "Try a smaller number.",
                "Let me think... Nope, thats too high!",
                "The number I am thinking of is less than that."]

    too_low = ["My number is bigger than that!",
               "Too small!",
               "Not large enough!",
               "Let me think... No, thats too small to be my number.",
               "I am thinking of a larger number.",
               "My number is larger than that!",
               "My number is greater than that!"]

    correct_guess = ["Let me think... Yes, that is in fact the number I am thinking of!",
                     "Good guess, it's correct!",
                     "Yep, thats my number!",
                     "Hmmmm... You are correct!",
                     "Spot on!",
                     "Let me consult with Grand Master Hoyle..... %s, according to Hoyle, you are correct!" %player_name,
                     "Spot on old chum! %i is the number I was thinking of!"%num_to_guess,
                     "Righteous answer %s, you are correct!" %player_name,
                     "%s, you are correct!"%player_name]
    '''
    I realize I could shorten the number of responses for each key and stretch them out. I think, however,
    having 5 responses for each of the five guesses gives the game a more intense breath of life... I also
    realize this may incentivise entering invalid input.

    !!!NOTICE!!! - Grabbing from invalid_answer does not scale with number of guesses that are not restricted to 5.
    '''
    invalid_answer = {1: ("Am I a joke to you?","Do you think I am kidding?","Did you read the rules?","I am warning you...","Where you not paying attention when I said invalid input would be punished?"),
                      2: ("When will you learn that your actions have conseqeunces?","Keep this up and you will run out of guesses!","Fortune favors the bold... unfortunately for you I do not."),
                      3: ("Listen here, play by the rules or else...","If you continue to misbehave I'll have to punish you."),                   
                      ## The reason the below sentence is duplicated is because otherwise the random choice will grab a random slice from the sentence
                      4: ("Right, if you enter another invalid input I'm putting an end to your shenanigans...\nTry me.",
                          "\nRight, if you enter another invalid input I'm putting an end to your shenanigans...\nTry me.")}

    while i < number_of_attempts:                                       # The player has x attempts to guess the random number
        try:                                                            # If the user gets cheeky and throws non-integer values we catch the sneak and lop off one of their guesses
            print("Attempts remaining: %i" %(number_of_attempts - i))   # Show how many guesse they have left
            num_guessed = int(input("Guess the number: "))              # Read in their guess
            if (num_guessed == num_to_guess):                           # If they correctly guessed the number show one of the victory messages and return the number of gueses taken
                print(delayed_print(random.choice(correct_guess)))
                if (i == 0):                                            # If they got it on their first try make i reflect as much
                    return i+1
                return i
            elif (num_guessed > MAX_RANGE):                             # If the number is greater then the max range print out a generic "Out of range" message
                i += 1
                print(delayed_print("Incorrect, the integer I am thinking of is no larger than 100"))
                print("")
            elif (num_guessed < MIN_RANGE):                             # If the number is lower then the min range print out a generic "Out of range" message
                i += 1
                print(delayed_print("Incorrect, the integer I am thinking of is no less than 1"))
                print("")
            elif (num_guessed > num_to_guess):                          # If they overshot the value increase the guess count and show a random message from too_high
                i += 1
                print(delayed_print(random.choice(too_high)))
                print("")
            else:                                                       # If they undershot the value increase the guess count and show a random message from too_low
                i+=1
                print(delayed_print(random.choice(too_low)))
                print("")
        except ValueError:                                              # If their being orny and enter string or char value
            '''
            I want the program to have a certain degree of life to it. That being said if someone changes the number
            of guesses a user is allowed to anything other than 5 then this won't work as intended. 
            
            I could probably use math to make the punishment scale but there exists a sweet spot of guesses that allows
            you to play the game and feel challenged by it... Well, as challenged and involved as one can get from 
            guessing a number.
            '''
            try:
                invalid_counter +=1       # Increase the number of times they've entered invalid input.
                if invalid_counter >= 5:  # We give them 5 chances to enter (This could be changed to number_of_attempts)
                    import webbrowser     # If they push their luck too much we open their webrowser and rickroll them then game over them and exit the program
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ") | ctypes.windll.user32.MessageBoxW(0, "Get Rickrolled you troll", "Get Rickrolled you troll", 0)
                    time.sleep(1)
                    print(delayed_print("-=Game Over=-"))
                    input("Press any key to contemplate the decisions you made...")
                    sys.exit(0)
                else:                    # If they have yet to reach the threshold of Rick then print one of the warning mesages associated with their number of invalid attempts 
                    print("")
                    print(delayed_print(random.choice(invalid_answer[invalid_counter])))
                    print("")
                    i += 1              # Make the user pay the troll their dues and dock them a guess
            except KeyError:            # Catch the case where someone decides to alter the number of attempts
                print("Incorrect: Illegal value submitted") 
                print("You has been docked a guess")
                i += 2                  # The user still has to pay the troll their dues times two
                print("")

    print(delayed_print("-=Game Over=-"))                      # If the user runs out of attempts show them game over text and the random number
    print("The number I was thinking of was %i" %num_to_guess)
    return i                                                   # Return the number of guesses taken

'''
Ask the user if they want to play again
'''
def keep_playing(player_name):
    valid_input = False
    valid_chars = ["y","n"]
    while valid_input == False:
        try:
            keep_playing = str(input("Do you wish to play again? (y/n) ")).lower()
            if keep_playing not in valid_chars:
                print("Error: Expecting a \"y\" or \"n\", recieved %s" %keep_playing)
                print("")
            elif keep_playing == "y":
                os.system('cls' if os.name == 'nt' else 'clear')
                return True
            else:
                print(delayed_print("Goodbye %s" %player_name))
                time.sleep(2.5)
                return False
        except ValueError:
            print("Error: Expecting a \"y\" or \"n\", recieved %s" %keep_playing)
            print("")

'''
Keep track of the session scores. This list wil die when the program is terminated.
'''
def update_session_score(score, list_of_player_scores):
    list_of_player_scores.append(score)                         # Add the most recent result to their score ledger
    if len(list_of_player_scores) > 1:                          # If they've played more than once print out their previous results
        print("Ledger of Guesses: %s" %list_of_player_scores)
    return list_of_player_scores                                # Send back the updated score ledger

'''
The only way to get onto the scoreboard is, and I cannot emphasize this enough,
have a lower score. The player will not get onto the highscore list if they tie
another user for a score.

Keep track of the top 3 best scores. This dict will not die when the program is terminated.
'''
def check_persistent_score(player_name, player_score):
    file = shelve.open("scores.txt")
    if len(file) < 3:                                # If the dict is empty theres nothing to check. Chuck the player's name and score into the scoreboard
        try:                                         # Check if the player's highscore is a new personal best
            if file[player_name] > player_score:   
                file[player_name] = player_score
                print(delayed_print("Congratulations %s, you've set a new personal highscore!" %player_name))
                read_persistent_score()
        except KeyError:                             # Catch the case where this is the player's first time
            file[player_name] = player_score         # Add their score to the highscore file
            print(delayed_print("Congratulations %s, you've set a new personal highscore!" %player_name))
            read_persistent_score()                  # Display the highscores
    else:                                            # If the dict is not empty
        for existing_score in sorted(file.values()): # Iterate through the highscores in descending order
            if player_score < existing_score:        # If the player's score is better than a pre-existing score replace the pre-existing score
                print(delayed_print("Congratulations %s, you've set a highscore!" %player_name))
                for user in file:                    # Iterate through the dictionary of current highscores
                    if file[user] == existing_score: # Find the user associated with the worse score and replace them
                        del file[user]
                        file[player_name] = player_score
                        break                        # Break out of the loops
                break
    file.close()                                     # Close the file

'''
I vaugley remember an issue my professor had when trying to run this program that involed a pre-existing file
interferring with correctly saving. That was long enough ago that I don't remember enough about what the problem
was to patch it. So if the program crashes it's more than likely a problem with the filename. The fix is either to
change the filename or delete the existing file.
'''
def read_persistent_score():
    file = shelve.open("scores.txt")                      # Open the highscore file
    if len(file) < 3:                                     # If the file is empty then don't do anything
        pass
    else:                                                 # Otherwise if their are names and scores inside of the file display a highscore scoreboard
        print("Highscores")                               
        print("="*20)
        with shelve.open("scores.txt") as db:             # Iterate over the inhabitants of the highscores and write their names and scores to the screen
            for player in db:
                print("%s : %i" %(player, db[player]))
        print("="*20)

'''
The Master Control Program (The Driver)
'''
def MCP(number_of_attempts):
    scores_for_session = []                 # Create an array to keep track of the user's scores during their session
    clear_screen()
    try:
        user = get_name()                   # Get the user's name
        read_persistent_score()             # Grab any pre-existing scores
        greetings(user,number_of_attempts)  # Greet the user
        cont_play = True                    # Throw the user into a while loop that will be broken once they no longer wish to play
        while (cont_play == True):          # Play the game
            score = guessing_game(user, number_of_attempts)                      # The guessing game
            check_persistent_score(user, score)                                  # Check if a highscore has been set
            scores_for_session = update_session_score(score, scores_for_session) # Update the player's scores based on the results
            cont_play = keep_playing(user)                                       # Check if they still want to play
    except KeyboardInterrupt:                                                    # Catch the intterupt request
        print("\nExiting the Matrix\n")
        time.sleep(1)
        sys.exit(0)
   
MCP(5) # Call the driver