# Workflow A — Stage 5: Monitoring & Iteration
# Video Evidence Investigation · Review & Search · Investigator

**Version:** 1.0 · **Status:** Pre-launch baseline — metrics not yet live
**Last updated:** 2026-04-27
**Context:** Stage 4 gates not yet passed. This document defines the monitoring framework
and iteration priorities to activate at launch. Baselines are targets, not actuals.

---

## Primary Metrics

| Metric | Definition | Target at Launch | Source |
|--------|-----------|-----------------|--------|
| Time to key moment | Minutes from video upload to investigator locating first relevant event | <3 min (45-min clip) | Product telemetry |
| AI tagging accuracy | % of AI-tagged events confirmed by investigator (user-validated, not model-reported) | ≥85% at launch → ≥92% by Month 3 | correction_log + reviewer_queue |
| Evidence retrieval speed | Time from semantic search query to ranked results displayed | <2 seconds | API response time log |
| Correction rate | % of auto-tagged events that receive a human correction | <10% at steady state | correction_log |
| Cost per video | Actual Gemini Flash cost per analysis run | ≤$0.006/video | API billing log |

---

## Guardrails (Zero-Tolerance)

```
Data integrity failures:      = 0  (SHA-256 mismatches in production)
Compliance audit failures:    = 0  (chain-of-custody challenges in court)
Unauthorized access events:   = 0  (any access outside granted permissions)
```

Breach of any guardrail = immediate incident response. Feature rollback if root cause
cannot be isolated within 24 hours. PM and Legal notified within 1 hour of detection.

---

## Feedback Collection (Built Into Product)

Per CLAUDE.md rules — feedback must be native, not a post-hoc survey.

```
Mechanism 1: Correction flag (≤1 action)
  → Every AI event has a flag icon
  → Tap/click → correction modal pre-filled with AI output
  → Confirm → writes to correction_log AND improvement_queue
  → This IS the feedback mechanism. No separate survey needed.

Mechanism 2: Reviewer queue implicit signal
  → Events surfaced to reviewer_queue (confidence <0.85) that are
    confirmed without edit → positive signal for threshold calibration
  → Events confirmed with edit → feeds improvement_queue
  → Events rejected entirely → strong negative signal

Mechanism 3: Search no-results rate
  → Queries returning 0 results logged with query text
  → High no-results rate on common terms = embedding gap or
    insufficient analysis coverage → triggers model review
```

---

## Adoption Stage Map

Feature adoption tracked against: `not caring → interested → understanding → evangelizing`

| Feature | Current Stage | Evidence | Next Stage Trigger |
|---------|--------------|----------|-------------------|
| Single video upload + AI summary | not caring | Pre-launch | First investigator completes a real case review using the summary |
| Semantic search | not caring | Pre-launch | Investigator finds a clip in <3 min that would have taken >30 min manually |
| Model comparison (Gemini vs GPT-4o) | not caring | Pre-launch | Investigator uses toggle to catch a detail missed by primary model |
| AI result correction (≤1 action) | not caring | Pre-launch | First correction submitted and logged — system responds correctly |
| Tactical-Link Re-ID | — | BLOCKED (GDPR) | Legal basis established → re-enter Stage 3 for this feature |

**Adoption velocity target:** ≥2 features reach "understanding" stage within 60 days of launch.

---

## Agent Triggers

### Market Analysis Agent
```
Trigger: Monthly, starting Month 1 post-launch
Questions:
  - Are real usage patterns (video length, clip volume, search frequency)
    consistent with competitive positioning assumptions?
  - Has Axon or Cellebrite shipped anything in the Review & Search cluster
    that closes the gap on semantic search or multi-camera tracking?
  - Does usage data suggest a pricing model adjustment is needed?
```

### Cost Analysis Agent
```
Trigger: End of Month 1, then quarterly
Questions:
  - Does actual cost per video match Stage 3 basis (~$0.005)?
  - What is the actual L1 filter rejection rate vs. assumed ~90%?
  - At current usage volume, is the two-layer architecture still
    the optimal cost structure, or does a different split make sense?

Early signal to watch:
  - If actual cost > $0.008/video → routing logic needs review
  - If L1 rejection rate < 70% → pixel diff threshold (15%) may need
    recalibration for real-world footage conditions
```

### User Analysis Agent
```
Trigger: End of Week 2, Week 4, Month 3
Questions:
  - Which features are investigators actually using vs. ignoring?
  - Is the correction rate (<10% target) being met — or are investigators
    not correcting because they don't trust the system at all?
  - Is the model comparison toggle being used, or is it invisible?
  - Map each investigator against the adoption stage for each feature
```

---

## Prioritisation Formula

```
Priority = user pain impact × solution confidence ÷ dev cost
```

### Next-Build Candidates (ranked at launch)

| Candidate | Pain Impact | Solution Confidence | Dev Cost | Priority Score | Rationale |
|-----------|-------------|--------------------|---------:|---------------|-----------|
| Tactical-Link Re-ID (post-GDPR resolution) | 9 | 8 | 6 | 12.0 | Highest differentiator; blocked not deprioritised — legal path exists |
| AI advisory label + court export package | 8 | 9 | 3 | 24.0 | Low dev cost, high compliance value, unlocks legal customers |
| Model comparison UX guidance | 6 | 9 | 2 | 27.0 | Lowest dev cost; removes cognitive load flagged in Stage 2 |
| Golden test set build + threshold validation | 7 | 9 | 3 | 21.0 | Required to exit Stage 4 — not optional |
| Batch upload + queue UI | 5 | 8 | 4 | 10.0 | Useful but not blocking any core investigator flow |
| Audio transcription (Whisper integration) | 7 | 8 | 4 | 14.0 | Extends v1.0 capability; enables keyword + semantic hybrid search |

**Top 3 at launch:**
1. Model comparison UX guidance (Score: 27.0) — fix the Stage 2 UX gap, minimal effort
2. AI advisory label + court export (Score: 24.0) — unlocks legal use and Stage 4 Legal gate
3. Golden test set build (Score: 21.0) — required to formally exit Stage 4

---

## Cost Model Variance Tracking

```
Stage 3 basis:       ~$0.005/video (45-min body cam, Gemini Flash)
Stage 3 target:      <$30 per 1,000hr

At launch, track:
  Actual cost/video:        [to be filled post-launch]
  Actual cost/1,000hr:      [to be filled post-launch]
  Variance from basis:      [to be calculated]
  L1 rejection rate actual: [to be filled post-launch]
  Trigger for review:       actual > $0.008/video OR variance > ±20%
```

---

## Iteration Brief Template (to be completed post-launch)

```
Period:              [Month / Quarter]
---
Primary Metrics:
  Time to key moment:         [actual] vs. <3 min target
  AI tagging accuracy:        [actual] vs. ≥85% target
  Evidence retrieval speed:   [actual] vs. <2s target
  Correction rate:            [actual] vs. <10% target
  Cost per video:             [actual] vs. ≤$0.006 target

Guardrails:
  Data integrity failures:    [count] — must be 0
  Compliance audit failures:  [count] — must be 0
  Unauthorized access events: [count] — must be 0

Adoption Stage Map:
  [feature]: [stage] → [evidence]

Cost Model Variance:
  Actual vs. Stage 3 basis: [variance %]
  L1 rejection rate: [actual] vs. ~90% assumed
  Action required: [yes/no — what]

Ranked Next-Build Candidates:
  1. [candidate] — Priority [score] — [one-line rationale]
  2. [candidate] — Priority [score] — [one-line rationale]
  3. [candidate] — Priority [score] — [one-line rationale]
```

---

## Stage 5 Activation Checklist

```
  ⬜ Stage 4 gate report signed off
  ⬜ Correction flag (≤1 action) live and writing to correction_log
  ⬜ Reviewer queue live and writing to improvement_queue
  ⬜ Search no-results rate logged
  ⬜ API billing log connected to cost tracking
  ⬜ Adoption stage map baseline set (all features: "not caring")
  ⬜ First iteration brief scheduled: 2 weeks post-launch
```
