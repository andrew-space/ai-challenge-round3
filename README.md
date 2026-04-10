# AI Challenge Arena - Round 3

This round delivers **two judge-targeted projects** in a single GitHub Pages deployment:

1. **Launch Tracker**: live dashboard of upcoming rocket launches worldwide (mission, rocket, site, UTC time, and countdown).
2. **Research Brief**: one-page synthesis on in-space manufacturing with at least 5 real papers and DOI citations.

## Project Structure

```text
Round 3/
├── agents/
├── research_pipeline/
├── site/
│   ├── index.html
│   ├── launch-tracker.html
│   ├── research-brief.html
│   ├── assets/
│   │   ├── launch.js
│   │   └── styles.css
│   └── .nojekyll
├── .env.example
├── .gitignore
└── README.md
```

## Judge Checklist Mapping

### Launch Tracker
- Dashboard is deployable on GitHub Pages: `site/launch-tracker.html`
- Uses real upcoming launch data: API `https://fdo.rocketlaunch.live`
- Live countdown for next launch: implemented in `site/assets/launch.js`
- Includes mission, rocket, launch site, date/time: table columns + hero card
- Responsive and polished: custom CSS with mobile breakpoints

### Research Brief
- Deployable as web page: `site/research-brief.html`
- In-space manufacturing coverage with structure and depth
- 6 real papers cited with DOI links
- Papers are DOI-verifiable via `https://doi.org/...`
- Professional writing style with explicit method and limitations

## Local Preview

Open the pages directly in browser:

- `site/index.html`
- `site/launch-tracker.html`
- `site/research-brief.html`

## Deployment (GitHub Pages)

Use the deployment guide in `DEPLOY-GITHUB-PAGES.md`.

Expected published URLs:

- `https://<your-username>.github.io/<repo-name>/launch-tracker.html`
- `https://<your-username>.github.io/<repo-name>/research-brief.html`

## Security Notes

- API keys must stay in `.env`
- `.env` is excluded via `.gitignore`
- Frontend pages use restrictive CSP meta headers
