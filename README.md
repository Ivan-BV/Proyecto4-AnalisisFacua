# 📊 Proyecto 4: Analisis de supermercados a través de Facua

## 📖 Descripción del Proyecto

- Este proyecto tiene como objetivo realizar un análisis detallado de los precios de productos en los principales supermercados de España, utilizando herramientas de web scraping, procesamiento de datos y análisis exploratorio de datos. La fuente principal de información será la plataforma FACUA: Precios Supermercados, una página que publica precios actualizados de productos básicos en supermercados como Alcampo, Carrefour, Dia, Eroski, Hipercor y Mercadona.

- A partir de los datos recolectados, se construirá una base de datos en SQL para almacenar la información de manera estructurada. Esto permitirá llevar a cabo un análisis exhaustivo sobre la comparación entre supermercados en base a los precios de los productos. Los resultados de este análisis se presentarán mediante visualizaciones, facilitando la identificación de diferencias significativas de precios y la comprensión de la evolución de los mismos a lo largo del tiempo.

## 🎯 Objetivos del proyecto

1. Scraping de datos: Extraer información detallada de todos los productos listados en la web de FACUA para cada supermercado, obteniendo datos de precios actualizados y organizados.

2. Almacenamiento en base de datos: Construir una base de datos SQL que almacene la información recolectada, asegurando su integridad y accesibilidad para el análisis posterior.

3. Análisis de Datos:

    - Comparación de Precios entre Supermercados: Identificar qué supermercados ofrecen los precios más competitivos y cuáles tienden a ser más caros, para cada producto específico.
    - Detección de Anomalías: Identificar subidas o bajadas de precios inusuales que podrían señalar prácticas abusivas o promociones.
    - Análisis de la Dispersión de Precios: Evaluar la variabilidad de los precios de un mismo producto en diferentes supermercados.
    - Comparación de Precios Promedio: Calcular y comparar los precios promedio de cada producto en diferentes supermercados.

4. Visualización de Datos: Crear gráficos y visualizaciones que permitan una comprensión clara de los resultados obtenidos en el análisis, facilitando la comparación y el seguimiento de las fluctuaciones de precios entre los diferentes supermercados.

## 🗂️ Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```bash
├── datos/                # Conjuntos de datos sin procesar y ya procesados
│   ├── output/           # Datos procesados y resultados finales
│   └── raw/              # Datos en bruto (sin procesar)
│
├── imagenes/             # Recursos gráficos para el README y el proyecto
│
├── notebooks/            # Notebooks con el contenido y análisis de datos
│
├── src/                  # Scripts para la limpieza y procesamiento de datos
│
├── README.md             # Descripción general del proyecto e instrucciones
└── requirements.txt      # Lista de dependencias del proyecto
```

## 🛠️ Instalación y Requisitos

Este proyecto utiliza [Python 3.12.7](https://docs.python.org/3.12/) y requiere las siguientes bibliotecas para la ejecución y análisis:

- [pandas 2.2.3](https://pandas.pydata.org/docs/)
- [matplotlib 3.9.2](https://matplotlib.org/stable/index.html)
- [seaborn 0.13.2](https://seaborn.pydata.org/tutorial.html)
- [beautifulsoup4 4.12.3](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [selenium 4.25.0](https://www.selenium.dev/documentation/)
- [asyncio 3.4.3](https://docs.python.org/3.12/library/asyncio.html)
- [psycopg2 2.9.10](https://www.psycopg.org/docs/)

Para instalar las dependencias, puedes ejecutar el siguiente comando dentro de un entorno virtual:

```bash
pip install -r requirements.txt
```

## 📊 Resultados y Conclusiones

Tras analizar los datos recogidos sobre los precios de cada categoria de productos se han generado diferentes gráficos:

<img src="imagenes/precios_aceite_girasol.png" />


- Conclusión de la comparativa de precios del *aceite de girasol*:
    - En cuanto a variabilidad de precios, **Alcampo**, **Carrefour** y **Dia** presentan un rango amplio de precios, con **Alcampo** y **Carrefour** mostrando valores atípicos bastante altos.
    - Distribución de precios: **Mercadona** y **Eroski** parecen ofrecer precios más estables y bajos en comparación con otros supermercados. **Alcampo** y **Carrefour**, por otro lado, tienen precios más dispersos y algunos valores atípicos elevados, lo que indica que podrían tener opciones de aceite de girasol premium o en presentaciones más grandes.
    - En resumen, **Mercadona** y **Eroski** ofrecen precios de aceite de girasol más consistentes y económicos, mientras que **Alcampo** y **Carrefour** presentan una mayor variación, con algunos precios altos fuera del rango típico.

<img src="imagenes/precios_aceite_oliva.png" />


- Conclusión de la comparativa de precios del *aceite de oliva*:
    - En cuanto a la variabilidad de precios, el precio del *aceite de oliva* muestra una variabilidad aún mayor en comparación con el *aceite de girasol*.
    **Eroski** y **Dia** tienen numerosos valores atípicos, lo que sugiere que disponen de una amplia gama de productos de *aceite de oliva* con distintas calidades y precios.
    - Hipercor y Alcampo también muestran precios elevados, aunque los precios en **Hipercor** parecen ser más altos en promedio y presentan varios valores atípicos, lo cual indica una posible oferta de productos de mayor calidad o en tamaños más grandes.
    - En resumen, Los precios del *aceite de oliva* son más altos y variables que los del aceite de girasol. **Hipercor** y **Alcampo** tienden a tener precios más altos, mientras que Dia y Eroski presentan la mayor dispersión, sugiriendo una amplia gama de opciones en estos supermercados.


<img src="imagenes/precios_leche.png" />


- Conclusión de la comparativa de precios de la *leche*:
    - La leche es el producto con menos variabilidad en comparación con los aceites. La mayoría de los supermercados tienen precios relativamente estables, aunque Carrefour y Dia presentan valores atípicos dispersos que indican opciones de leche más caras.
    - En cuanto a la distribución de precios, Mercadona, Alcampo y Eroski tienen precios más consistentes y bajos en promedio, con menos valores atípicos. Esto sugiere que estos supermercados mantienen un precio uniforme para sus productos de leche.
    - En resumen, La leche tiene menos variabilidad de precio en comparación con los aceites, y Mercadona, Alcampo y Eroski destacan por tener precios más consistentes y bajos.

- Conclusión final:
    - En general, la variabilidad de precios es menor para la *leche* y mayor para el *aceite de oliva*.
    Los supermercados **Mercadona** y **Eroski** suelen ofrecer precios más estables y económicos en los tres productos, mientras que **Carrefour**, **Alcampo** y **Dia** muestran una mayor dispersión de precios, especialmente en los aceites, lo que sugiere una mayor diversidad de productos o calidades en estos establecimientos.


## 🔄 Próximos Pasos

- Implementar análisis de la evolución historica de precios.
- Ampliar la busqueda de historiales de los últimos 30 días de productos especificos para hacer un análisis más preciso.
- Optimización de la obtención de URLs en las que se encuentran los datos historicos.
- Aumentar la precisión del análisis separando por capacidad de los envases.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar en este proyecto, por favor abre un pull request o una issue en este repositorio.

## ✒️ Autores

Iván Bravo - Autor principal del proyecto.