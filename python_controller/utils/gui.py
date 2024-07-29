import tkinter as tk

import json

def write_degree_to_json(degrees):
    """
    Writes the given degree value to a JSON file.
    
    Parameters:
        degrees (int): The degree value to write to the JSON file.
    """
    # Load existing data from the file, if any
    existing_data = read_settings_from_json()
    if existing_data is None:
        existing_data = {}
    
    # Update the degree value in the existing data
    existing_data['degree'] = degrees
    
    # Write the updated data back to the file
    with open('settings.json', 'w') as f:
        json.dump(existing_data, f)

def write_speed_to_json(speed):
    """
    Writes the given speed value to a JSON file.
    
    Parameters:
        speed (int): The speed value to write to the JSON file.
    """
    # Load existing data from the file, if any
    existing_data = read_settings_from_json()
    if existing_data is None:
        existing_data = {}
    
    # Update the speed value in the existing data
    existing_data['speed'] = speed
    
    # Write the updated data back to the file
    with open('settings.json', 'w') as f:
        json.dump(existing_data, f)

def read_settings_from_json():
    """
    Reads the degree and speed values from the JSON file and returns them as a dictionary.
    
    Returns:
        dict: A dictionary containing the degree and speed values read from the JSON file.
    """
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("JSON file not found.")
        return None

def on_slider_change(event):
    value_degree = int(slider.get())
    value_speed = int(slider2.get())
    write_degree_to_json(value_degree)
    write_speed_to_json(value_speed)

# Create main window
root = tk.Tk()
root.title("Slider Control")

# Create a slider widget
slider = tk.Scale(root, from_=-27, to=27, orient=tk.HORIZONTAL, command=on_slider_change)
slider2 = tk.Scale(root, from_=-1, to=3, orient=tk.HORIZONTAL, command=on_slider_change)
slider.pack(padx=200, pady=20)
slider2.pack(padx=200, pady=20)

# Start the Tkinter event loop
root.mainloop()