import requests
import json
from datetime import datetime, timedelta
from ydata_profiling import ProfileReport
from termcolor import colored
import pandas as pd
import sqlite3
import os


def get_series_data(date):
    url = f"http://api.tvmaze.com/schedule/web?date={date}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n [!] Error al obtener los datos de la fecha {date}: {e}")
        return []


def fetch_tv_shows_data():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    print(colored(f"\n [+] Obteniendo los datos de la API... Para las fechas {start_date} hasta {end_date}", "green"))
    all_data = [
        series
        for i in range((end_date - start_date).days + 1)
        for series in get_series_data((start_date + timedelta(days=i)).strftime('%Y-%m-%d'))
    ]

    for i in range((end_date - start_date).days + 1):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        daily_data = get_series_data(date)
        with open(f"../json/data_{date}.json", "w") as file:
            json.dump(daily_data, file, indent=4)
        print(f"\n [+] Escribiendo datos de la API... data_{date}.json")
    
    return all_data


def load_json_to_pandas_dataframe(json_folder="../json/"):
    all_files = [os.path.join(json_folder, file) for file in os.listdir(json_folder) if file.endswith(".json")]
    all_data = []
    for file in all_files:
        with open(file, 'r') as f:
            data = json.load(f)
            all_data.extend(data)
    
    df = pd.json_normalize(all_data)
    print(f"\n [+] Generando Data Frame Pandas...")
    return df
    