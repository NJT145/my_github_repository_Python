"""
I used my 3 days extra and one day late with %-25 decrease on my grade for that assignment.

Assuming that agent exits when it is on a blue or a green block.
Assuming discount=0.676 . ( I found it after built my functions. you would better to say it at pdf. )
"""

# rewards of blocks in order [white,light_blue,dark_blue,green]
rewards = [-1, -5, -10, 30]

# discount at each move; no discount.
discount = 0.676

# actions
(North, East, South, West, Exit) = (0, 1, 2, 3, 4)

# at each state, the agent can move to one of (North,East,South,West) directions and
# each move action can happen with move_prob=0.70
# or can switch to one of its perpendicular moves with probability switch_prob=((1-move_prob)/2)=0.15
move_prob = 0.70
switch_prob = ((1-move_prob)/2)


# naming the state coordinates
def states_localization(grid_config):
    """ naming states.
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
    """ compute v_values of states after 100 iterations.
    """
    # initialize step k
    k = 0
    # 2D list of states
    states = states_localization(grid_config)
    # building rewards dictionary for states
    colorID_dict = {}
    for row1 in range(len(grid_config)):
        for col1 in range(len(grid_config[row1])):
            colorID_dict[(states[row1][col1])] = grid_config[row1][col1]
    # initialize dictionary that has state coordinate tuple as key and v_value of state as value
    v_values_dict = {}
    for row in range(len(grid_config)):
        for col in range(len(grid_config[row])):
            # initialize v_values at 0 for k=0
            v_values_dict[(states[row][col])] = 0.0
    # let's make iterations untill k=100
    while k <= 100:
        nrow = len(grid_config)
        for row_num in range(nrow):
            ncol = len(grid_config[row_num])
            for col_num in range(ncol):
                state = states[row_num][col_num]
                # Agent will get reward and exit when it comes on a colored block.
                color_id = colorID_dict[state]
                if color_id != 0:
                    v_values_dict[state] = rewards[color_id]
                # calculate v_values for others...
                else:
                    # old v_values around...
                    (state_North, state_East, state_South, state_West) = (state, state, state, state)
                    if row_num > 0:
                        state_North = (((ncol-row_num-1) + 1), col_num)
                    if col_num < (ncol - 1):
                        state_East = ((ncol-row_num-1), (col_num + 1))
                    if row_num < (nrow - 1):
                        state_South = (((ncol-row_num-1) - 1), col_num)
                    if col_num > 0:
                        state_West = ((ncol-row_num-1), (col_num - 1))
                    # rewards of moving blocks around ...
                    reward_North = rewards[colorID_dict[state_North]]
                    reward_East = rewards[colorID_dict[state_East]]
                    reward_South = rewards[colorID_dict[state_South]]
                    reward_West = rewards[colorID_dict[state_West]]
                    # calculate q_values
                    q_values = []
                    ## q_value for action to move North
                    q_value_North = move_prob * (reward_North + discount * v_values_dict[state_North])
                    q_value_North += switch_prob * (reward_East + discount * v_values_dict[state_East])
                    q_value_North += switch_prob * (reward_West + discount * v_values_dict[state_West])
                    q_values.append(q_value_North)
                    ## q_value for action to move East
                    q_value_East = move_prob * (reward_East + discount * v_values_dict[state_East])
                    q_value_East += switch_prob * (reward_North + discount * v_values_dict[state_North])
                    q_value_East += switch_prob * (reward_South + discount * v_values_dict[state_South])
                    q_values.append(q_value_East)
                    ## q_value for action to move South
                    q_value_South = move_prob * (reward_South + discount * v_values_dict[state_South])
                    q_value_South += switch_prob * (reward_East + discount * v_values_dict[state_East])
                    q_value_South += switch_prob * (reward_West + discount * v_values_dict[state_West])
                    q_values.append(q_value_South)
                    ## q_value for action to move West
                    q_value_West = move_prob * (reward_West + discount * v_values_dict[state_West])
                    q_value_West += switch_prob * (reward_North + discount * v_values_dict[state_North])
                    q_value_West += switch_prob * (reward_South + discount * v_values_dict[state_South])
                    q_values.append(q_value_West)
                    # v_value result for that state after k iterations
                    v_values_dict[state] = float("%.1f" % max(q_values))
        k += 1
    # building the result list
    v_values = []
    nrow = len(states)
    for row0 in range(nrow):
        ncol = len(states[row0])
        for col0 in range(ncol):
            state1 = states[nrow - row0 - 1][col0]
            v_value =  v_values_dict[state1]
            v_values.append((state1, v_value))
    # and, returns...
    return v_values


def get_optimal_policy(grid_config):
    """
    """
    # let's get v_values
    v_values = compute_v_values(grid_config)
    # and states...
    states = states_localization(grid_config)
    # and let's put v_values to a dictionary for simplicity
    v_values_dict = {}
    for (state1, value1) in v_values:
        v_values_dict[state1] = value1
    # building rewards dictionary for states
    colorID_dict = {}
    for row1 in range(len(grid_config)):
        for col1 in range(len(grid_config[row1])):
            colorID_dict[(states[row1][col1])] = grid_config[row1][col1]
    # now, calculate q_values for each move, for each state, to find optimal policy
    policy = []
    top_to_bottom_policy = []
    nrow = len(grid_config)
    for row_num in range(nrow):
        row_list = []
        ncol = len(grid_config[row_num])
        for col_num in range(ncol):
            state = states[row_num][col_num]
            # Agent will get reward and exit when it is on a colored block.
            color_id = colorID_dict[state]
            if color_id != 0:
                row_list.append((state, Exit))
            # find optimal policy for others...
            else:
                # v_values around...
                (state_North, state_East, state_South, state_West) = (state, state, state, state)
                if row_num > 0:
                    state_North = (((ncol - row_num - 1) + 1), col_num)
                if col_num < (ncol - 1):
                    state_East = ((ncol - row_num - 1), (col_num + 1))
                if row_num < (nrow - 1):
                    state_South = (((ncol - row_num - 1) - 1), col_num)
                if col_num > 0:
                    state_West = ((ncol - row_num - 1), (col_num - 1))
                # rewards of moving blocks around ...
                reward_North = rewards[colorID_dict[state_North]]
                reward_East = rewards[colorID_dict[state_East]]
                reward_South = rewards[colorID_dict[state_South]]
                reward_West = rewards[colorID_dict[state_West]]
                # calculate q_values
                q_values = []
                ## q_value for action to move North
                q_value_North = move_prob * (reward_North + discount * v_values_dict[state_North])
                q_value_North += switch_prob * (reward_East + discount * v_values_dict[state_East])
                q_value_North += switch_prob * (reward_West + discount * v_values_dict[state_West])
                q_values.append((q_value_North, North))
                ## q_value for action to move East
                q_value_East = move_prob * (reward_East + discount * v_values_dict[state_East])
                q_value_East += switch_prob * (reward_North + discount * v_values_dict[state_North])
                q_value_East += switch_prob * (reward_South + discount * v_values_dict[state_South])
                q_values.append((q_value_East, East))
                ## q_value for action to move South
                q_value_South = move_prob * (reward_South + discount * v_values_dict[state_South])
                q_value_South += switch_prob * (reward_East + discount * v_values_dict[state_East])
                q_value_South += switch_prob * (reward_West + discount * v_values_dict[state_West])
                q_values.append((q_value_South, South))
                ## q_value for action to move West
                q_value_West = move_prob * (reward_West + discount * v_values_dict[state_West])
                q_value_West += switch_prob * (reward_North + discount * v_values_dict[state_North])
                q_value_West += switch_prob * (reward_South + discount * v_values_dict[state_South])
                q_values.append((q_value_West, West))
                optimal_move = max(q_values)
                (q_value, action) = optimal_move
                row_list.append((state, action))
        top_to_bottom_policy.append(row_list)
    for row0 in range(nrow):
        for col0 in top_to_bottom_policy[nrow - 1 - row0]:
            policy.append(col0)
    return policy


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

print("#"*999)

print("config =")
print("[[2, 2, 2, 2, 2, 2, 2, 2],")
print(" [2, 0, 0, 0, 1, 0, 0, 2],")
print(" [2, 0, 0, 1, 0, 0, 0, 2],")
print(" [2, 0, 0, 0, 1, 0, 0, 2],")
print(" [2, 0, 0, 0, 0, 0, 0, 2],")
print(" [2, 0, 0, 0, 0, 0, 0, 2],")
print(" [2, 0, 0, 0, 0, 0, 3, 2],")
print(" [2, 2, 2, 2, 2, 2, 2, 2]]")

print("#"*999)

v_values=compute_v_values(config)
print("compute_v_values(config) =")
print(v_values)

print("#"*999)

policy=get_optimal_policy(config)
print("get_optimal_policy(config) =")
print(policy)

print("#"*999)
