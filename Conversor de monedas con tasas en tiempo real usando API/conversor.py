import requests

def obtener_tasa(origen, destino):
    url = f"https://api.exchangerate.host/latest?base={origen}&symbols={destino}"
    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        print("Error al conectarse a la API.")
        return None
    datos = respuesta.json()
    return datos['rates'][destino]

def convertir_moneda():
    print("=== Conversor de Monedas ===")
    origen = input("Moneda origen (ej: USD, EUR, COP): ").upper()
    destino = input("Moneda destino: ").upper()
    try:
        cantidad = float(input(f"Cantidad en {origen}: "))
    except ValueError:
        print("Error: Ingrese un número válido.")
        return
    
    tasa = obtener_tasa(origen, destino)
    if tasa:
        resultado = cantidad * tasa
        print(f"{cantidad:.2f} {origen} = {resultado:.2f} {destino} (Tasa: {tasa:.4f})")

if __name__ == "__main__":
    convertir_moneda()
