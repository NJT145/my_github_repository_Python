"""


Assuming that agent exits when it is on a blue or a green block.
Assuming no discount.
"""

import copy

# rewards of blocks in order [white,light_blue,dark_blue,green]
rewards = [-1, -5, -10, 30]

# discount at each move; no discount.
discount = 1

# actions
(North, East, South, West, Exit) = (0, 1, 2, 3, 4)

# at each state, the agent can move to one of (North,East,South,West) directions and
# each move action can happen with move_prob=0.70
# or can switch to one of its perpendicular moves with probability switch_prob=((1-move_prob)/2)=0.15
move_prob = 0.70
switch_prob = ((1-move_prob)/2)
move_actions = [North, East, South, West]
switch_move = [(East, West), (North, South), (East, West), (North, South)]


# naming the state coordinates
def states_localization(grid_config):
    """
    """
    states = []
    nrow = len(grid_config)
    for row in range(nrow):
        row_states = []
        ncol = len(grid_config[row])
        for col in range(ncol):
            row_states.append(((ncol-row-1), col))
        states.append(row_states)
    return states


def compute_v_values(grid_config):
    """
    """
    # initialize step k
    k = 0
    # initialize dictionary that has state coordinate tuple as key and v_value of state as value
    states = states_localization(grid_config)
    v_values_dict = {}
    for row in range(len(grid_config)):
        for col in range(len(grid_config[row])):
            # initialize v_values at 0 for k=0
            v_values_dict[(states[row][col])] = 0
    # at k=1...
    k += 1
    for row1 in range(len(grid_config)):
        for col1 in range(len(grid_config[row1])):
            color_id_ = grid_config[row1][col1]
            if color_id_ != 0:
                v_values_dict[(states[row1][col1])] = rewards[color_id_]
    # let's make iterations untill k=100
    while k <= 100:
        current_v_values_dict = copy.deepcopy(v_values_dict)
        nrow = len(grid_config)
        for row_num in range(nrow):
            ncol = len(grid_config[row_num])
            for col_num in range(ncol):
                state = states[row_num][col_num]
                # Agent will exit when it comes on a colored block.
                color_id = grid_config[row_num][col_num]
                if color_id != 0:
                    pass
                # calculate v_values for others...
                else:
                    (v_value_North, v_value_East, v_value_South, v_value_West) = (0, 0, 0, 0)
                    if row_num > 0:
                        state_North = ((row_num - 1), col_num)
                        v_value_North = current_v_values_dict[state_North]
                    if col_num < (ncol - 1):
                        state_East = (row_num, (col_num + 1))
                        v_value_East = current_v_values_dict[state_East]
                    if row_num < (nrow - 1):
                        state_South = ((row_num + 1), col_num)
                        v_value_South = current_v_values_dict[state_South]
                    if col_num > 0:
                        state_West = (row_num, (col_num - 1))
                        v_value_West = current_v_values_dict[state_West]
                    # calculate q_values
                    q_values = []
                    ## q_value for action to move North
                    if row_num > 0:
                        pass
                        #q_value_North = current_v_values_dict[state] + (move_prob * ())
                    # q_value for action to move East

                    # q_value for action to move South

                    # q_value for action to move West

                    v_values_dict[(states[row_num][col_num])] = 0
        k += 1
    return v_values_dict


def get_optimal_policy(grid_config):
    """
    """
    #
    pass


# example configuration
config = [[2, 2, 2, 2, 2, 2, 2, 2],
          [2, 0, 0, 0, 1, 0, 0, 2],
          [2, 0, 0, 1, 0, 0, 0, 2],
          [2, 0, 0, 0, 1, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 3, 2],
          [2, 2, 2, 2, 2, 2, 2, 2]]
# path taken in above configuration
path = [(6, 1), (5, 1), (5, 2), (4, 2), (4, 3), (3, 3), (3, 4), (2, 4), (2, 5), (2, 6), (1, 6)]

compute_v_values(config)