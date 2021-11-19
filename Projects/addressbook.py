# File: addressbook.py
# Author: Eric Pan & Gabe Seidl
# Date: 09/23
# Description: Program that stores and displays addresses entered in by user.  Can also load 
#              and save addresses to a file.

import tkinter as tk
from tkinter.constants import BOTTOM
import re

class Address:
    """Class that creates objects containing address instance variables"""
    def __init__(self):
        """Instance Variables"""
        self.name = ""
        self.street = ""
        self.city = ""
        self.state = ""
        self.zip_code = ""


class AddressBook:
    def __init__(self):
        """ Constructor for AddressBook class """

        # Create window.
        self.window = tk.Tk()  
        self.window.title("AddressBook") 

        self.index = 0
        self.addresses = []
        #Frame for Address 
        frame = tk.Frame(self.window)
        frame.pack()
        frame.columnconfigure(2, weight = 3)

        #Label and Entry for Components
        self.name_label = tk.Label(frame, text = "Name")
        self.name_label.grid(row = 1, column = 1)
        self.name_var = tk.StringVar()
        self.name = tk.Entry(frame, width = 25, textvariable = self.name_var)
        self.name.grid(row = 1, column = 2, columnspan = 6, sticky = "EW", pady = 5, padx = 5)

        self.street_label = tk.Label(frame, text = "Street")
        self.street_label.grid(row = 2, column = 1)
        self.street_var = tk.StringVar()
        self.street = tk.Entry(frame, width = 25, textvariable = self.street_var)
        self.street.grid(row = 2, column = 2, columnspan = 6, sticky = "EW", pady = 5, padx = 5)

        self.city_label = tk.Label(frame, text = "City")
        self.city_label.grid(row = 3, column = 1)
        self.city_var = tk.StringVar()
        self.city = tk.Entry(frame, width = 15, textvariable = self.city_var)
        self.city.grid(row = 3, column = 2)

        self.state_label = tk.Label(frame, text = "STATE")
        self.state_label.grid(row = 3, column = 3)
        self.state_var = tk.StringVar()
        self.state = tk.Entry(frame, width = 5, textvariable = self.state_var)
        self.state.grid(row = 3, column = 4)

        self.zip_label = tk.Label(frame, text = "ZIP")
        self.zip_label.grid(row = 3, column = 5)
        self.zip_var = tk.StringVar()
        self.zip = tk.Entry(frame, width = 5, textvariable = self.zip_var)
        self.zip.grid(row = 3, column = 6)

        #Frame for Buttons
        b_frame = tk.Frame(self.window)
        b_frame.pack(pady = 3)
        
        #Buttons for functions of Address Book
        self.add_button = tk.Button(b_frame, text = "Add", width = 5, command = self.add)
        self.add_button.grid(row = 1, column = 1, sticky = "E")

        self.delete_button = tk.Button(b_frame, text = "Delete", width = 7, command = self.delete)
        self.delete_button.grid(row = 1, column = 2, sticky = "E")

        self.first_button = tk.Button(b_frame, text = "First", width = 6, command = self.first)
        self.first_button.grid(row = 1, column = 3, sticky = "E")

        self.next_button = tk.Button(b_frame, text = "Next", width = 6, command = self.next)
        self.next_button.grid(row = 1, column = 4, sticky = "E")

        self.previous_button = tk.Button(b_frame, text = "Previous", width = 7, command = self.previous)
        self.previous_button.grid(row = 1, column = 5, sticky = "E")

        self.last_button = tk.Button(b_frame, text = "Last", width = 5, command = self.last)
        self.last_button.grid(row = 1, column = 6, sticky = "E")

        #Frame for File Functions
        file_frame = tk.Frame(self.window)
        file_frame.pack(side = BOTTOM, padx = 5)
        #Labels, Functions, and Buttons for File Functions
        self.file_name = tk.Label(file_frame, text = "Filename")
        self.file_name.grid(row = 1, column = 1, sticky = "W")

        self.file_name_var = tk.StringVar()
        self.file_name = tk.Entry(file_frame, width = 10, textvariable = self.file_name_var)
        self.file_name.grid(row = 1, column = 2)

        self.load_file_button = tk.Button(file_frame, text = "Load File", width = 8, command = self.load)
        self.load_file_button.grid(row = 1, column = 3)

        self.save_button = tk.Button(file_frame, text = "Save to File", width = 10, command = self.save)
        self.save_button.grid(row = 1, column = 4)

        self.quit_button = tk.Button(file_frame, text = "Quit", width = 5, command = self.quit)
        self.quit_button.grid(row = 1, column = 5)

    def go(self):
        """ Start the event loop """
        self.window.mainloop()

    # You will add other methods.
    def add(self):
        """Creates address object from component entries and adds object to object list"""
        if not re.fullmatch("\s*", self.name_var.get()) and not re.fullmatch("\s*", self.street_var.get()) and not re.fullmatch("\s*", self.city_var.get()) and not re.fullmatch("\s*", self.state_var.get()) and not re.fullmatch("\s*", self.zip_var.get()):
            newAddy = Address()
            newAddy.name = self.name_var.get()
            newAddy.street = self.street_var.get()
            newAddy.city = self.city_var.get()
            newAddy.state = self.state_var.get()
            newAddy.zip_code = self.zip_var.get()
        if self.index == 0:
            self.addresses.append(newAddy)
        else:
            self.addresses.insert((self.index + 1), newAddy)


    def delete(self):
        """Removes address object from object list"""
        #Removes first object in object list and displays empty address
        if len(self.addresses) == 1:
            del self.addresses[0]
            self.name_var.set("")
            self.street_var.set("")
            self.city_var.set("")
            self.state_var.set("")
            self.zip_var.set("")
        #Removes last object in object list and displays previous address
        elif self.index == len(self.addresses) - 1:   
            del self.addresses[self.index]
            self.index -= 1
            self.name_var.set(self.addresses[self.index].name)
            self.street_var.set(self.addresses[self.index].street)
            self.city_var.set(self.addresses[self.index].city)
            self.state_var.set(self.addresses[self.index].state)
            self.zip_var.set(self.addresses[self.index].zip_code)
        #Removes address and displays next address
        else:
            del self.addresses[self.index]
            self.name_var.set(self.addresses[self.index].name)
            self.street_var.set(self.addresses[self.index].street)
            self.city_var.set(self.addresses[self.index].city)
            self.state_var.set(self.addresses[self.index].state)
            self.zip_var.set(self.addresses[self.index].zip_code)
        

    def first(self):
        """Displays first address in object list"""
        self.name_var.set(self.addresses[0].name)
        self.street_var.set(self.addresses[0].street)
        self.city_var.set(self.addresses[0].city)
        self.state_var.set(self.addresses[0].state)
        self.zip_var.set(self.addresses[0].zip_code)
        self.index = 0
    
    def next(self):
        """Displays next address in object list"""
        if self.index < len(self.addresses) - 1:
            self.index += 1
            self.name_var.set(self.addresses[self.index].name)
            self.street_var.set(self.addresses[self.index].street)
            self.city_var.set(self.addresses[self.index].city)
            self.state_var.set(self.addresses[self.index].state)
            self.zip_var.set(self.addresses[self.index].zip_code)

    def previous(self):
        """Displays previous address in object list"""
        if self.index > 0:
            self.index -= 1
            self.name_var.set(self.addresses[self.index].name)
            self.street_var.set(self.addresses[self.index].street)
            self.city_var.set(self.addresses[self.index].city)
            self.state_var.set(self.addresses[self.index].state)
            self.zip_var.set(self.addresses[self.index].zip_code)
            

    def last(self):
        """Displays last address in object list"""
        self.index = (len(self.addresses) - 1)
        self.name_var.set(self.addresses[self.index].name)
        self.street_var.set(self.addresses[self.index].street)
        self.city_var.set(self.addresses[self.index].city)
        self.state_var.set(self.addresses[self.index].state)
        self.zip_var.set(self.addresses[self.index].zip_code)
        

    def load(self):
        """Loads file entered by user"""
        #Checks for empty file
        try:
            #Checks for empty file field
            if len(self.file_name_var.get().strip()) > 0:
                self.filename = self.file_name_var.get()
                self.address_parts = []  #list for holding components of address from file
                self.ind = 1  #keeps track of what kind of address component
                self.newfile = open(self.filename, 'r')
                self.addresses.clear()
                #Runs through each line in file
                for line in self.newfile:
                    if len(line.split()) == 0:
                        pass
                    #If ind is 5, then address_parts list is full with each address component
                    #Creates object with components from list and appends new object to address list
                    elif self.ind == 5:
                        self.address_parts.append(line)
                        newAddy = Address()
                        newAddy.name = self.address_parts[0]
                        newAddy.street = self.address_parts[1]
                        newAddy.city = self.address_parts[2]
                        newAddy.state = self.address_parts[3]
                        newAddy.zip_code = self.address_parts[4]
                        self.addresses.append(newAddy)
                        self.ind = 1
                        self.address_parts.clear()
                    else:
                        self.address_parts.append(line)
                        self.ind += 1
                #displays first address
                self.first()
                self.newfile.close()
                self.file_name_var.set("")
        except IndexError:
            self.name_var.set("")
            self.street_var.set("")
            self.city_var.set("")
            self.state_var.set("")
            self.zip_var.set("")
            self.file_name_var.set("")


    def save(self):
        """Saves Address list to File entered by user"""
        self.filename = self.file_name_var.get()
        self.newfile = open(self.filename, "w")
        for i in range(0, len(self.addresses)):
            self.newfile.write(f"{self.addresses[i].name}\n")
            self.newfile.write(f"{self.addresses[i].street}\n")
            self.newfile.write(f"{self.addresses[i].city}\n")
            self.newfile.write(f"{self.addresses[i].state}\n")
            self.newfile.write(f"{self.addresses[i].zip_code}\n")
        self.newfile.close()
        self.file_name_var.set("")

    def quit(self):
        """Ends Program"""
        self.window.destroy()

def main():
    # Create the GUI program
    program = AddressBook()

    # Start the GUI event loop
    program.go()

if __name__ == "__main__":
    main()   
