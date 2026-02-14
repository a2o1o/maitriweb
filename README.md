# Maitri Website (Static Site)

This repo is a static, multi-page website intended to be served from a Google Cloud VM (nginx recommended).

## Local Preview

From PowerShell:

```powershell
cd C:\Users\anjgu\MaitriSite
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Deploy (Nginx Example)

1. Copy the contents of this folder to your VM (e.g. `/var/www/maitri`).
2. Configure nginx to serve that directory.

Example server block (adjust domain + paths):

```nginx
server {
  listen 80;
  server_name maitriaspire.org www.maitriaspire.org;

  root /var/www/maitri;
  index index.html;

  location / {
    try_files $uri $uri/ =404;
  }
}
```

## Editing Content

Pages:
- `index.html` (Home)
- `programs.html`
- `impact.html`
- `sakhi.html`
- `partners.html`
- `donate.html`
- `recognition.html`
- `contact.html`

Global styles: `assets/css/site.css`  
Global JS: `assets/js/site.js`

