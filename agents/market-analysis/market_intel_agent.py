"""
HALOS Market Intelligence Agent
Runs weekly web searches, analyzes results with Claude, and writes a delta report.

Usage:
  python market_intel_agent.py           # run with last-7-days date range
  python market_intel_agent.py --dry-run # search only, skip Claude analysis
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from openai import OpenAI
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
TARGETS_FILE = BASE_DIR / "search_targets.yaml"
CONTEXT_FILE = BASE_DIR / "market-intelligence.md"
REPORTS_DIR = BASE_DIR / "weekly-reports"
REPORTS_DIR.mkdir(exist_ok=True)

# ── Config ───────────────────────────────────────────────────────────────────
MODEL = "gpt-4o-mini"
MAX_RESULTS_PER_QUERY = 5


# ── Search ───────────────────────────────────────────────────────────────────

def search_tavily(query: str, days_back: int = 7) -> list[dict]:
    """Call Tavily Search API and return a list of {title, url, description}."""
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    response = client.search(
        query=query,
        max_results=MAX_RESULTS_PER_QUERY,
        days=days_back,
        include_answer=False,
    )
    results = []
    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("content", ""),
            "published_date": item.get("published_date", ""),
        })
    return results


def run_searches(targets: dict, days_back: int = 7) -> list[dict]:
    """Run all searches and return raw results with metadata."""
    all_results = []
    categories = ["competitors", "regulatory", "market_signals"]

    for category in categories:
        for target in targets.get(category, []):
            print(f"  Searching [{target['priority']}] {target['id']} ...")
            try:
                hits = search_tavily(target["query"], days_back)
                all_results.append({
                    "id": target["id"],
                    "category": category,
                    "priority": target["priority"],
                    "query": target["query"],
                    "results": hits,
                })
            except Exception as e:
                print(f"    ⚠ Search failed for {target['id']}: {e}")
                all_results.append({
                    "id": target["id"],
                    "category": category,
                    "priority": target["priority"],
                    "query": target["query"],
                    "results": [],
                    "error": str(e),
                })

    return all_results


# ── Analysis ─────────────────────────────────────────────────────────────────

def build_analysis_prompt(search_data: list[dict], context: str, week_label: str) -> str:
    results_text = json.dumps(search_data, ensure_ascii=False, indent=2)
    return f"""You are the Market Analysis agent for HALOS, a Video Forensics Platform for law enforcement (body cameras + digital evidence management). HALOS is based in Ireland, targeting European law enforcement first, then expanding globally.

## HALOS Market Context (your reference baseline)

{context}

---

## This Week's Search Results ({week_label})

{results_text}

---

## Your task

Analyze the search results above and produce a weekly delta report in the exact markdown format below.

## HALOS Strategic Direction (use this to judge what matters)

Three bets HALOS is making over the next 2–3 years:

1. SOFTWARE PLATFORM INDEPENDENCE
   Hardware (body cameras) is becoming a commodity. HALOS's real value will be the software platform — not just processing its own camera footage, but ingesting any video source: existing CCTV systems, S3-stored footage, third-party cameras. The goal is a platform that sells on its own merits, independent of hardware.
   → Signals that matter: competitors launching open/agnostic video ingestion, API integrations with CCTV or cloud storage, or locking customers into closed hardware ecosystems.

2. PROACTIVE INVESTIGATION PLATFORM
   Shift from reactive ("find footage after an incident") to proactive ("system flags anomalies in real time"). Examples: detecting sounds of altercations, surfacing clips automatically before a user has to search. This moves HALOS from evidence storage toward active situational intelligence.
   → Signals that matter: competitors launching real-time anomaly detection, audio AI, or proactive alerting features in law enforcement contexts.

3. JOBS-TO-BE-DONE INTERFACE REDESIGN
   HALOS is rebuilding its frontend away from the legacy "click camera → browse timeline" API-UI paradigm (10+ year old architecture). The new design filters out irrelevant footage and surfaces only key evidence — built around what the investigator needs to accomplish, not around the file system.
   → Signals that matter: competitors redesigning investigator UX, launching AI-curated evidence views, or winning deals specifically on UX grounds.

---

Rules:
- DATE FILTER (apply first): Only include a result if its published_date is within the last 30 days of {datetime.now().strftime("%Y-%m-%d")}, OR if no date is available but the content clearly references a recent event. If a result is older than 30 days and contains no new development, put it in "No Change" and note "(old news)".
- HALOS current GTM priority: Phase 1 = Ireland + UK. Phase 2 = Europe. Phase 3 = North America (Year 3+). Signals about North America markets should not exceed 🟡 Medium Impact unless they directly affect a competitor's European strategy.
- Only include signals where you found actual new information in the search results. If results are empty or irrelevant, put the item in "No Change".
- For each signal, add one sentence: "Impact on HALOS: ..." explaining specifically what this means for HALOS strategy, positioning, or GTM.
- 🔴 High Impact = directly threatens a HALOS differentiation assumption OR creates an immediate market opportunity in Phase 1/2 markets. Must be a confirmed development, not speculation.
- 🟡 Medium Impact = worth tracking but no immediate action needed.
- ⚪ Low Signal = market noise, FYI only.
- "PM Action Required" items should be specific and actionable, not vague.
- Keep each signal to 2-3 lines max. No long summaries.

## Output format (fill in exactly this structure)

# HALOS Market Intelligence — Weekly Delta
Period: {week_label}
Generated: {datetime.now().strftime("%Y-%m-%d")}

## 🔴 High Impact (PM Action Required)
<!-- List signals here, or write "None this week." -->

## 🟡 Medium Impact (Monitor)
<!-- List signals here, or write "None this week." -->

## ⚪ Low Signal (FYI)
<!-- List signals here, or write "None this week." -->

## No Change
<!-- List search target IDs where no new relevant information was found -->

---
## PM Action Items
<!-- Specific, actionable items only. Leave blank if none. -->
- [ ] ...
"""


def analyze_with_claude(search_data: list[dict], context: str, week_label: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = build_analysis_prompt(search_data, context, week_label)

    print("  Sending to OpenAI for analysis ...")
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# ── Report ───────────────────────────────────────────────────────────────────

def get_week_label() -> str:
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    iso_week = today.isocalendar()
    return f"{iso_week.year}-W{iso_week.week:02d} ({week_start.strftime('%b %d')} – {week_end.strftime('%b %d')})"


def get_report_filename() -> Path:
    today = datetime.now()
    iso = today.isocalendar()
    return REPORTS_DIR / f"{iso.year}-W{iso.week:02d}.md"


def save_report(content: str, path: Path) -> None:
    path.write_text(content, encoding="utf-8")
    print(f"\nReport saved: {path}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="HALOS Market Intelligence Agent")
    parser.add_argument("--dry-run", action="store_true", help="Search only, skip Claude analysis")
    parser.add_argument("--days", type=int, default=7, help="Search freshness window in days (default: 7)")
    args = parser.parse_args()

    week_label = get_week_label()
    report_path = get_report_filename()

    print(f"\n=== HALOS Market Intelligence Agent ===")
    print(f"Week : {week_label}")
    print(f"Output: {report_path}\n")

    # Load targets
    targets = yaml.safe_load(TARGETS_FILE.read_text(encoding="utf-8"))

    # Load market context
    context = CONTEXT_FILE.read_text(encoding="utf-8")

    # Run searches
    print("[ 1/2 ] Running searches ...")
    search_data = run_searches(targets, days_back=args.days)

    total_hits = sum(len(r["results"]) for r in search_data)
    print(f"        {len(search_data)} queries, {total_hits} results found\n")

    if args.dry_run:
        raw_path = report_path.with_suffix(".raw.json")
        raw_path.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Dry run complete. Raw results saved to: {raw_path}")
        return

    # Analyse with Claude
    print("[ 2/2 ] Analysing with Claude ...")
    report_content = analyze_with_claude(search_data, context, week_label)

    # Save report
    save_report(report_content, report_path)
    print("\nDone.")


if __name__ == "__main__":
    main()
