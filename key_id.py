import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import tensorflow as tf
from keras.models import load_model
import keras
import os
from tempfile import NamedTemporaryFile

# Global variables
typing_data = pd.DataFrame(columns=['timestamp', 'key', 'dwell_time', 'flight_time'])
key_press_time = {}
common_digraphs = ['th', 'he', 'in', 'er', 'an']  # Define common digraphs
user_id = None
backspace_count = 0  # To track errors

# Function to calculate dwell and flight times
def record_keystroke(key, current_time):
    global typing_data, key_press_time, backspace_count
    
    # Detect backspace for error rate
    if key == "Backspace":
        backspace_count += 1
    
    # Capture dwell time (time a key is held down)
    if key in key_press_time:
        dwell_time = current_time - key_press_time[key]
    else:
        dwell_time = 0.0
    
    # Capture flight time (time between keystrokes)
    if len(typing_data) > 0:
        last_time = typing_data['timestamp'].iloc[-1]
        flight_time = current_time - last_time
    else:
        flight_time = 0.0
    
    # Update data
    new_data = pd.DataFrame({
        'timestamp': [current_time],
        'key': [key],
        'dwell_time': [dwell_time],
        'flight_time': [flight_time]
    })

    typing_data = pd.concat([typing_data, new_data], ignore_index=True)
    
    # Update key press time
    key_press_time[key] = current_time

# Function to calculate common digraph timing
def calculate_common_digraph_time():
    digraph_times = []
    for i in range(1, len(typing_data)):
        pair = typing_data['key'].iloc[i-1] + typing_data['key'].iloc[i]
        if pair in common_digraphs:
            digraph_times.append(typing_data['flight_time'].iloc[i])
    if len(digraph_times) > 0:
        return np.mean(digraph_times)
    return 0.0

# Streamlit UI
st.title('Keystroke Dynamics Data Collection Tool')

# User ID input
user_id = st.text_input("Enter User ID", "User_1")

# Text input field
user_input = st.text_area('Type in the text box to collect data:', height=200)

# Record keystrokes
for char in user_input:
    record_keystroke(char, time.time())

# Real-time data visualization
if not typing_data.empty:
    st.subheader('Real-time Typing Data')

    # Plot dwell times
    fig1 = plt.figure()
    plt.plot(typing_data['timestamp'], typing_data['dwell_time'], label='Dwell Time')
    plt.xlabel('Time')
    plt.ylabel('Dwell Time (seconds)')
    plt.legend()
    st.pyplot(fig1)

    # Plot flight times
    fig2 = plt.figure()
    plt.plot(typing_data['timestamp'], typing_data['flight_time'], label='Flight Time')
    plt.xlabel('Time')
    plt.ylabel('Flight Time (seconds)')
    plt.legend()
    st.pyplot(fig2)

# Typing speed
if not typing_data.empty:
    st.subheader('Typing Speed')
    typing_speed = len(user_input) / (typing_data['timestamp'].iloc[-1] - typing_data['timestamp'].iloc[0]) * 60
    st.write(f"Typing Speed: {typing_speed:.2f} characters per minute")

# Error rate (based on backspaces)
error_rate = (backspace_count / len(user_input)) * 100 if len(user_input) > 0 else 0
st.write(f"Error Rate: {error_rate:.2f}%")

# Common digraph timing
common_digraph_time = calculate_common_digraph_time()
st.write(f"Common Digraph Time: {common_digraph_time:.4f} seconds")

# Updated model loading section
st.subheader("Upload Trained Model (.h5, .keras, or SavedModel) to Predict User")
uploaded_file = st.file_uploader("Choose a model file", type=["h5", "keras"])
uploaded_folder = st.text_input("Or enter the path to a SavedModel folder")

model = None

if uploaded_file is not None:
    # Save uploaded model to a temporary file to load
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_filepath = temp_file.name

    try:
        # Load the model based on file extension
        if temp_filepath.endswith('.h5'):
            model = load_model(temp_filepath, compile=False)
            st.success("Model successfully loaded (H5 format)!")
        elif temp_filepath.endswith('.keras'):
            model = load_model(temp_filepath)
            st.success("Model successfully loaded (.keras format)!")
        else:
            st.error("Unsupported file format. Please upload a .h5 or .keras file.")
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(temp_filepath)

elif uploaded_folder:
    try:
        # Load SavedModel as a TFSMLayer
        model = keras.layers.TFSMLayer(uploaded_folder, call_endpoint='serving_default')
        st.success("SavedModel successfully loaded as TFSMLayer!")
    except Exception as e:
        st.error(f"Failed to load SavedModel: {str(e)}")

# Run prediction if model is loaded
if model is not None and not typing_data.empty:
    # Extract feature vector from collected data
    avg_dwell_time = typing_data['dwell_time'].mean()
    avg_flight_time = typing_data['flight_time'].mean()

    # Construct input feature vector
    input_vector = np.array([[avg_dwell_time, avg_flight_time, typing_speed, error_rate]])
    
    # Get the input shape expected by the model
    if isinstance(model, keras.layers.TFSMLayer):
        input_shape = model.input_shape[1:]  # Exclude batch dimension
    else:
        input_shape = model.input_shape[1:]  # Exclude batch dimension

    # Reshape input to match the model's expected input shape
    if len(input_shape) == 2:  # If the model expects 3D input (samples, time steps, features)
        input_vector = input_vector.reshape((1, 1, input_vector.shape[1]))
    elif len(input_shape) == 1:  # If the model expects 2D input (samples, features)
        input_vector = input_vector.reshape((1, input_vector.shape[1]))

    # Predict user
    try:
        if isinstance(model, keras.layers.TFSMLayer):
            prediction = model(input_vector)
        else:
            prediction = model.predict(input_vector)
        
        predicted_user = np.argmax(prediction)
        st.write(f"Predicted User ID: {predicted_user}")
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        st.write(f"Input shape: {input_vector.shape}")
        st.write(f"Expected input shape: {input_shape}")

# Option to save data to CSV
if st.button("Save Collected Data"):
    output_data = pd.DataFrame({
        'user_id': [user_id] * len(typing_data),
        'avg_dwell_time': [typing_data['dwell_time'].mean()],
        'avg_flight_time': [typing_data['flight_time'].mean()],
        'typing_speed': [typing_speed],
        'error_rate': [error_rate],
        'common_digraph_time': [common_digraph_time]
    })
    
    # Save the data to CSV
    output_data.to_csv('real_typing_data.csv', index=False)
    st.success("Data saved to real_typing_data.csv")
