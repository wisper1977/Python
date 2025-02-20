import sys

# Read the game grid
grid = [input().strip() for _ in range(10)]

# Read the number of robots
robot_count = int(input())

# Store robot positions and directions
robots = []
for _ in range(robot_count):
    x, y, direction = input().split()
    robots.append((int(x), int(y), direction))

# Find safe platform cells to place arrows
platforms = []
for y in range(10):
    for x in range(19):
        if grid[y][x] == '.':  # Empty platform cell
            platforms.append((x, y))

# Simple strategy: Redirect robots initially to avoid immediate danger
commands = []
for x, y, direction in robots:
    if (x, y) in platforms:
        if direction == 'U':
            new_dir = 'R'  # Redirect upward-moving robots to the right
        elif direction == 'D':
            new_dir = 'L'  # Redirect downward-moving robots to the left
        elif direction == 'L':
            new_dir = 'U'  # Redirect left-moving robots upwards
        elif direction == 'R':
            new_dir = 'D'  # Redirect right-moving robots downwards
        commands.append(f"{x} {y} {new_dir}")

# Output the arrow placements
print(" ".join(commands))
