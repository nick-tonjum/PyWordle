from tkinter import *
from tkinter import messagebox
from pynput import keyboard
import random


# Creates the main window
window = Tk()

# Configure the title, dimensions, and background color
window.title("PyWordle")
window.configure(height=720,width=640)
window.configure(background="#DDFEFF")


# Variable to track whether the window is in focus or not
# (used to make sure the program doesn't track the keyboard when it's not in focus)
focused = False


# Creating some variables
currentrow = 1 # Row the new letter will be typed on
currentcolumn = 1 # Column the letter will be typed on
queuedletters = []


# Open the wordlist file and read each line as an object in the word list
wordlistfile = open("wordlist.txt",'r')
wordlist = wordlistfile.readlines()


# Function to interpret keyboard presses
def OnType(key):
    if focused: # Only interpret the keypresses if the window is in focus
        try:
            # Get the letter of the key that was pressed
            letter = key.char
            if letter.lower() in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                                  's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                # Add the letter to the letter 'queue' (type it on screen)
                queuedletters.append(letter.upper()) 
        except: # If there happens to be any errors, check if the key was the 'delete' key, otherwise ignore it completely
            try:
                if key.name == "backspace":
                    queuedletters.append("backspace")
            except:
                pass
            pass


# Using the keyboard listener module to listen to the keyboard
# Each time the keyboard is pressed the OnType function is called with the pressed key as a parameter
keyboardlistener = keyboard.Listener(on_press=OnType)
keyboardlistener.start()


# List to keep track of all the plotted boxes on screen
rows = [] 

# Function to track how many correct letters are in a word. If this is 5, then the game ends
correctletters = 0

# Function to check an entire word (row) to see how close it is to the predetermined word
def Check(row):
    global rows, selectedword, correctletters
    row -= 1
    column = 0
    correctletters = 0
    for label in rows[row]: # For each letter box in the row
        letter = label.cget("text") # Get the letter from the box
        if letter == selectedword[column]: # If that letter is in it's correct spot
            label.config(bg="#9DFF81") # Color it's box green
            correctletters += 1
        elif letter in selectedword: # If the letter is still in the word
            label.config(bg="#FDFF81") # Color it's box yellow
        else: # If none of the above conditions apply (the letter is wrong)
            label.config(bg="#FFCFCF") # Color it's box red
        column += 1 # Move onto the next column


# Function to restart/start the game
def RestartGame(condition=None):
    global selectedword, wordlist, currentrow, currentcolumn, queuedletters, correctletters, rows
    
    # If a condition is set (win or lose) display a message before starting a new game
    if condition == "win":
        messagebox.showinfo(title="Game Over",message="The word was " + selectedword + "\nYou Won!")
    if condition == "lose":
        messagebox.showerror(title="Game Over", message="The word was " + selectedword + "\nYou Lost!")
        
    # Start a new game and select a random word from the word list, making it uppercase
    selectedword = random.choice(wordlist).upper() 
    
    #print(selectedword) # Print the selected word in the console (for debugging purposes)
    currentrow = 1 # Set the current row to row 1
    currentcolumn = 1 # Set the current row to row 1
    correctletters = 0 # Set the correct letters to 0
    queuedletters = [] # Clear the queue of letters to be typed out
    rows = [] # Clear the rows and columns
    PlotBoxes() # Plot a new set of empty boxes


# Function to plot out the boxes on the screen
def PlotBoxes():
    global rows
    # The starting position of the boxes (top left corner coordinates)
    x = 80
    y = 100
    # Function to erase all currently existing boxes
    for row in rows:
        for column in row:
            column.destroy()
    # Plot new boxes
    for i in range(0,5): # 5 rows
        columns = []
        for z in range(0,5): # 5 column
            # Create a new box
            box = Label(relief="solid",padx=20,width=1,height=1,text="",font=("Arial",50))
            
            # Place the newly created box at a certain position. Depending on the current
            # row and column (tracking with the i and z variables in the for loops)
            # it's coordinates are shifted to the right or down in increments of 100 pixels
            # X value is the starting position value (80) plus the current column (z) * 100
            # Y value is the starting position value (100) plus the current row (i) * 100
            box.place(x=x+(z*100),y=y+(i*100))
            
            # If the box is in the first row, color it white
            if i == 0:
                box.config(bg="#FFFFFF")
            columns.append(box)
        rows.append(columns)


# Start a new game right away when this script is launched
RestartGame()

# Everything below runs constantly as the game goes on
while True:
    
    # Change the 'focused' variable based on if the window is focused or not
    if not window.focus_get() == None:
        focused = True
    else:
        focused = False
        
    # For each letter that's been typed out and processed into the queue
    for letter in queuedletters:
        # If it's a backspace, remove the last letter
        if letter == "backspace":
            if currentcolumn > 1:
                currentcolumn -= 1
                rows[currentrow-1][currentcolumn-1].configure(text="")
            queuedletters.remove(letter)
        # Otherwise
        else:
            # Change the text in the current box (determined by the current row and current column variables)
            # to the current letter that was just typed and put in queue.
            # *
            # Note: We're removing 1 from the currentrow and currentcolumn variables because of how lists
            # keeps track of objects. Since 0 is the first object in a list instead of 1, we have to subtract 1
            # from both variables to be able to address it properly.
            rows[currentrow-1][currentcolumn-1].configure(text=letter)
            
            # If we just processed the last letter in a column
            if currentcolumn == 5:
                # Check the current column's word with our Check() function
                Check(currentrow)
                
                # Move onto the next row and set our currentcolumn back to 1
                currentrow += 1
                currentcolumn = 1
                
                # If we haven't won or lost yet, every box in the column we just finished white
                if not correctletters == 5:
                    if not currentrow == 6:
                        for column in rows[currentrow-1]:
                            column.configure(bg="#FFFFFF")
            
            # If we haven't processed the last letter in the column, continue onto the next
            else:
                currentcolumn += 1
                
            # After typing the letter on screen, remove it from the queue since we're done with it
            queuedletters.remove(letter)

    if correctletters == 5: # If all letters are correct, restart the game with the "win" condition to display a message
        RestartGame("win")
    if currentrow == 6: # If we're now on row 6 (out of turns since we only have 5 rows) restart the game with the "lose" condition to display a message
        RestartGame("lose")
        
    # The below commands constantly keep our window and boxes updated
    window.update_idletasks()
    window.update()
