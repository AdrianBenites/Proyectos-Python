import streamlit as st

st.set_page_config(page_title="Calculadora de IMC", page_icon="⚖️")

st.title("⚖️ Calculadora de IMC")
st.write("Calcula tu Índice de Masa Corporal de forma rápida y sencilla.")

peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
altura = st.number_input("Estatura (m)", min_value=0.0, step=0.01)

if peso > 0 and altura > 0:
    imc = peso / (altura ** 2)
    st.markdown(f"### Tu IMC es: `{imc:.2f}`")

    if imc < 18.5:
        st.warning("Bajo peso")
    elif 18.5 <= imc < 25:
        st.success("Peso normal")
    elif 25 <= imc < 30:
        st.info("Sobrepeso")
    else:
        st.error("Obesidad")
else:
    st.info("Ingresa tu peso y altura para calcular tu IMC.")

