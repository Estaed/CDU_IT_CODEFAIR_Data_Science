# example_open_meteo_uluru.py
# This script fetches historical weather data for Uluru from Open-Meteo API
# and saves it to a CSV file. It retrieves hourly data for temperature,
# cloud cover, and precipitation over a specified date range.

import requests
import pandas as pd
import json  # For parsing if needed, but requests handles JSON

# Uluru coordinates
latitude = -25.3444
longitude = 131.0369

# Date range (adjust as needed; Open-Meteo supports from 1940 onwards)
start_date = '2015-01-01'
end_date = '2024-12-31'  # Up to end of 2024; current date is 2025-09-22

# API endpoint
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}&"
    f"start_date={start_date}&end_date={end_date}&"
    f"hourly=temperature_2m,cloud_cover,precipitation"
)

# Make the API request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract hourly data
    hourly = data['hourly']
    
    # Create a DataFrame
    df = pd.DataFrame({
        'time': hourly['time'],
        'temperature_2m': hourly['temperature_2m'],
        'cloud_cover': hourly['cloud_cover'],
        'precipitation': hourly['precipitation']
    })
    
    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    # Save to CSV
    output_file = 'uluru_weather_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    
    # Optional: Print first few rows
    print(df.head())
else:
    print(f"Error: {response.status_code} - {response.text}")