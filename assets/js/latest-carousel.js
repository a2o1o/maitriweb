(() => {
  const root = document.querySelector('[data-latest-carousel]');
  if (!root) return;
  const track = root.querySelector('[data-latest-track]');
  const slides = [...track.querySelectorAll('.latest-slide')];
  const controls = root.querySelector('[data-latest-controls]');
  const pause = root.querySelector('[data-latest-pause]');
  const status = root.querySelector('[data-latest-status]');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = motion.matches;
  let visible = false;
  let hovered = false;
  let timer;

  const positions = () => {
    const max = Math.max(0, track.scrollWidth - track.clientWidth);
    const left = track.getBoundingClientRect().left;
    const points = slides.map(slide => Math.min(max, Math.max(0,
      slide.getBoundingClientRect().left - left + track.scrollLeft)));
    return points.filter((point, i) => i === 0 || Math.abs(point - points[i - 1]) > 2);
  };
  const advance = (direction, manual = false) => {
    const points = positions();
    let current = 0;
    points.forEach((point, i) => {
      if (Math.abs(point - track.scrollLeft) < Math.abs(points[current] - track.scrollLeft)) current = i;
    });
    const next = (current + direction + points.length) % points.length;
    track.scrollTo({ left: points[next], behavior: motion.matches ? 'instant' : 'smooth' });
    if (manual) status.textContent = `Community highlights: view ${next + 1} of ${points.length}`;
  };
  const sync = () => {
    clearInterval(timer);
    pause.textContent = paused ? 'Play' : 'Pause';
    pause.setAttribute('aria-label', paused ? 'Play automatic slideshow' : 'Pause automatic slideshow');
    if (!paused && visible && !hovered && !document.hidden && !root.contains(document.activeElement)) {
      timer = setInterval(() => advance(1), 6000);
    }
  };
  root.querySelector('[data-latest-prev]').addEventListener('click', () => { advance(-1, true); sync(); });
  root.querySelector('[data-latest-next]').addEventListener('click', () => { advance(1, true); sync(); });
  pause.addEventListener('click', () => { paused = !paused; sync(); });
  root.addEventListener('mouseenter', () => { hovered = true; sync(); });
  root.addEventListener('mouseleave', () => { hovered = false; sync(); });
  root.addEventListener('focusin', sync);
  root.addEventListener('focusout', () => setTimeout(sync, 0));
  track.addEventListener('pointerdown', () => { paused = true; sync(); }, { passive: true });
  track.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      paused = true;
      advance(event.key === 'ArrowRight' ? 1 : -1, true);
      sync();
    }
  });
  document.addEventListener('visibilitychange', sync);
  motion.addEventListener('change', () => { if (motion.matches) paused = true; sync(); });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }, { threshold: 0.15 });
    observer.observe(root);
  } else {
    visible = true;
  }
  controls.hidden = false;
  sync();
})();
