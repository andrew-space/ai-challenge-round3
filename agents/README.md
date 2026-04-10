# Round 3 Agent Playbook

Learning outcomes from previous rounds are reused with a modular team workflow:

1. **Research API Scout**: fetches and shortlists candidate sources.
2. **Evidence Verifier**: validates DOI, metadata, and claim-source alignment.
3. **Dashboard Builder**: builds responsive frontend with secure API integration.
4. **Deploy and QA**: publishes to GitHub Pages and runs checklist verification.

## Session 1 — Status (2026-04-09)

| Deliverable | Status |
|---|---|
| `site/launch-tracker.html` | ✅ Built — live API fetch, countdown, responsive table |
| `site/research-brief.html` | ✅ Built — 1-page brief, 6 DOI citations verified |
| `site/assets/styles.css` | ✅ Shared design system (dark-accent, mobile-responsive) |
| `site/assets/launch.js` | ✅ Countdown + live fetch logic (IIFE, escapeHtml, CSP-safe) |
| `site/index.html` | ✅ Landing hub linking both deliverables |
| `research_pipeline/build_brief.py` | ✅ Pipeline script (Crossref + S2 + DOI verify + Ghost Defense) |
| `research_pipeline/requirements.txt` | ✅ Dependencies installed (python-dotenv, requests) |
| `.env.example` | ✅ Template for secrets |
| `.gitignore` | ✅ Excludes .env, __pycache__, generated output |
| GitHub Pages deployment | ❌ **NOT DONE — next session priority** |

## Session 2 — What To Do Next (Timebox ≈ 20 min)

1. **5 min** — Create GitHub repo and push (see `DEPLOY-GITHUB-PAGES.md` for exact steps)
2. **3 min** — Enable Pages: Settings → Pages → Branch: main, Folder: /site
3. **3 min** — Wait for deploy, open live URLs
4. **5 min** — Run QA checklist (Agent 4)
5. **2 min** — Copy live URLs and submit to competition

## CSP Note for Deployment

The `launch-tracker.html` CSP header currently allows `connect-src https://fdo.rocketlaunch.live`.
If GitHub Pages blocks cross-origin fetch at runtime, switch the JS to a CORS-friendly proxy or
remove the meta CSP and rely on HTTPS-only policy.
