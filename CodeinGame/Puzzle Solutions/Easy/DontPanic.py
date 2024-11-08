import sys
import math

# nb_floors: number of floors
# width: width of the area
# nb_rounds: maximum number of rounds
# exit_floor: floor on which the exit is found
# exit_pos: position of the exit on its floor
# nb_total_clones: number of generated clones
# nb_additional_elevators: ignore (always zero)
# nb_elevators: number of elevators
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in input().split()]

# Store the position of elevators by floor
elevators = {}
for i in range(nb_elevators):
    elevator_floor, elevator_pos = [int(j) for j in input().split()]
    elevators[elevator_floor] = elevator_pos

# game loop
while True:
    inputs = input().split()
    clone_floor = int(inputs[0])  # floor of the leading clone
    clone_pos = int(inputs[1])  # position of the leading clone on its floor
    direction = inputs[2]  # direction of the leading clone: LEFT or RIGHT

    # Determine the target position (elevator or exit)
    target_pos = exit_pos if clone_floor == exit_floor else elevators.get(clone_floor, None)

    if target_pos is not None:
        # Check if the clone is moving in the right direction towards the target
        if (clone_pos < target_pos and direction == "LEFT") or (clone_pos > target_pos and direction == "RIGHT"):
            # If moving away from the target, block to change direction
            print("BLOCK")
        else:
            # Otherwise, wait to keep moving in the current direction
            print("WAIT")
    else:
        # No action needed if there's no relevant target (defensive programming)
        print("WAIT")
