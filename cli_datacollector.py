```python
import time
import csv
import os
from pynput import keyboard

# Directory to save the CSV file
output_directory = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(output_directory, "typing_data.csv")

# Dictionary to store typing pattern data
typing_data = {
    'press_times': {},  # Key: key, Value: press timestamp
    'release_times': {},  # Key: key, Value: release timestamp
    'dwell_times': [],  # Dwell time for each keypress
    'flight_times': [],  # Time between consecutive key presses
    'key_pressed': [],  # Sequence of keys pressed
    'error_rate': 0,  # Number of backspaces
    'user_id': 'User_1'  # Default user ID
}

last_release_time = None  # To track flight time
start_time = time.time()  # To calculate typing speed
key_count = 0  # To track the number of keypresses

# Function to handle key press
def on_press(key):
    global last_release_time, key_count

    try:
        key_char = key.char  # Handle alphanumeric keys
    except AttributeError:
        key_char = str(key)  # Handle special keys (e.g., shift, ctrl)

    # Record press time
    typing_data['press_times'][key_char] = time.time()
    typing_data['key_pressed'].append(key_char)
    key_count += 1

    # Calculate flight time if it's not the first keypress
    if last_release_time is not None:
        flight_time = typing_data['press_times'][key_char] - last_release_time
        typing_data['flight_times'].append(flight_time)

    # Handle backspace to track errors
    if key == keyboard.Key.backspace:
        typing_data['error_rate'] += 1

# Function to handle key release
def on_release(key):
    global last_release_time

    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    # Record release time
    typing_data['release_times'][key_char] = time.time()

    # Calculate dwell time
    dwell_time = typing_data['release_times'][key_char] - typing_data['press_times'][key_char]
    typing_data['dwell_times'].append(dwell_time)

    # Update last release time
    last_release_time = typing_data['release_times'][key_char]

    # Stop listener if 'esc' is pressed
    if key == keyboard.Key.esc:
        # Save the collected data to a CSV
        save_typing_data_to_csv()
        return False

# Function to save typing data to a CSV
def save_typing_data_to_csv():
    global key_count

    # Calculate typing speed (characters per minute)
    elapsed_time = time.time() - start_time
    typing_speed = (key_count / elapsed_time) * 60

    # Calculate average dwell and flight times
    avg_dwell_time = sum(typing_data['dwell_times']) / len(typing_data['dwell_times']) if typing_data['dwell_times'] else 0
    avg_flight_time = sum(typing_data['flight_times']) / len(typing_data['flight_times']) if typing_data['flight_times'] else 0

    # Save the data to a CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            typing_data['user_id'],
            avg_dwell_time,
            avg_flight_time,
            typing_speed,
            typing_data['error_rate'],
            time.strftime('%Y-%m-%d %H:%M:%S')
        ])
    print(f"Typing data saved to {csv_file}")

# Start the listener in the background
def start_monitoring():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Ensure CSV file has headers if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'user_id',
            'avg_dwell_time',
            'avg_flight_time',
            'typing_speed',
            'error_rate',
            'timestamp'
        ])

# Run the monitoring function
if __name__ == "__main__":
    print("Start typing (press 'esc' to stop)...")
    start_monitoring()
```