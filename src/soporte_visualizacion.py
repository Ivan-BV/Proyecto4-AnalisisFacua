
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


def generar_boxplot(df: pd.DataFrame, titulo, xlabel, ylabel, rotation=None):
    """
    Genera un boxplot usando los dos primeros valores de columnas en el DataFrame proporcionado.

    Parámetros:
        df : pd.DataFrame
            DataFrame que contiene los datos a graficar. La primera columna debe corresponder
            a los valores para el eje y, y la segunda columna a los valores categóricos del eje x.
    
    titulo : str
        Título del gráfico.
    
    xlabel : str
        Etiqueta del eje x.
    
    ylabel : str
        Etiqueta del eje y.
    
    rotation : int, optional
        Ángulo de rotación para las etiquetas del eje x. Si no se proporciona, no rota las etiquetas.
    
    Retorna:
        None
            La función no retorna ningún valor, muestra el boxplot generado.
    """
    plt.figure(figsize=(15,8))
    sns.boxplot(y=df.columns[0],
                x=df.columns[1],
                data=df,
                palette="crest"
                )
    if rotation is not None:
        plt.xticks(rotation=45)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.tight_layout()
    plt.show()

