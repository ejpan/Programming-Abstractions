# File: statement_eval.py
# Author: Gabriel Seidl / Eric Pan
# Date: September 14, 2021
# Description: Program that reads and interprets a
#    file containing simple expression and assignment
#    statements.

import re  # For regular expressions

class BadStatement(Exception):
    pass

def interpret_statements(filename):

    """
    Function that reads statements from the file whose
    name is filename, and prints the result of each statement,
    formatted exactly as described in the psa1 problem statement.  
    interpret_statements must use the evaluate_expression function,
    which appears next in this file.
    """
    variables = {}
    linecount = 0
    f = open(filename)
    #Reads each line, removes comments, and ignores empty lines.
    for line in f:
        linecount += 1
        statement = line.split("#")[0].strip()
        #Try/catch block for bad statements and file errors.
        try:
            if len(statement) > 0:
                tokens = statement.split()
                #Checks if statement is an assignment or an expression.
                if len(tokens) >= 3 and tokens[1] == "=":
                    #Checks variable name using regular expression.
                    valid = re.fullmatch("[a-z_]\w*", tokens[0])
                    if not valid:
                        raise BadStatement
                    else:
                        #Creates new key and assigns the total to the key for assignments.
                        variables[tokens[0]] = evaluate_expression(tokens[2:], variables)
                        print(f"Line {linecount}: {tokens[0]} = {variables[tokens[0]]:.2f}")
                else:
                    val_of_line = evaluate_expression(tokens, variables)
                    print(f"Line {linecount}: {statement} = {val_of_line:.2f}")
            
        except BadStatement:
            print(f"Line {linecount}: Invalid statement")
        except FileNotFoundError:
            print("File not found. Please try again.")

def evaluate_expression(tokens, variables):
    """
    Function that evaluates an expression represented by tokens.
    tokens is a list of strings that are the tokens of the expression.  
    For example, if the expression is "salary + time - 150", then tokens would be
    ["salary", "+", "time", "-", "150"].  variables is a dictionary that maps 
    previously assigned variables to their floating point values.

    Returns the value that is assigned.

    If the expression is invalid, the BadStatemen exception is raised.
    """
    total = 0
    for i in range(len(tokens)):
        #Checks if token is in dictionary.
        in_dict = tokens[i] in variables
        #Checks operator for every odd index.
        if i % 2 == 1:
            if (tokens[i] == "-" or tokens[i] == "+") and i != len(tokens) - 1:
                continue
            else:
                raise BadStatement

        else:
            #Casts total of variable in dictionary as a float.
            if in_dict:
                number = float(variables[tokens[i]])
            #Casts number to float.
            elif is_number(tokens[i]):
                number = float(tokens[i])
            else:
                raise BadStatement
            #Adds first valid number to total.
            if i == 0 and (in_dict or is_number(tokens[i])):
                total += number
            elif tokens[i-1] == "+":
                total += number
            elif tokens[i-1] == "-":
                total -= number
            else:
                raise BadStatement

    return total

def is_number(num):
    """
    Function that floats a variable to check if a number is a valid number
    using try/catch block. Returns True if input can be casted as float.
    """
    try:
        float(num)
        return True
    except ValueError:
        return False
            



            
            
    

    
# You can add additional helper method(s) if you want.

if __name__ == "__main__":
    file_name = "statements.txt"  # you can create another file with statements
                                  # and change the name of this variable to that
                                  # filename.
    
    interpret_statements(file_name)
