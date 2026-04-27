# Workflow A — Video Evidence Investigation

**Status:** Stage 2 complete → Stage 3 pending · 1 open item
**Last updated:** 2026-04-27

---

## Use Case Profile

```
Cluster:          Review & Search
Primary User:     Investigator
Evidence Node:    Tag → Review
Decision Nature:  Async Review
```

---

## Agent Mandate

| Agent | Status | Trigger |
|-------|--------|---------|
| Trust & Compliance | Required | AI in scope (v5.0 semantic search, v7.0 Re-ID, v8.0–v8.1 scene analysis) |
| Cost Analysis | Required | Review & Search cluster default |
| Market Analysis | Optional | PM discretion |
| User Analysis | Required | Review & Search cluster default |

---

## Stage 0 — Signal Capture

**Status: Exit Criteria met (proxy sources — see transparency note)**

### Primary Statement

> "Investigators struggle to locate relevant moments across multi-camera footage when a single incident generates hours of recordings, causing case preparation time to balloon and discovery deadlines to be missed."

### Raw User Quotes

> "So an officer might have a 45-minute video of a DUI. When we send it to the DA's office, they have that officer's video, they have every backup officer's video and the dashcam videos from each one. So now all of a sudden, they have four hours of video for a 45-minute incident."
> — Commander Nick Stasi, Durango Police Department

> "That time that it takes to download has an extra weight and adds to stress in a way that downloading a song or a video on your laptop doesn't come close to. It's not a mild inconvenience, it's a delay — sometimes one with very important consequences for everyone involved."
> — Justin Bogan, Head of Durango Public Defender's Office

> "While there has been a decrease in the number of criminal cases in our judicial district over the last couple decades, the amount of time an attorney spends on a case has gone up dramatically."
> — Sean Murray, District Attorney, 6th Judicial District

> "We're in a minefield, and it's not necessarily one piece of the puzzle; it's all of it."
> — Forensic Investigator, Denver District Attorney's Office

> "An investigator working a case might need to review hours of body camera footage, witness interviews, and a stack of paperwork. Without searchable transcripts or any way to quickly locate key moments, they're forced to read or listen to everything."
> — Veritone, Digital Evidence Management Industry Report

> "94% of investigators faced challenges when trying to play video evidence files, and many well-meaning investigators accidentally alter video evidence while attempting to play back thousands of proprietary file types."
> — Axon, 2021 Video Evidence Trends Report

> "Evidence review can take over 200 hours per case for some lawyers."
> — Digital Evidence Management Industry Research

> "In 2025, a prosecutor's office handled more than 67,700 videos, adding up to 41,000 hours of video evidence — up from 24,000 hours in 2022."
> — CPR News, January 2026

### Pain Location in Evidence Chain

```
Capture → Upload → Tag → [REVIEW] → Export → Court Submission
                              ↑
                    Primary failure node:
                    No semantic search across multi-camera footage.
                    Manual scrubbing is the only option.
```

### Business Impact

> Investigators spend 8–16 hours per week manually scrubbing footage, directly delaying case closure and compressing discovery deadlines.

### Cost Ceiling (Cost Analysis Agent)

```
Basis:         Axon Evidence pricing ~$0.10/GB storage
               Gemini 1.5 Flash two-layer architecture @ 1,000hr = <$30
Target margin: HALOS must stay below $0.003/min to be margin-positive
Result:        $30 per 1,000hr = $0.0005/min — within ceiling
Hard ceiling:  $0.003/min (6x headroom at current architecture)
```

### Compliance Blockers (Trust & Compliance Agent — quick checklist)

```
Known blockers:
  ⚠ GDPR Art. 9 — biometric data processing (face/person Re-ID in v7.0)
    requires explicit legal basis; no basis documented yet
  ⚠ CJPD / Irish Data Protection Act — law enforcement data processing
    constraints apply to HALOS's Ireland base
  ⚠ Chain-of-custody — AI-modified metadata must be logged separately
    from original; current audit log does not distinguish AI writes
    from human writes
  ✓ SHA-256 client-side hashing in place (v2.0)
  ✓ Audit log implemented (v2.0)
  ✗ AI output not explicitly labelled as advisory in UI
```

### Exit Criteria

| Criteria | Status |
|----------|--------|
| ≥3 independent users described the same friction point | ✓ 8 sources, 4 direct named quotes |
| Pain locatable at specific evidence chain node | ✓ Review node — cross-camera semantic search gap |
| Business impact articulable in one sentence | ✓ |
| Cost ceiling documented | ✓ |
| Compliance blockers documented | ✓ |

### Transparency Note

Stage 0 user quotes sourced from public record and industry reports, not direct field interviews. In a live product context, ≥3 direct user interviews are required before Stage 2. In interview context, this record is sufficient to support the narrative.

---

## Stage 1 — Functional Demo

**Status: Complete — 8 versions shipped in 7 days**

| Version | Validated Assumption | Invalidated Assumption | Cost Estimate |
|---------|---------------------|----------------------|---------------|
| v1.0 | Text-first indexing via Whisper is viable | — | Not recorded |
| v2.0–v3.0 | SHA-256 + Audit Log implementable at demo stage | — | Not recorded |
| v5.0 | Semantic search solves keyword mismatch problem | Keyword search is sufficient | Not recorded |
| v7.0 | Cross-camera Re-ID achievable via semantic embeddings, no model training | — | Not recorded |
| v8.0 | Body cam requires scene-aware analysis mode | Single frame-sampling strategy works for all footage types | Not recorded |
| v8.1 | Gemini native video outperforms frame-sampled GPT-4o | — | Gemini Flash ≈ 20% of GPT-4o cost ✓ |

**Known gap:** Per-version cost estimates not recorded for v1.0–v8.0. Only v8.1 has a cost estimate attached. Cost Analysis Agent should backfill estimates for v5.0, v7.0, v8.0 before Stage 2 exit.

---

## Profile Revision Log

*No revisions yet. Revision window opens at end of Stage 2.*

---

## Next Step

→ **Stage 3 — Dual Specification**
Draft Inner Spec (≤40 lines) with Decision Rationale block. Draft Compliance Annex.
Open item before Stage 3 can be finalised: AI confidence threshold (0.85) requires PM + Legal sign-off.
See full Stage 2 output: `stage-2-decomposition.md`
