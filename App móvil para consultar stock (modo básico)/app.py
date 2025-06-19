import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consulta de Stock", layout="centered")

st.title("📦 Consulta de Inventario")
st.write("Busca productos y revisa sus existencias desde el celular.")

# Conexión
def obtener_datos():
    with sqlite3.connect("inventario.db") as conn:
        return pd.read_sql_query("SELECT nombre, cantidad, precio FROM productos", conn)

df = obtener_datos()

# Buscador
busqueda = st.text_input("🔍 Buscar producto")

if busqueda:
    resultados = df[df["nombre"].str.contains(busqueda, case=False)]
else:
    resultados = df

st.dataframe(resultados, use_container_width=True)
