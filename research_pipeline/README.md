# Round 3 Research Pipeline

This folder implements the Day-3 API workflow:

1. Search (Semantic Scholar + Crossref)
2. Verify (DOI resolution check)
3. Synthesize (auto brief)
4. Critique (Ghost Defense heuristic pass)

## Setup

```powershell
cd "AI Challenge Arena\Round 3"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r research_pipeline\requirements.txt
copy .env.example .env
```

Populate `.env` with your keys if available.

## Run

```powershell
python research_pipeline\build_brief.py
```

## Output

- `research_pipeline/generated/verified_papers.json`
- `research_pipeline/generated/brief.md`
- `research_pipeline/generated/ghost_defense.json`
- `site/data/research_pipeline_output.json`

## Security

- Never commit `.env`
- Never hardcode keys in Python or JavaScript
