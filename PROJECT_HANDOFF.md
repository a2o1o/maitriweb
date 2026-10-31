# Maitri Website Handoff

This file keeps the website context inside the project so a new chat opened at
`C:\Users\anjgu\MaitriSite` has a reliable starting point. The former
`C:\Windows\System32` working directory is not the website workspace.

## Current site

- Static HTML/CSS/JS; no framework or build step.
- Git remote: `git@github.com:a2o1o/maitriweb.git`, branch `main`.
- Production: https://www.maitriaspire.org, nginx on GCP VM `polymarket-vm-ca`
  (`northamerica-northeast1-a`, project `folkloric-rite-95004`).
- VM checkout: `/var/www/maitriweb`.
- Keep `Sakhi<sup class="ai-sup">AI</sup>` markup and existing visual language.

## Recent website work

- Testimonial photos have a square wrapper, `object-fit: cover`, and circular
  clipping in `assets/css/site.css` (`37b7463`).
- The April-June 2026 quarterly PDF is in `assets/reports/2026/` and linked
  from `impact.html` (`630576a`). It was verified live after deployment.
- The homepage has a "Latest from Maitri" link and section (`135418d`).
  `assets/js/instagram.js` reads a public cache; `ops/instagram/sync.py` can
  refresh six posts and cache their images. The systemd timer is configured
  for Monday and Thursday at 09:00 Asia/Kolkata.

## Instagram connection still needed

The Instagram account is `@maitri_aspiring_together` (Creator). The homepage
currently shows a direct profile link. The service code is installed on the VM,
but the account was not connected and the timer was disabled at the last check.
The owner must create a Meta developer app using Instagram API with Instagram
Login and grant `instagram_business_basic`. Follow
[ops/instagram/README.md](ops/instagram/README.md) to add a long-lived token
privately on the VM, run the first sync, and enable the timer. Never put the
token in chat, Git, or a web-served file.

## Deployment

After committing and pushing website changes, deploy from a reusable CMD session:

```cmd
call "C:\Users\anjgu\tools\google-cloud-sdk\bin\gcloud.cmd" compute ssh polymarket-vm-ca --zone northamerica-northeast1-a --project folkloric-rite-95004 --ssh-key-file="C:\Users\anjgu\MaitriSite\_gcloud_tmp_ssh" --ssh-flag="-batch" --command "cd /var/www/maitriweb && sudo git pull --ff-only && sudo nginx -t && sudo systemctl reload nginx"
```

## Worktree and source material

The local worktree had a pre-existing change in `assets/css/site.css` and
untracked image, key, and `.gitkeep` files at the last check. Inspect `git
status` before editing; do not discard or commit unrelated files by default.
The `_gcloud_tmp_ssh` key is local deployment material, not a site asset.

The broader Maitri image library is at
`C:\Users\anjgu\Documents\LMFI\Maitri\website`. Curated candidates and a
manifest are under its `_site_candidates` directory. These are source
materials outside the website repo; copy only selected assets into
`assets/img/` when they are used on the site.

## Working here in future chats

Open `C:\Users\anjgu\MaitriSite` as the Codex project/workspace before
starting a new website chat. The saved global Codex instructions specify one
reusable CMD session for commands to avoid flashing terminal windows.
The conversation transcript itself cannot be moved by moving files; this
handoff preserves the operational context in the project.
