# Importar las bibliotecas necesarias
import pandas as pd
from tkinter import Tk, filedialog

# Crear una ventana oculta de tkinter
# Esto es necesario para abrir el cuadro de diálogo de selección de archivos
root = Tk()
root.withdraw()  # Ocultar la ventana principal (solo queremos el diálogo)

# Abrir ventana para seleccionar el archivo CSV
# Se abrirá el explorador de archivos de Windows
print("Selecciona tu archivo CSV...")
ruta_archivo = filedialog.askopenfilename(
    title="Selecciona el archivo CSV",
    filetypes=[("Archivos CSV", ".csv"), ("Todos los archivos", ".*")]
)

# Verificar que se seleccionó un archivo
if ruta_archivo:
    print(f"\nArchivo seleccionado: {ruta_archivo}\n")
    
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(ruta_archivo)
    
    # Mostrar las primeras 5 filas del DataFrame
    print("Primeras 5 filas:")
    print(df.head())

    # Mostrar las ultimas 5 filas del DataFrame
    print("ultimas 5 filas:")
    print(df.tail())     # últimas 5 filas
    
    # Mostrar información general del DataFrame
    print("\nInformación del DataFrame:")
    print(df.info())
    
    # Mostrar estadísticas descriptivas
    print("\nEstadísticas descriptivas:")
    print(df.describe())
    
    # Mostrar dimensiones
    print(f"\nDimensiones: {df.shape[0]} filas y {df.shape[1]} columnas")
    
    # Visualizar el DataFrame completo en VS Code
    df
    
else:
    # Si no se seleccionó ningún archivo
    print("No se seleccionó ningún archivo.")