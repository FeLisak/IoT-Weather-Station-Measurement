// Highlight active nav link based on current path
document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('.navbar-links a');
  links.forEach(link => {
    if (link.getAttribute('href') === window.location.pathname) {
      link.classList.add('active');
    }
  });
});
