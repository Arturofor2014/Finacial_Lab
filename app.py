from pathlib import Path
import re

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent
APP_URL = "https://finaciallab-aa2dclwsudeucdiuhncpdm.streamlit.app"

st.set_page_config(
    page_title="FINACIAL_LAB by Tony | Modelación Financiera",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def build_page(filename: str, section: str = "") -> str:
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

    # Los enlaces entre páginas conservan también la sección de destino.
    html = html.replace('href="cursos.html#inscripcion"', f'href="{APP_URL}/?page=cursos&section=inscripcion" target="_top"')
    html = html.replace('href="index.html#metodo"', f'href="{APP_URL}/?page=inicio&section=metodo" target="_top"')
    html = html.replace('href="index.html#resultados"', f'href="{APP_URL}/?page=inicio&section=resultados" target="_top"')
    html = html.replace('href="cursos.html"', f'href="{APP_URL}/?page=cursos" target="_top"')
    html = html.replace('href="index.html"', f'href="{APP_URL}/?page=inicio" target="_top"')

    if section in {"metodo", "resultados", "inscripcion", "incluye"}:
        scroll_script = f"""
        <script>
          window.addEventListener('load', () => {{
            setTimeout(() => document.getElementById('{section}')?.scrollIntoView(), 150);
          }});
        </script>
        """
        html = html.replace("</body>", f"{scroll_script}</body>")
    return html


page = st.query_params.get("page", "inicio")
section = st.query_params.get("section", "")
filename = "cursos.html" if page == "cursos" else "index.html"

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
# El iframe conserva intactos el diseño, las fuentes, el logo y las animaciones.
components.html(build_page(filename, section), height=900, scrolling=True)
