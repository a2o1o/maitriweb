(() => {
  const grid = document.querySelector('[data-instagram-feed]');
  if (!grid) return;
  const fallback = document.querySelector('[data-instagram-fallback]');
  fetch('assets/data/instagram/feed.json', { cache: 'no-cache' })
    .then(response => {
      if (!response.ok) throw new Error('Feed unavailable');
      return response.json();
    })
    .then(feed => {
      if (!Array.isArray(feed.posts)) return;
      for (const post of feed.posts.slice(0, 6)) {
        const url = new URL(post.permalink);
        if (url.protocol !== 'https:' || url.hostname !== 'www.instagram.com') continue;
        if (!/^assets\/data\/instagram\/[a-f0-9]+\.(jpg|png|webp)$/.test(post.image)) continue;
        const date = new Date(post.timestamp);
        if (Number.isNaN(date.getTime())) continue;
        const link = document.createElement('a');
        link.className = 'instagram-post';
        link.href = url.href;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        const img = document.createElement('img');
        img.src = post.image;
        img.alt = post.caption ? String(post.caption).slice(0, 180) : 'Maitri community update';
        img.loading = 'lazy';
        img.width = img.height = 600;
        img.addEventListener('error', () => {
          link.remove();
          if (!grid.children.length) { grid.hidden = true; fallback.hidden = false; }
        });
        const caption = document.createElement('p');
        caption.textContent = post.caption || 'View this update on Instagram';
        const time = document.createElement('time');
        time.dateTime = date.toISOString();
        time.textContent = date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Kolkata' });
        link.append(img, caption, time);
        grid.append(link);
      }
      grid.hidden = !grid.children.length;
      fallback.hidden = !!grid.children.length;
    })
    .catch(() => { /* Keep the profile link available when the feed cannot load. */ });
})();
