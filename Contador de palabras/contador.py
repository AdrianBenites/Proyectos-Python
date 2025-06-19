from collections import Counter

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        return lineas
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def contar_palabras(lineas):
    texto = " ".join(lineas).lower()
    palabras = texto.split()
    return Counter(palabras)

def mostrar_resultados(palabras, lineas):
    print(f"Total de líneas: {len(lineas)}")
    print(f"Total de palabras: {sum(palabras.values())}")
    print("\nTop 10 palabras más comunes:")
    for palabra, frecuencia in palabras.most_common(10):
        print(f"{palabra}: {frecuencia}")
    
    palabra_buscar = input("\n¿Quieres buscar una palabra específica? (déjalo en blanco para omitir): ").lower()
    if palabra_buscar:
        print(f"La palabra '{palabra_buscar}' aparece {palabras.get(palabra_buscar, 0)} veces.")

if __name__ == "__main__":
    archivo = input("Ingresa el nombre del archivo .txt a analizar: ")
    lineas = leer_archivo(archivo)
    if lineas:
        palabras = contar_palabras(lineas)
        mostrar_resultados(palabras, lineas)
