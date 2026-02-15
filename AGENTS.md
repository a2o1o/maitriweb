# Agent Instructions

## Skills

A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. Below is the list of skills that can be used. Each entry includes a name, description, and file path so you can open the source for full instructions when using a specific skill.

### Available skills

- `skill-creator`: Guide for creating effective skills. Use when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations. (file: `C:/Users/anjgu/.codex/skills/.system/skill-creator/SKILL.md`)
- `skill-installer`: Install Codex skills into `$CODEX_HOME/skills` from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, or install a skill from another repo (including private repos). (file: `C:/Users/anjgu/.codex/skills/.system/skill-installer/SKILL.md`)

### How to use skills

- Discovery: The list above is the skills available in this session (name + description + file path). Skill bodies live on disk at the listed paths.
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. Multiple mentions mean use them all. Do not carry skills across turns unless re-mentioned.
- Missing/blocked: If a named skill isn't in the list or the path can't be read, say so briefly and continue with the best fallback.
- How to use a skill (progressive disclosure):
  1. After deciding to use a skill, open its `SKILL.md`. Read only enough to follow the workflow.
  2. When `SKILL.md` references relative paths (e.g., `scripts/foo.py`), resolve them relative to the skill directory listed above first, and only consider other paths if needed.
  3. If `SKILL.md` points to extra folders such as `references/`, load only the specific files needed for the request; don't bulk-load everything.
  4. If `scripts/` exist, prefer running or patching them instead of retyping large code blocks.
  5. If `assets/` or templates exist, reuse them instead of recreating from scratch.
- Coordination and sequencing:
  - If multiple skills apply, choose the minimal set that covers the request and state the order you'll use them.
  - Announce which skill(s) you're using and why (one short line). If you skip an obvious skill, say why.
- Context hygiene:
  - Keep context small: summarize long sections instead of pasting them; only load extra files when needed.
  - Avoid deep reference-chasing: prefer opening only files directly linked from `SKILL.md` unless you're blocked.
  - When variants exist (frameworks, providers, domains), pick only the relevant reference file(s) and note that choice.
- Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue.

# Maitri Website Handoff Note (For Dev/Designer)

## What This Is

- Static multi-page site for Maitri (no build step).
- Repo: `https://github.com/a2o1o/maitriweb` (branch `main`)
- Production: `https://www.maitriaspire.org` served from a Google Cloud VM via nginx.

## Local Workspace

- Local code folder: `C:\Users\anjgu\MaitriSite`
- Key files:
  - `index.html` (homepage)
  - `programs.html`, `impact.html`, `partners.html`, `recognition.html`, `sakhi.html`, `donate.html`, `contact.html`
  - CSS: `assets/css/site.css`
  - JS: `assets/js/site.js`
  - Images: `assets/img/` (includes hero + partner/recognition logos in `assets/img/logos/`)

## Branding + Copy Requirements Already Implemented

- Maitri logo + palette applied globally (logo file used in header is referenced from `assets/img/`).
- SakhiAI styling: use `Sakhi<sup class="ai-sup">AI</sup>` (do not write plain "Sakhi AI").
- Homepage hero headline updated to:
  - A bridge for successful school to work transition
  - for girls from govt schools in Delhi
  (in `C:\Users\anjgu\MaitriSite\index.html`)

## Layout Decisions / UX

- Evidence-led credibility block (`section.cred-strip`) was moved to appear after "An aspiration engine" section on the homepage.
- Logo wall alignment in `cred-strip` uses a CSS grid to keep UN Women / MeitY / EY aligned.
- Special-character/mojibake issue was fixed by using ASCII hyphen in copy (avoid en-dash/odd chars if encoding issues reappear).

## Image Library for Future Use

- Source image folder (provided by Maitri team): `C:\Users\anjgu\Documents\LMFI\Maitri\website`
- Curated, renamed review set:
  - `C:\Users\anjgu\Documents\LMFI\Maitri\website\_site_candidates\canva\` (9 Canva banners with descriptive filenames)
  - `C:\Users\anjgu\Documents\LMFI\Maitri\website\_site_candidates\photos\` (selected photos, renamed `photo-XX-*`)
  - Mapping file: `C:\Users\anjgu\Documents\LMFI\Maitri\website\_site_candidates\manifest.csv` (new filename -> original path)
- Contact sheets (for quick selection):
  - `C:\Users\anjgu\Documents\LMFI\Maitri\website\_review\contact-sheet-photos-1.png`
  - `C:\Users\anjgu\Documents\LMFI\Maitri\website\_review\contact-sheet-canva.png`

Suggested usage:

- Use a single-subject or strong moment photo for the homepage hero background (keep faces visible; do not over-blur).
- Use Canva banners as section separators or header panels for Programs/Impact pages.

## Deployment (GCP VM)

- GCP project: `folkloric-rite-95004`
- VM: `polymarket-vm` (zone `us-east1-b`)
- Site directory on VM: `/var/www/maitriweb`
- Nginx serves the site (Debian 12).
- Pull + reload command used:
  - `cd /var/www/maitriweb && sudo git pull && sudo systemctl reload nginx`

From this Windows machine, you can run:

- `& "C:\Users\anjgu\tools\google-cloud-sdk\bin\gcloud.cmd" compute ssh polymarket-vm --zone us-east1-b --project folkloric-rite-95004 --command "cd /var/www/maitriweb && sudo git pull && sudo systemctl reload nginx"`

Non-interactive hostkey pin that worked:

- `& "C:\Users\anjgu\tools\google-cloud-sdk\bin\gcloud.cmd" compute ssh polymarket-vm --zone us-east1-b --project folkloric-rite-95004 --ssh-flag="-batch" --ssh-flag="-hostkey" --ssh-flag="SHA256:5wCGtzNHs1Id9lA0NZgiRFWRqbmwora/fNVXIoM8FQw" --command "cd /var/www/maitriweb && sudo git pull && sudo systemctl reload nginx"`

## Git Notes (Windows)

- Git dubious ownership can occur if the folder ownership differs from the current user. Fix was:
  - `git config --global --add safe.directory C:/Users/anjgu/MaitriSite`
- HTTPS pushing from sandboxed contexts caused issues earlier; current working approach is SSH remote:
  - `origin` is `git@github.com:a2o1o/maitriweb.git`
- Global git settings applied during troubleshooting:
  - `core.sshCommand` set to Windows OpenSSH: `C:/Windows/System32/OpenSSH/ssh.exe`
  - credential helper was unset at one point (verify on new machines)

## What Was Just Done Recently (So You Dont Revert It)

- Homepage hero headline updated (copy).
- Homepage section order changed: aspiration engine before credibility strip.
- VM pulled latest from GitHub and nginx reloaded successfully afterward.

## Where to Make Common Changes

- Homepage hero text/buttons/background: `C:\Users\anjgu\MaitriSite\index.html` and hero-related CSS in `assets/css/site.css`.
- Partner/recognition logos and alignment: `assets/img/logos/*` + `.logo-wall` styles in `assets/css/site.css`.
- SakhiAI page: `sakhi.html` (ensure `Sakhi<sup class="ai-sup">AI</sup>` is preserved across nav + headings).
- Global nav/footer consistency: repeated in each HTML file (no templating). If you change nav items, update all pages.

## Recommended Next Improvements (If Youre Continuing)

- Add an image selection pass for the hero background (choose 1 strongest photo and crop for desktop/mobile).
- Add an explicit Spotify link for Ninaad (copy currently says "Listen to Ninaad on Spotify" but still links to Instagram; update link if Spotify URL is available).
- Add `.gitattributes` to standardize LF/CRLF (there were repeated warnings about line endings on Windows).
- If you want faster editing, consider introducing a minimal templating step later (but current system is intentionally static/no-build).

If you want, I can also produce a site map + content blocks inventory per page (what each section is, what its goal is, and what image slot it should use).

