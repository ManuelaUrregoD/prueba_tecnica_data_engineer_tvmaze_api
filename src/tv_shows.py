import requests
import json
from datetime import datetime, timedelta
from ydata_profiling import ProfileReport
from termcolor import colored
import pandas as pd
import sqlite3
import os


def get_series_data(date):
    URL = f"http://api.tvmaze.com/schedule/web?date={date}"
    
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(colored(f"\n [!] Error al obtener los datos de la fecha {date}: {e}", "red"))
        return []


def fetch_tv_shows_data(start_date, end_date):
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

        print(colored(f"\n [+] Escribiendo datos de la API... data_{date}.json", "green"))
    
    return all_data


def load_json_to_pandas_dataframe(json_folder="../json/"):
    all_files = [os.path.join(json_folder, file) for file in os.listdir(json_folder) if file.endswith(".json")]
    all_data = []
    for file in all_files:
        with open(file, 'r') as f:
            data = json.load(f)
            all_data.extend(data)
    
    df = pd.json_normalize(all_data)
    print(colored(f"\n [+] Generando Data Frame Pandas...", "green"))

    return df


def profile_data(df):
    print(colored(f"\n [+] Exportando profiling en formato HTML...", "green"))
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

    print(colored(f"\n [+] Se limpiaron con exito los datos...", "green"))    
    return df_clean


def save_dataframe_to_parquet(df, file_path="../data/shows.parquet"):
    df.to_parquet(file_path, compression='snappy')
    

def insert_data_to_db(df_clean, db_name):
    
    # Obtener la ruta del archivo de la base de datos desde un directorio atrás
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", db_name))

    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insertar datos en la tabla Shows
    for _, row in df_clean.iterrows():
        try:
            # Insertar datos en Shows
            cursor.execute('''
                INSERT OR IGNORE INTO Shows (
                    id, url, name, genres, status, runtime, averageRuntime, premiered, ended, 
                    officialSite, language, type, webChannel_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row.get('_embedded.show.id'), row.get('_embedded.show.url'), row.get('_embedded.show.name'),
                row.get('_embedded.show.genres'), row.get('_embedded.show.status'), 
                row.get('_embedded.show.runtime'), row.get('_embedded.show.averageRuntime'), 
                row.get('_embedded.show.premiered'), row.get('_embedded.show.ended'),
                row.get('_embedded.show.officialSite'), row.get('_embedded.show.language'), 
                row.get('_embedded.show.type'), row.get('_embedded.show.webChannel.id')
            ))
            
            # Insertar datos en Episodes
            cursor.execute('''
                INSERT OR IGNORE INTO Episodes (
                    id, show_id, url, name, season, number, type, airdate, airtime, 
                    airstamp, runtime
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row.get('id'), row.get('_embedded.show.id'), row.get('url'), row.get('name'),
                row.get('season'), row.get('number'), row.get('type'), row.get('airdate'),
                row.get('airtime'), row.get('airstamp'), row.get('runtime')
            ))

            # Insertar datos en Networks
            cursor.execute('''
                INSERT OR IGNORE INTO Networks (
                    id, name, country_name, country_code
                ) VALUES (?, ?, ?, ?)
            ''', (
                row.get('_embedded.show.network.id'), row.get('_embedded.show.network.name'),
                row.get('_embedded.show.network.country.name'), row.get('_embedded.show.network.country.code')
            ))
            
            # Insertar datos en WebChannels
            cursor.execute('''
                INSERT OR IGNORE INTO WebChannels (
                    id, network_id, name, country_name, country_code, officialSite
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row.get('_embedded.show.webChannel.id'), row.get('_embedded.show.network.id'),
                row.get('_embedded.show.webChannel.name'), row.get('_embedded.show.webChannel.country.name'),
                row.get('_embedded.show.webChannel.country.code'), row.get('_embedded.show.webChannel.officialSite')
            ))

        except sqlite3.Error as e:
            print(colored(f"\n [!] Error al insertar los datos: {e}", "red"))
    print(colored(f"\n [+] Se insertan con exito los datos...", "green"))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
    all_data = fetch_tv_shows_data(datetime(2024, 1, 1), datetime(2024, 1, 31))
    df = load_json_to_pandas_dataframe()
    profile_data(df)
    df_clean = clean_data(df)
    save_dataframe_to_parquet(df_clean)
    insert_data_to_db(df_clean, "tv_shows.db")
