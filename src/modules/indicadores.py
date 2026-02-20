"""
indicadores.py
──────────────
Módulo de consulta de Indicadores de Gestión.
Permite seleccionar años, meses de corte y frecuencias,
y descarga todos los registros paginados.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from datetime import datetime

from src.api.client import KawakClient
from src.config import ALL_YEARS, DATES_BY_YEAR, FREQUENCIES
from src.utils.exports import show_results
from src.utils.ui import info_box, section_title


def render(client: KawakClient) -> None:
    section_title("📈", "Indicadores de Gestión")
    info_box(
        "Seleccione los años y meses de corte para consultar "
        "los resultados de indicadores por frecuencia."
    )

    # ── Selección de años ────────────────────────────────────────────────────
    col_a, col_b = st.columns([1, 2])
    with col_a:
        selected_years: list[str] = st.multiselect(
            "Años",
            options=ALL_YEARS,
            default=[str(datetime.now().year)],
            help="Puede seleccionar múltiples años",
        )

    if not selected_years:
        st.warning("Seleccione al menos un año para continuar.")
        return

    # ── Selección de meses ───────────────────────────────────────────────────
    all_entries: list[tuple[str, str]] = []
    for y in selected_years:
        all_entries.extend(DATES_BY_YEAR[y])

    labels = [e[0] for e in all_entries]
    values = [e[1] for e in all_entries]

    with col_b:
        selected_labels: list[str] = st.multiselect(
            "Meses de corte",
            options=labels,
            default=labels[:1],
            help="Seleccione uno o más meses de corte",
        )

    if not selected_labels:
        st.warning("Seleccione al menos un mes de corte.")
        return

    selected_dates = [values[labels.index(lbl)] for lbl in selected_labels]

    # ── Selección de frecuencias ─────────────────────────────────────────────
    selected_freqs: list[int] = st.multiselect(
        "Frecuencias de medición",
        options=list(FREQUENCIES.keys()),
        default=list(FREQUENCIES.keys()),
        format_func=lambda x: FREQUENCIES[x],
    )

    if not selected_freqs:
        st.warning("Seleccione al menos una frecuencia.")
        return

    # ── Consulta ─────────────────────────────────────────────────────────────
    if st.button("Consultar Indicadores", use_container_width=True):
        all_data: list[pd.DataFrame] = []
        total = len(selected_dates) * len(selected_freqs)
        bar   = st.progress(0, text="Iniciando consulta…")
        done  = 0

        for ff in selected_dates:
            for f in selected_freqs:
                npage = 1
                while True:
                    body = client.post(
                        "/api/v1/indicadores/result",
                        {"cutoffDate": ff, "frequency": f, "page": npage},
                    )
                    if not body or "message" not in body or "data" not in body["message"]:
                        break
                    records = body["message"]["data"]
                    if not records:
                        break
                    df_page = pd.json_normalize(records)
                    df_page["frecuencia"]  = FREQUENCIES[f]
                    df_page["fecha_corte"] = ff
                    all_data.append(df_page)
                    npage += 1

                done += 1
                bar.progress(done / total, text=f"Procesando {ff} — {FREQUENCIES[f]}…")

        bar.empty()

        if all_data:
            show_results(
                pd.concat(all_data, ignore_index=True),
                "indicadores_kawak.xlsx",
                "Indicadores",
            )
        else:
            st.warning("Sin datos para las fechas y frecuencias seleccionadas.")
