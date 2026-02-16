(() => {
  // Used by CSS to apply animations only when JS is running.
  document.documentElement.classList.add('js');

  const topbar = document.querySelector('.topbar');
  const hamb = document.querySelector('[data-hamb]');
  if (hamb && topbar) {
    hamb.addEventListener('click', () => {
      const open = topbar.classList.toggle('open');
      hamb.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  const path = (location.pathname || '').toLowerCase();
  const file = path.split('/').pop() || 'index.html';
  document.querySelectorAll('nav a[data-nav]').forEach((a) => {
    const href = (a.getAttribute('href') || '').toLowerCase();
    if (href === file) a.classList.add('active');
  });

  const els = Array.from(document.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in window && els.length) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      }
    }, { threshold: 0.12 });

    els.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min(i * 45, 220)}ms`;
      io.observe(el);
    });
  } else {
    els.forEach((el) => el.classList.add('in'));
  }

  // Lightweight carousel used on Programs -> "How Maitri works".
  const carousel = document.querySelector('[data-how-carousel]');
  if (carousel) {
    const track = carousel.querySelector('[data-how-track]');
    const slides = track ? Array.from(track.querySelectorAll('.how-slide')) : [];
    const prev = carousel.querySelector('[data-how-prev]');
    const next = carousel.querySelector('[data-how-next]');

    if (track && slides.length > 1) {
      let idx = 0;
      let timer = null;

      const clamp = (n) => {
        if (n < 0) return slides.length - 1;
        if (n >= slides.length) return 0;
        return n;
      };

      const render = () => {
        track.style.transform = `translateX(-${idx * 100}%)`;
      };

      const go = (n) => {
        idx = clamp(n);
        render();
      };

      const start = () => {
        if (timer) clearInterval(timer);
        timer = setInterval(() => go(idx + 1), 4000);
      };

      const stop = () => {
        if (timer) {
          clearInterval(timer);
          timer = null;
        }
      };

      if (prev) prev.addEventListener('click', () => { go(idx - 1); start(); });
      if (next) next.addEventListener('click', () => { go(idx + 1); start(); });

      carousel.addEventListener('mouseenter', stop);
      carousel.addEventListener('mouseleave', start);
      carousel.addEventListener('focusin', stop);
      carousel.addEventListener('focusout', start);

      render();
      start();
    }
  }
})();


