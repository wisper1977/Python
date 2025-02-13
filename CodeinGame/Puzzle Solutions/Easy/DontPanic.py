data = list(map(int, input().split()))
nb_floors, width, nb_rounds, exit_floor, exit_pos, _, _, nb_elevators = data

elevators = {exit_floor: exit_pos, **{floor: pos for floor, pos in (map(int, input().split()) for _ in range(nb_elevators))}}

while True:
    clone_floor, clone_pos, direction = input().split()
    clone_floor, clone_pos = int(clone_floor), int(clone_pos)
    
    if clone_floor == -1:
        print("WAIT")
        continue
    
    target_pos = elevators.get(clone_floor, exit_pos)
    print("BLOCK" if (clone_pos < target_pos and direction == "LEFT") or (clone_pos > target_pos and direction == "RIGHT") else "WAIT")
