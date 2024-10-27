import psycopg2
from psycopg2 import OperationalError, errorcodes, errors

def conectar_bbdd(nombre_bbdd):
    """
    Establece una conexión a una base de datos PostgreSQL.

    Esta función utiliza la librería `psycopg2` para conectarse a una base de datos
    PostgreSQL en un host local, utilizando el nombre de usuario y la contraseña especificados
    en el código. La función asume que el servidor de la base de datos está en el mismo equipo
    (localhost) y que las credenciales de acceso son correctas.

    Parámetros:
    ----------
    nombre_bbdd : str
        Nombre de la base de datos a la que se desea conectar.

    Retorna:
    -------
    connection : psycopg2.extensions.connection
        Objeto de conexión a la base de datos PostgreSQL.
    """
    connection = psycopg2.connect(
        host="localhost",
        database=nombre_bbdd,
        user="postgres",
        password="admin"
    )
    return connection

def crear_tablas(cursor):
    """
    Crea las tablas necesarias en la base de datos para almacenar información de supermercados,
    categorías, productos y precios históricos. Esta función utiliza SQL para crear las tablas si
    no existen, definiendo las relaciones necesarias mediante claves foráneas.

    Parámetros:
    ----------
    cursor : psycopg2.extensions.cursor
        Un cursor de la conexión a la base de datos PostgreSQL que permite ejecutar
        consultas SQL.

    Tablas Creadas:
    --------------
    1. Supermercados:
       - id_supermercado : SERIAL PRIMARY KEY
       - nombre_supermercado : VARCHAR(100), único y no nulo

       Contiene los nombres de los supermercados. La clave primaria es `id_supermercado`.

    2. Categorias:
       - id_categoria : SERIAL PRIMARY KEY
       - nombre_categoria : VARCHAR(100), único y no nulo

       Almacena las categorías de productos, identificadas por `id_categoria`.

    3. Productos:
       - id_producto : SERIAL PRIMARY KEY
       - nombre_producto : VARCHAR(200), único y no nulo

       Almacena los nombres de productos. La clave primaria es `id_producto`.

    4. PreciosHistoricos:
       - id_registro : SERIAL PRIMARY KEY
       - id_supermercado : INT, clave foránea que referencia `Supermercados(id_supermercado)`
       - id_categoria : INT, clave foránea que referencia `Categorias(id_categoria)`
       - id_producto : INT, clave foránea que referencia `Productos(id_producto)`
       - fecha : DATE, no nulo
       - precio : NUMERIC(10, 2), no nulo
       - variacion : VARCHAR(100), opcional

       Guarda los registros históricos de precios, asociando productos, categorías, y supermercados
       con una fecha y un precio específico. Incluye claves foráneas para asegurar la integridad referencial,
       con opciones de `ON DELETE CASCADE` y `ON UPDATE CASCADE` para actualizaciones y eliminaciones en cascada.
    """

    query_tabla_supermercados = """
    CREATE TABLE IF NOT EXISTS Supermercados (
        id_supermercado SERIAL PRIMARY KEY,
        nombre_supermercado VARCHAR(100) UNIQUE NOT NULL
    )
    """
    cursor.execute(query_tabla_supermercados)

    query_tabla_categorias = """
    CREATE TABLE IF NOT EXISTS Categorias (
        id_categoria SERIAL PRIMARY KEY,
        nombre_categoria VARCHAR(100) UNIQUE NOT NULL
    )
    """
    cursor.execute(query_tabla_categorias)

    query_tabla_productos = """
    CREATE TABLE IF NOT EXISTS Productos (
        id_producto SERIAL PRIMARY KEY,
        nombre_producto VARCHAR(200) UNIQUE NOT NULL
    )
    """
    cursor.execute(query_tabla_productos)

    query_tabla_registro_historico = """
    CREATE TABLE IF NOT EXISTS PreciosHistoricos (
        id_registro SERIAL PRIMARY KEY,
        id_supermercado INT NOT NULL,
        id_categoria INT NOT NULL,
        id_producto INT NOT NULL,
        fecha DATE NOT NULL,
        precio NUMERIC(10, 2) NOT NULL,
        variacion VARCHAR(100),
        FOREIGN KEY (id_supermercado)
            REFERENCES Supermercados(id_supermercado)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (id_categoria)
            REFERENCES Categorias(id_categoria)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (id_producto)
            REFERENCES Productos(id_producto)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
    """
    cursor.execute(query_tabla_registro_historico)
        

def insertar_datos(cursor, df, nombre_tabla):
    """
    Inserta registros en la base de datos en función de los datos proporcionados en el DataFrame y la tabla de destino.

    Parámetros:
    ----------
    cursor : psycopg2.extensions.cursor
        Cursor activo de la conexión a la base de datos PostgreSQL que permite ejecutar
        consultas SQL.

    df : pandas.DataFrame
        DataFrame que contiene los datos a insertar en la tabla. Las columnas deben
        coincidir con los campos necesarios para la tabla especificada.

    nombre_tabla : str
        Nombre de la tabla donde se insertarán los datos. Este parámetro determina
        qué tipo de datos se esperan en el DataFrame y cómo se insertarán en la base de datos.
        Valores válidos: 'supermercados', 'categorias', 'productos', 'precios_historicos'.

    Funcionalidad:
    --------------
    Dependiendo del valor de `nombre_tabla`, la función ejecutará una consulta `INSERT INTO` en la
    tabla correspondiente:
    
    - 'supermercados': Inserta nombres de supermercados en la tabla `Supermercados`.
    - 'categorias': Inserta nombres de categorías en la tabla `Categorias`.
    - 'productos': Inserta nombres de productos en la tabla `Productos`.
    - 'precios_historicos': Inserta registros detallados de precios históricos en la tabla `PreciosHistoricos`.
      Aquí se espera que el DataFrame incluya `id_producto`, `id_supermercado`, `id_categoria`, `fecha`, `precio`, 
      y `variacion`.

    Notas:
    ------
    - La función asume que los valores en el DataFrame están en el orden y formato correctos para cada
      tipo de tabla.
    - Las columnas en el DataFrame deben tener nombres específicos para cada tabla:
        - 'supermercados': columna 'supermercado'
        - 'categorias': columna 'categoria'
        - 'productos': columna 'producto'
        - 'precios_historicos': columnas 'id_producto', 'id_supermercado', 'id_categoria', 'fecha', 'precio', 'variacion'
    """
    for index, row in df.iterrows():
        if nombre_tabla == 'supermercados':
            cursor.execute("""INSERT INTO Supermercados (nombre_supermercado)
                           VALUES (%s)""",
                           (row['supermercado'],))
        elif nombre_tabla == 'categorias':
            cursor.execute("""INSERT INTO Categorias (nombre_categoria)
                           VALUES (%s)""",
                           (row['categoria'],))
        elif nombre_tabla == 'productos':
            cursor.execute("""INSERT INTO Productos (nombre_producto)
                           VALUES (%s)""",
                           (row['producto'],))
        elif nombre_tabla == 'precios_historicos':
            cursor.execute("""
                INSERT INTO PreciosHistoricos (id_producto, id_supermercado, id_categoria, fecha, precio, variacion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (row['id_producto'], row['id_supermercado'], row['id_categoria'], row['fecha'], row['precio'], row['variacion']))
