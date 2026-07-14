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
