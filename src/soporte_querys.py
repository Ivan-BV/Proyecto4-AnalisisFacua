
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import pandas as pd
from src.soporte_creacion_bbdd import conectar_bbdd

def extraer_datos(nomrbe_bbdd, query):
    """
    Extrae datos de una base de datos utilizando una consulta SQL.

    Esta función se conecta a la base de datos especificada, ejecuta la consulta
    proporcionada y devuelve los resultados obtenidos.

    Parámetros:
        nomrbe_bbdd (str): El nombre de la base de datos de la cual se quiere extraer información.
        query (str): La consulta SQL a ejecutar en la base de datos.

    Retorna:
        list: Una lista de tuplas, donde cada tupla representa una fila de resultados
               devueltos por la consulta SQL.

    Lanza:
        Exception: Si ocurre un error al conectarse a la base de datos o al ejecutar la consulta.
    """
    connection = conectar_bbdd(nomrbe_bbdd)
    cursor = connection.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()
    return resultados

# Función para hacer la media de productos agrupando por supermercado
def extraer_media(df: pd.DataFrame, columna_precio: str, nuevo_nombre=""):
    """
    Calcula la media de los precios agrupados por supermercado en un DataFrame.

    Esta función toma un DataFrame y calcula la media de los valores en la columna 
    especificada (columna_precio), agrupando por la columna "supermercado". 
    Opcionalmente, permite renombrar la columna de resultados.

    Parámetros:
        df (pd.DataFrame): El DataFrame que contiene los datos de precios y supermercados.
        columna_precio (str): El nombre de la columna que contiene los precios de los productos.
        nuevo_nombre (str, opcional): Un nuevo nombre para la columna de media. 
                                       Si se proporciona, la columna se renombrará. 
                                       Por defecto es una cadena vacía.

    Retorna:
        pd.DataFrame: Un nuevo DataFrame que contiene los supermercados y sus precios medios.
                       La columna de precios medios se redondea a dos decimales.
    """
    df_media = df.groupby("supermercado")[columna_precio].mean()
    df_media = df_media.reset_index()
    df_media[columna_precio] = df_media[columna_precio].astype(float).round(2)
    if nuevo_nombre != "":
        df_media.rename(columns={columna_precio: nuevo_nombre}, inplace=True)
    return df_media
