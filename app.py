from pathlib import Path
import re
from urllib.parse import quote

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
    html = html.replace('href="cursos.html#inscripcion"', f'href="{APP_URL}/?page=inscripcion" target="_blank"')
    html = html.replace('href="index.html#metodo"', f'href="{APP_URL}/?page=inicio&section=metodo" target="_top"')
    html = html.replace('href="index.html#resultados"', f'href="{APP_URL}/?page=inicio&section=resultados" target="_top"')
    html = html.replace('href="cursos.html"', f'href="{APP_URL}/?page=cursos" target="_top"')
    html = html.replace('href="index.html"', f'href="{APP_URL}/?page=inicio" target="_top"')

    # Llamados de inscripción: abren la página nativa controlada por Python.
    html = html.replace(
        'href="mailto:contacto@financialab.com?subject=Inscripción%20curso%20Modelación%20Financiera"',
        f'href="{APP_URL}/?page=inscripcion" target="_blank"',
    )
    html = html.replace(
        'href="#inscripcion">Inscribirme al curso',
        f'href="{APP_URL}/?page=inscripcion" target="_blank">Inscribirme al curso',
    )
    html = html.replace(
        f'href="{APP_URL}/?page=cursos" target="_top">Comenzar ahora',
        f'href="{APP_URL}/?page=inscripcion" target="_blank">Comenzar ahora',
    )

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


def render_registration() -> None:
    """Formulario nativo: Python procesa los datos y crea el enlace privado."""
    st.markdown(
        """
        <style>
          .block-container {max-width: 1080px !important; padding: 2.2rem 1.5rem 5rem !important;}
          [data-testid="stForm"] {background:#0b2136;border:1px solid rgba(255,255,255,.14);padding:2rem;border-top:4px solid #82b92b;}
          h1,h2,h3,label,p {color:#fff !important;}
          .register-brand {color:#82b92b;font-weight:800;letter-spacing:.08em;margin-bottom:2.5rem;}
          .register-brand small {display:block;color:#aab5c0;font-weight:500;letter-spacing:.12em;}
          .register-hero {padding:2rem 0 1.5rem;}
          .register-hero h1 {font-size:clamp(2.6rem,7vw,5.7rem);line-height:1;text-transform:uppercase;margin:.5rem 0 1rem;}
          .register-hero h1 span {color:#82b92b;}
          .price-box {background:#82b92b;color:#061426;padding:1rem 1.3rem;margin:1.5rem 0 2rem;font-weight:700;}
          div.stButton > button, a[data-testid="stLinkButton"] {background:#82b92b !important;color:#061426 !important;border:0 !important;font-weight:800 !important;}
        </style>
        <a href="/?page=inicio" target="_self" style="color:#a9da4d;text-decoration:none">← Volver al inicio</a>
        <div class="register-brand">FINACIAL_LAB <small>by Tony</small></div>
        <div class="register-hero">
          <div style="color:#a9da4d;font-weight:700;letter-spacing:.12em">INSCRIPCIÓN AL CURSO</div>
          <h1>Modelación financiera<br><span>con rigor.</span></h1>
          <p>Completa tus datos. Python preparará tu solicitud y podrás continuar la conversación directamente con Tony por WhatsApp.</p>
        </div>
        <div class="price-box">ACCESO COMPLETO · US$ 149 · PAGO COORDINADO PERSONALMENTE</div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("registration_form"):
        name = st.text_input("Nombre completo *", placeholder="Escribe tu nombre")
        email = st.text_input("Correo electrónico *", placeholder="nombre@correo.com")
        phone = st.text_input("Número de WhatsApp", placeholder="Ejemplo: +57 300 000 0000")
        interest = st.selectbox(
            "Principal objetivo",
            ["Presentar un proyecto a inversionistas", "Evaluar una inversión", "Mejorar mis habilidades financieras", "Otro"],
        )
        accepted = st.checkbox("Autorizo el uso de estos datos para gestionar mi solicitud de inscripción.")
        submitted = st.form_submit_button("Preparar mi inscripción")

    if submitted:
        if not name.strip() or not email.strip() or not accepted:
            st.error("Completa nombre, correo y la autorización para continuar.")
            return

        try:
            whatsapp_number = st.secrets.get("WHATSAPP_NUMBER", "")
        except Exception:
            whatsapp_number = ""
        message = (
            f"Hola Tony, quiero inscribirme al curso de Modelación Financiera.\n\n"
            f"Nombre: {name.strip()}\nCorreo: {email.strip()}\n"
            f"WhatsApp: {phone.strip() or 'No indicado'}\nObjetivo: {interest}"
        )
        st.success("Tu solicitud está lista.")
        if whatsapp_number:
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={quote(message)}"
            st.link_button("Continuar en WhatsApp ↗", whatsapp_url, type="primary", use_container_width=True)
        else:
            st.warning("Falta configurar WHATSAPP_NUMBER en los Secrets de Streamlit.")
            st.code(message, language=None)


if page == "inscripcion":
    render_registration()
    st.stop()

# El iframe conserva intactos el diseño, las fuentes, el logo y las animaciones.
components.html(build_page(filename, section), height=900, scrolling=True)
