import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
import sys
import os

# Agregar el directorio 'src' al sys.path para poder importar tv_shows
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','src')))
from tv_shows import get_series_data, clean_data, fetch_tv_shows_data, load_json_to_pandas_dataframe

# Fixture para simular los datos crudos del api
data_mock = [
    {
        'id': 1,
        'name': 'Show A',
        'season': 2023,
        '_embedded': {
            'show': {
                'id': 1,
                'name': 'Show A',
                'runtime': 60,
                'averageRuntime': 60,
                'genres': ['Drama', 'Action'],
                'schedule': {'days': ['Monday']},
            }
        }
    }
]

@pytest.fixture
def sample_raw_data():
    """
    Fixture que proporciona datos crudos para las pruebas
    """
    return data_mock

@patch('tv_shows.requests.get')
def test_get_series_data(mock_get):
    """
    Prueba de get_series_data para validar la respuesta de la API.
    """
    mock_get.return_value.json.return_value = data_mock
    mock_get.return_value.raise_for_status = MagicMock()
    data = get_series_data('2024-01-05')
    assert data == data_mock

@patch('tv_shows.get_series_data')
def test_fetch_tv_shows_data(mock_get_series_data, sample_raw_data):
    """
    Prueba fetch_tv_shows_data para validar datos extraídos de varias fechas.
    """
    mock_get_series_data.return_value = sample_raw_data
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 2)
    all_data = [
        series
        for i in range((end_date - start_date).days + 1)
        for series in sample_raw_data
    ]
    assert len(all_data) == 2  # Se espera un dato por cada día. 
    assert all_data[0]['name'] == 'Show A'

@patch('tv_shows.os.listdir')
@patch('tv_shows.open', new_callable=MagicMock)
def test_load_json_to_pandas_dataframe(mock_open, mock_listdir, sample_raw_data):
    """
    Prueba load_json_to_pandas_dataframe para validar la carga de los archivos json.
    """
    mock_listdir.return_value = ['data_2024-01-01.json']
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(sample_raw_data)
    df = load_json_to_pandas_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0]['name'] == 'Show A'

def test_clean_data():
    """
    Prueba clean_data para validar el proceso de limpieza.
    """
    # Crear DataFrame de prueba
    df = pd.json_normalize(data_mock)
    df_clean = clean_data(df)

    # Validar que se eliminaron correctamente las columnas
    assert 'rating.average' not in df_clean.columns

    # Validar que se eliminaron los duplicados
    assert df_clean.duplicated().sum() == 0

    # Validar que los géneros se transformaron a una cadena de texto
    assert '_embedded.show.genres' in df_clean.columns
    assert isinstance(df_clean['_embedded.show.genres'].iloc[0], str)

    # Validar que no exista el valor 2024 en la columna 'season'
    assert 2024 not in df_clean['season'].values

    # Validar que los días de la semana se transformaron a números
    if '_embedded.show.schedule.days' in df_clean.columns:
        assert df_clean['_embedded.show.schedule.days'].iloc[0] == '1'

if __name__ == "__main__":
    pytest.main()
