# Reading the input values
f, w, r, c, g, t, a, e = map(int, input().split())

# Initialize an empty dictionary to store the elevators' positions
h = {}

# Reading the elevator data and storing it in the dictionary
for _ in range(e):
    k, l = map(int, input().split())  # Read the floor number and elevator position
    h[k] = l  # Map the floor number to the elevator position

# The main game loop
while True:
    # Reading clone's current floor, position, and direction
    b, p, d = input().split()
    b, p = int(b), int(p)  # Convert floor and position to integers

    # Determine the elevator position for the current floor
    # If the clone is on the exit floor, we use the exit's position instead of the elevator's position
    m = g if b == c else h.get(b)

    # Logic to decide whether to block or wait
    if m and ((p < m and d == "LEFT") or (p > m and d == "RIGHT")):
        print("BLOCK")  # Block the clone if it's about to collide with an elevator
    else:
        print("WAIT")  # Otherwise, allow the clone to move freely
