from pathlib import Path
import re

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent

st.set_page_config(
    page_title="FinanciaLab | Modelación Financiera",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def build_page(filename: str) -> str:
    """Carga la web estática e integra CSS y JavaScript para Streamlit."""
    html = (ROOT / filename).read_text(encoding="utf-8")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    javascript = (ROOT / "script.js").read_text(encoding="utf-8")

    html = re.sub(
        r'<link rel="stylesheet" href="styles\.css">',
        f"<style>{css}</style>",
        html,
    )
    html = re.sub(
        r'<script src="script\.js"></script>',
        f"<script>{javascript}</script>",
        html,
    )

    # Los enlaces entre archivos se convierten en rutas de la app Streamlit.
    html = html.replace('href="cursos.html"', 'href="?page=cursos" target="_top"')
    html = html.replace('href="index.html"', 'href="?page=inicio" target="_top"')
    return html


page = st.query_params.get("page", "inicio")
filename = "cursos.html" if page == "cursos" else "index.html"

# El contenido es largo; la altura evita una barra de desplazamiento interna.
page_height = 4550 if filename == "cursos.html" else 4300

st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .stApp {background: #061426;}
      .block-container {padding: 0; max-width: 100%;}
      iframe {display: block;}
    </style>
    """,
    unsafe_allow_html=True,
)
components.html(build_page(filename), height=page_height, scrolling=False)
