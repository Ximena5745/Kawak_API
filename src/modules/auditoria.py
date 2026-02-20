"""
auditoria.py
────────────
Módulo de consulta de Auditorías — Hallazgos.

Consume el endpoint paginado /api/v1/hallazgos.
Estructura de respuesta esperada:
    {
      "code": 200,
      "status": "success",
      "message": {
        "pagination": { "totalRows": N, "totalPages": N, ... },
        "data": [
          { "ID", "AUD_ID", "AUD_NOMBRE", "HALLAZGO",
            "CONFORME", "PROCESO", "NORMA", "NUM_NUMERAL",
            "NUMERAL", "AUDITOR_LIDER", "ID_OM" }
        ]
      }
    }
"""

from __future__ import annotations

import html as html_lib

import pandas as pd
import streamlit as st

from src.api.client import KawakClient
from src.utils.exports import show_download_button
from src.utils.ui import info_box, section_title


def render(client: KawakClient) -> None:
    section_title("🔍", "Auditorías — Hallazgos")
    info_box(
        "Consulta los hallazgos registrados en las auditorías internas y externas. "
        "La consulta recorre automáticamente todas las páginas disponibles."
    )

    # ── Parámetros ───────────────────────────────────────────────────────────
    with st.expander("⚙️ Parámetros de consulta", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            conformidad: str = st.selectbox(
                "Filtrar por conformidad (opcional)",
                ["Todos", "No Conformidad", "Observación", "Conforme"],
            )
        with col2:
            perpage: int = st.number_input(
                "Registros por página", min_value=10, max_value=200, value=50, step=10
            )

    # ── Consulta ─────────────────────────────────────────────────────────────
    if st.button("Consultar Auditorías", use_container_width=True):
        extra: dict = {"perPage": perpage}
        if conformidad != "Todos":
            extra["conforme"] = conformidad

        with st.spinner("Consultando auditorías…"):
            records = client.fetch_all_pages("/api/v1/hallazgos", extra)

        if not records:
            st.warning("No se encontraron registros de auditoría.")
            return

        df = pd.json_normalize(records)

        # Decodificar entidades HTML en la columna HALLAZGO (e.g. &oacute; → ó)
        if "HALLAZGO" in df.columns:
            df["HALLAZGO"] = df["HALLAZGO"].apply(
                lambda x: html_lib.unescape(str(x)) if pd.notnull(x) else x
            )

        # ── Métricas de resumen ───────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total hallazgos", f"{len(df):,}")
        if "CONFORME" in df.columns:
            c2.metric(
                "No conformidades",
                int(df["CONFORME"].str.contains("No Conformidad", na=False).sum()),
            )
            c3.metric(
                "Observaciones",
                int(df["CONFORME"].str.contains("Observaci", na=False).sum()),
            )
        if "AUD_NOMBRE" in df.columns:
            c4.metric("Auditorías únicas", df["AUD_NOMBRE"].nunique())

        st.dataframe(df, use_container_width=True, height=420)
        show_download_button(df, "auditoria_hallazgos.xlsx", "Hallazgos")
