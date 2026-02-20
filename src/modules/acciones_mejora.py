"""
acciones_mejora.py
──────────────────
Módulo de consulta de Acciones de Mejora.
Endpoint: GET /api/v1/accionesMejora
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.api.client import KawakClient
from src.utils.exports import show_results
from src.utils.ui import info_box, section_title


def render(client: KawakClient) -> None:
    section_title("🚀", "Acciones de Mejora")
    info_box(
        "Consulta las acciones correctivas, preventivas y de mejora "
        "registradas en el sistema Kawak."
    )

    if st.button("Consultar Acciones de Mejora", use_container_width=True):
        with st.spinner("Consultando…"):
            records = client.fetch_all_pages("/api/v1/accionesMejora")

        if records:
            show_results(
                pd.json_normalize(records),
                "acciones_mejora.xlsx",
                "Acciones",
            )
        else:
            st.warning("No se encontraron acciones de mejora.")
