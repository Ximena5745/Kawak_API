"""
ui.py
─────
Componentes de interfaz reutilizables:
  - CSS empresarial (inject_css)
  - Header principal (render_header)
  - Sidebar con navegación (render_sidebar)
  - Footer institucional (render_footer)
  - Helpers de secciones (section_title, info_box)
"""

import streamlit as st

# ─── CSS corporativo ──────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2137 0%, #1a3a5c 100%);
    border-right: 3px solid #2a4a6b;
}
section[data-testid="stSidebar"] * { color: #f0f4f8 !important; }
section[data-testid="stSidebar"] .stRadio label {
    color: #b0c4d8 !important;
    font-size: 0.85rem;
    font-weight: 500;
}

/* ── Header principal ── */
.main-header {
    background: linear-gradient(135deg, #0d2137 0%, #1a3a5c 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(13,33,55,.3);
}
.main-header h1 { color:#fff !important; font-size:1.8rem; font-weight:700; margin:0; }
.main-header p  { color:#b0c4d8 !important; font-size:.9rem; margin:.2rem 0 0 0; }

/* ── Títulos de sección ── */
.section-title {
    color: #1a3a5c;
    font-size: 1.2rem;
    font-weight: 600;
    border-bottom: 2px solid #2563eb;
    padding-bottom: .5rem;
    margin-bottom: 1rem;
}

/* ── Caja informativa ── */
.info-box {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    border-radius: 0 8px 8px 0;
    padding: .8rem 1rem;
    margin: .5rem 0;
    color: #1e40af;
    font-size: .88rem;
}

/* ── Badge de estado ── */
.badge-ok {
    background: #dcfce7; color: #166534;
    padding: .2rem .7rem; border-radius: 20px;
    font-size: .78rem; font-weight: 600;
}

/* ── Botones ── */
.stButton > button {
    background: linear-gradient(135deg,#1a3a5c,#2563eb) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; padding: .6rem 2rem !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(26,58,92,.3) !important;
    transition: all .2s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; }

/* ── Footer ── */
.footer {
    text-align: center; color: #94a3b8; font-size: .78rem;
    padding: 1.5rem 0 .5rem 0;
    border-top: 1px solid #e2e8f0; margin-top: 2rem;
}
</style>
"""

# ─── Menú de navegación ───────────────────────────────────────────────────────
_MENU: dict[str, str] = {
    "📈 Indicadores":           "Indicadores",
    "🔍 Auditorías":            "Auditoria",
    "⚠️ Salidas No Conformes":  "SNC",
    "🚀 Acciones de Mejora":    "Mejora",
    "📄 Documentos":            "Documentos",
    "🛡️ Riesgos":               "Riesgos",
}


# ─── Funciones públicas ───────────────────────────────────────────────────────

def inject_css() -> None:
    """Inyecta los estilos CSS corporativos en la aplicación."""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header() -> None:
    """Renderiza el encabezado institucional."""
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1>Portal Kawak</h1>
                <p>Consulta integrada del Sistema de Gestión de Calidad · Poligran</p>
            </div>
            <div style="font-size:3rem;opacity:.8;">📊</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(instancia: str) -> str:
    """
    Renderiza el sidebar con logo, estado de conexión y navegación.
    Devuelve la clave interna del módulo seleccionado.
    """
    with st.sidebar:
        # Identidad institucional
        st.markdown(
            """
            <div style="text-align:center;padding:1rem 0 1.5rem 0;">
                <div style="font-size:2.5rem;">🏛️</div>
                <div style="font-size:1.1rem;font-weight:700;color:#fff;letter-spacing:.05em;">POLIGRAN</div>
                <div style="font-size:.75rem;color:#b0c4d8;margin-top:.2rem;">Sistema de Gestión de Calidad</div>
            </div>
            <hr style="border-color:#2a4a6b;margin-bottom:1rem;">
            """,
            unsafe_allow_html=True,
        )

        # Badge de conexión
        if "token" in st.session_state:
            st.markdown(
                f'<div style="text-align:center;margin-bottom:1rem;">'
                f'<span class="badge-ok">● Conectado</span>'
                f'<div style="font-size:.72rem;color:#94a3b8;margin-top:.3rem;">'
                f'Sesión: {st.session_state.get("login_time", "--:--")}</div></div>',
                unsafe_allow_html=True,
            )

        # Navegación
        st.markdown(
            '<div style="font-size:.75rem;color:#b0c4d8;font-weight:600;'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:.5rem;">Módulos</div>',
            unsafe_allow_html=True,
        )
        selection = st.radio("nav", list(_MENU.keys()), label_visibility="collapsed")

        # Info de instancia + renovar sesión
        st.markdown("<hr style='border-color:#2a4a6b;margin-top:1rem;'>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:.72rem;color:#6b8fb5;text-align:center;">'
            f'Instancia: <strong style="color:#60a5fa">{instancia}</strong></div>',
            unsafe_allow_html=True,
        )
        if st.button("🔄 Renovar sesión", use_container_width=True):
            st.session_state.pop("token",      None)
            st.session_state.pop("login_time", None)
            st.rerun()

    return _MENU[selection]


def render_footer(year: int) -> None:
    """Renderiza el pie de página institucional."""
    st.markdown(
        f'<div class="footer">Portal Kawak · '
        f'Institución Universitaria Politécnico Grancolombiano · {year}</div>',
        unsafe_allow_html=True,
    )


def section_title(icon: str, title: str) -> None:
    """Título estilizado para cada sección."""
    st.markdown(f'<p class="section-title">{icon} {title}</p>', unsafe_allow_html=True)


def info_box(text: str) -> None:
    """Caja de información azul."""
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)
