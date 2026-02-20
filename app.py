"""
app.py
──────
Punto de entrada de la aplicación Portal Kawak.

Ejecutar con:
    streamlit run app.py
"""

import requests
import streamlit as st
from datetime import datetime

from src.config import get_credentials
from src.api.client import KawakClient
from src.utils.ui import inject_css, render_header, render_sidebar, render_footer
from src.modules import (
    indicadores,
    auditoria,
    salidas_nc,
    acciones_mejora,
    documentos,
    riesgos,
)

# ─── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Portal Kawak | Poligran",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Credenciales ─────────────────────────────────────────────────────────────
EMAIL, PASSWORD, INSTANCIA, BASE_URL = get_credentials()

# ─── Módulos disponibles ──────────────────────────────────────────────────────
_MODULES = {
    "Indicadores": indicadores,
    "Auditoria":   auditoria,
    "SNC":         salidas_nc,
    "Mejora":      acciones_mejora,
    "Documentos":  documentos,
    "Riesgos":     riesgos,
}


# ─── Autenticación ────────────────────────────────────────────────────────────
def _login() -> bool:
    """Obtiene el token de la API y lo guarda en session_state."""
    try:
        with st.spinner("Autenticando con la API de Kawak…"):
            resp = requests.post(
                f"{BASE_URL}/login",
                data={"email": EMAIL, "password": PASSWORD, "instancia": INSTANCIA},
                timeout=20,
            )
        if resp.status_code == 200:
            token = resp.json().get("message", {}).get("Authorization")
            if token:
                st.session_state.token      = token
                st.session_state.login_time = datetime.now().strftime("%H:%M:%S")
                return True
        st.error(f"Error de autenticación ({resp.status_code}). Verifique las credenciales.")
    except requests.exceptions.Timeout:
        st.error("Tiempo de espera agotado al conectar con la API.")
    except Exception as exc:
        st.error(f"Error de conexión: {exc}")
    return False


# ─── Aplicación principal ─────────────────────────────────────────────────────
def main() -> None:
    inject_css()
    render_header()

    # Autenticación automática al iniciar o al renovar sesión
    if "token" not in st.session_state:
        if not _login():
            st.stop()

    # Instanciar cliente y renderizar navegación
    client = KawakClient(st.session_state.token, BASE_URL)
    modulo = render_sidebar(INSTANCIA)

    # Enrutamiento al módulo seleccionado
    if modulo in _MODULES:
        _MODULES[modulo].render(client)

    render_footer(datetime.now().year)


if __name__ == "__main__":
    main()
