"""
filehandling

Description: This module provides utility functions for file handling operations, including reading from and writing to CSV and JSON files.

Functions:
    - read_csv(file_path): Read data from a CSV file.
    - write_csv(file_path, data, fieldnames): Write data to a CSV file.
    - read_json(file_path): Read data from a JSON file.
    - write_json(file_path, data): Write data to a JSON file.
"""

import csv, json

def read_csv(file_path):
    """
    Read data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list of dict: List of dictionaries representing rows of data from the CSV file.
    """
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_path, data, fieldnames):
    """
    Write data to a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        data (list of dict): Data to be written to the CSV file.
        fieldnames (list of str): Field names for the CSV file.

    Returns:
        None
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def read_json(file_path):
    """
    Read data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Data read from the JSON file.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def write_json(file_path, data):
    """
    Write data to a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        data (dict): Data to be written to the JSON file.

    Returns:
        None
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    # Test the functions here

    # Test read_csv function
    csv_data = read_csv("example.csv")
    print("CSV data:", csv_data)

    # Test write_csv function
    write_csv("example_output.csv", csv_data, ['name', 'age', 'city'])
    print("CSV data written to 'example_output.csv'.")

    # Test read_json function
    json_data = read_json("example.json")
    print("JSON data:", json_data)

    # Test write_json function
    write_json("example_output.json", json_data)
    print("JSON data written to 'example_output.json'.")
