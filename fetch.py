import requests
import datetime
import os
import json
import pandas as pd

def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return "HTTP Error extracting data"        
    except Exception as e:
        return e
    
def write_data_to_json(data, file):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d")
    directory = os.path.dirname(file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        with open(f"{file}_{time_now}.json", "w") as f:
            json.dump(data, f)
        return "File written successfully"
    except Exception as e:
        return e

def create_df(json):
    try:
        df = pd.DataFrame(json)
        columns = ["id", "name", "brewery_type", "city", "state", "postal_code", "country", "phone", "website_url"]
        existing_cols = [col for col in columns if col in df.columns]
        rel_df = df[existing_cols]
        return rel_df
    except Exception as e:
        return e

def from_api_to_df(url, file):
    response = fetch_data(url)
    save_file = write_data_to_json(response, file)
    df = create_df(response)

url = f"https://api.openbrewerydb.org/v1/breweries"
file = "raw_data/breweries"
from_api_to_df(url, file)