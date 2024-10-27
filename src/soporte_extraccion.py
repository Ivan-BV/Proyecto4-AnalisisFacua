
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from tqdm import tqdm
import asyncio
import aiohttp

# Función para obtener las URLs de los supermercados
def obtener_lista_url(driver):
    """
    Extrae y devuelve un diccionario con nombres y URLs de una serie de elementos en una página web.

    La función utiliza el controlador de Selenium `driver` para navegar por una sección específica de la página,
    extrayendo el nombre y el enlace asociado de cada elemento en la sección. A medida que avanza por la página,
    toma el nombre visible del elemento y su URL, y los almacena en un diccionario.

    Args:
        driver (webdriver): Instancia del controlador Selenium WebDriver ya configurado para interactuar con la página.

    Returns:
        dict: Un diccionario donde las claves son los nombres de los elementos y los valores son las URLs correspondientes.
              Formato: {nombre: url, ...}

    Nota:
        La función avanza a través de una lista de elementos en la página, simulando una espera de 0.5 segundos entre 
        cada extracción para reducir la posibilidad de problemas de carga.
    """

    diccionario_url = {}
    
    # Como solo existen 6 supermercados dentro de Facua almacenamos todas las URLs con un bucle
    for pagina in tqdm(range(1, 7)):
        
        # Obtención y limpieza del nombre
        nombre_url = driver.find_element("css selector", f"body > section:nth-child(4) > div > div.row.gx-4.gx-lg-6.row-cols-2.row-cols-md-2.row-cols-xl-6.justify-content-center > div:nth-child({pagina}) > div > div.card-body.p-4 > div > p")
        nombre_url = nombre_url.text.replace("\n", "").replace(".", "").replace("Precios en ", "")

        # Obtención de la URL
        boton_acceder = driver.find_element("css selector", f"body > section:nth-child(4) > div > div.row.gx-4.gx-lg-6.row-cols-2.row-cols-md-2.row-cols-xl-6.justify-content-center > div:nth-child({pagina}) > div > div.card-footer.p-4.pt-0.border-top-0.bg-transparent > div > a")
        url = boton_acceder.get_attribute("href")

        # Almacenamiento del nombre y la URL obtenidas en el diccionario vacío
        diccionario_url[nombre_url] = url

    return diccionario_url

# Función para obtener las URLs de las categorías
def obtener_categorias(lista_url, driver):
    """
    Navega a través de una lista de URLs y extrae categorías y sus enlaces, almacenándolos en un diccionario.

    Para cada URL en `lista_url`, la función abre la página, espera a que los elementos carguen y extrae los nombres 
    y enlaces de hasta tres categorías. Cada categoría es almacenada en un diccionario, donde las claves son los 
    nombres de las categorías y los valores son sus URLs.

    Args:
        lista_url (list): Lista de URLs a visitar y extraer categorías.
        driver (webdriver): Instancia de Selenium WebDriver para controlar la navegación en la web.

    Returns:
        dict: Diccionario donde cada clave es el nombre de una categoría y cada valor es su URL.
              Formato: {nombre_categoria: url_categoria, ...}

    Nota:
        Utiliza `implicitly_wait` y `sleep` para manejar el tiempo de carga de los elementos, con una pausa de 
        0.5 segundos entre cada extracción.
    """

    diccionario_categorias = {}

    # Obtengo las categorias de la lista de URLs que hemos obtenido con la función obtener_lista_url
    for url in tqdm(lista_url):

        # Redirección a la url
        driver.get(url)
        
        # Pausa de 0.5 segundos para que le de tiempo a cargar la página correctamente
        sleep(0.5)

        # Bucle para obtener la nuevas URLs y poder seguir navegando hacia los historicos
        for n in range(1, 4):
                
                # Obtención y limpieza del nombre
                nombre_categoria = driver.find_element("css selector", f"body > section:nth-child(4) > div > div.row.gx-4.gx-lg-5.row-cols-2.row-cols-md-3.row-cols-xl-4.justify-content-center > div:nth-child({n}) > div > div.card-body.p-4 > div > p")
                nombre_categoria = nombre_categoria.text.replace("\n", "").replace(".", "")

                # Obtención de la URL
                boton_categoria = driver.find_element("css selector", f"body > section:nth-child(4) > div > div.row.gx-4.gx-lg-5.row-cols-2.row-cols-md-3.row-cols-xl-4.justify-content-center > div:nth-child({n}) > div > div.card-footer.p-4.pt-0.border-top-0.bg-transparent > div > a")
                url_categoria = boton_categoria.get_attribute("href")

                # Almacenamiento del nombre y la URL obtenidas en el diccionario vacío
                diccionario_categorias[nombre_categoria] = url_categoria

    return diccionario_categorias


#Función para obtener las URLs del historico de cada producto
def obtener_subcategorias(diccionario):
    """
    Obtiene las URLs del histórico de cada producto en diferentes categorías.

    La función recibe un diccionario de categorías y recorre cada una para extraer productos y sus enlaces de 
    historial desde la página web de cada categoría. Realiza una solicitud HTTP a cada URL de categoría, analiza el 
    contenido HTML para localizar los productos y guarda los enlaces al historial de cada producto en un diccionario 
    anidado que organiza los datos por súper categoría y categoría.

    Args:
        diccionario (dict): Diccionario de categorías, donde cada clave es el nombre de una súper 
                                       categoría y cada valor es un diccionario con nombres de categorías y sus URLs.
                                       Formato: {nombre_super: {nombre_categoria: url_categoria, ...}, ...}

    Returns:
        dict: Diccionario donde cada clave es el nombre de una súper categoría y cada valor es otro diccionario 
              de categorías con productos y sus URLs de historial.
              Formato: {nombre_super: {nombre_categoria: {producto: url_historial, ...}, ...}, ...}

    Nota:
        Utiliza `requests` para realizar solicitudes HTTP y `BeautifulSoup` para analizar el HTML de cada página.
        La función incluye pausas de 0.5 segundos entre cada extracción de producto para moderar la frecuencia 
        de acceso al servidor.
    """
    diccionario_subcategorias = {}

    # Bucle para iterar sobre cada supermercado
    for nombre_super, categorias in tqdm(diccionario.items()):
        subcategorias = {}

        # Bucle para iterar sobre cada categoria
        for nombre_categoria, url_categoria in categorias.items():
            res = requests.get(url_categoria)

            # Comprobación de la conexión correcta
            if res.status_code == 200:
                sopa = BeautifulSoup(res.content, "html.parser")
                
                # Busqueda de las tarjetas que contiene la información de todos los productos
                productos = sopa.find_all("div", {"class": "card h-100"})
                dicc_productos = {}

                # Bucle para iterar sobre todos los productos encontrados
                for producto in productos:

                    # Obtención del nombre
                    nombre = producto.find("p", {"class": "fw-bolder"}).getText().replace("\n", "").replace(".", "")
                    
                    # Obtención del enlace
                    enlace = producto.find_all("a")

                    # En caso que el texto de la etiqueta html de enlace sea "Historico"
                    # obtenemos el atributo href para almacenar la url obtenida a través de este.
                    if enlace[0].getText() == "Histórico":
                        url = enlace[0].get("href")
                        dicc_productos[nombre] = url
                        sleep(0.5)
                
                # Almacenamiento del nombre de cada supermercado, categoria, nombre del producto
                # y su respectiva URL para mantener su categorización
                subcategorias[nombre_categoria] = dicc_productos
        diccionario_subcategorias[nombre_super] = subcategorias
    return diccionario_subcategorias


"""
--- A partir de aquí comienzan las funciones asíncronas ---

Estas funcionas se llaman entre sí para generar asíncronía y control.

Funcionan de la siguiente manera:

    - Primero se hace la llamada a extraer_informacion. Dentro de esta función se llama a tarea_con_semaforo
    para poder limitar el número de tareas simultaneas que puede ejecutar al mismo tiempo.

    - Esta última función va llamando a obtener_tablas que es la que devuelve la información de las tablas en forma
    de dataframes.

    - Una vez han terminado todas las tareas generadas se concatenan en un solo data frame y este es el
    dataframe que se retorna.
"""
async def obtener_tablas(url, producto, categoria, supermercado):

    # Generamos una sesion asincrónica para no bloquear la ejecución de otras tareas
    async with aiohttp.ClientSession() as session:

        # Realizamos cada solicitud de forma asincrónica guardando la respuesta en res
        async with session.get(url) as res:

            # Verificación de la conexión correcta
            if res.status == 200:

                # Utilización de await res.text() para obtener el texto HTML de manera asincrónica
                sopa = BeautifulSoup(await res.text(), "html.parser")
                tabla = sopa.find("table", {"class": "table table-striped table-responsive text-center"})
                filas = tabla.find_all("tr")
                datos = []

                # Iteración sobre las filas encontradas anteriormente y omitimos el encabezado con filas[1:]
                for fila in filas[1:]:
                    columnas = fila.find_all("td")

                    # Comprobación de la longitud de las columnas. En caso de ser 3 almacenamos la información.
                    if len(columnas) == 3:
                        dia = columnas[0].text.strip()
                        precio = float(columnas[1].text.strip().replace(",", "."))
                        variacion = columnas[2].text.strip()
                        datos.append([dia, precio, variacion, producto, categoria, supermercado])
                
                # Convertimos a data frame
                df = pd.DataFrame(datos, columns=["Día", "Precio (€)", "Variación", "Producto", "Categoría", "Supermercado"])
                return df

async def tarea_con_semaforo(semaforo, url, producto, categoria, supermercado):
    # Función intermedia para controlar la ejecución simultanea de las tareas
    async with semaforo:
        return await obtener_tablas(url, producto, categoria, supermercado)

async def extraer_informacion(diccionario_urls):

    # Generación del semaforo. Esto nos va a permitir limitar el número de tareas simultaneas
    # en ejecución a 10.
    semaforo = asyncio.Semaphore(10)
    tareas = []

    # Almacenamos en una lista todas las tareas iterando sobre el diccionario obtenido
    for supermercado, categorias in diccionario_urls.items():
        for categoria, productos in categorias.items():
            for producto, url in productos.items():

                # Pasamos como parametros toda la información necesaria para generar el diccionario
                # ordenado de forma correcta. Además del semaforo mencionado anteriormente.
                tareas.append(tarea_con_semaforo(semaforo, url, producto, categoria, supermercado))

    # Almacenamiento de los resultados una vez han terminado todas las tareas
    resultados = await asyncio.gather(*tareas)

    # Conversión a data frame para un mejor tratamiento de los datos antes de su subida a la bbdd
    df_final = pd.concat(resultados, ignore_index=True, axis=0)
    return df_final