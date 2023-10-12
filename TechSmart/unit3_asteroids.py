"""
Unit 3 Project: Asteroids

Description:
"""

# Imports
import random, tsapp, math

# Variables and lists
asteroids = [] # List to store Asteroids
bullets = []  # List to store bullets
score = 0
font = "Roboto-Black.ttf"
game_over = False  # New variable to track game state

window = tsapp.GraphicsWindow()
bg = tsapp.Sprite("AlienSpace.jpg", 0, 0)
ship = tsapp.Sprite("SpaceShuttle.png", 509, 286.5, .25)
score_text = tsapp.TextLabel(font, 50, 10, 50, 500, str(score), tsapp.WHITE)
game_over_text = tsapp.TextLabel(font, 100, 200, 250, 1000, "GAME OVER!!", tsapp.RED)

window.add_object(bg)
window.add_object(ship)
window.add_object(score_text)

ship.angle = 0

# Start spawning asteroids
for i in range(4):
    
    # Generate random position for the asteroid while ensuring it's not too close to the ship
    while True:
        x = random.randint(0, 700)
        y = random.randint(0, 475)
        min_distance = 200  # Minimum distance between asteroid and ship
        if math.sqrt((x - ship.x) ** 2 + (y - ship.y) ** 2) >= min_distance:
            break

    # Load an asteroid image (replace "asteroid.png" with your own image)
    asteroid = tsapp.Sprite("Asteroid.png", x, y)

    # Create the asteroid on the canvas
    window.add_object(asteroid)
    asteroid.x_speed = random.randint(-100, 100)  # Random horizontal speed
    asteroid.y_speed = random.randint(-100, 100)  # Random vertical speed

    # Add the asteroid to the list
    asteroids.append(asteroid)
    
while window.is_running and not game_over:
    
    ## -- Movement -- ##

    if tsapp.is_key_down(tsapp.K_d):
        ship.x_speed = 100

    elif tsapp.is_key_down(tsapp.K_a):
        ship.x_speed = -100
        
    else:
        ship.x_speed = 0

    ## -- Vertical movement -- ##

    if tsapp.is_key_down(tsapp.K_w):
        ship.y_speed = -100

    elif tsapp.is_key_down(tsapp.K_s):
        ship.y_speed = 100

    else:
        ship.y_speed = 0

    ## -- Vertical movement -- ##

    if tsapp.is_key_down(tsapp.K_q):
        ship.angle += 5

    elif tsapp.is_key_down(tsapp.K_e):
        ship.angle -= 5

    ## -- Fire Bullet -- ##
    if tsapp.is_key_down(tsapp.K_SPACE):
        bullet_speed = 150  # Adjust bullet speed as needed
        
        # Convert ship.angle to radians (ship.angle is in degrees)
        angle_degrees = ship.angle
        
        # Convert degrees to radians by multiplying by pi / 180
        angle_radians = angle_degrees * 3.141592653589793 / 180.0
        
        # Calculate the horizontal and vertical components of the speed vector
        bullet_x_speed = -bullet_speed * math.sin(angle_radians)
        bullet_y_speed = -bullet_speed * math.cos(angle_radians)

        
        bullet = tsapp.Sprite("NumberDecimalRed.png", ship.x, ship.y-50)
        bullet.x_speed = bullet_x_speed
        bullet.y_speed = bullet_y_speed
        bullets.append(bullet)
        window.add_object(bullet)
    
    # Sprite Walls for Window    
    for asteroid in asteroids:
        x = asteroid.center_x
        y = asteroid.center_y
        
        # Check if the asteroid hits the left or right boundary
        if x < 127 or x > 891:
            asteroid.x_speed = -asteroid.x_speed  # Reverse horizontal speed
        
        # Check if the asteroid hits the top or bottom boundary
        if y < 98 or y > 475:
            asteroid.y_speed = -asteroid.y_speed  # Reverse vertical speed
            
        # Check for collision between ship and asteroid
        if ship.is_colliding_rect(asteroid):
            game_over = True
            break  # Exit the loop when collision is detected
            
    # Check for collisions between bullets and asteroids
    for bullet in bullets:
        for asteroid in asteroids:
            if asteroid.is_colliding_rect(bullet):
                asteroids.remove(asteroid)
                asteroid.destroy()
                bullets.remove(bullet)
                bullet.destroy()
                score += 1
                score_text.text = score

    # Game over logic
    if game_over:
        window.add_object(game_over_text)
        
    window.finish_frame()
