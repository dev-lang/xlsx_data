# Importamos pandas para manipulación de datos
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## PASO 1 PRECARGA Y LIMPIEZA DE DATOS
# Cargamos el archivo Excel, omitiendo la primera fila y usando la tercera como encabezado
df = pd.read_excel("Existencias bovinas.xlsx", engine="openpyxl", skiprows=1, header=0)

# Listas para almacenar los nombres de las columnas
columnas_con_nulos = []
columnas_sin_nulos = []

# Iteramos sobre cada columna en el DataFrame
for columna in df.columns:
    # Si la columna tiene algún valor nulo, la agregamos a `columnas_con_nulos`
    if df[columna].isnull().any():
        columnas_con_nulos.append(columna)
    else:
        # Si no tiene valores nulos, la agregamos a `columnas_sin_nulos`
        columnas_sin_nulos.append(columna)

# Reemplazamos los valores nulos por 0 en las columnas que tienen nulos
df[columnas_con_nulos] = df[columnas_con_nulos].fillna(0)

# Convertimos todas las columnas numéricas a tipo entero
for columna in df.select_dtypes(include=['float', 'int']).columns:
    df[columna] = df[columna].astype(int)

# Eliminamos las columnas 'provincia_id' y 'departamento_id' (datos irrelevantes)
df = df.drop(columns=['provincia_id', 'departamento_id'])

# Mostramos el DataFrame después de reemplazar los valores nulos
print(df.head())

## FIN PASO 1 PRECARGA Y LIMPIEZA DE DATOS

# Sumamos las columnas de animales por 'año', 'provincia' y 'departamento'
animales_cols = ['vacas', 'vaquillonas', 'novillos', 'novillitos', 'terneros', 'terneras', 'toros', 'toritos', 'bueyes']
df['total_animales'] = df[animales_cols].sum(axis=1)

# Agrupamos por 'año', 'provincia' y 'departamento' para ver la cantidad total de animales
df_grouped = df.groupby(['año', 'provincia', 'departamento'])['total_animales'].sum().reset_index()

# Crear el gráfico para cada tipo de animal a lo largo de los años
plt.figure(figsize=(12, 8))

# Sumamos las cantidades de cada tipo de animal por 'año'
df_animales = df.groupby(['año'])[animales_cols].sum()

# Usamos seaborn para crear un gráfico de líneas para cada tipo de animal
sns.lineplot(data=df_animales, dashes=False, markers=True)

# Agregamos detalles al gráfico
plt.title('Evolución de los Animales por Año', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Animales', fontsize=12)

# Mostrar el gráfico
plt.tight_layout()
plt.show()
