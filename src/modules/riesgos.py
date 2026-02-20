"""
riesgos.py
──────────
Módulo de consulta de Control de Riesgos.
Endpoint: GET /api/v1/controlesRiesgo?id_del_sistema_de_gestion_de_riesgos={id}

Permite seleccionar los IDs de sistemas de gestión de riesgos
a consultar y combina todos los resultados en un único DataFrame.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.api.client import KawakClient
from src.utils.exports import show_results
from src.utils.ui import info_box, section_title

_DEFAULT_IDS = [6, 8, 9, 10, 11, 12, 13]


def render(client: KawakClient) -> None:
    section_title("🛡️", "Control de Riesgos")
    info_box(
        "Controles de riesgo por sistema de gestión. "
        "Ingrese los IDs de los sistemas a consultar, separados por coma."
    )

    ids_input: str = st.text_input(
        "IDs de sistemas de gestión de riesgos",
        value=", ".join(map(str, _DEFAULT_IDS)),
        help="Números enteros separados por coma",
    )

    try:
        codigos = [int(x.strip()) for x in ids_input.split(",") if x.strip().isdigit()]
    except Exception:
        codigos = _DEFAULT_IDS

    if not codigos:
        st.warning("Ingrese al menos un ID válido.")
        return

    if st.button("Consultar Riesgos", use_container_width=True):
        dataframes: list[pd.DataFrame] = []
        progress = st.progress(0, text="Iniciando…")

        for i, codigo in enumerate(codigos):
            endpoint = f"/api/v1/controlesRiesgo?id_del_sistema_de_gestion_de_riesgos={codigo}"
            body = client.get(endpoint)
            if body:
                data = body.get("message", {}).get("data", [])
                if data:
                    df = pd.json_normalize(data)
                    df["sistema_id"] = codigo
                    dataframes.append(df)
            progress.progress((i + 1) / len(codigos), text=f"Sistema {codigo}…")

        progress.empty()

        if dataframes:
            show_results(
                pd.concat(dataframes, ignore_index=True),
                "riesgos.xlsx",
                "Riesgos",
            )
        else:
            st.warning("No se encontraron datos de riesgos para los IDs indicados.")
