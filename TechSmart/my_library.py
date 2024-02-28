"""
my_library

Description:
"""

import tsapp, random, time, sys, os, pygame, requests

# Function to clear screen
def clear_screen():
    """
    Clears the console screen.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# wait x second
def wait_seconds(seconds):
    """
    Pauses the program execution for the specified number of seconds.

    Args:
        seconds (int): The number of seconds to wait.

    Returns:
        None
    """
    pygame.init()
    pygame.time.wait(seconds * 1000)
    
# tsapp Function to create a countdown clock    
def ts_countdown(seconds, font="Roboto-Black.ttf", position=(100, 100), initial_color=tsapp.BLUE, countdown_color=tsapp.RED):
    """
    Displays a countdown timer on a graphics window.

    Args:
        seconds (int): The number of seconds for the countdown.
        font (str): The font to be used for displaying the countdown.
        position (tuple): The position (x, y) of the countdown display.
        initial_color (tuple): The initial color of the countdown display.
        countdown_color (tuple): The color of the countdown display when counting down.

    Returns:
        None
    """
    # Create a window
    window = tsapp.GraphicsWindow()

    # Create a TextLabel
    countdown = tsapp.TextLabel(font, position[0], position[1], 100, 100, str(seconds), initial_color)
    timesup = tsapp.TextLabel(font, position[0], position[1], 100, 800, "Time is up!!", tsapp.RED)

def update_countdown_text(i):
    """
    Updates the countdown text with the current value of 'i'.

    Args:
    i (int): The current countdown value.

    Returns:
    None
    """
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

import requests

def call_api(url, method='GET', params=None, headers=None, timeout=10):
    """
    Calls an API and returns the response.

    Args:
        url (str): The URL of the API.
        method (str): The HTTP method to be used (GET, POST, PUT, DELETE, etc.).
        params (dict, optional): Parameters to be sent with the request.
        headers (dict, optional): Headers to be sent with the request.
        timeout (int, optional): Timeout for the request in seconds.

    Returns:
        dict: The JSON response from the API.
    """
    try:
        response = requests.request(method, url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.Timeout:
        print("Timeout error: The request to", url, "timed out.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return None

# Example usage:
api_url = "https://jsonplaceholder.typicode.com/posts/1"
response_data = call_api(api_url)
if response_data:
    print(response_data)
