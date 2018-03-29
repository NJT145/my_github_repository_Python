##Assignment2

### This code is built with Python 2.7 programming language.
#######################################################################################################################
import copy
import Queue
import time
#######################################################################################################################
EMPTY = 0
BLUE = 1
GREEN = 2
RED = 4
#######################################################################################################################

def get_successors(initial_state):
    """Successor function for the block world puzzle

       Parameters
       ----------
       initial_state: 2-dimensional array representing initial block world config

       row_1: row of first empty block.
       col_1: column of first empty block.
       row_2: row of second empty block.
       col_2: column of second empty block.

       Returns
       -------
       expanded_states: type - list of 2D arrrays
    """
    expanded_states = []
    #------------------------------------------------------------------------------------------------------------------
    [[row_1, col_1], [row_2, col_2]] = findEmptyPlaces(initial_state)
    #------------------------------------------------------------------------------------------------------------------
    # when moving a blue block to empty (blank) places ...
    ## with first empty (blank) block at row_1 and col_1
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", BLUE):
        expanded_states.append(move(1, "up", initial_state, row_1, col_1))
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", BLUE):
        expanded_states.append(move(1, "down", initial_state, row_1, col_1))
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", BLUE):
        expanded_states.append(move(1, "left", initial_state, row_1, col_1))
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", BLUE):
        expanded_states.append(move(1, "right", initial_state, row_1, col_1))
    ## with second empty (blank) block at row_2 and col_2
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "up", BLUE):
        expanded_states.append(move(1, "up", initial_state,row_2,col_2))
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "down", BLUE):
        expanded_states.append(move(1, "down", initial_state, row_2, col_2))
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", BLUE):
        expanded_states.append(move(1, "left", initial_state, row_2, col_2))
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", BLUE):
        expanded_states.append(move(1, "right", initial_state, row_2, col_2))
    # ------------------------------------------------------------------------------------------------------------------
    # when moving a green block to empty (blank) places ...
    ## with vertical green block
    ### with only first empty (blank) block at row_1 and col_1
    ##### moving empty block at row_1 and col_1 to upwards
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 2, col_1, "up", GREEN)==False:
        expanded_states.append(move(2, "up", initial_state, row_1, col_1))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "right", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 2, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 2, col_1, "right", GREEN) == False:
        expanded_states.append(move(2, "up", initial_state, row_1, col_1))
    ##### moving empty block at row_1 and col_1 to downwards
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 2, col_1, "down", GREEN)==False:
        expanded_states.append(move(2, "down", initial_state, row_1, col_1))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "right", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 2, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 2, col_1, "right", GREEN) == False:
        expanded_states.append(move(2, "down", initial_state, row_1, col_1))
    ### with only second empty (blank) block at row_2 and col_2
    ##### moving empty block at row_2 and col_2 to upwards
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "down", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 - 1, col_2, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2 - 2, col_2, "up", GREEN)==False:
        expanded_states.append(move(2, "up", initial_state, row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_2, col_2, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "down", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 - 1, col_2, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 - 1, col_2, "right", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 - 1, col_2, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2 - 2, col_2, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 - 2, col_2, "right", GREEN) == False:
        expanded_states.append(move(2, "up", initial_state, row_2, col_2))
    ##### moving empty block at row_2 and col_2 to downwards
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "up", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 1, col_2, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 2, col_2, "down", GREEN)==False:
        expanded_states.append(move(2, "down", initial_state, row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_2, col_2, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "up", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 1, col_2, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 1, col_2, "right", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 1, col_2, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 2, col_2, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 2, col_2, "right", GREEN) == False:
        expanded_states.append(move(2, "down", initial_state, row_2, col_2))
    ### with two empty blocks together
    ##### moving empty blocks to upwards
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 2, col_1, "up", GREEN)==False:
        expanded_states.append(move(2, "up", move(2, "up", initial_state, row_1, col_1), row_2, col_2))
    ##### moving empty blocks to downwards
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 1, col_2, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2 + 2, col_2, "down", GREEN)==False:
        expanded_states.append(move(2, "down", move(2, "down", initial_state, row_1, col_1), row_2, col_2))
    ##### moving empty blocks to left
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "left", GREEN) == False:
        expanded_states.append(move(1, "left", move(1, "left", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "down", GREEN) == False:
        expanded_states.append(move(1, "left", move(1, "left", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "down", GREEN) == False:
        expanded_states.append(move(1, "left", move(1, "left", initial_state, row_1, col_1), row_2, col_2))
    ##### moving empty blocks to right
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "right", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "right", GREEN) == False:
        expanded_states.append(move(1, "right", move(1, "right", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "right", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "right", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "down", GREEN) == False:
        expanded_states.append(move(1, "right", move(1, "right", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "down", GREEN) == False:
        expanded_states.append(move(1, "right", move(1, "right", initial_state, row_1, col_1), row_2, col_2))
    ## with horizontal green block
    ### with only first empty (blank) block at row_1 and col_1
    ##### moving empty block at row_1 and col_1 to left
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 2, "left", GREEN) == False:
        expanded_states.append(move(2, "left", initial_state, row_1, col_1))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "down", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 2, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 2, "down", GREEN) == False:
        expanded_states.append(move(2, "left", initial_state, row_1, col_1))
    ##### moving empty block at row_1 and col_1 to right
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 2, "right", GREEN) == False:
        expanded_states.append(move(2, "right", initial_state, row_1, col_1))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "down", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 2, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 + 2, "down", GREEN) == False:
        expanded_states.append(move(2, "right", initial_state, row_1, col_1))
    ### with only second empty (blank) block at row_2 and col_2
    ##### moving empty block at row_2 and col_2 to left
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 2, "left", GREEN) == False:
        expanded_states.append(move(2, "left", initial_state, row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "down", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 2, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 - 2, "down", GREEN) == False:
        expanded_states.append(move(2, "left", initial_state, row_2, col_2))
    ##### moving empty block at row_2 and col_2 to right
    if check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 2, "right", GREEN) == False:
        expanded_states.append(move(2, "right", initial_state, row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", EMPTY) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "down", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 2, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 2, "down", GREEN) == False:
        expanded_states.append(move(2, "right", initial_state, row_2, col_2))
    ### with two empty blocks together
    ##### moving empty blocks to upwards
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1 + 1, "right", GREEN) == False:
        expanded_states.append(move(1, "up", move(1, "up", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1 + 1, "up", GREEN) == False:
        expanded_states.append(move(1, "up", move(1, "up", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1 + 1, "up", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 - 1, col_1 + 1, "right", GREEN):
        expanded_states.append(move(1, "up", move(1, "up", initial_state, row_1, col_1), row_2, col_2))
    ##### moving empty blocks to downwards
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1 + 1, "right", GREEN) == False:
        expanded_states.append(move(1, "down", move(1, "down", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "down", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1 + 1, "down", GREEN) == False:
        expanded_states.append(move(1, "down", move(1, "down", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "down", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "left", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1 + 1, "down", GREEN) == False and \
            check_NeigbourEqualTo_X(initial_state, row_1 + 1, col_1 + 1, "right", GREEN):
        expanded_states.append(move(1, "down", move(1, "down", initial_state, row_1, col_1), row_2, col_2))
    ##### moving empty blocks to left
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1 - 1, "left", GREEN):
        expanded_states.append(move(2, "left", move(2, "left", initial_state, row_1, col_1), row_2, col_2))
    ##### moving empty blocks to right
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", GREEN) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2 + 1, "right", GREEN):
        expanded_states.append(move(2, "right", move(2, "right", initial_state, row_1, col_1), row_2, col_2))
    # ------------------------------------------------------------------------------------------------------------------
    # when moving a red block to empty (blank) places ...
    if check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "up", RED) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "up", RED):
        expanded_states.append(move(2, "up", move(2, "up", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", RED) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "down", RED):
        expanded_states.append(move(2, "down", move(2, "down", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "left", RED) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "left", RED):
        expanded_states.append(move(2, "left", move(2, "left", initial_state, row_1, col_1), row_2, col_2))
    elif check_NeigbourEqualTo_X(initial_state, row_1, col_1, "down", EMPTY) and \
            check_NeigbourEqualTo_X(initial_state, row_1, col_1, "right", RED) and \
            check_NeigbourEqualTo_X(initial_state, row_2, col_2, "right", RED):
        expanded_states.append(move(2, "right", move(2, "right", initial_state, row_1, col_1), row_2, col_2))
    # ------------------------------------------------------------------------------------------------------------------
    return expanded_states

def uniform_cost_search(initial_state):
    """Finds the path taken by the uniform cost search algorithm
       Parameters
       ----------
       initial_state: 2-dimensional array representing initial block world config
       Returns
       -------
       path: (sequence of states to solve the block world) type - list of 2D arrays
    """
    path = []
    # our goal state is when bottom-left corner of red block is at last row and at first column.
    row_goal = 3
    col_goal = 0
    # need a min priority queue, so let's use Queue module of Python's standard library.
    minQueue = Queue.PriorityQueue()
    # let's create our paths and put them in our minQueue and so on ...
    start = time.clock()
    BREAK = False
    while BREAK == False:
        #
        if minQueue.empty():
            PATH = [initial_state]
        else:
            minPath = minQueue.get(False)
            PATH = minPath[1]
        #
        last_state = (PATH[-1])
        #
        if last_state[row_goal][col_goal] == 4:
            path = PATH
            BREAK = True
        else:
            states = get_successors(last_state)
            for state in states:
                if state not in PATH:
                    child_path = copy.deepcopy(PATH)
                    child_path.append(state)
                    if state[row_goal][col_goal] == 4:
                        path = PATH
                        BREAK = True
                    else:
                        minQueue.put((len(child_path), child_path))
            BREAK = True

    func_time = time.clock() - start
    print "time of func: "+str(func_time)

    return path

def a_star_heuristic(state):
    """Euclidean distance heuristic for a star algorithm
       Parameters
       ----------
       state: 2-dimensional array representing block world state
       Returns
       -------
       Euclidean distance (type- float) as defined in the assignment description
    """


    return 0.0

def a_star_search(initial_state):
    """Finds the path taken by the a star search algorithm
       Parameters
       ----------
       initial_state: 2-dimensional array representing initial block world config
       Returns
       -------
       path: (sequence of states to solve the block world) type-list of 2D arrays
    """
    path = []


    return path

#######################################################################################################################
#######################################################################################################################

def findEmptyPlaces(initial_state):
    """Finds rows and colums of empty places.
       initial_state: 2-dimensional array representing initial block world config.
       empty1_row: row of first empty block.
       empty1_column: column of first empty block.
       empty2_row: row of second empty block.
       empty2_column: column of second empty block.
       empty_RowColumnIndex: [[empty1_row,empty1_column],[empty2_row,empty2_column]] .
    """
    empty_RowColumnIndex = []
    row_size = len(initial_state)
    for row in range(row_size):
        column_size = len(initial_state[row])
        for column in range(column_size):
            if (initial_state[row][column]==EMPTY):
                empty_RowColumnIndex.append([row,column])
    return empty_RowColumnIndex

def check_NeigbourEqualTo_X(initial_state, row, col, direction, X):
    """Checks if initial_state[row][col] has a neigbour equal to X at defined direction.
       If neigbour at defined direction is equal to X then the function returns true, else returns false.
    """
    if direction=="up":
        if row>0:
            return (initial_state[row - 1][col] == X)
    elif direction=="down":
        if row<3:
            return (initial_state[row + 1][col] == X)
    elif direction=="left":
        if col>0:
            return (initial_state[row][col - 1] == X)
    elif direction=="right":
        if col<3:
            return (initial_state[row][col + 1] == X)
    else:
        raise TypeError
    return False

def move(move_step, direction, initial_state,row,col):
    """Return the result when you move block at row 'row' and column 'col' to 'move_step' times, at defined direction,
       if there exist any espace at that direction.
    """
    if direction=="up":
        moveTo_row = row - move_step
        moveTo_col = col
    elif direction=="down":
        moveTo_row = row + move_step
        moveTo_col = col
    elif direction=="left":
        moveTo_row = row
        moveTo_col = col - move_step
    elif direction=="right":
        moveTo_row = row
        moveTo_col = col + move_step
    else:
        raise TypeError("direction must be one of { \"up\", \"down\", \"right\", \"left\" }")

    if (moveTo_row<0 or moveTo_col<0) or (moveTo_row>3 or moveTo_col>3):
        raise Exception("!!!no where to move!!!")
    else:
        expanded_state = copy.deepcopy(initial_state)
        expanded_state[moveTo_row][moveTo_col] = initial_state[row][col]
        expanded_state[row][col] = initial_state[moveTo_row][moveTo_col]
        return expanded_state

###########################################################################################################

class Path(object):
    def __init__(self, path):
        self.path = path
        self.priority = len(self.path)
        self.last_state = self.path[-1]
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
    def append(self, last_state):
        self.path.append(last_state)
        self.priority += 1
        self.last_state = last_state

###########################################################################################################
###########################################################################################################
#copied from visualise.py

import Tkinter as tk
import threading
import time

class BlockInterface(object):
    def __init__(self, master,G):
        master.title("BlockWorld")
        canv_frame=tk.Frame(master)
        canv_frame.pack()
        self.canvas= tk.Canvas(canv_frame, width=10, height=60, bg="gray")
        self.canvas.pack(padx=10, pady=10)
        self.trace = G
        self.create_grid(G[0])
        self.activate(G[0])

    def create_rect(self,coord, val):
        if val==0:
            fill="white"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)
        elif val == 1:
            fill ="blue"
            self.canvas.create_rectangle(coord, fill=fill, outline="black")
        elif val == 2:
            fill = "green"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)
        elif val == 4:
            fill = "red"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)

    def create_row(self, vector, y_coord):
        y0, y1=y_coord
        w=70
        x0, x1=0, w
        self.canvas.configure(width=w*len(vector))
        for i in range(len(vector)):
            self.create_rect([x0,y0,x1,y1], vector[i])
            x0=x1
            x1+=w
        return

    def create_grid(self, matrix):
        yc_og= (0,60)
        yc=(0,60)
        self.canvas.configure(height=60*len(matrix))
        for vector in matrix:
            self.create_row(vector, yc)
            yc=(yc[1],yc[1]+yc_og[1])

    def update_grid(self, G):
        self.canvas.update()
        self.create_grid(G)

    def activate(self, G):
        thread=threading.Thread(target=lambda: self.solve_puzzle(G))
        thread.daemon=True # End thread when program is closed
        thread.start()

    def solve_puzzle(self, G):
        i=0
        while True:
            try:
                time.sleep(1)
                G= self.trace[i]
                self.update_grid(G)
                i+=1
            except IndexError:
                break


def start_simulation(G):
    root=tk.Tk()
    root.resizable(0,0)
    BlockInterface(root,G)
    root.mainloop()

# this is an example sequence to check that the simulation works
example_sequence= [[[1,2,1,1],[1,2,4,4],[2,2,4,4],[1,1,0,0]],
                   [[1,2,1,1],[1,2,0,0],[2,2,4,4],[1,1,4,4]],
                   [[1,2,1,0],[1,2,0,1],[2,2,4,4],[1,1,4,4]],
                   [[1,2,0,1],[1,2,0,1],[2,2,4,4],[1,1,4,4]],
                   [[1,0,2,1],[1,0,2,1],[2,2,4,4],[1,1,4,4]]]

# call the start simulation function with your sequence of moves (returned by UCS or A*)
# as long as your moves are valid, it will work as expected

start_simulation(example_sequence)
###########################################################################################################
###########################################################################################################


"""
abc = [[2,4,4,1],
       [2,4,4,1],
       [0,1,1,1],
       [0,2,2,1]]

[[row1,col1],[row2,col2]] = findEmptyPlaces(abc)
print "row1:", row1,", col1:", col1
print "row2:", row2,", col2:", col2

for i in abc:
    print i

print "__"

result_state = get_successors(abc)

for i in (result_state):
    for j in i:
        print j
    print "1-1-1"
"""
print "---"
initial_state = [ [1,2,1,1], [1,2,4,4], [2,2,4,4], [1,1,0,0] ]
print initial_state
print "#--#"
print uniform_cost_search(initial_state)
