"""
File: fractal_tree.py
Author: Sharthok Rayan Pal & Eric Pan
Date: 10/10/2021
Description: Displays fractal tree
"""
import tkinter as tk
import math

class FractalTree:
    def __init__(self):
        """ Constructor for Fractal Tree class """


        self.window = tk.Tk() 
        self.window.title("Fractal Tree")


        #Fractal Tree Canvas
        self.canvas = tk.Canvas(self.window, width = 400, height = 400, borderwidth = 1, relief = 'solid')
        self.canvas.pack()
        self.canvas.grid(row = 1, column = 1)

        #Creates Button Frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row = 2, column = 1)

        #Creates the Advance Button
        self.button = tk.Button(self.button_frame, text = "Advance", width = 7, command = self.advance)
        self.button.grid(row = 2, column = 1, sticky = "EW")

        #Creates the Reset button
        self.button = tk.Button(self.button_frame, text = "Reset", width = 5, command = self.reset)
        self.button.grid(row = 2, column = 2, sticky = "EW")

        #Creates the quit button
        self.button = tk.Button(self.button_frame, text = "Quit", width = 5, command = self.quit)
        self.button.grid(row = 2, column = 3, sticky = "EW")

        #Creates the initial branch that is one-thirds times the height of the canvas
        self.canvas.create_line(200, 390, 200, 257)
        self.length = 400 * (1/3) #133
        self.current_levels_of_recursion = 0
        self.line_ratio = 0.58

        self.window.mainloop()

    def draw_fractal(self, x, y, length, deg, levels_of_recursion):
        """ Function for drawing the fractal with 5 parameters. 
        This computes the angles for the left and right child branches 
        of the fractal and draws the line  """

        if levels_of_recursion == 0:
            return
        else:
            
            #Computed the angle for the right portion of the fractal
            new_length = length * self.line_ratio
            new_deg_r = deg - 36
            angle_r = math.radians(new_deg_r)
            r_x = math.cos(angle_r) * new_length
            r_y = math.sin(angle_r) * new_length
            

            #Computes the angle for the left portion of the fractal
            new_deg_l = deg + 36
            angle_l = math.radians(new_deg_l)
            l_x = math.cos(angle_l) * new_length
            l_y = math.sin(angle_l) * new_length

            #Draws the line for both (left and right) parts of the fractal
            self.canvas.create_line(x,y, x + r_x, y - r_y, tag = "line")
            self.canvas.create_line(x,y, x + l_x, y - l_y, tag = "line")

            #Right Fractal recursion
            self.draw_fractal(x + r_x,y - r_y,new_length,new_deg_r, levels_of_recursion-1)
            #Left Fractal Recursion
            self.draw_fractal(x + l_x, y - l_y,new_length,new_deg_l, levels_of_recursion-1)


    def advance(self):
        """ Advance one level of recursion """
        
        
        #Advances one level of recursion by calling draw_fractal and increasing the levels of recursion
        self.deg = 90
        self.current_levels_of_recursion += 1
        self.draw_fractal(200, 257, self.length,self.deg, self.current_levels_of_recursion)

    def reset(self):
        """ Resets the recursion to 0 and removes any child branches. """
        self.canvas.delete("line")
        self.current_levels_of_recursion = 0


    def quit(self):
        """ Quits program """
        self.window.destroy()

if __name__ == "__main__":
    FractalTree()