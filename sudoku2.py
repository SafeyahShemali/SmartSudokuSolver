#!/usr/bin/env python
# coding:utf-8
import math
import operator
import random
import time
import statistics


"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import copy
import sys

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

  
"""
Done by Safeyah 
"""
def select_unassigned_variable(MRV_Domains):
    min_domain_length = 1000
    min_domain = None
    cellVariable = None

    for cellVar in MRV_Domains:
        if len(MRV_Domains[cellVar]) <= min_domain_length:
            cellVariable = cellVar
            min_domain_length = len(MRV_Domains[cellVar])
            min_domain = MRV_Domains[cellVar]

    del MRV_Domains[cellVariable]
    return cellVariable, min_domain

def backtracking_recursive(board):

    # base rule of recursive /  check if it  is complte
    if 0 not in board.values():
        return board

    # 1: get empty cells and their count
    emptyCells = getEmptyCells(board)

    # 2: (Inference) get the valid domain for each empty cell (check the consistency) without fprward checking
    MRV_Domains = checkConsistency(emptyCells, board)

    # 3 selecting the minimum remaining value
    # var = min(MRV_Domains , key= MRV_Domains.get)
    # order_domain_values = MRV_Domains[var]
    # del MRV_Domains[var]
    var, order_domain_values = select_unassigned_variable(MRV_Domains)

    for value in order_domain_values:
        # get a copy from the current MRV in case backtracking
        old_MRV_Domains = copy.deepcopy(MRV_Domains)

        # check the consisitency by raw, coloum, box
        valid = checkConsistencyWithForwardChecking(var,value,MRV_Domains)

        if valid:
            # add the assignment
            board[var] = value

            solved_board = backtracking_recursive(board)

            if solved_board != False:
                return solved_board

            # when it is false, I should retun things back, like the value that i delted from the MRV_domain
            board[var] = 0
            MRV_Domains = old_MRV_Domains

    return False

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    return backtracking_recursive(board)

def getEmptyCells(board):
    emptyCells = {}

    for i in board:
        if board[i] == 0:
            emptyCells[i] = 0

    return emptyCells

def checkConsistency(emptyCells, board):
    # the disctionary of the remaining value of each empty cell
    MRV_Domain = {}

    # the whole domain
    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for cellVar in emptyCells:
        # get the dimention of the cell
        cellRow = cellVar[0]
        cellCol = cellVar[1]

        '''CHECK THE ROW'''
        # track current values in a row
        current_row_values = []

        for c in COL:
            # get the numbers exact in the rows
            cellCheckKey = cellRow + c

            # not empty and it is not the curren empty cell we are validate
            if board[cellCheckKey] != 0:
                current_row_values.append(board[cellCheckKey])

        # get the valid values for the selected cell
        valid_row_values = list(set(domain).difference(current_row_values))

        '''CHECK THE COL'''
        # track current values in a row
        current_col_values = []

        for r in ROW:
            # get the numbers exact in the rows
            cellCheckKey = r + cellCol

            # not empty and it is not the curren empty cell we are validate
            if board[cellCheckKey] != 0:
                current_col_values.append(board[cellCheckKey])

        # get the valid values for the selected cell
        valid_col_values = list(set(domain).difference(current_col_values))

        '''CHECK THE SubGrid 'BOX' '''
        # track current values in a row
        current_subgrid_values = []

        for r in [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]:
            for c in [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]:
                if cellRow in r and cellCol in c:
                    # I will take the sub-row (r) and sub-raw (c)
                    for i in r:
                        for j in c:
                            if board[i + j] != 0:
                                current_subgrid_values.append(board[i + j])
                    break

        # get the  values for the selected cell
        valid_subgrid_values = list(set(domain).difference(current_subgrid_values))

        # the selected empty cell domain
        cell_valid_domain = list(set(valid_row_values) & set(valid_col_values) & set(valid_subgrid_values))

        # add this to the MRV_Domain which we will use in the backtracking
        MRV_Domain[cellVar] = cell_valid_domain

    return MRV_Domain

def checkConsistencyWithForwardChecking(cellVar, cellValue, MRV_Domains):
    # get the dimention of the cell
    cellRow = cellVar[0]
    cellCol = cellVar[1]

    '''Check the ROW'''
    for c in COL:
        # get the numbers exact in the rows
        cellCheckKey = cellRow + c

        # get the domain of adjacent cells
        # just check the empty cells
        if cellCheckKey in MRV_Domains.keys():
             # check if the selected value violate the acr consistency
             # if the value in the cellchek domain
             if cellValue in MRV_Domains[cellCheckKey]:
             #check if the selected value is the only calue if other cell check
             #ex. cellVar (I6) , the cellVal = 4 , MRV_Domains[cellCheckKey] = 4, then we can not select 4 for I6
                if len(MRV_Domains[cellCheckKey]) == 1:
                    return False
                else:
                    # we will get out the value from cellCheckKey
                    MRV_Domains[cellCheckKey].remove(cellValue)

    '''Check the COL'''
    for r in ROW:
        # get the numbers exact in the rows
        cellCheckKey = r + cellCol

        # get the domain of adjacent cells
        # just check the empty cells
        if cellCheckKey in MRV_Domains.keys():
             # check if the selected value violate the acr consistency
             # if the value in the cellchek domain
             if cellValue in MRV_Domains[cellCheckKey]:
             #check if the selected value is the only calue if other cell check
             #ex. cellVar (I6) , the cellVal = 4 , MRV_Domains[cellCheckKey] = 4, then we can not select 4 for I6
                if len(MRV_Domains[cellCheckKey]) == 1:
                    return False
                else:
                    # we will get out the value from cellCheckKey
                    MRV_Domains[cellCheckKey].remove(cellValue)

    '''CHECK THE SubGrid 'BOX' '''
    for r in [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]:
        for c in [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]:
            if cellRow in r and cellCol in c:
                # I will take the sub-row (r) and sub-raw (c)
                for i in r:
                    for j in c:
                        # get the domain of adjacent cells
                        # just check the empty cells
                        if cellCheckKey in MRV_Domains.keys():
                            # check if the selected value violate the acr consistency
                            # if the value in the cellchek domain
                            if cellValue in MRV_Domains[cellCheckKey]:
                                # check if the selected value is the only calue if other cell check
                                # ex. cellVar (I6) , the cellVal = 4 , MRV_Domains[cellCheckKey] = 4, then we can not select 4 for I6
                                if len(MRV_Domains[cellCheckKey]) == 1:
                                    return False
                                else:
                                    # we will get out the value from cellCheckKey
                                    MRV_Domains[cellCheckKey].remove(cellValue)
                break
    return True


"""
End: Done by Safeyah 
"""

if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        # 3 search and backtracking
        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        #Timimg stuff
        Min = math.inf
        Max = -math.inf
        Mean = 0
        Standard_deviation = 0
        timings = []

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            # record start time
            start = time.time()

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            # record end time
            end = time.time()
            timings.append((end-start) * 10**3)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        """
        Added by Safeyah for Evaultion 
        """
        Min = min(timings)
        Max = max(timings)
        Mean = statistics.mean(timings)
        Standard_deviation = statistics.pstdev(timings)
        # and end time in milli. secs
        print('Min:', Min)
        print('Max:', Max)
        print('Mean:', Mean)
        print('Standard_deviation:', Standard_deviation)
        
        print("Finishing all boards in file.")