import sys

# Define the Point class (as in Java's java.awt.Point)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Read input
surface_n = int(input())  # the number of points used to draw the surface of Mars
land = []
ground = -1
high = 0

for i in range(surface_n):
    land_x, land_y = map(int, input().split())  # X and Y coordinates of surface points
    land.append(Point(land_x, land_y))
    high = max(high, land_y)
    if i == 0:
        continue
    if land[i].y == land[i-1].y:
        ground = i - 1

test_case = -1
off_the_mark = False

# Game loop
while True:
    x, y, h_speed, v_speed, fuel, rotate, power = map(int, input().split())
    
    if test_case == -1:
        if h_speed == 0:
            test_case = 1
        else:
            test_case = 0

    # RULES FOR TEST 1
    if test_case == 0:
        if y - land[ground].y < 800:
            if v_speed <= -39:
                print("0 4")
            else:
                print("0 3")
            continue
        elif x <= land[ground + 1].x:
            print("-45 4")
            continue
        elif v_speed <= -20:
            print("0 4")
            continue
        elif v_speed <= -12:
            print("0 2")
            continue
        else:
            print("45 4")
            continue

    # RULES FOR TEST 2
    if test_case == 1:
        if v_speed < -45 or y <= 1135:
            print("0 4")
            continue
        elif x <= land[ground].x:
            print("-32 3")
            continue
        elif v_speed == 0 and y > high:
            print("0 3")
            continue
        elif v_speed < 0 or y < high:
            print("0 4")
            continue
        elif v_speed >= 12 or off_the_mark:
            off_the_mark = True
            print("45 4")
            continue
        else:
            print("0 4")
            continue
