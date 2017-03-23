import optimization

domain = [(0,9)] * (len(optimization.PEOPLE)*2)

# step1
s = optimization.random_optimize(domain, optimization.schedule_cost)
print optimization.schedule_cost(s)
optimization.print_schedule(s)

# step2
s = optimization.random_optimize_with_multiple_starting_solutions(5, domain, optimization.schedule_cost)
print optimization.schedule_cost(s)
optimization.print_schedule(s)

