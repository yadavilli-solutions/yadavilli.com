// Header scroll effect
const header = document.getElementById('site-header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 20);
}, { passive: true });

// Mobile nav toggle
const navToggle = document.getElementById('nav-toggle');
const navMobile = document.getElementById('nav-mobile');
navToggle?.addEventListener('click', () => {
  navMobile.classList.toggle('open');
  navToggle.classList.toggle('open');
});

// Fade-up on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 80);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0, rootMargin: '0px 0px -20px 0px' });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

// Safety net. A background tab freezes IntersectionObserver, so a page loaded
// out of view can be scrolled while every section is still at opacity 0. Sweep
// anything on screen that the observer has not reached: once after load, and
// again whenever the tab comes back into view.
const revealOnScreen = () => {
  document.querySelectorAll('.fade-up:not(.visible)').forEach(el => {
    const box = el.getBoundingClientRect();
    if (box.top < window.innerHeight && box.bottom > 0) el.classList.add('visible');
  });
};

window.addEventListener('load', () => setTimeout(revealOnScreen, 1200));
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) setTimeout(revealOnScreen, 100);
});

// Animated stat counters
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseInt(el.dataset.count);
    const duration = 1800;
    const start = performance.now();
    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(ease * target);
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target;
    };
    requestAnimationFrame(tick);
    countObserver.unobserve(el);
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-count]').forEach(el => countObserver.observe(el));
