import time
import sys
import os

def clear_screen():
    """Clear the cmd/terminal window."""
    os.system('cls' if os.name == 'nt' else 'clear')


def delayed_print(text):
    """Print character by character, include a delay after each sentence."""
    # Chars to pause after
    pause_chars = ['.','?','!', ',']
    
    for character in text:
        # Push the char into the output buffer
        sys.stdout.write(character)
        
        # Push the contents of the output buffer to the screen
        sys.stdout.flush()
        
        if character in pause_chars:
            time.sleep(0.75)
            
        time.sleep(0.045)
    print("\n")
    # Return an empty string otherwise print statements will
    # concatenate "None" when utilizing this method.
    #return ""
