"""
documentos.py
─────────────
Módulo de consulta de Gestión Documental.
Endpoint: GET /api/v1/docs
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.api.client import KawakClient
from src.utils.exports import show_results
from src.utils.ui import info_box, section_title


def render(client: KawakClient) -> None:
    section_title("📄", "Gestión Documental")
    info_box(
        "Documentos del Sistema de Gestión registrados en Kawak: "
        "procedimientos, instructivos, formatos y registros."
    )

    if st.button("Consultar Documentos", use_container_width=True):
        with st.spinner("Consultando…"):
            records = client.fetch_all_pages("/api/v1/docs")

        if records:
            show_results(
                pd.json_normalize(records),
                "documentos.xlsx",
                "Documentos",
            )
        else:
            st.warning("No se encontraron documentos.")
