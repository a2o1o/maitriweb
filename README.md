# Maitri Website

This directory is the website workspace. It is a static multi-page site with no
build step. The current setup and pending work are in
[PROJECT_HANDOFF.md](PROJECT_HANDOFF.md).

- Production: https://www.maitriaspire.org
- Repository: https://github.com/a2o1o/maitriweb

## Local preview

From `C:\Users\anjgu\MaitriSite`, run `python -m http.server 8080` and open
`http://localhost:8080/index.html`. Use another port if 8080 is busy.

## Main files

- `index.html`: homepage
- `impact.html`: stories and reports
- `programs.html`, `partners.html`, `sakhi.html`, `donate.html`,
  `contact.html`: other main pages
- `assets/css/site.css`, `assets/js/site.js`: shared styling and behavior
- `assets/css/instagram.css`, `assets/js/instagram.js`: Instagram section
- `ops/instagram/README.md`: Instagram connection and timer setup
- `report-work/`: editable Maitri report source files and previews (local only)

