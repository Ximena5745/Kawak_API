import streamlit as st
import pandas as pd
import requests

# Configuración inicial de la página
st.set_page_config(
    page_title="Menú de Consultas API",
    page_icon="📊",
    layout="centered"
)

# Título del frontend
st.title("📊 Menú Interactivo de Consultas API")

# Descripción inicial
st.write("Seleccione una opción para realizar la consulta correspondiente a la API.")

# Opciones del menú
menu_options = [
    "Indicadores",
    "Salidas No Conformes",
    "Acciones de Mejora",
    "Documentos",
    "Riesgos"
]

# Selector interactivo
selected_option = st.selectbox("Seleccione una opción", menu_options)

# Botón para ejecutar la consulta
if st.button("
