from pathlib import Path
import re

import streamlit as st


ROOT = Path(__file__).parent

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
        "",
        html,
    )

    # st.html renderiza directamente en la aplicación (sin iframe). Las
    # animaciones y acordeones se muestran abiertos porque Streamlit no ejecuta
    # JavaScript dentro del HTML por seguridad.
    html = html.replace(
        "</head>",
        """
        <style>
          .reveal { opacity: 1 !important; transform: none !important; }
          .module-content { display: block !important; }
          .module button > strong { display: none; }
        </style>
        </head>
        """,
    )

    # Los enlaces entre páginas conservan también la sección de destino.
    html = html.replace('href="cursos.html#inscripcion"', 'href="/?page=cursos&section=inscripcion" target="_top"')
    html = html.replace('href="index.html#metodo"', 'href="/?page=inicio&section=metodo" target="_top"')
    html = html.replace('href="index.html#resultados"', 'href="/?page=inicio&section=resultados" target="_top"')
    html = html.replace('href="cursos.html"', 'href="/?page=cursos" target="_top"')
    html = html.replace('href="index.html"', 'href="/?page=inicio" target="_top"')

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
    </style>
    """,
    unsafe_allow_html=True,
)
# Renderizado directo, sin la ruta interna /~/+/. De esta manera todos los
# enlaces del encabezado y los llamados a la acción navegan en la app principal.
st.html(build_page(filename, section))
