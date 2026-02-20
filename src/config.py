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
    Prioridad: st.secrets["kawak"] → valores por defecto.
    """
    try:
        cfg = st.secrets["kawak"]
        return (
            cfg.get("email",     "aquiroga@poligran.edu.co"),
            cfg.get("password",  "tPLLryr7J2925F7U"),
            cfg.get("instancia", "poligran"),
            cfg.get("base_url",  "https://api.kawak.com.co"),
        )
    except Exception:
        return (
            "aquiroga@poligran.edu.co",
            "tPLLryr7J2925F7U",
            "poligran",
            "https://api.kawak.com.co",
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
