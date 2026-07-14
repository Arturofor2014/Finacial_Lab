# FINACIAL_LAB by Tony — Curso de Modelación Financiera

Sitio web responsive con una landing page y una página de curso. El mismo repositorio puede publicarse en GitHub Pages o ejecutarse como aplicación en Streamlit Community Cloud.

## Archivos principales

- `index.html`: landing page.
- `cursos.html`: detalle y programa del curso.
- `styles.css`: diseño responsive.
- `script.js`: menú, animaciones y módulos desplegables.
- `app.py`: punto de entrada para Streamlit.
- `requirements.txt`: dependencias de Streamlit.

## Publicar en GitHub

1. Crea un repositorio nuevo en GitHub.
2. Sube todos los archivos de esta carpeta a la raíz del repositorio.
3. En el repositorio, entra a **Settings > Pages**.
4. En **Build and deployment**, selecciona **Deploy from a branch**.
5. Selecciona la rama `main`, la carpeta `/ (root)` y guarda.

GitHub mostrará la dirección pública cuando termine el despliegue.

## Publicar en Streamlit Community Cloud

1. Entra a [share.streamlit.io](https://share.streamlit.io/) con tu cuenta de GitHub.
2. Selecciona **Create app**.
3. Elige el repositorio y la rama `main`.
4. En **Main file path**, escribe `app.py`.
5. Pulsa **Deploy**.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Antes de publicar, reemplaza el correo, el precio y los demás datos provisionales por la información comercial definitiva.
