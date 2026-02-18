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


------------------------------------------------------------
Homepage Narrative Restructure (Index Page Only)
------------------------------------------------------------

Scope:
Apply ONLY to index.html unless explicitly instructed otherwise.
Do not modify other pages unless necessary for image reuse.

Goal:
Restructure homepage into:

Hook → Problem → Solution → Proof → Recognition → Leadership Loop → Vision/Mission → Final CTA

Keep:
- Current layout system (hero overlay, rounded cards, chip styles)
- Open Sans font
- Existing navigation
- Existing color palette
- Static HTML structure
- No new libraries

Do NOT:
- Imply formal MOUs with schools
- Modify other HTML pages
- Change navigation or footer
- Remove existing sections unless replaced by this structure

------------------------------------------------------------
Section Details
------------------------------------------------------------

1) HERO (replace overlay text only)
Eyebrow:
SISTERHOOD. COURAGE. ASPIRATION.

H1:
Expanding ambition, access, and leadership
for first-generation young women

Subheadline:
Peer mentoring, structured pathways, and sisterhood that opens real opportunities across education and early careers.

Micro line:
Currently operating across government school communities in Delhi.

Buttons:
- Partner → partners.html
- Support → donate.html
- How it works → #how-it-works

------------------------------------------------------------

2) PROBLEM SECTION (new)
Title:
Talent is everywhere. Access is not.

Body:
Many first-generation young women carry ambition and capability, but face barriers in exposure, social capital, and professional networks—especially at key transitions from school to higher education and early careers.

Add chips:
Exposure gap
Network gap
Transition gap

After this section insert:
<div class="section-divider"></div>

------------------------------------------------------------

3) SOLUTION (id="how-it-works")

Title:
Building leadership that multiplies

Subline:
A long-term ecosystem — not one-time workshops.

3 Cards (link to programs.html):
Structured Sisterhood
Mentorship & Social Capital
Opportunity Pathways

After this section insert:
<div class="section-divider"></div>

------------------------------------------------------------

4) PROOF (Impact in action)

Metrics row:
150+ young women engaged
60+ internships enabled
30+ alumna mentors
Growing partner network

Include ONE testimonial with photo:

Quote (exact text):
"I am Aditi and I came across Maitri community when my senior at school introduced me to it. Through the guidance and mentorship at Maitri, I became an EY Disha scholar. Today, I am a part of Content and Scholarship team at Maitri and guide my juniors to get the opportunity that I got through Maitri community."

Attribution:
— Aditi, EY Disha Scholar

Include image:
Reuse Aditi image from impact page if available.
If not available, use: assets/img/aditi.jpg

Add link below testimonial:
Read more stories → impact.html

After this section insert:
<div class="section-divider"></div>

------------------------------------------------------------

5) RECOGNITION
Keep existing recognition block.
Rename heading to:
Evidence-led credibility

------------------------------------------------------------

6) LEADERSHIP LOOP

Title:
The Maitri leadership loop

Diagram row:
Young Woman → Peer Leader → Alumna → Mentor → Expanding Network

Line below:
Maitri grows through the leaders it creates.

After this section insert:
<div class="section-divider"></div>

------------------------------------------------------------

7) VISION + MISSION

Vision:
A future where every girl’s ambition is matched by access — and strengthened by sisterhood.

Mission:
Bridging aspiration and access for first-generation young women through structured sisterhood, mentorship, and opportunity pathways.

Footnote:
Currently operating across government school communities in Delhi via volunteers and SMC networks.

After this section insert:
<div class="section-divider"></div>

------------------------------------------------------------

8) FINAL CTA

Title:
Join the sisterhood that builds leaders

Buttons:
- Apply as a Student → Google Form (open in new tab)
- Become a Mentor → programs.html
- Partner With Us → partners.html
- Support Maitri → donate.html

------------------------------------------------------------
Divider CSS (add to assets/css/site.css if not present)
------------------------------------------------------------

.section-divider {
  height: 2px;
  width: 100%;
  background: linear-gradient(
    90deg,
    rgba(216, 76, 135, 0.55),
    rgba(240, 122, 107, 0.55),
    rgba(242, 200, 75, 0.55),
    rgba(79, 167, 181, 0.55),
    rgba(140, 122, 200, 0.55)
  );
  margin: 48px 0;
  border-radius: 999px;
}

------------------------------------------------------------
Typography Constraints
------------------------------------------------------------

- Keep Open Sans.
- H1 ~48px (700)
- Section headers ~32px (700)
- Body 16–17px (400)
- Buttons 700 weight
- Maintain responsive layout

------------------------------------------------------------

