# Agent 1 - Research API Scout

## Status: ✅ Completed in Session 1

## What Was Done
- Queried Crossref with 4 topic variants: `in-space manufacturing`, `microgravity additive manufacturing`, `space manufacturing additive`, `3D printing microgravity`
- Retrieved 99 unique DOI-bearing records
- Selected 6 high-relevance 2021-2026 papers for the brief

## API Used
- Crossref (`api.crossref.org`) — no key needed
- Semantic Scholar rate-limited at time of session (429 error). Requires `SEMANTIC_SCHOLAR_KEY` in `.env` for full access.

## Next Session
- If Semantic Scholar key is available: add to `.env` and rerun `research_pipeline/build_brief.py`
- Output goes to `research_pipeline/generated/verified_papers.json`

## Quality Rules
- Keep only papers with DOI
- Prefer peer-reviewed venues (Acta Astronautica, npj Microgravity, Additive Manufacturing Frontiers)
- Mark uncertain records for verifier
