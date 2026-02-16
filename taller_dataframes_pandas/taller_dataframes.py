# Importar las bibliotecas necesarias
import pandas as pd
import matplotlib.pyplot as plt
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
    
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(ruta_archivo)
    
    # Mostrar las primeras 5 filas del DataFrame
    print("Primeras 5 filas:")
    print(df.head())

    # Mostrar las ultimas 5 filas del DataFrame
    print("ultimas 5 filas:")
    print(df.tail())     # últimas 5 filas
    
    # Mostrar información general del DataFrame
    print("\nInformación general del DataFrame:")
    print(df.info())
    
      # Mostrar Nombre de las columnas
    print("\nNombre de las columnas:")
    print(df.columns)

    # Mostrar índice de las filas
    print("\nÍndice de las filas:")
    print(df.index)
    
     # Mostrar estadísticas descriptivas de las columnas numéricas
    print("\nEstadísticas descriptivas de las columnas numéricas:")
    print(df.describe())
    
    # Mostrar dimensiones
    print(f"\nDimensiones: {df.shape[0]} filas y {df.shape[1]} columnas")

    # PREGUNTAS DEL TALLER
    print("\n" + "="*60)
    print("RESPUESTAS A LAS PREGUNTAS DEL TALLER")
    print("="*60)

    # 1. ¿Cuál es la variable con mayor promedio?
    print("\n1. Variable con mayor promedio:")
    promedios = df.mean(numeric_only=True)
    variable_mayor_promedio = promedios.idxmax()
    valor_mayor_promedio = promedios.max()
    print(f"   La variable '{variable_mayor_promedio}' tiene el mayor promedio: {valor_mayor_promedio:.2f}")
    print("\n   Promedios de todas las variables numéricas:")
    print(promedios)

    # 2. ¿Existen valores nulos?
    print("\n2. Valores nulos:")
    valores_nulos_por_columna = df.isnull().sum()
    total_nulos = valores_nulos_por_columna.sum()
    if total_nulos > 0:
        print(f"   Sí, existen {total_nulos} valores nulos en total.")
        print("\n   Valores nulos por columna:")
        print(valores_nulos_por_columna[valores_nulos_por_columna > 0])
    else:
        print("   No, no existen valores nulos en el dataset.")

    # 3. ¿Qué columnas son categóricas?
    print("\n3. Columnas categóricas:")
    columnas_categoricas = df.select_dtypes(include=['object']).columns
    if len(columnas_categoricas) > 0:
        print(f"   Hay {len(columnas_categoricas)} columna(s) categórica(s):")
        for col in columnas_categoricas:
            print(f"   - {col}")
    else:
        print("   No hay columnas categóricas (tipo object) en el dataset.")

    print("\n" + "="*60)

    # 🧹 PARTE 3: LIMPIEZA DE DATOS
    print("\n" + "="*60)
    print("🧹 LIMPIEZA DE DATOS - VALORES FALTANTES")
    print("="*60)

    # Si hay valores nulos, aplicar limpieza
    if total_nulos > 0:
        print(f"\n⚠️  Se detectaron {total_nulos} valores nulos.")
        print("   Aplicando limpieza de datos...\n")

        # OPCIÓN 1: Eliminar filas con valores nulos (comentado)
        # df = df.dropna()
        # print("   ✓ Filas con valores nulos eliminadas.")

        # OPCIÓN 2: Rellenar valores nulos con el promedio (activo)
        df.fillna(df.mean(numeric_only=True), inplace=True)
        print("   ✓ Valores nulos rellenados con el promedio de cada columna.")

        # Verificar que ya no hay nulos
        print(f"\n   Verificación: {df.isnull().sum().sum()} valores nulos restantes.")
        print(f"   Dimensiones después de limpieza: {df.shape[0]} filas y {df.shape[1]} columnas")
    else:
        print("\n✅ No hay valores nulos en el dataset.")
        print("   No es necesario aplicar limpieza de datos.")

    print("\n" + "="*60)

    # 📊 PARTE 6: VISUALIZACIÓN BÁSICA DE DATOS
    print("\n" + "="*60)
    print("📊 VISUALIZACIÓN BÁSICA DE DATOS")
    print("="*60)

    # --- Histograma de Salarios ---
    if 'Salario' in df.columns:
        plt.figure(figsize=(8, 5))
        df['Salario'].hist(bins=10, color='#5BA3CF', edgecolor='black')
        plt.title('Distribución de Salarios')
        plt.xlabel('Salario ($)')
        plt.ylabel('Frecuencia')
        plt.tight_layout()
        plt.show()
        print("   ✓ Histograma de Salarios generado.")
    else:
        print("   ⚠️  Columna 'Salario' no encontrada. Histograma omitido.")

    # --- Gráfico de barras: Salario promedio por Ciudad ---
    if 'Salario' in df.columns and 'Ciudad' in df.columns:
        plt.figure(figsize=(8, 5))
        df.groupby('Ciudad')['Salario'].mean().plot(kind='bar', color='#F2AD5E', edgecolor='black')
        plt.title('Salario Promedio por Ciudad')
        plt.xlabel('Ciudad')
        plt.ylabel('Salario Promedio ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        print("   ✓ Gráfico de barras (Salario promedio por Ciudad) generado.")
    else:
        print("   ⚠️  Columnas 'Salario' y/o 'Ciudad' no encontradas. Gráfico de barras omitido.")

    # --- Scatter plot: Edad vs Salario ---
    if 'Edad' in df.columns and 'Salario' in df.columns:
        plt.figure(figsize=(8, 5))
        df.plot(x='Edad', y='Salario', kind='scatter', color='#6BCB77', ax=plt.gca())
        plt.title('Edad vs Salario')
        plt.xlabel('Edad')
        plt.ylabel('Salario ($)')
        plt.tight_layout()
        plt.show()
        print("   ✓ Scatter plot (Edad vs Salario) generado.")
    else:
        print("   ⚠️  Columnas 'Edad' y/o 'Salario' no encontradas. Scatter plot omitido.")

    # --- Box plot: Distribución de Salarios por Departamento ---
    if 'Salario' in df.columns and 'Departamento' in df.columns:
        plt.figure(figsize=(8, 5))
        df.boxplot(column='Salario', by='Departamento', grid=False)
        plt.title('Distribución de Salarios por Departamento')
        plt.suptitle('')  # Eliminar el título automático de pandas
        plt.xlabel('Departamento')
        plt.ylabel('Salario ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        print("   ✓ Box plot (Salarios por Departamento) generado.")
    else:
        print("   ⚠️  Columnas 'Salario' y/o 'Departamento' no encontradas. Box plot omitido.")

    print("\n" + "="*60)

    # Visualizar el DataFrame completo en VS Code
    df
    
else:
    # Si no se seleccionó ningún archivo
    print("No se seleccionó ningún archivo.")