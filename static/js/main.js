// Main interactions: Mobile menu, Alert dismissals, Dynamic UI utilities
document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Toggle
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', navMenu.classList.contains('open'));
    });
  }

  // Flash Alert Auto-Dismissal
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    // Auto dismiss after 6 seconds
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(50px)';
      setTimeout(() => alert.remove(), 400);
    }, 6000);

    // Manual close button
    const closeBtn = alert.querySelector('.alert-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        alert.remove();
      });
    }
  });
});
