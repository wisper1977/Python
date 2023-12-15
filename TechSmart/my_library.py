"""
my_library

Description:
"""

import tsapp, random, time, sys, os, pygame

# Function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# wait x second
def wait_seconds(seconds):
    pygame.init()
    pygame.time.wait(seconds * 1000)
    
# tsapp Function to create a countdown clock    
def ts_countdown(seconds, font="Roboto-Black.ttf", position=(100, 100), initial_color=tsapp.BLUE, countdown_color=tsapp.RED):
    # Create a window
    window = tsapp.GraphicsWindow()

    # Create a TextLabel
    countdown = tsapp.TextLabel(font, position[0], position[1], 100, 100, str(seconds), initial_color)
    timesup = tsapp.TextLabel(font, position[0], position[1], 100, 800, "Time is up!!", tsapp.RED)

    def update_countdown_text(i):
        countdown.text = str(i)

    # Add the text to the scene
    window.add_object(countdown)

    # Main loop
    for i in range(seconds, -1, -1):
        update_countdown_text(i)

        if 1 <= i <= 3:
            countdown.color = countdown_color

        elif i == 0:
            window.add_object(timesup)
            countdown.visible = False

        wait_seconds(1)
        window.finish_frame()
