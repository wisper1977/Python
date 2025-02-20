import sys
import math
from collections import Counter

log=lambda x: print(x, file=sys.stderr, flush=True)
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

surface_n = int(input())  # the number of points used to draw the surface of Mars.
surface=[]

for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    surface.append((land_x,land_y))

# --------------------------------------
#           FIND LANDING SPOT    
# --------------------------------------
prevX, prevY = (0, 0)
landing = []
for x, y in surface:
    if prevY == y:
        landing.append([prevX, prevY])
        landing.append([x, y])
    prevX, prevY = x, y
landing_x = sum([x for x, _ in landing])/2
landing_y = sum([y for _, y in landing])/2

# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]
    delta_y = y - landing_y
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    a = -3.711 + 2
    b = v_speed
    c = delta_y
    # log(f"b: {b}")

    t = (b-math.sqrt(-4*a*c + b**2)/2*a)
    log(f"t: {t}")

    lx = landing_x
    hx = t * h_speed 
    future_x = x + hx
    delta_x = lx-future_x

    log(f"future_x: {future_x} landing_x: {landing_x}")
    log(f"y: {y}, landing_y: {landing_y}")
    log(f"h_speed: {h_speed}")
    log(f"delta_x: {delta_x}")

    rotation = min(int(math.sqrt(abs(lx-future_x))),30)
    y_vec = math.cos(math.radians(rotation))
    if delta_x > 0: rotation = -rotation

    # # high air
    # if y >= 2500:
    #     thrust = 3
    # # mid air
    if delta_y >= 100:
        if landing_y > 2000 and abs(landing_x-x) > 500: 
            thrust = 4
            rotation = min(15,rotation)
        elif abs(v_speed) > 20: thrust = 4
        else: thrust = int(3.711 // y_vec)
    else:
        thrust = 0
        rotation = 0

    print(f"{rotation} {thrust}")
