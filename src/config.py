"""
config.py
─────────
Centraliza credenciales, constantes y generación de fechas.
Las credenciales se leen desde st.secrets (Streamlit Cloud / .streamlit/secrets.toml).
"""

import calendar
import streamlit as st

# ─── Etiquetas de meses en español ───────────────────────────────────────────
MONTHS_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

# ─── Frecuencias de indicadores ───────────────────────────────────────────────
FREQUENCIES: dict[int, str] = {
    2: "Mensual",
    3: "Trimestral",
    5: "Quincenal",
    6: "Semestral",
    7: "Anual",
}


def get_credentials() -> tuple[str, str, str, str]:
    """
    Devuelve (email, password, instancia, base_url).
    Las credenciales deben estar en .streamlit/secrets.toml (local)
    o en Streamlit Cloud → Settings → Secrets.

    Formato requerido en secrets.toml:
        [kawak]
        email     = "usuario@dominio.com"
        password  = "contraseña"
        instancia = "nombre_instancia"
        base_url  = "https://api.kawak.com.co"   # opcional
    """
    try:
        cfg = st.secrets["kawak"]
    except (KeyError, FileNotFoundError):
        st.error(
            "⚠️ **Credenciales no configuradas.** "
            "Crea el archivo `.streamlit/secrets.toml` con la sección `[kawak]` "
            "o configura los Secrets en Streamlit Cloud. "
            "Consulta el archivo `.streamlit/secrets.toml.example` como guía."
        )
        st.stop()

    for field in ("email", "password", "instancia"):
        if not cfg.get(field):
            st.error(f"⚠️ Falta el campo `{field}` en la sección `[kawak]` de secrets.toml.")
            st.stop()

    return (
        cfg["email"],
        cfg["password"],
        cfg["instancia"],
        cfg.get("base_url", "https://api.kawak.com.co"),
    )


def generate_dates_by_year(start: int = 2015, end: int = 2030) -> dict[str, list[tuple[str, str]]]:
    """
    Genera un diccionario {año: [(etiqueta, fecha_ISO), ...]}.
    La fecha es el último día de cada mes.
    """
    result: dict[str, list[tuple[str, str]]] = {}
    for year in range(start, end + 1):
        entries: list[tuple[str, str]] = []
        for month in range(1, 13):
            last_day = calendar.monthrange(year, month)[1]
            label = f"{MONTHS_ES[month - 1]} {year}"
            value = f"{year}-{month:02d}-{last_day:02d}"
            entries.append((label, value))
        result[str(year)] = entries
    return result


# Constantes precalculadas al importar el módulo
DATES_BY_YEAR: dict[str, list[tuple[str, str]]] = generate_dates_by_year()
ALL_YEARS: list[str] = list(DATES_BY_YEAR.keys())
