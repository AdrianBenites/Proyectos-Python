import pandas as pd

def analizar_csv(path, chunk_size=50000):
    print(f"\n📁 Analizando: {path}")
    filas = 0
    resumen = []
    columnas = []
    for chunk in pd.read_csv(path, chunksize=chunk_size):
        if not columnas:
            columnas = chunk.columns.tolist()
        filas += len(chunk)
        resumen.append(chunk.describe(include='all'))

    print(f"✅ Total de filas procesadas: {filas}")
    print(f"🧾 Columnas: {columnas}")

    # Combinar descripciones
    resumen_final = pd.concat(resumen).groupby(level=0).mean(numeric_only=True)
    print("\n📊 Resumen estadístico:")
    print(resumen_final)

    # Mostrar primeras y últimas filas
    df_sample = pd.read_csv(path, nrows=5)
    print("\n🔍 Primeras 5 filas:")
    print(df_sample)

    df_tail = pd.read_csv(path, skiprows=lambda x: x < filas - 5 and x != 0)
    print("\n🔎 Últimas 5 filas:")
    print(df_tail)

if __name__ == "__main__":
    archivo = input("📂 Ingresa la ruta del archivo CSV: ")
    analizar_csv(archivo)
