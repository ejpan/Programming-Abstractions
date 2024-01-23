"""
Module: Snake7

Authors: Long Pham and Eric Pan

Emails: longpham@sandiego.edu and epan@sandiego.edu

Date: November 30, 2021

Description: A Python implementation of greedy snake using Tkinter and implemented
using the model-view-controller design pattern.

Iteration 7:
Final iteration of the snake program.  This last iteration implements the event
handler functions in the controller (the Snake class) that were created
as stub functions in iteration 5.
"""
import random
import tkinter as tk
from enum import IntEnum
import time
import unittest

class Snake:
    """ This is the controller """
    def __init__(self):
        """ Initializes the snake game """
        self.NUM_ROWS = 30
        self.NUM_COLS = 30
        self.DEFAULT_STEP_TIME_MILLIS = 1000

        self.model = SnakeModel(self.NUM_ROWS, self.NUM_COLS)
        self.view = SnakeView(self.NUM_ROWS, self.NUM_COLS)
        #Checks if start button is to start program or continue game.
        self.start_click = "start"
        #Intializes direction, game status, and wraparound
        self.direction = 0
        self.is_running = None
        self.wraparound = False
        self.model.wraparound = False

        # Intializes default time and time when game is paused
        self.DEFAULT_TIME = 0.00
        self.paused_time = 0.00
        self.time = 0.00

        # Step time is 1 second
        self.step_time_millis = self.DEFAULT_STEP_TIME_MILLIS
        self.pts_sec = 0
        self.time_state = None

        # Set the handlers for the buttons
        self.view.set_start_handler(self.start_handler)
        self.view.set_pause_handler(self.pause_handler)
        self.view.set_step_speed_handler(self.step_speed_handler)
        self.view.set_reset_handler(self.reset_handler)
        self.view.set_quit_handler(self.quit_handler)
        self.view.set_wraparound_handler(self.wraparound_handler)
        self.view.set_left_handler(self.left_handler)
        self.view.set_right_handler(self.right_handler)
        self.view.set_up_handler(self.up_handler)
        self.view.set_down_handler(self.down_handler)

        # Initializes the snake and food on the grid
        self.start_handler()

        self.view.window.mainloop()

    def start_handler(self):
        """ Starts snake game """
        #Checks to see if game needs to start or continue.
        if self.start_click == "already run":
            return
        if self.start_click == "start":
            self.start_click = "run"
        if self.start_click == "run":
            for row in range(self.NUM_ROWS):
                for col in range(self.NUM_COLS):
                    if [row,col] == self.model.snake[0]:
                        self.view.make_snakehead(row,col)
                    if self.model.is_food(row,col):
                        self.view.make_food(row, col)
            self.is_running = True
            self.model.change_dir = True
            if self.time_state == "pause":
                self.time_state = "run"
            
            self.start_click = "already run"
            self.start_time = time.time()
            self.time_diff = self.start_time - self.paused_time
            self.DEFAULT_TIME = self.DEFAULT_TIME + self.time_diff
            self.view.schedule_next_step(self.step_time_millis, self.continue_simulation)
    
    def pause_handler(self):
        if self.direction == 0:
            return
        elif self.is_running:
            self.view.cancel_next_step()
            self.is_running = False
            self.model.change_dir = False
            self.time_state = "pause"
            self.start_click = "start"
            self.paused_time = time.time()

    def step_speed_handler(self, value):
        self.step_time_millis = self.DEFAULT_STEP_TIME_MILLIS // int(value)

    def quit_handler(self):
        self.view.window.destroy()

    def reset_handler(self):
        if self.is_running is None:
            return
        self.pts_sec = 0
        self.model.reset()
        self.view.reset()
        self.view.game_over_label["text"] = ""
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS):
                if [row,col] == self.model.snake[0]:
                    self.view.make_snakehead(row,col)
                if self.model.is_food(row,col):
                    self.view.make_food(row, col)
        self.is_running = True
        self.model.change_dir = True
        self.time_state = None
        self.start_click = "already run"
        self.direction = 0
        self.view.schedule_next_step(self.step_time_millis, self.continue_simulation)

    def wraparound_handler(self):
        if not self.wraparound:
            self.wraparound = True
            self.model.wraparound = True
        else:
            self.wraparound = False
            self.model.wraparound = False

    def up_handler(self, event):
        """ Snake turns up """
        #Checks if game is at start or paused.
        if self.start_click == "run" or self.start_click == "already run":
            #Starts timer when no direction indicating game is starting.
            if self.direction == 0:
                self.time_state = "run"
                self.DEFAULT_TIME = time.time()
            self.direction = "UP"
            self.model.make_direction(self.direction)

    def right_handler(self, event):
        """ Snake turns right """
        #Checks if game is at start or paused.
        if self.start_click == "run" or self.start_click == "already run":
            #Starts timer when no direction indicating game is starting.
            if self.direction == 0:
                self.time_state = "run"
                self.DEFAULT_TIME = time.time()
            self.direction = "RIGHT"
            self.model.make_direction(self.direction)

    def down_handler(self, event):
        """ Snake turns down """
        #Checks if game is at start or paused.
        if self.start_click == "run" or self.start_click == "already run":
            #Starts timer when no direction indicating game is starting.
            if self.direction == 0:
                self.time_state = "run"
                self.DEFAULT_TIME = time.time()
            self.direction = "DOWN"
            self.model.make_direction(self.direction)

    def left_handler(self, event):
        """ Snake turns left """
        #Checks if game is at start or paused.
        if self.start_click == "run" or self.start_click == "already run":
            #Starts timer when no direction indicating game is starting.
            if self.direction == 0:
                self.time_state = "run"
                self.DEFAULT_TIME = time.time()
            self.direction = "LEFT"
            self.model.make_direction(self.direction)

    def continue_simulation(self):
        """ Checks if game is running or at game over stage """
        if not self.model.gameover:
            self.one_step()
            self.view.schedule_next_step(self.step_time_millis, self.continue_simulation)

    def continue_timer(self):
        """ Checks if game is running or at game over stage for timer """
        if not self.model.gameover:
            self.one_sec()
            self.view.schedule_next_sec(10, self.continue_timer)

    def one_step(self):
        """ One step of the game """
        self.model.one_step()
        #Stops game if game is over
        if self.model.gameover == True:
            self.game_over()
            return
        #Creates the snake head, snake, and food in grid.
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS):
                if self.model.is_snake(row, col):
                    if [row, col] == self.model.snake[0]:
                        self.view.make_snakehead(row,col)
                    else:
                        self.view.make_snake(row, col)
                elif self.model.is_food(row, col):
                    self.view.make_food(row, col)
                else:
                    self.view.make_empty(row, col)
        #Timer is on if game is running
        if self.time_state == "run":
            self.one_sec()

    def one_sec(self):
        """ Keeps track of time in game """
        self.time += 0.01
        #Current time subtracted by time when game starts.
        self.time = time.time() - self.DEFAULT_TIME
        #Update labels for points, time, and average points per second.
        self.view.points_num["text"] = str(self.model.pts)
        self.view.time_num["text"] = f'{self.time:.2f}'
        self.pts_sec = self.model.pts / self.time
        self.view.pts_sec_num["text"] = f'{self.pts_sec:.2f}'
    
    def game_over(self):
        """ Stops game and displays Game Over label """
        self.view.game_over_label["text"] = "Game over"
        self.pause_handler

class SnakeView:
    def __init__(self, num_rows, num_cols):
        """ Initialize view of the game """
        self.CELL_SIZE = 20
        self.CONTROL_FRAME_HEIGHT = 100
        self.SCORE_FRAME_WIDTH = 200

        self.num_rows = num_rows
        self.num_cols = num_cols

        self.window = tk.Tk()
        self.window.title("Greedy Snake")

        # Create frame for grid of cells, and put cells in the frame
        self.grid_frame = tk.Frame(self.window, height = num_rows * self.CELL_SIZE,
                                width = num_cols * self.CELL_SIZE)
        self.grid_frame.grid(row = 1, column = 1) # use grid layout manager
        self.cells = self.add_cells()

        # Create frame for controls
        self.control_frame = tk.Frame(self.window, width = num_cols * self.CELL_SIZE + self.SCORE_FRAME_WIDTH, 
                                height = self.CONTROL_FRAME_HEIGHT)
        self.control_frame.grid(row = 2, column = 1, columnspan= 2) # use grid layout manager
        self.control_frame.grid_propagate(False)
        (self.start_button, self.pause_button, 
         self.step_speed_slider, self.reset_button, 
         self.quit_button, self.wraparound_button) = self.add_control()

        #Create frame for scoreboard
        self.score_frame = tk.Frame(self.window, width =self.SCORE_FRAME_WIDTH, 
                                height = num_rows * self.CELL_SIZE, borderwidth = 1, relief = "solid")  
        self.score_frame.grid(row = 1, column = 2)
        self.score_frame.grid_propagate(False)
        (self.score_label, self.points_frame, self.time_frame,
        self.pts_sec_frame, self.game_over_label) = self.add_score()

    def add_cells(self):
        """ Add cells to the grid frame """
        cells = []
        for r in range(self.num_rows):
            row = []
            for c in range(self.num_cols):
                self.frame = tk.Frame(self.grid_frame, width = self.CELL_SIZE, 
                           height = self.CELL_SIZE, borderwidth = 1, 
                           relief = "solid")
                self.frame.grid(row = r, column = c) # use grid layout manager
                row.append(self.frame)
            cells.append(row)
        return cells

    def add_control(self):
        """ 
        Create control buttons and slider, and add them to the control frame 
        """
        self.start_button = tk.Button(self.control_frame, text="Start")
        self.start_button.grid(row=1, column=1, padx = 25)
        self.pause_button = tk.Button(self.control_frame, text="Pause")
        self.pause_button.grid(row=1, column=2, padx = 25)
        self.step_speed_slider = tk.Scale(self.control_frame, from_=1, to=10, 
                    label="Step Speed", showvalue=0, orient=tk.HORIZONTAL)
        self.step_speed_slider.grid(row=1, column=3, padx = 25)
        self.reset_button = tk.Button(self.control_frame, text="Reset")
        self.reset_button.grid(row=1, column=4, padx = 25)
        self.quit_button = tk.Button(self.control_frame, text="Quit")
        self.quit_button.grid(row=1, column=5, padx = 25)
        self.wraparound_button = tk.Checkbutton(self.control_frame, text = "Wraparound")
        self.wraparound_button.grid(row = 1, column = 6, padx = 25)
        # Vertically center the controls in the control frame
        self.control_frame.grid_rowconfigure(1, weight = 1) 

        # Horizontally center the controls in the control frame
        self.control_frame.grid_columnconfigure(0, weight = 1) 
        self.control_frame.grid_columnconfigure(7, weight = 1) 
                                                            
        return (self.start_button, self.pause_button, self.step_speed_slider, 
                self.reset_button, self.quit_button, self.wraparound_button)

    def add_score(self):
        """ 
        Create score counter label, timer label, average score per second label,
        game over label, and adds them to the score frame 
        """
        self.score_label = tk.Label(self.score_frame, text = "Score")
        self.score_label.grid(row = 1, column = 1)
        #Points counter label
        self.points_frame = tk.Frame(self.score_frame, borderwidth = 1, relief = "solid")
        self.points_frame.grid(row = 2, column = 1, pady = 25)
        self.points_label = tk.Label(self.points_frame, text = "Points:")
        self.points_label.grid(row = 1, column = 1)
        self.points_num = tk.Label(self.points_frame, text = "0")
        self.points_num.grid(row = 1, column = 2)
        #timer label
        self.time_frame = tk.Frame(self.score_frame, borderwidth = 1, relief = "solid")
        self.time_frame.grid(row = 3, column = 1, pady = 25)
        self.time_label = tk.Label(self.time_frame, text = "Time:")
        self.time_label.grid(row = 1, column =  1)
        self.time_num = tk.Label(self.time_frame, text = "0.00")
        self.time_num.grid(row = 1, column = 2)
        #Points per second label
        self.pts_sec_frame = tk.Frame(self.score_frame, borderwidth = 1, relief = "solid")
        self.pts_sec_frame.grid(row = 4, column = 1, pady = 25)
        self.pts_sec_label = tk.Label(self.pts_sec_frame, text = "Points per sec:")
        self.pts_sec_label.grid(row = 1, column = 1)
        self.pts_sec_num = tk.Label(self.pts_sec_frame, text = "0.00")
        self.pts_sec_num.grid(row = 1, column = 2)
        #Game over label
        self.game_over_label = tk.Label(self.score_frame, text = None)
        self.game_over_label.grid(row = 5, column = 1, pady = 25)

        self.score_frame.grid_columnconfigure(1, weight = 1)

        return(self.score_label, self.points_frame, self.time_frame, 
                self.pts_sec_frame, self.game_over_label)

    def set_start_handler(self, handler):
        """ Assigns start button to start handler """
        self.start_button.configure(command = handler)

    def set_pause_handler(self, handler):
        """ Assigns pause button to pause handler """
        self.pause_button.configure(command = handler)

    def set_step_speed_handler(self, handler):
        """ Assigns step speed button to step speed handler """
        self.step_speed_slider.configure(command = handler)

    def set_reset_handler(self, handler):
        """ Assigns reset button to start handler """
        self.reset_button.configure(command = handler)

    def set_quit_handler(self, handler):
        """ Assigns start button to start handler """
        self.quit_button.configure(command = handler)

    def set_wraparound_handler(self, handler):
        """ Assigns wraparound button to wraparound handler """
        self.wraparound_button.configure(command = handler)

    def set_left_handler(self, handler):
        """ Assigns left arrow key button to left arrow key handler """
        self.window.bind('<Left>', handler)

    def set_right_handler(self, handler):
        """ Assigns right arrow key button to right arrow key handler """
        self.window.bind('<Right>', handler)

    def set_up_handler(self, handler):
        """ Assigns up arrow key button to up arrow key handler """
        self.window.bind('<Up>', handler)

    def set_down_handler(self, handler):
        """ Assigns down arrow key button to down arrow key handler """
        self.window.bind('<Down>', handler)
    
    def make_snakehead(self, row, column):
        """ Fills in snake head cell in grid black """
        self.cells[row][column]['bg'] = 'black'

    def make_snake(self, row, column):
        """ Fills in snake body cell in grid blue """
        self.cells[row][column]['bg'] = 'blue'
    
    def make_empty(self, row, column):
        """ Fills in empty cell in grid white """
        self.cells[row][column]['bg'] = 'white'

    def make_food(self, row, column):
        """ Fills in food cell in grid red """
        self.cells[row][column]['bg'] = 'red'
    
    def reset(self):
        """ Resets the game to default """
        #Every cell becomes empty
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.make_empty(r, c)
        #Stops steps in game
        #Assigns values to default
        self.cancel_next_step()
        self.game_over_label["text"] = ""
        self.points_num["text"] = "0"
        self.time_num["text"] = "0.00"
        self.pts_sec_num["text"] = "0.00"
    
    def schedule_next_step(self, step_time_millis, step_handler):
        """ schedule next step of the simulation """
        self.start_timer_object = self.grid_frame.after(step_time_millis, step_handler)
    
    def cancel_next_step(self):
        """ cancel the scheduled next step of simulation """
        self.grid_frame.after_cancel(self.start_timer_object)

class SnakeModel:
    def __init__(self, num_rows, num_cols):
        """ initialize the model of the game """
        self.num_rows = num_rows
        self.num_cols = num_cols
        #Initializes state for cells in grid
        self.state = [[CellState.EMPTY for c in range(self.num_cols)] 
                        for r in range(self.num_rows)]
        #Creates initial snake and food
        self.snake = []
        snake_head = self.make_snake_head()
        self.snake.append(snake_head)
        self.food = self.make_food()

        self.pts = 0
        self.direction = None
        self.change_dir = True
        self.wraparound = False
        self.gameover = False
    
    def make_direction(self, direction):
        """ Checks to see direction is valid """
        if self.direction == "UP" and direction == "DOWN" and self.change_dir:
            return
        elif self.direction == "RIGHT" and direction == "LEFT" and self.change_dir:
            return
        elif self.direction == "DOWN" and direction == "UP" and self.change_dir:
            return
        elif self.direction == "LEFT" and direction == "RIGHT" and self.change_dir:
            return
        elif self.change_dir:
            self.direction = direction

    def make_snake_head(self):
        """ Creates snake head """
        row = random.randrange(0, self.num_cols)
        col = random.randrange(0, self.num_rows)
        self.state[row][col] = CellState.SNAKE
        return [row,col]

    def make_snake(self, row, col):
        """ Makes the cell in row, col alive  """
        self.state[row][col] = CellState.SNAKE
        return [row, col]
    
    def make_empty(self, row, col):
        """ Makes the cell in row, col empty """
        self.state[row][col] = CellState.EMPTY

    def make_food(self):
        """ Creates random food cell """
        row = random.randrange(0, self.num_cols)
        col = random.randrange(0, self.num_rows)
        #Creates food on a cell that isn't part of the snake
        while [row, col] in self.snake:
            row = random.randrange(0, self.num_cols)
            col = random.randrange(0, self.num_rows)
        self.state[row][col] = CellState.FOOD
        return [row,col]
    
    def is_snake(self, row, col):
        """ Checks if cell is part of the snake """
        return self.state[row][col] == CellState.SNAKE

    def is_food(self, row, col):
        """ Checks if cell is food """
        return self.state[row][col] == CellState.FOOD

    def reset(self):
        """ Resets grid to default """
        #Resets grid to all empty
        self.state = [[CellState.EMPTY for c in range(self.num_cols)] 
                        for r in range(self.num_rows)]
        #Creates initial snake head and food when game resets
        self.snake = []
        snake_head = self.make_snake_head()
        self.snake.append(snake_head)
        self.food = self.make_food()
        self.pts = 0
        #Defaults direction, gameover stage, and empty tail
        self.direction = None
        self.change_dir = True
        self.gameover = False
        self.empty_tail = None

    def one_step(self):
        """ One step of the game """
        #One Step for if wraparound feature is off
        if self.wraparound == False:
            #Moves snake body by adding temporary variable
            #to store prev square location.
            for s in range(0, len(self.snake) - 1):
                #Last coordinate of snake will become empty for each step.
                if s == 0:
                    #Assigns last coordinate to empty tail.
                    self.empty_tail = self.snake[len(self.snake) - 1]
                #Moves snake and assigns snake to grid.
                self.snake[len(self.snake) - 1 - s] = list(self.snake[len(self.snake) - 2 - s])
                self.state[self.snake[len(self.snake) - 1 - s][0]][self.snake[len(self.snake) - 1 - s][1]] = CellState.SNAKE
            #Empty tail becomes empty
            if len(self.snake) > 1:
                self.state[self.empty_tail[0]][self.empty_tail[1]] = CellState.EMPTY
            else:
                self.state[self.snake[0][0]][self.snake[0][1]] = CellState.EMPTY
            #Makes new snake head in the direction of user's choice.
            if self.direction == "UP":
                self.snake[0][0] = self.snake[0][0] - 1
            elif self.direction == "RIGHT":
                self.snake[0][1] = self.snake[0][1] + 1
            elif self.direction == "DOWN":
                self.snake[0][0] = self.snake[0][0] + 1
            elif self.direction == "LEFT":
                self.snake[0][1] = self.snake[0][1] - 1
            #Checks snake is within boundary
            if self.snake[0][0] < 0 or self.snake[0][0] > (self.num_rows - 1) or self.snake[0][1] < 0 or self.snake[0][1] > (self.num_cols - 1):
                self.gameover = True
                return
            #Checks if snake head collides with body
            else:
                if len(self.snake) > 1:
                    for body in self.snake[1:]:
                        if self.snake[0] == body:
                            self.gameover = True
                            return
            self.state[self.snake[0][0]][self.snake[0][1]] = CellState.SNAKE
        #One Step for if wraparound feature is on
        elif self.wraparound == True:
            self.one_step_wraparound()
        #Checks if snake eats food
        self.check_food()
    
    def one_step_wraparound(self):
        """ One step of the game if wraparound feature is on"""
        for s in range(0, len(self.snake) - 1):
            if s == 0:
                self.empty_tail = self.snake[len(self.snake) - 1]
            self.snake[len(self.snake) - 1 - s] = list(self.snake[len(self.snake) - 2 - s])
            self.state[self.snake[len(self.snake) - 1 - s][0]][self.snake[len(self.snake) - 1 - s][1]] = CellState.SNAKE
        if len(self.snake) > 1:
            self.state[self.empty_tail[0]][self.empty_tail[1]] = CellState.EMPTY
        else:
            self.state[self.snake[0][0]][self.snake[0][1]] = CellState.EMPTY
        #Snake spawns across the grid when crossing boundary
        if self.direction == "UP":
            self.snake[0][0] = self.snake[0][0] - 1
            if self.snake[0][0] < 0:
                self.snake[0][0] += (self.num_rows)
        elif self.direction == "RIGHT":
            self.snake[0][1] = self.snake[0][1] + 1
            if self.snake[0][1] >= self.num_cols:
                self.snake[0][1] -= (self.num_cols)
        elif self.direction == "DOWN":
            self.snake[0][0] = self.snake[0][0] + 1
            if self.snake[0][0] >= self.num_rows:
                self.snake[0][0] -= (self.num_rows)
        elif self.direction == "LEFT":
            self.snake[0][1] = self.snake[0][1] - 1
            if self.snake[0][1] < 0:
                self.snake[0][1] += (self.num_rows)
        #Checks if snake head collides with body
        if len(self.snake) > 1:
            for body in self.snake[1:]:
                if self.snake[0] == body:
                    self.gameover = True
                    return
        self.state[self.snake[0][0]][self.snake[0][1]] = CellState.SNAKE
        #Checks if snake eats food
        self.check_food()

    def check_food(self):
        """ Checks if snake eats apple"""
        if self.snake[0] == self.food:
            #Adds body depending on direction when length of snake is 1
            if len(self.snake) == 1:
                if self.direction == "UP":
                    self.snake.append(self.make_snake(self.snake[0][0] + 1, self.snake[0][1]))
                elif self.direction == "RIGHT":
                    self.snake.append(self.make_snake(self.snake[0][0], self.snake[0][1] - 1))
                elif self.direction == "DOWN":
                    self.snake.append(self.make_snake(self.snake[0][0] - 1, self.snake[0][1]))
                elif self.direction == "LEFT":
                    self.snake.append(self.make_snake(self.snake[0][0], self.snake[0][1] + 1))
                self.pts += 1
            #Adds snake body to the last previous coordinate of snake when apple is eaten.
            else:
                self.snake.append(self.make_snake(self.empty_tail[0], self.empty_tail[1]))
                self.pts += 1
            #Makes new food
            self.food = self.make_food()
            
        
class CellState(IntEnum):
    """ 
    Use IntEnum so that the test code below can
    set cell states using 0's and 1's
    """
    EMPTY = 0
    SNAKE = 1
    FOOD = 2

if __name__ == "__main__":
   snake_game = Snake()
