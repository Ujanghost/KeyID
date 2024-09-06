import numpy as np
import pandas as pd

# Parameters for synthetic data generation
n_users = 10  # Number of users
n_samples_per_user = 500  # Number of typing samples per user

# Function to generate synthetic typing data for one user
def generate_typing_data(n_samples, user_id):
    # Generate random dwell times (in seconds)
    dwell_times = np.random.uniform(0.1, 0.5, size=n_samples)
    
    # Generate random flight times (in seconds)
    flight_times = np.random.uniform(0.05, 0.3, size=n_samples)
    
    # Generate random typing speeds (characters per minute)
    typing_speeds = np.random.uniform(100, 400, size=n_samples)
    
    # Generate random error rates (percentage)
    error_rates = np.random.uniform(0.01, 0.05, size=n_samples)
    
    # Generate random digraph timing (for common key pairs)
    common_digraph_times = np.random.uniform(0.08, 0.2, size=n_samples)
    
    # Create a DataFrame for the generated samples
    data = pd.DataFrame({
        'user_id': [user_id] * n_samples,
        'avg_dwell_time': dwell_times,
        'avg_flight_time': flight_times,
        'typing_speed': typing_speeds,
        'error_rate': error_rates,
        'common_digraph_time': common_digraph_times
    })
    
    return data

# Generate data for all users
all_data = pd.DataFrame()

for user_id in range(1, n_users + 1):
    user_data = generate_typing_data(n_samples_per_user, user_id)
    all_data = pd.concat([all_data, user_data], ignore_index=True)

# Shuffle the dataset (optional but recommended)
all_data = all_data.sample(frac=1).reset_index(drop=True)

# Save the dataset to a CSV file for future use
all_data.to_csv('synthetic_typing_data.csv', index=False)

# Print the first few rows of the synthetic data
print(all_data.head())
