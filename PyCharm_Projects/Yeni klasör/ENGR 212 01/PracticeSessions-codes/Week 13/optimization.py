import time
import random
import math

PEOPLE = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
DESTINATION = "LGA"

FLIGHTS = {}
for line in file('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(",")
    FLIGHTS.setdefault((origin, dest), [])

    # Add details to the list of possible flights
    FLIGHTS[(origin, dest)].append((depart, arrive, int(price)))

def get_minutes(t):
    x = time.strptime(t, "%H:%M")
    return x[3] * 60 + x[4]

def print_schedule(row):
    for i in range(0, len(row), 2):
        name = PEOPLE[i/2][0]
        origin = PEOPLE[i/2][1]

        out = FLIGHTS[(origin, DESTINATION)][row[i]]
        ret = FLIGHTS[(DESTINATION, origin )][row[i+1]]
        print "%10s%10s %5s-%5s $%3s %5s-%5s $%3s" % (name, origin,
                                                     out[0], out[1], out[2],
                                                     ret[0], ret[1], ret[2])


s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]

#  This function is extended
def schedule_cost(solution):
    total_price = 0
    latest_arrival = 0
    earliest_departure = 24 * 60
    #---------------------------
    time_in_air = 0 # time which is spent in air (or on plane)
    time_penalty = 0
    #---------------------------

    for i in range(0, len(solution), 2):
        # Get the inbound and outbound flights
        origin = PEOPLE[i/2][1]
        outbound = FLIGHTS[(origin, DESTINATION)][solution[i]]
        inbound = FLIGHTS[(DESTINATION, origin)][solution[i+1]]
        #---------------------------
        time_in_air += get_minutes(outbound[1]) - get_minutes(outbound[0]) # we add the difference of time intervals of outbound to the time that is spent in air
        time_in_air += get_minutes(inbound[1]) - get_minutes(inbound[0]) # we add the difference of time intervals of inbound to the time that is spent in air
        #---------------------------

        # Total price is the price of all outbound and return flights
        total_price += outbound[2]
        total_price += inbound[2]

        # Track is the latest arrival and earliest departure
        if latest_arrival < get_minutes(outbound[1]):
            latest_arrival = get_minutes(outbound[1])

        if earliest_departure > get_minutes(inbound[0]):
            earliest_departure = get_minutes(inbound[0])

    #---------------------------
    if earliest_departure < 8 * 60:
        time_penalty = 20  # we add a penalty of $20 for making anyone to get to the airport before 8 a.m.
    #---------------------------

    # Every person must wait at the airport until the latest person arrives.
    # They must also arrive at the same time and wait for their flights.
    total_wait = 0
    for i in range(0, len(solution), 2):
        # Get the inbound and outbound flights
        origin = PEOPLE[i/2][1]
        outbound = FLIGHTS[(origin, DESTINATION)][solution[i]]
        inbound = FLIGHTS[(DESTINATION, origin)][solution[i+1]]

        total_wait += latest_arrival - get_minutes(outbound[1])
        total_wait += get_minutes(inbound[0]) - earliest_departure

    # Does this solution require an extra day of car rental? That will be $50!
    if latest_arrival < earliest_departure:
        total_price += 50

    #return total_price + total_wait
    #-------------------------------
    time_in_air_cost_perMinute = time_in_air * .5 # .5 is equal to $.50
    return total_price + total_wait + time_in_air_cost_perMinute + time_penalty
    #-------------------------------------------

def random_optimize(domain, cost_fn):
    best = 9999999999
    best_row = None
    for i in range(1000):
        # Create a random solution
        row = [random.randint(d[0], d[1]) for d in domain]

        # Get the cost
        cost = cost_fn(row)

        # Compare it to the best one so far
        if cost < best:
            best = cost
            best_row = row
    return row

domain = [(0, 9)] * len(PEOPLE) * 2


# This is a new function implemented in order to do the handling for multiple starting points and return the best one.
def random_optimize_with_multiple_starting_solutions(num_tries, domain, cost_fn):
    assert(num_tries > 0) # we check if number of tries is higher than 0, if so, continue
    solutions = []
    for i in range(num_tries): # for each try, find the schedule
        solutions.append(random_optimize(domain, cost_fn))

    #print solutions
    ranked_solutions = [(cost_fn(sol), sol) for sol in solutions] # make pairs of tuple --> (cost, schedule) for each schedule
    #print ranked_solutions
    ranked_solutions.sort() # sort them depending upon their cost
    return ranked_solutions[0][1] # and return the schedule of the lowest cost


def hill_climb(domain, cost_fn):
    # Create a random solution
    sol = [random.randint(d[0], d[1]) for d in domain]

    while True:
        # Create a list of neighboring solutions
        neighbors = []
        for j in range(len(domain)):
            # One away in each direction
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])

        # See what the best solution amongst the neighbors is
        current = cost_fn(sol)
        best = current
        for neighbor in neighbors:
            cost = cost_fn(neighbor)
            if cost < best:
                best = cost
                sol = neighbor

        if best == current:
            return sol

def annealing_optimize(domain, cost_fn, t=10000.0, cool=0.95, step=1):
    # Initialize the values randomly
    vec = [random.randint(d[0], d[1]) for d in domain]

    while t > 0.1:
        # Choose one of the indices
        i = random.randint(0, len(domain) - 1)

        # Choose a direction
        dir = random.randint(-step, step)
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]:
            vecb[i]=domain[i][0]
        elif vecb[i]>domain[i][1]:
            vecb[i]=domain[i][1]

        old_cost = cost_fn(vec)
        new_cost = cost_fn(vecb)
        p = pow(math.e, (-old_cost-new_cost) / t)
        if new_cost < old_cost or random.random() < p:
            vec = vecb
        t = t * cool
    return vec


def genetic_optimize(domain, cost_fn, pop_size=50, step=1, mut_prob=0.2, elite=0.2, maxiter=100):
    def mutate(vec):
        i = random.randint(0, len(domain) - 1)
        if random.random() < 0.5 and vec[i] > domain[i][0]:
            return vec[0:i] + [vec[i]-step] + vec[i+1:]
        elif vec[i]<domain[i][1]:
            return vec[0:i] + [vec[i]+step] + vec[i+1:]

    def crossover(r1,r2):
        return r1
        i=random.randint(1, len(domain) - 2)
        return r1[0:i] + r2[i:]

    # Build the initial population
    pop = []
    for i in range(pop_size):
        vec = [random.randint(d[0], d[1]) for d in domain]
        pop.append(vec)

    top_elite = int(elite * pop_size)

    print type(pop)

    # Main Loop
    for i in range(maxiter):
        scores = [(cost_fn(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s, v) in scores]

        pop = ranked[0:top_elite]
        while len(pop) < pop_size:
            if random.random() < mut_prob:
                c = random.randint(0, top_elite)
                pop.append(mutate(ranked[c]))
            else:
                c1 = random.randint(0, top_elite)
                c2 = random.randint(0, top_elite)
                pop.append(crossover(ranked[c1], ranked[c2]))
    return scores[0][1]