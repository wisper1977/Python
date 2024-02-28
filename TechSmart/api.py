"""
api

Description: This module provides utility functions for making API calls and parsing API responses.

Functions:
    - call_api(url, method='GET', params=None, headers=None, timeout=10): Calls an API and returns the response.
    - parse_api_response(api_response): Parses an API response and converts it into a list of dictionaries.
"""

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

def parse_api_response(api_response):
    """
    Parses an API response and converts it into a list of dictionaries.

    Args:
        api_response (dict): The API response in JSON format.

    Returns:
        list of dict: A list of dictionaries representing the data from the API response.
    """
    try:
        data = api_response.json()
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            print("API response format not recognized.")
            return []
    except ValueError:
        print("Unable to parse API response as JSON.")
        return []

if __name__ == "__main__":
    # Test the functions here

    # Test call_api function
    response = call_api("https://jsonplaceholder.typicode.com/posts/1")
    print("API response:", response)

    # Test parse_api_response function
    parsed_data = parse_api_response(response)
    print("Parsed data:", parsed_data)
