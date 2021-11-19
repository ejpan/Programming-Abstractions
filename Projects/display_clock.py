# File: addressbook.py
# Author: Eric Pan and Gabriel Seidl
# Date: October 3, 2021
# Description: Program that displays a GUI clock with function to pause and start current time.

import math 
import datetime
import tkinter as tk
from tkinter.constants import BOTTOM

class Display_Clock:
    def __init__(self):
        """Constructor for Display_Clock class"""
        self.window = tk.Tk() # Create a window
        self.window.title("Current Time") # Set a title
        
        #Clock Canvas
        self.clock_square = 200
        self.canvas = tk.Canvas(self.window, width = self.clock_square,height = self.clock_square)
        self.canvas.pack()
        #Radius of clock is 80% of half of the canvas
        self.clock_radius = 0.8
        x_0 = 100 * (1 - self.clock_radius)
        y_0 = 100 * (1 - self.clock_radius)
        x_1 = 200 - x_0
        y_1 = 200 - y_0
        self.canvas.create_oval(x_0, y_0 , x_1, y_1)
        
        self.canvas.create_text(100,x_0 +5, text="12", fill="black", font=("Arial"))
        self.canvas.create_text(100,x_1 -5, text="6", fill="black", font=("Arial"))
        self.canvas.create_text(x_0 +5,100, text="9", fill="black", font=("Arial"))
        self.canvas.create_text(x_1-5,100, text="3", fill="black", font=("Arial"))

        #Gets current time. Assigns each time component to seperate variables.
        self.current_time = datetime.datetime.now()
        self.hour = self.current_time.hour
        self.minute = self.current_time.minute
        self.second = self.current_time.second
        self.time = (f"{self.hour}:{self.minute}:{self.second}")
        self.canvas.create_text(100,190 ,text = self.time, fill=("black"), font=("Arial"), tag = "time")
        
        b_frame = tk.Frame(self.window)
        b_frame.pack(side = BOTTOM)

        #Button that switches between stop and start function
        self.button = tk.Button(b_frame, text = "Stop", width = 5, command = self.stop)
        self.button.grid(row = 1, column = 1)

        #Button that quits the program
        self.quit_button = tk.Button(b_frame, text = "Quit", width = 5, command = self.quit)
        self.quit_button.grid(row = 1, column = 2)
        
        self.seconds_update = 0
        self.timer = self.window.after(self.seconds_update, self.start)
        self.window.mainloop()

    def start(self):
        """Gets current time and updates current display on clock"""
        self.canvas.delete("hands")
        self.canvas.delete("time")
        self.current_time = datetime.datetime.now()
        self.hour = self.current_time.hour
        self.minute = self.current_time.minute
        self.second = self.current_time.second

        #Converts Military time to Standard time
        if self.hour > 12:
            self.hour -= 12
        elif self.hour == 0:
            self.hour = 12
        
        #Displays 0 in front of minute and second if digit is single
        if self.minute < 10:
            self.minute_str = "0" + str(self.minute)
        else:
            self.minute_str = str(self.minute)

        if self.second < 10:
            self.second_str = "0" + str(self.second)
        else:
            self.second_str = str(self.second)

        #Displays current time
        self.time = (f"{self.hour}:{self.minute_str}:{self.second_str}")
        self.canvas.create_text(100,190 ,text = self.time, fill=("black"), font=("Arial"), tag = "time")


        #Hour Hand
        #Hour hand is 50% length of clock radius
        self.hour_ratio = 0.5
        self.hour_length = 80 * self.hour_ratio
        #Converts current hour time to radian measurements to get new position of time
        if self.hour < 3:
            self.hour_angle = math.radians(((self.minute / 60 + self.second / 3600 + self.hour) + 9) * 30)
            x_hours = 100 + (math.cos(self.hour_angle) * self.hour_length)
            y_hours = 100 + (math.sin(self.hour_angle) * self.hour_length)
        else:
            self.hour_angle = math.radians(((self.minute / 60 + self.second / 3600 + self.hour) - 3) * 30)
            x_hours = 100 + (math.cos(self.hour_angle) * self.hour_length)
            y_hours = 100 + (math.sin(self.hour_angle) * self.hour_length)
        #Creates the hour hand
        self.canvas.create_line(100, 100, x_hours, y_hours , fill = 'green', tag = "hands")


        #Minute Hand
        #Minute hand is 65% length of clock radius
        self.minute_ratio = 0.65
        self.minute_length = 80 * self.minute_ratio
        #Converts current minute time to radian measurements to get new position of time
        if self.minute < 15:
            self.minute_angle = math.radians(((self.second / 60 + self.minute) + 45) * 6) 
            x_minutes = 100 + (math.cos(self.minute_angle) * self.minute_length)
            y_minutes = 100 + (math.sin(self.minute_angle) * self.minute_length)
        else:
            self.minute_angle = math.radians(((self.second / 60 + self.minute) - 15) * 6)
            x_minutes = 100 + (math.cos(self.minute_angle) * self.minute_length)
            y_minutes = 100 + (math.sin(self.minute_angle) * self.minute_length)
        self.canvas.create_line(100, 100, x_minutes, y_minutes , fill = 'blue', tag = "hands")
            

        #Second hand
        #Second hand is 80% length of clock radius
        self.second_ratio = 0.8
        self.second_length = 80 * self.second_ratio
        #Converts current second time to radian measurements to get new position of time
        if self.second < 15:
            self.second_angle = math.radians((self.second + 45) * 6)
            x_seconds = 100 + (math.cos(self.second_angle) * self.second_length)
            y_seconds = 100 + (math.sin(self.second_angle) * self.second_length)
        else:
            self.second_angle = math.radians((self.second - 15) * 6 )
            x_seconds = 100 + (math.cos(self.second_angle) * self.second_length)
            y_seconds = 100 + (math.sin(self.second_angle) * self.second_length)
        self.canvas.create_line(100, 100, x_seconds, y_seconds , fill = 'red', tag = "hands")

        #Start button becomes Stop button
        self.button["text"] = "Stop"
        self.button["command"] = self.stop

        #Gets current time for every second by using recursion
        self.seconds_update = 1000
        self.timer = self.window.after(self.seconds_update, self.start)
    
    def stop(self):
        """Stops the clock from updating time"""
        self.window.after_cancel(self.timer)
        #Stop button becomes Start button
        self.button["text"] = "Start"
        self.button["command"] = self.start
        

    def quit(self):
        """Ends Program"""
        self.window.destroy()
        
if __name__ == "__main__":
    Display_Clock()
