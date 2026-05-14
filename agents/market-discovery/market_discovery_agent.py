"""
HALOS Market Discovery Agent
Runs monthly searches to find non-enforcement verticals with the same pain as law enforcement.
Outputs an Opportunity Brief — ranked by (pain fit × solution confidence ÷ entry cost).

Usage:
  python market_discovery_agent.py           # run full discovery
  python market_discovery_agent.py --dry-run # search only, skip OpenAI analysis
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

import yaml
from openai import OpenAI
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
TARGETS_FILE = BASE_DIR / "discovery_targets.yaml"
CONTEXT_FILE = BASE_DIR / "opportunity_context.md"
BRIEFS_DIR = BASE_DIR / "opportunity-briefs"
BRIEFS_DIR.mkdir(exist_ok=True)

# ── Config ───────────────────────────────────────────────────────────────────
MODEL = "gpt-4o-mini"
MAX_RESULTS_PER_QUERY = 5


# ── Search ───────────────────────────────────────────────────────────────────

def search_tavily(query: str, days_back: int = 30) -> list[dict]:
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


def run_searches(targets: dict, days_back: int = 30) -> list[dict]:
    all_results = []
    layers = ["pain_signals", "adoption_signals", "trigger_signals"]

    for layer in layers:
        for target in targets.get(layer, []):
            print(f"  Searching [{target['priority']}] {target['id']} ...")
            try:
                hits = search_tavily(target["query"], days_back)
                all_results.append({
                    "id": target["id"],
                    "layer": layer,
                    "priority": target["priority"],
                    "query": target["query"],
                    "results": hits,
                })
            except Exception as e:
                print(f"    ⚠ Search failed for {target['id']}: {e}")
                all_results.append({
                    "id": target["id"],
                    "layer": layer,
                    "priority": target["priority"],
                    "query": target["query"],
                    "results": [],
                    "error": str(e),
                })

    return all_results


# ── Analysis ─────────────────────────────────────────────────────────────────

def build_discovery_prompt(search_data: list[dict], context: str, month_label: str) -> str:
    results_text = json.dumps(search_data, ensure_ascii=False, indent=2)
    today = datetime.now().strftime("%Y-%m-%d")

    return f"""You are the Market Discovery agent for HALOS, a Video Forensics Platform.
Your job is to find industries that need video analysis but that HALOS has not yet considered.
Do NOT start from HALOS's product. Start from the search results and surface what you find.

## HALOS Platform Context (background only — do not use to filter results)

{context}

---

## This Month's Search Results ({month_label})

{results_text}

---

## Your task

Read the search results and answer these questions for each industry that appears:

1. WHAT INDUSTRY IS THIS?
   Name it precisely. Not "enterprise" — name the actual sector.

2. WHAT IS THEIR PAIN? (use their own words from the results)
   What exactly is broken or slow or risky for them?
   Quote directly from the search results where possible.

3. WHAT ARE THEY DOING ABOUT IT NOW?
   What workaround or incumbent tool are they using?
   Why is that solution inadequate?

4. WHAT IS TRIGGERING THIS NOW?
   Choose one primary trigger type:
   - Regulatory: new law or compliance requirement
   - Incident: a high-profile failure or scandal forced action
   - Cost: AI/technology costs dropped enough to make this feasible
   - Scale: their business grew and the old manual process broke
   - Gap: the dominant vendor doesn't serve this vertical
   If none clearly apply, write "unclear — needs investigation."

5. SURPRISE SCORE (1–3)
   How unexpected is this vertical for a video forensics company?
   3 = completely unexpected — would never come up in a law enforcement conversation
   2 = adjacent — obvious in hindsight but not on the standard radar
   1 = expected — law enforcement-adjacent (ignore these, they are already known)

---

## Rules
- DATE FILTER: Only include results published within 60 days of {today}, or undated results with clearly recent content.
- Only write up an industry if you found actual evidence in the search results. Do not invent.
- Surprise score 1 industries (law enforcement-adjacent): list them in "Already Known" and skip the full brief.
- Prioritise UK and Ireland signals. European signals are secondary.
- Quote the source results — do not paraphrase the pain into HALOS language.
- No scoring against HALOS fit. That is a separate exercise. This brief is about what is true in the market.

---

## Output format

# HALOS Market Discovery — Market Map
Month: {month_label}
Generated: {today}

## Unexpected Industries (Surprise Score 2–3)

### [Industry Name] — Surprise: [score] — Trigger: [type]
Pain (their words): "[direct quote or close paraphrase from search results]"
Current workaround: [what they use now and why it fails]
Trigger detail: [one sentence on what is forcing action now]
Evidence quality: [how many results, how concrete]

---
[repeat for each industry with evidence]

---

## Already Known (Surprise Score 1 — law enforcement-adjacent)
[List only — no full brief needed]

---

## No Signal
[List search IDs where results were empty or irrelevant]

---

## Market Map Summary

| Industry | Surprise | Trigger Type | Evidence Quality | Pain Clarity |
|----------|----------|--------------|-----------------|--------------|
| ...      | ...      | ...          | ...             | ...          |

---

## Most Unexpected Finding
[One paragraph: the industry from these results that HALOS would be least likely to think of, and why the signal is credible]
"""


def analyze_with_openai(search_data: list[dict], context: str, month_label: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = build_discovery_prompt(search_data, context, month_label)

    print("  Sending to OpenAI for analysis ...")
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# ── Report ───────────────────────────────────────────────────────────────────

def get_month_label() -> str:
    return datetime.now().strftime("%Y-%m")


def get_brief_filename() -> Path:
    return BRIEFS_DIR / f"{get_month_label()}.md"


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="HALOS Market Discovery Agent")
    parser.add_argument("--dry-run", action="store_true", help="Search only, skip OpenAI analysis")
    parser.add_argument("--days", type=int, default=30, help="Search freshness window in days (default: 30)")
    args = parser.parse_args()

    month_label = get_month_label()
    brief_path = get_brief_filename()

    print(f"\n=== HALOS Market Discovery Agent ===")
    print(f"Month : {month_label}")
    print(f"Output: {brief_path}\n")

    targets = yaml.safe_load(TARGETS_FILE.read_text(encoding="utf-8"))
    context = CONTEXT_FILE.read_text(encoding="utf-8")

    print("[ 1/2 ] Running searches ...")
    search_data = run_searches(targets, days_back=args.days)

    total_hits = sum(len(r["results"]) for r in search_data)
    print(f"        {len(search_data)} queries, {total_hits} results found\n")

    if args.dry_run:
        raw_path = brief_path.with_suffix(".raw.json")
        raw_path.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Dry run complete. Raw results saved to: {raw_path}")
        return

    print("[ 2/2 ] Analysing with OpenAI ...")
    brief_content = analyze_with_openai(search_data, context, month_label)

    brief_path.write_text(brief_content, encoding="utf-8")
    print(f"\nOpportunity brief saved: {brief_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
