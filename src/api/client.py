"""
client.py
─────────
Cliente HTTP centralizado para la API Kawak.

Uso:
    client = KawakClient(token, base_url)
    records = client.fetch_all_pages("/api/v1/hallazgos")
    body    = client.post("/api/v1/indicadores/result", payload)
"""

from __future__ import annotations

import json
import requests
import streamlit as st


class KawakClient:
    """Encapsula todas las llamadas a la API Kawak."""

    def __init__(self, token: str, base_url: str) -> None:
        self.token    = token
        self.base_url = base_url.rstrip("/")

    # ── Encabezados ─────────────────────────────────────────────────────────
    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": self.token,
            "Content-Type":  "application/json",
            "Accept":        "application/json",
        }

    # ── Métodos HTTP base ────────────────────────────────────────────────────
    def get(
        self,
        endpoint: str,
        params:   dict | None = None,
        timeout:  int         = 30,
    ) -> dict | None:
        """GET genérico. Devuelve el JSON parseado o None si hay error."""
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as exc:
            st.warning(f"Error GET `{endpoint}`: {exc}")
            return None

    def post(
        self,
        endpoint: str,
        payload:  dict,
        timeout:  int = 30,
    ) -> dict | None:
        """POST genérico. Devuelve el JSON parseado o None si hay error / 500."""
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.post(
                url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=timeout,
            )
            if resp.status_code == 500:
                return None
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as exc:
            st.warning(f"Error POST `{endpoint}`: {exc}")
            return None

    # ── Paginación automática ────────────────────────────────────────────────
    def fetch_all_pages(
        self,
        endpoint:     str,
        extra_params: dict | None = None,
    ) -> list[dict]:
        """
        Recorre todas las páginas de un endpoint paginado y devuelve
        todos los registros concatenados.

        Espera respuestas con la estructura:
            { "message": { "pagination": { "totalPages": N }, "data": [...] } }
        """
        all_records: list[dict] = []
        npage       = 1
        total_pages = 1
        progress    = st.progress(0, text="Descargando página 1…")

        while npage <= total_pages:
            params: dict = {"page": npage}
            if extra_params:
                params.update(extra_params)

            body = self.get(endpoint, params=params)
            if not body or "message" not in body or "data" not in body["message"]:
                break

            pagination  = body["message"].get("pagination", {})
            total_pages = pagination.get("totalPages", 1)
            records     = body["message"]["data"]

            if records:
                all_records.extend(records)

            progress.progress(
                min(npage / total_pages, 1.0),
                text=f"Página {npage} de {total_pages}…",
            )
            npage += 1

        progress.empty()
        return all_records
