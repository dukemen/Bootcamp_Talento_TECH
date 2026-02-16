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

    # 📊 PARTE 5: AGRUPACIÓN Y ANÁLISIS
    print("\n" + "="*60)
    print("📊 PARTE 5: AGRUPACIÓN Y ANÁLISIS")
    print("="*60)

    # Detectar columnas relevantes para el análisis
    columnas_texto = df.select_dtypes(include=['object']).columns
    columnas_numericas = df.select_dtypes(include=['number']).columns

    # Buscar columna de ciudad (puede llamarse 'Ciudad', 'city', etc.)
    col_ciudad = None
    for col in columnas_texto:
        if col.lower() in ['ciudad', 'city', 'ciudad_residencia', 'ubicacion']:
            col_ciudad = col
            break

    # Buscar columna de salario
    col_salario = None
    for col in columnas_numericas:
        if col.lower() in ['salario', 'salary', 'sueldo', 'ingreso', 'ingresos']:
            col_salario = col
            break

    if col_ciudad and col_salario:
        # 1. ¿Qué ciudad tiene mayor promedio salarial?
        print(f"\n1. Promedio salarial por ciudad (columnas: '{col_ciudad}', '{col_salario}'):")
        promedio_por_ciudad = df.groupby(col_ciudad)[col_salario].mean().sort_values(ascending=False)
        print(promedio_por_ciudad)
        ciudad_mayor_salario = promedio_por_ciudad.idxmax()
        valor_mayor_salario = promedio_por_ciudad.max()
        print(f"\n   ✅ La ciudad con mayor promedio salarial es '{ciudad_mayor_salario}' con ${valor_mayor_salario:,.2f}")

        # 2. ¿Cuál ciudad tiene más registros?
        print(f"\n2. Cantidad de registros por ciudad:")
        registros_por_ciudad = df.groupby(col_ciudad).size().sort_values(ascending=False)
        print(registros_por_ciudad)
        ciudad_mas_registros = registros_por_ciudad.idxmax()
        cantidad_registros = registros_por_ciudad.max()
        print(f"\n   ✅ La ciudad con más registros es '{ciudad_mas_registros}' con {cantidad_registros} registros")

        # Extra: Resumen estadístico agrupado por ciudad
        print(f"\n3. Resumen estadístico del salario por ciudad:")
        resumen = df.groupby(col_ciudad)[col_salario].agg(['mean', 'median', 'min', 'max', 'count'])
        resumen.columns = ['Promedio', 'Mediana', 'Mínimo', 'Máximo', 'Cantidad']
        resumen = resumen.sort_values('Promedio', ascending=False)
        print(resumen)
    else:
        # Si no se encuentran las columnas exactas, intentar con la primera columna categórica
        if len(columnas_texto) > 0 and len(columnas_numericas) > 0:
            col_grupo = columnas_texto[0]
            col_valor = columnas_numericas[0]
            print(f"\n   No se encontraron columnas 'Ciudad'/'Salario'.")
            print(f"   Usando '{col_grupo}' para agrupar y '{col_valor}' para calcular:\n")

            # 1. Promedio por grupo
            print(f"1. Promedio de '{col_valor}' por '{col_grupo}':")
            promedio_grupo = df.groupby(col_grupo)[col_valor].mean().sort_values(ascending=False)
            print(promedio_grupo)
            print(f"\n   ✅ '{promedio_grupo.idxmax()}' tiene el mayor promedio: {promedio_grupo.max():,.2f}")

            # 2. Conteo por grupo
            print(f"\n2. Cantidad de registros por '{col_grupo}':")
            conteo_grupo = df.groupby(col_grupo).size().sort_values(ascending=False)
            print(conteo_grupo)
            print(f"\n   ✅ '{conteo_grupo.idxmax()}' tiene más registros: {conteo_grupo.max()}")
        else:
            print("\n   ⚠️  No se encontraron columnas adecuadas para agrupación.")

    print("\n" + "="*60)

    # Visualizar el DataFrame completo en VS Code
    df

else:
    # Si no se seleccionó ningún archivo
    print("No se seleccionó ningún archivo.")