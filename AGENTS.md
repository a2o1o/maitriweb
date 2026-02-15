# Maitri Web (Static Site) - Developer Notes

This repository is a static HTML/CSS/JS website deployed to a Google Cloud VM.
There is no build step.

## Quick Start (Local)
- Start a local server from the repo root:
  - `powershell -ExecutionPolicy Bypass -File .\\start-local.ps1`
  - Or: `python -m http.server 8080`
- Open `http://localhost:8080/index.html`

## Key Paths
- Pages: `*.html` in repo root (`index.html`, `programs.html`, `impact.html`, etc.)
- Styles: `assets/css/site.css`
- Scripts: `assets/js/site.js`
- Images: `assets/img/`

## Content Conventions
- Always render SakhiAI as: `Sakhi<sup class="ai-sup">AI</sup>`
- Keep copy ASCII-safe where possible (avoid fancy dashes) to prevent encoding/mojibake issues in some Windows flows.

## Deployment (GCP VM)
- VM serves `/var/www/maitriweb` via nginx.
- Typical deploy:
  - `cd /var/www/maitriweb && sudo git pull`
  - `sudo systemctl reload nginx`

## Hygiene
- Do not commit secrets (PATs, login outputs).
- Local screenshot artifacts are ignored via `.gitignore` (`_shots/`).

