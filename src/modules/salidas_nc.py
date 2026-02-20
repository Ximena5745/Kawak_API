"""
salidas_nc.py
─────────────
Módulo de consulta de Salidas No Conformes.
Endpoint: GET /api/v1/salidasNoConformes/pool
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.api.client import KawakClient
from src.utils.exports import show_results
from src.utils.ui import info_box, section_title


def render(client: KawakClient) -> None:
    section_title("⚠️", "Salidas No Conformes")
    info_box(
        "Listado de productos o servicios que no cumplen con los requisitos establecidos "
        "en el Sistema de Gestión de Calidad."
    )

    if st.button("Consultar Salidas No Conformes", use_container_width=True):
        with st.spinner("Consultando…"):
            records = client.fetch_all_pages("/api/v1/salidasNoConformes/pool")

        if records:
            show_results(
                pd.json_normalize(records),
                "salidas_no_conformes.xlsx",
                "SNC",
            )
        else:
            st.warning("No se encontraron salidas no conformes.")
