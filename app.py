from pathlib import Path
import re

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent
APP_URL = "https://finaciallab-aa2dclwsudeucdiuhncpdm.streamlit.app"
WHATSAPP_URL = "https://wa.me/qr/5IDLUU54GZORE1"

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
    html = html.replace('href="cursos.html#inscripcion"', f'href="{APP_URL}/?page=inscripcion" target="_top"')
    html = html.replace('href="index.html#metodo"', f'href="{APP_URL}/?page=inicio&section=metodo" target="_top"')
    html = html.replace('href="index.html#resultados"', f'href="{APP_URL}/?page=inicio&section=resultados" target="_top"')
    html = html.replace('href="cursos.html"', f'href="{APP_URL}/?page=cursos" target="_top"')
    html = html.replace('href="index.html"', f'href="{APP_URL}/?page=inicio" target="_top"')

    # Llamados de inscripción: abren la página nativa controlada por Python.
    html = html.replace(
        'href="mailto:contacto@financialab.com?subject=Inscripción%20curso%20Modelación%20Financiera"',
        f'href="{APP_URL}/?page=inscripcion" target="_top"',
    )
    html = html.replace(
        'href="#inscripcion">Inscribirme al curso',
        f'href="{APP_URL}/?page=inscripcion" target="_top">Inscribirme al curso',
    )
    html = html.replace(
        f'href="{APP_URL}/?page=cursos" target="_top">Comenzar ahora',
        f'href="{APP_URL}/?page=inscripcion" target="_top">Comenzar ahora',
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
    """Formulario nativo con la misma identidad visual de la landing."""
    st.markdown(
        """
        <style>
          .block-container {max-width:1300px !important;padding:1.4rem 3rem 5rem !important;}
          [data-testid="stForm"] {background:#fff;border:0;padding:2rem;box-shadow:0 24px 70px rgba(0,0,0,.28);border-top:5px solid #82b92b;}
          [data-testid="stForm"] label,[data-testid="stForm"] p {color:#15202a !important;}
          .register-header {display:flex;align-items:center;justify-content:space-between;padding:.2rem 0 2.2rem;border-bottom:1px solid rgba(255,255,255,.14);}
          .register-brand {color:#fff;font-size:1.2rem;font-weight:800;letter-spacing:.08em;line-height:1;}
          .register-brand b {color:#82b92b;}.register-brand small {display:block;color:#aab5c0;font-size:.58rem;font-weight:500;letter-spacing:.16em;margin-top:.35rem;}
          .back-link {color:#cbd3db !important;text-decoration:none;font-size:.85rem;}.back-link:hover{color:#a9da4d !important;}
          .register-hero {padding:4.5rem 2.5rem 2rem 0;}
          .register-kicker {color:#a9da4d;font-size:.78rem;font-weight:800;letter-spacing:.14em;}
          .register-hero h1 {color:#fff !important;font-size:clamp(3.2rem,6vw,6.3rem);line-height:.98;text-transform:uppercase;margin:1.2rem 0 1.5rem;letter-spacing:-.03em;}
          .register-hero h1 span {color:#82b92b;}
          .register-hero p {color:#bdc6cf !important;font-size:1.05rem;max-width:620px;}
          .benefit {display:flex;gap:.8rem;color:#fff;margin:1.1rem 0;font-size:.92rem}.benefit b{display:grid;place-items:center;min-width:26px;height:26px;border:1px solid #82b92b;border-radius:50%;color:#82b92b;}
          .form-title {background:#82b92b;color:#061426;padding:1.1rem 1.4rem;font-weight:800;margin:3rem 0 0;letter-spacing:.04em;}
          .price-line {display:flex;justify-content:space-between;align-items:end;background:#0b2136;padding:1.1rem 1.4rem;color:#fff}.price-line strong{font-size:2rem}.price-line span{font-size:.72rem;color:#aab5c0;}
          div.stButton > button, a[data-testid="stLinkButton"] {background:#82b92b !important;color:#061426 !important;border:0 !important;font-weight:800 !important;}
          @media(max-width:700px){.block-container{padding:1rem 1rem 4rem!important}.register-header{padding-bottom:1rem}.register-hero{padding:2.5rem 0 1rem}.register-hero h1{font-size:3.2rem}.form-title{margin-top:1rem}}
        </style>
        <div class="register-header">
          <div class="register-brand">FINACIAL_<b>LAB</b><small>by Tony</small></div>
          <a class="back-link" href="/?page=inicio" target="_self">← Volver al inicio</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.18, .82], gap="large")
    with left:
        st.markdown(
            """
            <div class="register-hero">
              <div class="register-kicker">● INSCRIPCIÓN AL CURSO</div>
              <h1>Modelación financiera<br><span>con rigor.</span></h1>
              <p>Da el siguiente paso para construir modelos que demuestran viabilidad, generan confianza y convencen a inversionistas.</p>
              <div class="benefit"><b>✓</b><span>Acceso al curso completo y materiales editables.</span></div>
              <div class="benefit"><b>✓</b><span>Acompañamiento directo para coordinar tu inscripción.</span></div>
              <div class="benefit"><b>✓</b><span>Pago acordado personalmente con Tony por WhatsApp.</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="form-title">ACCESO COMPLETO</div><div class="price-line"><strong>US$ 149</strong><span>PAGO ÚNICO</span></div>', unsafe_allow_html=True)
        with st.form("registration_form"):
            name = st.text_input("Nombre completo *", placeholder="Escribe tu nombre")
            email = st.text_input("Correo electrónico *", placeholder="nombre@correo.com")
            phone = st.text_input("Número de WhatsApp", placeholder="Ejemplo: +57 300 000 0000")
            interest = st.selectbox(
                "Principal objetivo",
                ["Presentar un proyecto a inversionistas", "Evaluar una inversión", "Mejorar mis habilidades financieras", "Otro"],
            )
            accepted = st.checkbox("Autorizo el uso de estos datos para gestionar mi solicitud.")
            submitted = st.form_submit_button("Preparar mi inscripción", use_container_width=True)

    if submitted:
        if not name.strip() or not email.strip() or not accepted:
            st.error("Completa nombre, correo y la autorización para continuar.")
            return

        st.success("Tu solicitud está lista.")
        st.caption(f"Inscripción preparada para {name.strip()} · {interest}")
        st.link_button("Continuar en WhatsApp ↗", WHATSAPP_URL, type="primary", use_container_width=True)


if page == "inscripcion":
    render_registration()
    st.stop()

# El iframe conserva intactos el diseño, las fuentes, el logo y las animaciones.
components.html(build_page(filename, section), height=900, scrolling=True)
