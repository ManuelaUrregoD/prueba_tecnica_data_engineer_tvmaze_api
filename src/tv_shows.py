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


def profile_data(df):
    print("\n [+] Exportando profiling en formato HTML...")
    profile = ProfileReport(df, title="Profiling a datos del 1 de enero del 2024")
    profile.to_file("../profiling/data_profiling.html")


def clean_data(df):
    
    #1. Eliminar columnas con más del 85% de valores faltantes y columnas con datos no soportados e irrelevantes. 
    columns_to_drop = [
        'rating.average', '_embedded.show.network', '_embedded.show.dvdCountry', '_embedded.show.externals.tvrage', 
        'image', '_embedded.show.image', '_embedded.show.network.officialSite', '_embedded.show.webChannel', 
        '_embedded.show.webChannel.country', '_embedded.show.dvdCountry.name', '_embedded.show.dvdCountry.code', 
        '_embedded.show.dvdCountry.timezone', '_embedded.show.image', '_embedded.show.network', 'image', '_embedded.show.runtime', 
        '_embedded.show.schedule.time', '_embedded.show.schedule.days','_embedded.show.rating.average', '_embedded.show.weight', 
        '_embedded.show.externals.thetvdb', '_embedded.show.externals.imdb','_embedded.show.summary', '_embedded.show.updated',
        '_links.self.href', '_links.show.href', '_links.show.name','_embedded.show._links.self.href', '_embedded.show._links.previousepisode.href',
        '_embedded.show._links.previousepisode.name', '_embedded.show._links.nextepisode.href', '_embedded.show._links.nextepisode.name', 
        'summary', 'image.medium', 'Image.original', '_embedded.show.network.country.timezone', '-embedded.show.webChannel.country.timezone'
        ]
    
    df_clean = df.drop(columns=columns_to_drop, errors='ignore')
    
    
    # 2. Eliminación de valores atípicos 
    df_clean = df_clean[df_clean['season'] != 2024]


    # 3. Transformar columnas con datos no compatibles
    columns_to_transform = ['_embedded.show.genres', '_embedded.show.dvdPaís', '_embedded.show.schedule.days']
    for column in columns_to_transform:
        if column in df_clean.columns:
            df_clean[column] = df_clean[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
            
    # 4. Eliminar filas con más del 80% de valores faltantes
    df_clean = df_clean.dropna(thresh=len(df_clean.columns) * 0.8)
    

    # 5. Rellenar valores faltantes relevantes
    columns_to_fill_median = ['runtime', 'rating.average', '_embedded.show.averageRuntime']
    for column in columns_to_fill_median:
        if column in df_clean.columns:
            df_clean[column] = df_clean[column].fillna(df_clean[column].median())
    
    
    # 6. Eliminar duplicados
    df_clean = df_clean.drop_duplicates()
    
    # 7. Transformar columnas categóricas altamente desequilibradas
    if 'type' in df_clean.columns:
        type_counts = df_clean['type'].value_counts()
        df_clean['type'] = df_clean['type'].apply(lambda x: x if type_counts[x] > 10 else 'Other')
    
    # 8. Convertir columnas categóricas a valores numéricos
    categorical_columns = ['_embedded.show.language', '_embedded.show.type']
    for column in categorical_columns:
        if column in df_clean.columns:
            df_clean = pd.get_dummies(df_clean, columns=[column])

    # 9. Eliminar columnas altamente correlacionadas
    columns_to_drop_correlated = ['_embedded.show.network.country.name', '_embedded.show.network.country.code']
    df_clean = df_clean.drop(columns=columns_to_drop_correlated, errors='ignore')

    return df_clean