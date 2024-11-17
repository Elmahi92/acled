import configparser
import requests
import pandas as pd
from datetime import datetime

def fetch_acled_data():
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('config.txt')
    
    # Extract necessary parameters from config
    email = config['API']['email']
    api_key = config['API']['api_key']
    country = config['API']['country']
    start_date = config['API']['start_date']
    
    # Get the current date in 'yyyy-mm-dd' format for the end_date
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Create the event_date string using the pipe separator
    event_date = f"{start_date}|{end_date}"
    
    all_data = []  # To store data from all API requests
    limit = 20000  # Number of records per request
    offset = 0  # Used to paginate
    base_url = "https://api.acleddata.com/acled/read"
    
    # Define the parameters
    params = {
        'key': api_key,
        'email': email,
        'country': country,
        'event_date': event_date,  # Use pipe separator in event_date
        'event_date_where': 'BETWEEN',
        'limit': limit,
        'offset': offset
    }

    # Send the GET request
    response = requests.get(base_url, params=params)
    
    # Raise exception if the request fails
    response.raise_for_status()
    
    # Parse the response JSON
    response_json = response.json()
    data = response_json['data']
    
    # Extend all_data with the fetched data
    all_data.extend(data)
    
    # Return the data as a DataFrame
    return pd.DataFrame(all_data)

# Example of calling the function
df = fetch_acled_data()
print(df)
