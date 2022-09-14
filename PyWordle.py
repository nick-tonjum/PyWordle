from tkinter import *
from tkinter import messagebox
from pynput import keyboard
import random

window = Tk()
window.title("PyWordle")
window.configure(height=720,width=640)

window.configure(background="#DDFEFF")
focused = False

currentrow = 1
currentcolumn = 1
queuedletters = []

wordlistfile = open("wordlist.txt",'r')
wordlist = wordlistfile.readlines()

def OnType(key):
    if focused:
        try:
            letter = key.char
            if letter.lower() in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                                  's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                queuedletters.append(letter.upper())
        except:
            try:
                if key.name == "backspace":
                    queuedletters.append("backspace")
            except:
                pass
            pass

keyboardlistener = keyboard.Listener(on_press=OnType)
keyboardlistener.start()

rows = []
correctletters = 0

def Check(row):
    global rows, selectedword, correctletters
    row -= 1
    column = 0
    correctletters = 0
    for label in rows[row]:
        letter = label.cget("text")
        if letter == selectedword[column]:
            label.config(bg="#9DFF81")
            correctletters += 1
        elif letter in selectedword:
            label.config(bg="#FDFF81")
        else:
            label.config(bg="#FFCFCF")
        column += 1

def RestartGame(condition=None):
    global selectedword, wordlist, currentrow, currentcolumn, queuedletters, correctletters, rows
    if condition == "win":
        messagebox.showinfo(title="Game Over",message="The word was " + selectedword + "\nYou Won!")
    if condition == "lose":
        messagebox.showerror(title="Game Over", message="The word was " + selectedword + "\nYou Lost!")
    selectedword = random.choice(wordlist).upper()
    ##print(selectedword)
    currentrow = 1
    currentcolumn = 1
    correctletters = 0
    queuedletters = []
    rows = []
    PlotBoxes()



def PlotBoxes():
    global rows
    x = 80
    y = 100
    for row in rows:
        for column in row:
            column.destroy()
    for i in range(0,5):
        columns = []
        for z in range(0,5):
            box = Label(relief="solid",padx=20,width=1,height=1,text="",font=("Arial",50))
            box.place(x=x+(z*100),y=y+(i*100))
            if i == 0:
                box.config(bg="#FFFFFF")
            columns.append(box)
        rows.append(columns)



RestartGame()

while True:
    if not window.focus_get() == None:
        focused = True
    else:
        focused = False
    for letter in queuedletters:
        if letter == "backspace":
            if currentcolumn > 1:
                currentcolumn -= 1
                rows[currentrow-1][currentcolumn-1].configure(text="")
            queuedletters.remove(letter)
        else:
            rows[currentrow-1][currentcolumn-1].configure(text=letter)
            if currentcolumn == 5:
                Check(currentrow)
                currentrow += 1
                currentcolumn = 1
                if not correctletters == 5:
                    if not currentrow == 6:
                        for column in rows[currentrow-1]:
                            column.configure(bg="#FFFFFF")
            else:
                currentcolumn += 1
            queuedletters.remove(letter)

    if correctletters == 5:
        RestartGame("win")
    if currentrow == 6:
        RestartGame("lose")
    window.update_idletasks()
    window.update()
