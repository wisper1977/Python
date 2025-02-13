import sys

# Read initialization inputs
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = map(int, input().split())

# Dictionary to store elevator positions per floor
elevators = {}
for _ in range(nb_elevators):
    floor, pos = map(int, input().split())
    elevators[floor] = pos

# Add exit position as an "elevator" for logic simplicity
elevators[exit_floor] = exit_pos

while True:
    # Read the current state of the leading clone
    inputs = input().split()
    clone_floor = int(inputs[0])
    clone_pos = int(inputs[1])
    direction = inputs[2]
    
    # If no active clone, wait
    if clone_floor == -1:
        print("WAIT")
        continue
    
    # Get the target position (exit or elevator on this floor)
    target_pos = elevators.get(clone_floor, exit_pos)
    
    # Determine whether to block or wait
    if (clone_pos < target_pos and direction == "LEFT") or (clone_pos > target_pos and direction == "RIGHT"):
        print("BLOCK")
    else:
        print("WAIT")
