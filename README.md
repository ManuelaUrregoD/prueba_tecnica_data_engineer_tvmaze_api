# prueba_tecnica_data_engineer_tvmaze_api
Prueba técnica para Data Engineer que obtiene y procesa datos de TV shows de enero de 2024 desde la API de TVMaze, utilizando `requests`, `json`, `pandas` y `SQLite` para análisis y muestra de resultados.

## Descripción del Proyecto

Este proyecto tiene como objetivo obtener datos de programas de televisión a través de la API de TVMaze, realizar un procesamiento de estos datos, y almacenarlos para análisis posterior. Los datos se recopilan, limpian y transforman, para luego ser almacenados en una base de datos SQLite y exportados a archivos en formato Parquet. Además, se genera un informe de perfilado de datos para conocer mejor la estructura y calidad de los mismos.

## Tecnologías Utilizadas

- **Lenguaje**: Python
- **Bibliotecas**: `requests`, `json`, `pandas`, `sqlite3`, `ydata_profiling`, `termcolor`
- **Base de Datos**: SQLite
- **Formatos de Almacenamiento**: JSON, Parquet

## Estructura del Proyecto

El proyecto tiene la siguiente estructura de directorios:

- `data/`: Archivos en formato Parquet generados a partir de los datos limpiados.
- `db/`: Archivo de la base de datos SQLite generada.
- `json/`: Archivos JSON obtenidos de las consultas a la API de TVMaze.
- `model/`: Imagen del modelo de datos creado para almacenar la información.
- `profiling/`: Archivos del informe de perfilado de datos en formato HTML.
- `src/`: Scripts de Python desarrollados para el proyecto.
- `venv/`: Entorno virtual de Python.

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


## Análisis del Perfilado de Datos

Se realizó un perfilado de datos utilizando la librería `ydata_profiling` para entender mejor la calidad y estructura de los datos obtenidos. El informe generado incluye estadísticas descriptivas, distribuciones de datos y correlaciones entre columnas. El archivo con el informe está disponible en la carpeta `profiling/` como `data_profiling.html`.


## Modelo de Datos

El modelo de datos fue diseñado para almacenar la información de los programas de televisión y sus episodios, así como de las redes de emisión y canales web asociados. La estructura incluye las siguientes tablas:

- **Shows**: Información general de los shows.
- **Episodes**: Información de los episodios de cada show.
- **Networks**: Información de las redes de televisión.
- **WebChannels**: Información de los canales web.

Una imagen del modelo de datos se encuentra en la carpeta `model/`.


## Contacto

Para cualquier consulta o duda sobre este proyecto, puedes contactarme a través de GitHub: [ManuelaUrregoD](https://github.com/ManuelaUrregoD).
