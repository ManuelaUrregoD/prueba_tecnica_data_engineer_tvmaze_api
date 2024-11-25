# PRUEBA TÉCNICA DATA INGINEER - TV MAZE API
Prueba técnica para Data Engineer que consiste en diseñar y desarrollar una ETL que obtiene, transforma y carga datos de programas de televisión emitidos en enero de 2024 desde la API de TVMaze. Utilizando requests para la extracción, json y pandas para transformar y analizar los datos, y SQLite para su almacenamiento en un modelo optimizado, la ETL pasa por todas las etapas: recopilación de datos crudos, limpieza y perfilado, transformación en DataFrames estructurados, exportación en formato Parquet con compresión snappy, y carga en una base de datos para su posterior análisis y generación de resultados como el tiempo promedio de emisión, conteo de programas por género y dominios únicos de sitios oficiales.


## Descripción del Proyecto

Este proyecto se ejecuta a través de un entorno virtual que asegura un entorno aislado y controlado para manejar las dependencias necesarias. tiene como objetivo obtener datos de programas de televisión a través de la API de TVMaze, realizar un procesamiento de estos datos, y almacenarlos para análisis posterior. Los datos se recopilan, limpian y transforman, para luego ser almacenados en una base de datos SQLite y exportados a archivos en formato Parquet. Además, se genera un informe de perfilado de datos para conocer mejor la estructura y calidad de los mismos.

## Tecnologías Utilizadas

- **Lenguaje**: Python
- **Bibliotecas**: `requests`, `json`, `pandas`, `sqlite3`, `ydata_profiling`, `termcolor`, `pytest`, `coverage`, `pytest-cov`
- **Base de Datos**: SQLite
- **Formatos de Almacenamiento**: JSON, Parquet
- **Pruebas**: Pruebas unitarias con pytest, coverage, y pytest-cov 


## Estructura del Proyecto

El proyecto tiene la siguiente estructura de directorios:

- `data/`: Archivos en formato Parquet generados a partir de los datos limpiados.
- `db/`: Archivo de la base de datos SQLite generada.
- `json/`: Archivos JSON obtenidos de las consultas a la API de TVMaze.
- `model/`: Imagen del modelo de datos creado para almacenar la información.
- `profiling/`: Archivos del informe de perfilado de datos en formato HTML.
- `src/`: Scripts de Python desarrollados para el proyecto.
- `src/tests/`: Archivos de pruebas unitarias desarrolladas para validar el código.
- requirements.txt: Archivo que contiene las dependencias y librerías necesarias para el proyecto en un entorno virtualizado. 


## Instalación y Ejecución

Siga los siguientes pasos para instalar y ejecutar el proyecto:

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/ManuelaUrregoD/prueba_tecnica_data_engineer_tvmaze_api.git
    ```

2. Navegar hasta la carpeta del proyecto:

    ```bash
    cd prueba_tecnica_data_engineer_tvmaze_api
    ```

3. Crear un entorno virtual:

    ```bash
    python3 -m venv venv
    ```

4. Activar el entorno virtual:

    - **Windows**:

      ```bash
      venv\Scripts\activate
      ```

    - **Mac/Linux**:

      ```bash
      source venv/bin/activate
      ```

5. Instalar las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

6. Navegar hasta la carpeta `src`:

    ```bash
    cd src
    ```

7. Ejecutar el script principal:

    ```bash
    python tv_shows.py
    ```

8. **Resultados de la ejecución**: 
   Los datos obtenidos de la API serán procesados y almacenados en las carpetas correspondientes (`json/`, `data/`, `db/`).


## Descripción del Código

El código principal se encuentra en el archivo `tv_shows.py` dentro de la carpeta `src`. El flujo de trabajo del script incluye los siguientes pasos:

1. **Obtención de Datos**: Los datos de los programas de televisión se obtienen de la API de TVMaze para las fechas especificadas (enero 2024). Estos datos se almacenan en archivos JSON dentro de la carpeta `json/`.

2. **Carga de Datos en un DataFrame**: Los archivos JSON se cargan en un DataFrame de `pandas` para facilitar su manipulación y análisis.

3. **Perfilado de Datos**: Se genera un informe de perfilado de datos en formato HTML que se guarda en la carpeta `profiling/` para proporcionar una visión general de la calidad y estructura de los datos.

4. **Limpieza de Datos**: El script limpia los datos realizando acciones como:
    - Eliminación de columnas irrelevantes o con muchos valores faltantes.
    - Eliminación de valores atípicos y duplicados.
    - Transformación de columnas categóricas y manejo de valores faltantes.
    - Conversión de datos categóricos a valores numéricos.

5. **Almacenamiento en Formato Parquet**: Los datos limpiados se guardan en la carpeta `data/` en formato Parquet para un acceso rápido y eficiente.

6. **Inserción en la Base de Datos SQLite**: Los datos se insertan en una base de datos SQLite con varias tablas, y el archivo de la base de datos se guarda en la carpeta `db/`.

7. **Consultas en la Base de Datos SQLite**: Se realizan consultas sobre la base de datos para extraer información relevante. 

## Análisis del Perfilado de Datos

Se realizó un perfilado de datos utilizando la librería `ydata_profiling` para entender mejor la calidad y estructura de los datos obtenidos. El informe generado incluye estadísticas descriptivas, distribuciones de datos y correlaciones entre columnas. El archivo con el informe está disponible en la carpeta `profiling/` como `data_profiling.html`.

## Consultas en la base de Datos

Se realizan tres consultas a la base de datos SQLite

- Promedio del Runtime: Calcula el runtime promedio de todos los shows emitidos en enero de 2024.
- Conteo de Shows por Género: Cuenta la cantidad de shows agrupados por género para los shows emitidos en enero de 2024.
- Dominios Únicos del Sitio Oficial: Obtiene una lista de dominios únicos de los sitios oficiales de los shows emitidos en enero de 2024.

## Modelo de Datos

El modelo de datos fue diseñado para almacenar la información de los programas de televisión y sus episodios, así como de las redes de emisión y canales web asociados. La estructura incluye las siguientes tablas:

- **country**: Almacena información sobre los países, incluyendo código, nombre y zona horaria. 
- **genres**: Contiene la lista de los diferentes géneros de los programas de televisión.
- **networks**: Almacena la información de las redes de televisión, como nombre, sitio oficial y el país asociado.
- **WebChannels**: Almacena la información de los canales web, como nombre, sitio oficial y el país asociado.
- **shows**: Contiene información general de los programas de televisión, como nombre, idioma, estatus, fecha de estreno, entre otros datos. Además, se relaciona con los canales web y redes de televisión.
- **episodes**: Almacena la información de los episodios de cada programa, incluyendo nombre, temporada, fecha y hora de emisión, duración, entre otros detalles.
- **showGenre**: Relaciona los programas de televisión con sus géneros correspondientes.

Una imagen del modelo de datos se encuentra en la carpeta `model/`.

## Pruebas unitarias

Se han desarrollado pruebas unitarias para validar el correcto funcionamiento del código, ubicadas en la carpeta `src/tests` Estas pruebas incluyen:

- Prueba de get_series_data: Valida que la función pueda obtener y procesar correctamente la respuesta de la API.
- Prueba de fetch_tv_shows_data: Valida la extracción de datos de varias fechas y asegura la integridad de los datos obtenidos.
- Prueba de load_json_to_pandas_dataframe: Valida la carga de archivos JSON en un DataFrame de pandas.
- Prueba de clean_data: Valida el proceso de limpieza de datos, incluyendo la eliminación de columnas irrelevantes y la transformación de valores categóricos.

## Ejecución pruebas unitarias

Para ejecutar las pruebas unitarias, siga los siguientes pasos:

1. Navegar a la carpeta principal del proyecto:

    ```bash
    cd prueba_tecnica_data_engineer_tvmaze_api
    ```

2. Ejecutar las pruebas:

    ```bash
    pytest src/tests/
    ```

3. Generar un reporte de cobertura de pruebas:

    ```bash
    pytest --cov=src src/tests/
    ```


## Contacto

Para cualquier consulta o duda sobre este proyecto, puedes contactarme a través de GitHub: [ManuelaUrregoD](https://github.com/ManuelaUrregoD).
