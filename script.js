const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('.nav-links');

menuButton?.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.textContent = open ? '×' : '☰';
});

document.querySelectorAll('.nav-links a').forEach(link => link.addEventListener('click', () => {
  menu?.classList.remove('open');
  if (menuButton) {
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.textContent = '☰';
  }
}));

// Streamlit renderiza el sitio dentro de un iframe cuya ruta interna es /~/+/.
// Interceptamos la navegación para que los anclajes se muevan dentro del sitio
// y los cambios de página se abran desde la raíz real de la aplicación.
document.addEventListener('click', event => {
  const link = event.target.closest('a');
  if (!link) return;

  const destination = link.getAttribute('href');
  if (!destination) return;

  if (destination.startsWith('#')) {
    const target = document.getElementById(destination.slice(1));
    if (target) {
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', destination);
    }
    return;
  }

  if (destination.startsWith('?page=')) {
    event.preventDefault();
    window.top.location.href = `/${destination}`;
  }
});

document.querySelectorAll('.module button').forEach(button => {
  button.addEventListener('click', () => button.closest('.module').classList.toggle('open'));
});

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
document.querySelectorAll('#year').forEach(element => element.textContent = new Date().getFullYear());
