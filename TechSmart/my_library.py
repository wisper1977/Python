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
def ts_countdown(seconds):
   
    # Create a window
    window = tsapp.GraphicsWindow() 

    # Create a TextLabel  
    countdown = tsapp.TextLabel("Roboto-Black.ttf", 100, 100, 100, 100, str(seconds), tsapp.BLUE)
    timesup = tsapp.TextLabel("Roboto-Black.ttf", 100, 100, 100, 800, "Time is up!!", tsapp.RED)
    
    # Add the text to the scene
    window.add_object(countdown)
    
    # Main loop
    for i in range (seconds,-1,-1):
        
        # Every 30 frames, if i is greater than 0, subtract 1 from the countdown
        if i > 0:
            countdown.text = str(i)
            wait_seconds(1)
        
        if 1 <= i <= 3:
            countdown.color = tsapp.RED
            
        elif i == 0:
            window.add_object(timesup)
            countdown.visible = False
            
        window.finish_frame()
        
