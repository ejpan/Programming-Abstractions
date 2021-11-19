"""
File: moving_circles.py 

Author: Sharthok Rayan Pal & Eric Pan

Date: 10/10/21

Description: Program that gets two circle locations from the
user, then draws a line between them, and 
displays the distance between them midway along
the line.  The user can drag either circle around,
and the distance is kept updated.
"""

# Imports
from tkinter import *
import tkinter as tk
from enum import Enum
import math

class MovingCircles:
    def __init__(self):
        """ Constructor for Fractal Tree class """

        self.window = tk.Tk()
        self.window.title("Moving Circles")

        #Circle Canvas
        self.canvas = tk.Canvas(self.window, width = 400, height = 400)
        self.canvas.pack()
        self.canvas.grid(row = 1, column = 1)
        
        #Initalizes state and binds button press and motion to mouse_click and mouse_motion handlers.
        self.state = State.FIRST_BOB
        self.BOB_r = 20
        self.canvas.bind("<ButtonPress-1>", self.mouse_click_handler)
        self.canvas.bind("<B1-Motion>", self.mouse_motion_handler)

        self.fill_color = 'red'

        #Creates Button frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row = 2, column = 1)

        #Creates Button to clear the screen
        self.button = tk.Button(self.button_frame, text = "Clear", width = 5, command = self.clear)
        self.button.grid(row = 2, column = 1)

        #Creates Button that quits the program
        self.quit_button = tk.Button(self.button_frame, text = "Quit", width = 5, command = self.quit)
        self.quit_button.grid(row = 2, column = 2)

        self.BOB = None

        self.window.mainloop()

    def mouse_click_handler(self,event):
        """ Function that handles the mouse click event. This creates the circles and line that displays the length. """

        #Creates the first circle
        if self.state == State.FIRST_BOB:
            self.firstBOB_x = event.x
            self.firstBOB_y = event.y
            self.firstBOB = self.canvas.create_oval(self.firstBOB_x - self.BOB_r, self.firstBOB_y - self.BOB_r, self.firstBOB_x + self.BOB_r, self.firstBOB_y + self.BOB_r, fill = self.fill_color, tags = ("all", "firstBOB"))
            self.state = State.SECOND_BOB

        #Creates the second circle AND the line
        elif self.state == State.SECOND_BOB:
            self.secondBOB_x = event.x
            self.secondBOB_y = event.y
            self.canvas.create_line(self.firstBOB_x, self.firstBOB_y, self.secondBOB_x, self.secondBOB_y, fill = self.fill_color, tags = ("all", "line"))
            self.line_length_var = (math.sqrt(((self.secondBOB_x - self.firstBOB_x)**2)+((self.secondBOB_y - self.firstBOB_y)**2)))
            self.float_length = "{:.2f}".format(self.line_length_var)
            self.textcord_x = (self.secondBOB_x + self.firstBOB_x)/2
            self.textcord_y = (self.secondBOB_y + self.firstBOB_y)/2
            self.canvas.create_text(self.textcord_x, self.textcord_y, text = self.float_length, tag = "length")
            self.secondBOB = self.canvas.create_oval(self.secondBOB_x - self.BOB_r, self.secondBOB_y - self.BOB_r, self.secondBOB_x + self.BOB_r, self.secondBOB_y + self.BOB_r, fill = self.fill_color, tags = ("all", "secondBOB"))
            self.state = State.BOB
        
        #This code chooses the BOB upon user click
        elif self.state == State.BOB:
            self.pos1 = self.canvas.coords(self.firstBOB)
            self.pos2 = self.canvas.coords(self.secondBOB)
            self.mx = event.x
            self.my = event.y
            if (self.mx >= self.pos2[0] and self.mx <= self.pos2[2] and self.my >= self.pos2[1] and self.my <= self.pos2[3]):
                self.BOB = self.secondBOB
                self.STABLE_BOB = self.pos1
                self.MOVING_BOB = self.secondBOB
            elif (self.mx >= self.pos1[0] and self.mx <= self.pos1[2] and self.my >= self.pos1[1] and self.my <= self.pos1[3]):
                self.BOB = self.firstBOB
                self.STABLE_BOB = self.pos2
                self.MOVING_BOB = self.firstBOB
            else:
                self.BOB = None
                

    
    def mouse_motion_handler(self, event):
        """ Function that handles the mouse motion event. This updates the circle location and the line that displays the length. """

        #Checks the state of self.BOB
        if self.BOB == None:
            return
        
        #Moves a circle when the user clicks on a BOB
        elif self.state == State.BOB:
            self.canvas.delete("line")
            self.canvas.delete("length")
            current_x = event.x
            current_y = event.y

            #Gets the change in distance from the current mouse position and previous mouse position
            del_x = current_x - self.mx
            del_y = current_y - self.my

            #Moves BOB
            self.canvas.move(self.BOB, del_x, del_y)
            self.mx = current_x
            self.my = current_y

            #This creates the line
            self.move = self.canvas.coords(self.MOVING_BOB)
            self.canvas.create_line(self.STABLE_BOB[0] + self.BOB_r, self.STABLE_BOB[1] + self.BOB_r, self.move[0] + self.BOB_r, self.move[1]+ self.BOB_r, fill = self.fill_color, tags = ("all", "line"))

            #Computes the magnitude of the line and is displayed
            self.line_length_var = (math.sqrt((((self.move[0] + self.BOB_r) - (self.STABLE_BOB[0] + self.BOB_r) )**2)+(((self.move[1]+ self.BOB_r) - (self.STABLE_BOB[1] + self.BOB_r))**2)))
            self.float_length = "{:.2f}".format(self.line_length_var)
            self.textcord_x = (self.STABLE_BOB[0] + self.BOB_r + self.move[0] + self.BOB_r)/2
            self.textcord_y = (self.STABLE_BOB[1] + self.BOB_r + self.move[1]+ self.BOB_r)/2
            self.canvas.create_text(self.textcord_x, self.textcord_y, text = self.float_length, tag = "length")
        
            



    def clear(self):
        """ Function that clears the canvas. """
        self.canvas.delete('all')
        self.state = State.FIRST_BOB

    def quit(self):
        """ Function that quits the program. """

        self.window.destroy()

class State(Enum):
    """ Handles the mouse click stages. """
    FIRST_BOB = 1
    SECOND_BOB = 2
    BOB = 3
    STILL = 4

  
if __name__ == "__main__":
    # Create GUI
    MovingCircles()