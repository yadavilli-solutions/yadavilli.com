// Theme toggle. The inline script in head.html applies the saved choice before
// first paint; this file only handles clicks on the toggle.
(function () {
  var root = document.documentElement;
  var button = document.querySelector('[data-theme-toggle]');
  if (!button) return;

  function current() {
    var forced = root.getAttribute('data-theme');
    if (forced === 'light' || forced === 'dark') return forced;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function label() {
    button.setAttribute(
      'aria-label',
      current() === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'
    );
  }

  button.addEventListener('click', function () {
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
    label();
  });

  label();
})();
