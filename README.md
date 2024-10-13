# Keystroke Dynamics Data Collection Tool

This Python script is designed to collect and analyze keystroke dynamics, which can be used to identify unique typing patterns. The tool runs in the background and automatically logs parameters such as dwell time, flight time, typing speed, and error rate. The collected data is saved in a CSV file for future analysis and model training.

## Features

- **Real-time Keystroke Monitoring**: Tracks and logs key press and release times.
- **Dwell Time Calculation**: Measures the time a key is held down (dwell time).
- **Flight Time Calculation**: Measures the time between consecutive key presses (flight time).
- **Error Rate Tracking**: Tracks the number of errors based on backspace usage.
- **Typing Speed Calculation**: Calculates the typing speed in characters per minute.
- **Automatic Data Logging**: Saves the collected typing data into a CSV file in the directory where the program is stored.
- **Background Execution**: Monitors keystrokes in the background while the user types.

## Neural Network and Deep Learning Integration

### Overview

This tool incorporates neural networks (NN) and deep learning (DL) technologies to identify individuals based on their unique typing patterns. The model uses a combination of traditional keystroke dynamics parameters and additional features like typing speed and error rate, providing better accuracy and efficiency.

- **Neural Networks (NN)**: Neural networks are trained to recognize typing patterns and identify users based on their behavior. The collected parameters are fed into the neural network, which then learns the user's unique keystroke dynamics over time.
- **Deep Learning (DL)**: Advanced deep learning models like Convolutional Neural Networks (CNN) are used to improve the prediction capabilities by learning complex relationships between the parameters.

### Model Architecture

- **Input Layer**: Receives data such as dwell time, flight time, typing speed, and error rate.
- **Hidden Layers**: Consists of multiple dense layers that help in learning non-linear relationships between the inputs.
- **Output Layer**: Provides predictions on user identity by comparing typing data with stored profiles.

### Visualizing Deep Learning in Action

Deep learning models are particularly effective in recognizing complex patterns, such as common digraph times (e.g., "th," "he") and error patterns, which are difficult to notice with traditional statistical methods.

![Keystroke Dynamics Model Overview](https://image.shutterstock.com/image-illustration/neural-network-deep-learning-diagram-260nw-1370089854.jpg)

This figure provides a high-level overview of the keystroke dynamics model architecture, illustrating how data flows through a deep learning network to classify users.

## Data Collected

The script collects the following data points and saves them into a CSV file:

- `user_id`: A unique identifier for the user (default: "User_1").
- `avg_dwell_time`: The average time a key is held down.
- `avg_flight_time`: The average time between key presses.
- `typing_speed`: The typing speed calculated in characters per minute.
- `error_rate`: The percentage of errors (based on backspace usage).
- `timestamp`: The time when the data was recorded.

### Example Data Flow

1. **Keystrokes Captured**: Key press and release times are recorded.
2. **Parameters Calculated**: Dwell times, flight times, typing speed, and error rate are calculated.
3. **Model Training**: Data is passed through a neural network to train the system to recognize unique typing styles.

![Keystroke Dynamics Example](https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Keystroke-dynamics-overview.svg/1280px-Keystroke-dynamics-overview.svg.png)

This image demonstrates the flow of keystroke dynamics data, from key press capture to the neural network processing phase.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- `pynput` library for capturing keystrokes.
- `csv` module (included with Python).
- Any necessary libraries like `os` (included with Python).

### Install `pynput`:


pip install pynput
How to Use
Download or Clone the Repository:

bash
Copy code
git clone 
Run the Script:

Navigate to the directory where the script is located and run:

bash
Copy code
python typing_data_collector.py
Start Typing:

Once the script starts, begin typing in any application. The tool will record your typing patterns in the background. Press Esc to stop the data collection.

Check the Output:

A CSV file (typing_data.csv) will be automatically created in the same directory as the script. This file will contain the collected data, which can be used for training machine learning models or conducting further analysis.

CSV File Example
Here’s an example of how the CSV file looks:

user_id	avg_dwell_time	avg_flight_time	typing_speed	error_rate	timestamp
User_1	0.1025	0.2301	35.5	2	2024-09-05 14:32:10
User_2	0.0987	0.2154	42.3	1	2024-09-05 14:35:22
Customization
Change the user_id
By default, the user_id is set to User_1. You can modify this by changing the value in the typing_data dictionary:

python
Copy code
typing_data['user_id'] = 'Custom_User_ID'
Modify Collected Data
You can easily add or modify parameters to collect more detailed typing behavior by modifying the dictionary structure in the script.

Dependencies
The script depends on the following Python packages:

pynput: For capturing keyboard input.
csv: For saving the collected data in a CSV format.
Install the dependencies using:

bash
Copy code
pip install pynput
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Author
Ujan <3
Email: ujan.g570@gmail.com

Feel free to reach out with any questions, suggestions, or contributions!
