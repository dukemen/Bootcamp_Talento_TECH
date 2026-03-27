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

    # PARTE 4: SELECCIÓN Y FILTROS
    print("\n" + "="*60)
    print("🔍 SELECCIÓN Y FILTROS")
    print("="*60)

    # --- 4.1 Selección de columnas ---
    print("\n--- 4.1 Selección de columnas ---")

    # Seleccionar una sola columna
    primera_columna = df.columns[0]
    print(f"\n   Seleccionando la columna '{primera_columna}':")
    print(df[primera_columna].head(10))

    # Seleccionar múltiples columnas
    if len(df.columns) >= 3:
        columnas_seleccionadas = list(df.columns[:3])
        print(f"\n   Seleccionando las primeras 3 columnas {columnas_seleccionadas}:")
        print(df[columnas_seleccionadas].head(10))

    # Seleccionar columnas numéricas
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    if columnas_numericas:
        print(f"\n   Columnas numéricas encontradas: {columnas_numericas}")
        print(df[columnas_numericas].head(10))

    # Seleccionar columnas categóricas
    columnas_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    if columnas_categoricas:
        print(f"\n   Columnas categóricas encontradas: {columnas_categoricas}")
        print(df[columnas_categoricas].head(10))

    # --- 4.2 Selección de filas con loc e iloc ---
    print("\n--- 4.2 Selección de filas con loc e iloc ---")

    # iloc: selección por posición (índice numérico)
    print("\n   Primeras 5 filas con iloc:")
    print(df.iloc[:5])

    print("\n   Filas de la 3 a la 7 con iloc:")
    print(df.iloc[2:7])

    # Selección de filas y columnas específicas con iloc
    if len(df.columns) >= 3:
        print("\n   Filas 0-4, columnas 0-2 con iloc:")
        print(df.iloc[:5, :3])

    # loc: selección por etiqueta
    print(f"\n   Fila con índice 0 usando loc:")
    print(df.loc[0])

    # --- 4.3 Filtros con condiciones ---
    print("\n--- 4.3 Filtros con condiciones ---")

    # Filtrar empleados mayores de 30 años (si existe la columna 'Edad')
    if 'Edad' in df.columns:
        print("\n   Filtrar empleados con Edad > 30:")
        print(df[df['Edad'] > 30])

        # Guardar el resultado en una nueva variable
        empleados_mayores = df[df['Edad'] > 30]
        print(f"\n   Empleados mayores de 30: {len(empleados_mayores)} de {len(df)} totales")
        print(empleados_mayores)

    if columnas_numericas:
        # Filtro con una condición numérica (dinámico)
        col_num = columnas_numericas[0]
        mediana = df[col_num].median()
        filtro_mayor = df[df[col_num] > mediana]
        print(f"\n   Filas donde '{col_num}' > {mediana:.2f} (mediana):")
        print(f"   Se encontraron {len(filtro_mayor)} filas de {len(df)} totales")
        print(filtro_mayor.head(10))

        # Filtro con condición menor o igual
        filtro_menor = df[df[col_num] <= mediana]
        print(f"\n   Filas donde '{col_num}' <= {mediana:.2f} (mediana):")
        print(f"   Se encontraron {len(filtro_menor)} filas de {len(df)} totales")
        print(filtro_menor.head(10))

    # --- 4.4 Filtros con múltiples condiciones ---
    print("\n--- 4.4 Filtros con múltiples condiciones ---")

    # Filtrar con AND: Edad > 30 Y Salario > 4000
    if 'Edad' in df.columns and 'Salario' in df.columns:
        print("\n   Filtro AND: Edad > 30 Y Salario > 4000:")
        filtro_edad_salario = df[(df['Edad'] > 30) & (df['Salario'] > 4000)]
        print(f"   Se encontraron {len(filtro_edad_salario)} filas")
        print(filtro_edad_salario)

    # Filtrar con OR: Ciudad es Bogota O Ciudad es Medellin
    if 'Ciudad' in df.columns:
        print("\n   Filtro OR: Ciudad es 'Bogota' O Ciudad es 'Medellin':")
        filtro_ciudades = df[(df['Ciudad'] == 'Bogota') | (df['Ciudad'] == 'Medellin')]
        print(f"   Se encontraron {len(filtro_ciudades)} filas")
        print(filtro_ciudades)

    if len(columnas_numericas) >= 2:
        col1 = columnas_numericas[0]
        col2 = columnas_numericas[1]
        mediana1 = df[col1].median()
        mediana2 = df[col2].median()

        # Condición AND (&) - dinámico
        filtro_and = df[(df[col1] > mediana1) & (df[col2] > mediana2)]
        print(f"\n   Filtro AND: '{col1}' > {mediana1:.2f} Y '{col2}' > {mediana2:.2f}:")
        print(f"   Se encontraron {len(filtro_and)} filas")
        print(filtro_and.head(10))

        # Condición OR (|) - dinámico
        filtro_or = df[(df[col1] > mediana1) | (df[col2] > mediana2)]
        print(f"\n   Filtro OR: '{col1}' > {mediana1:.2f} O '{col2}' > {mediana2:.2f}:")
        print(f"   Se encontraron {len(filtro_or)} filas")
        print(filtro_or.head(10))

    # --- 4.5 Filtros con isin() y between() ---
    print("\n--- 4.5 Filtros con isin() y between() ---")

    if columnas_categoricas:
        col_cat = columnas_categoricas[0]
        valores_unicos = df[col_cat].dropna().unique()
        print(f"\n   Valores únicos en '{col_cat}': {valores_unicos[:10]}")

        # Filtrar usando isin() con los primeros 2 valores únicos
        if len(valores_unicos) >= 2:
            valores_filtro = list(valores_unicos[:2])
            filtro_isin = df[df[col_cat].isin(valores_filtro)]
            print(f"\n   Filtro isin({valores_filtro}):")
            print(f"   Se encontraron {len(filtro_isin)} filas")
            print(filtro_isin.head(10))

    if columnas_numericas:
        col_between = columnas_numericas[0]
        q1 = df[col_between].quantile(0.25)
        q3 = df[col_between].quantile(0.75)
        filtro_between = df[df[col_between].between(q1, q3)]
        print(f"\n   Filtro between: '{col_between}' entre Q1({q1:.2f}) y Q3({q3:.2f}):")
        print(f"   Se encontraron {len(filtro_between)} filas (rango intercuartílico)")
        print(filtro_between.head(10))

    # --- 4.6 Filtros con query() ---
    print("\n--- 4.6 Filtros con query() ---")

    if columnas_numericas:
        col_query = columnas_numericas[0]
        promedio = df[col_query].mean()
        consulta = f"`{col_query}` > {promedio:.2f}"
        filtro_query = df.query(consulta)
        print(f"\n   Usando df.query(\"{consulta}\"):")
        print(f"   Se encontraron {len(filtro_query)} filas")
        print(filtro_query.head(10))

    # --- 4.7 Valores únicos y conteo ---
    print("\n--- 4.7 Valores únicos y conteo de frecuencias ---")

    for col in df.columns:
        n_unicos = df[col].nunique()
        print(f"\n   '{col}': {n_unicos} valores únicos")
        if n_unicos <= 20:
            print(f"   Distribución de valores:")
            print(df[col].value_counts())

    # --- 4.8 Ordenamiento (sorting) ---
    print("\n--- 4.8 Ordenamiento ---")

    if columnas_numericas:
        col_orden = columnas_numericas[0]
        print(f"\n   Top 10 filas ordenadas por '{col_orden}' (descendente):")
        print(df.sort_values(by=col_orden, ascending=False).head(10))

        print(f"\n   Top 10 filas ordenadas por '{col_orden}' (ascendente):")
        print(df.sort_values(by=col_orden, ascending=True).head(10))

    # --- Resumen final ---
    print("\n" + "="*60)
    print("📊 RESUMEN DE SELECCIÓN Y FILTROS")
    print("="*60)
    print(f"   Total de filas en el dataset: {len(df)}")
    print(f"   Total de columnas: {len(df.columns)}")
    print(f"   Columnas numéricas: {len(columnas_numericas)}")
    print(f"   Columnas categóricas: {len(columnas_categoricas)}")
    if columnas_numericas:
        print(f"\n   Estadísticas de '{columnas_numericas[0]}':")
        print(f"   - Mínimo: {df[columnas_numericas[0]].min()}")
        print(f"   - Máximo: {df[columnas_numericas[0]].max()}")
        print(f"   - Promedio: {df[columnas_numericas[0]].mean():.2f}")
        print(f"   - Mediana: {df[columnas_numericas[0]].median():.2f}")

    print("\n" + "="*60)

    # Visualizar el DataFrame completo en VS Code
    df

else:
    # Si no se seleccionó ningún archivo
    print("No se seleccionó ningún archivo.")