"""
exports.py
──────────
Utilidades para exportar DataFrames a Excel y mostrar
el botón de descarga en la interfaz Streamlit.
"""

import io
import pandas as pd
import streamlit as st


def df_to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Datos") -> bytes:
    """Serializa un DataFrame a bytes de Excel (.xlsx)."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    buf.seek(0)
    return buf.read()


def show_download_button(df: pd.DataFrame, filename: str, sheet: str = "Datos") -> None:
    """Renderiza el botón de descarga de Excel para un DataFrame."""
    st.download_button(
        label="⬇️ Descargar Excel",
        data=df_to_excel_bytes(df, sheet),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )


def show_results(df: pd.DataFrame, filename: str, sheet: str = "Datos") -> None:
    """Muestra métricas de resumen, tabla y botón de descarga."""
    c1, c2, c3 = st.columns(3)
    c1.metric("Total registros", f"{len(df):,}")
    c2.metric("Columnas",        len(df.columns))
    c3.metric("Estado",          "✅ Exitoso")
    st.dataframe(df, use_container_width=True, height=420)
    show_download_button(df, filename, sheet)
