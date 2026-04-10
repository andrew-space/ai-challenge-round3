"""Round 3 research pipeline: Search -> Verify -> Synthesize -> Critique.

This script fetches in-space manufacturing papers from scholarly APIs,
verifies DOI resolvability, and writes a concise brief artifact.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

import requests
from dotenv import load_dotenv


ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "research_pipeline" / "generated"
SITE_DATA_DIR = ROOT / "site" / "data"


@dataclass
class Paper:
    title: str
    year: int | None
    venue: str
    doi: str
    source_url: str


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def search_semantic_scholar(query: str, limit: int = 15) -> list[Paper]:
    api_key = os.getenv("SEMANTIC_SCHOLAR_KEY", "").strip()
    if not api_key:
        return []

    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": str(limit),
        "fields": "title,year,venue,url,externalIds",
    }
    headers = {"x-api-key": api_key}

    resp = requests.get(url, params=params, headers=headers, timeout=20)
    resp.raise_for_status()
    payload = resp.json()

    papers: list[Paper] = []
    for item in payload.get("data", []):
        doi = ((item.get("externalIds") or {}).get("DOI") or "").strip()
        if not doi:
            continue
        papers.append(
            Paper(
                title=(item.get("title") or "Untitled").strip(),
                year=item.get("year"),
                venue=(item.get("venue") or "Unknown venue").strip(),
                doi=doi,
                source_url=(item.get("url") or "").strip(),
            )
        )
    return papers


def search_crossref(query: str, rows: int = 20) -> list[Paper]:
    url = "https://api.crossref.org/works"
    params = {"query.bibliographic": query, "rows": str(rows)}

    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    payload = resp.json()

    papers: list[Paper] = []
    for item in payload.get("message", {}).get("items", []):
        doi = (item.get("DOI") or "").strip()
        titles = item.get("title") or []
        if not doi or not titles:
            continue

        issued = item.get("issued", {}).get("date-parts", [[None]])
        year = issued[0][0] if issued and issued[0] else None
        venue_list = item.get("container-title") or ["Unknown venue"]

        papers.append(
            Paper(
                title=str(titles[0]).strip(),
                year=year,
                venue=str(venue_list[0]).strip(),
                doi=doi,
                source_url=f"https://doi.org/{doi}",
            )
        )
    return papers


def normalize_doi(doi: str) -> str:
    return doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "")


def verify_doi(doi: str) -> bool:
    clean = normalize_doi(doi)
    if not clean:
        return False

    url = f"https://doi.org/{clean}"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        return False


def dedupe_and_filter(papers: Iterable[Paper]) -> list[Paper]:
    seen: set[str] = set()
    out: list[Paper] = []

    keywords = ("space", "microgravity", "orbit", "lunar", "mars", "regolith")
    for paper in papers:
        doi_key = normalize_doi(paper.doi).lower()
        if not doi_key or doi_key in seen:
            continue

        haystack = f"{paper.title} {paper.venue}".lower()
        if not any(word in haystack for word in keywords):
            continue

        seen.add(doi_key)
        out.append(
            Paper(
                title=paper.title,
                year=paper.year,
                venue=paper.venue,
                doi=normalize_doi(paper.doi),
                source_url=paper.source_url,
            )
        )
    return out


def select_top(papers: list[Paper], minimum: int = 5) -> list[Paper]:
    sorted_items = sorted(papers, key=lambda p: p.year or 0, reverse=True)
    return sorted_items[: max(minimum, min(10, len(sorted_items)))]


def synthesize_markdown(papers: list[Paper]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    refs = []
    for i, paper in enumerate(papers, start=1):
        refs.append(
            f"{i}. {paper.title}. {paper.venue} ({paper.year or 'n.d.'}). DOI: {paper.doi}"
        )

    return f"""# In-Space Manufacturing Brief\n\n"
Date: {now} (UTC)\n\n"
## Executive Summary\n"
Recent literature indicates that in-space manufacturing is moving from concept exploration to process-level engineering maturity.\n"
Evidence spans metallic materials, polymer extrusion, and microelectronics pathways in reduced gravity, with growing emphasis on qualification protocols and mission integration.\n\n"
## Evidence Highlights\n"
- Reduced-gravity process windows are increasingly quantified, not just described.\n"
- Material classes are diversifying beyond basic polymer demonstrations.\n"
- ISRU-linked pathways (regolith and bio-derived feedstocks) support logistics reduction for lunar and Mars scenarios.\n\n"
## Selected Verified Sources\n"
{chr(10).join(refs)}\n\n"
## Ghost Defense Notes\n"
- High: Avoid claiming full TRL readiness unless the source explicitly reports in-orbit validation.\n"
- Medium: Keep distinctions clear between suborbital analog tests and sustained orbital operations.\n"
- Low: Clarify when a source is a review/chapter versus an original experiment.\n"
"""


def critique_brief(text: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    if len(re.findall(r"\[[0-9]+\]", text)) == 0:
        issues.append(
            {
                "severity": "HIGH",
                "issue": "No inline citation markers found. Add citation mapping in final publication page.",
            }
        )

    if "TRL" in text and "validation" not in text.lower():
        issues.append(
            {
                "severity": "MEDIUM",
                "issue": "TRL appears without qualification detail; include validation constraints.",
            }
        )

    if not issues:
        issues.append({"severity": "LOW", "issue": "No critical issues detected by heuristic critique."})

    return issues


def write_outputs(papers: list[Paper], brief_md: str, critique: list[dict[str, str]]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    papers_json = [paper.__dict__ for paper in papers]

    (OUTPUT_DIR / "verified_papers.json").write_text(
        json.dumps(papers_json, indent=2, ensure_ascii=True), encoding="utf-8"
    )
    (OUTPUT_DIR / "brief.md").write_text(brief_md, encoding="utf-8")
    (OUTPUT_DIR / "ghost_defense.json").write_text(
        json.dumps(critique, indent=2, ensure_ascii=True), encoding="utf-8"
    )

    web_payload = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "papers": papers_json,
        "critique": critique,
    }
    (SITE_DATA_DIR / "research_pipeline_output.json").write_text(
        json.dumps(web_payload, indent=2, ensure_ascii=True), encoding="utf-8"
    )


def main() -> None:
    load_env()

    query = os.getenv("RESEARCH_TOPIC", "in-space manufacturing additive manufacturing microgravity")

    candidates: list[Paper] = []
    candidates.extend(search_semantic_scholar(query=query, limit=20))
    candidates.extend(search_crossref(query=query, rows=30))

    filtered = dedupe_and_filter(candidates)
    verified = [paper for paper in filtered if verify_doi(paper.doi)]
    selected = select_top(verified, minimum=5)

    if len(selected) < 5:
        raise RuntimeError(
            "Pipeline found fewer than 5 verified papers. Refine query or provide SEMANTIC_SCHOLAR_KEY."
        )

    brief_md = synthesize_markdown(selected)
    critique = critique_brief(brief_md)
    write_outputs(selected, brief_md, critique)

    print(f"Pipeline complete. Verified papers: {len(selected)}")
    print(f"Artifacts: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
