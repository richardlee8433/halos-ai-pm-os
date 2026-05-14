# Opportunity Brief: Commercial Fleet Insurance
**For:** CTPO
**Date:** 2026-05-14
**Status:** Unvalidated — based on market signals, not customer conversations

---

## The Opportunity in One Sentence

Commercial fleet insurers are sitting on millions of hours of dashcam footage they cannot process at scale — fraud is at record levels, AI costs just crossed the affordability threshold, and no one owns the software layer.

---

## Why Now

Three forces converged in 2024–2026:

**1. Video volume crossed the manual processing threshold**
Commercial fleet dashcam adoption is now standard in the UK. A 100-vehicle fleet generates hundreds of hours of footage daily. Insurers are contractually receiving this footage but have no scalable way to analyze it. The backlog is growing faster than headcount can address.

**2. Fraud is at a historic high**
UK "Crash for Cash" fraud (staged accidents) hit record levels in 2023–2024. ABI data shows detected fraud value up significantly year-on-year. Dashcam footage is the primary counter-fraud tool — but only if it can be retrieved, authenticated, and analyzed quickly. Currently it isn't.

**3. AI analysis cost just crossed the SMB threshold**
Two years ago, large-scale video analysis was cost-prohibitive for mid-sized insurers. That floor has dropped. The ROI calculation now works: catching one staged-accident fraud claim covers the cost of months of AI analysis. Procurement decisions are being made now.

---

## The Customer Pain

*In their own words, not Video Wisdom language:*

- "We receive dashcam clips from 40 different device brands. Half of them won't open in our claims system."
- "By the time we've retrieved and reviewed the footage, the fraud window has closed."
- "We can't tell if a clip submitted by a claimant has been edited. We have no way to verify."
- "Our adjusters spend 3–4 hours per disputed claim just locating and formatting video."

*(Sources: ABI fraud reports, insurance claims forum discussions, insurer job postings for "video evidence analyst" roles — all indirect. Needs direct customer validation.)*

---

## What Exists Today and Why It Fails

| Tool | What it does | Why it fails here |
|------|-------------|-------------------|
| SightCall / Encircle | Adjuster captures video on-site | Solves new capture, not existing footage ingestion |
| Claims management systems (Guidewire, Duck Creek) | Case management | No video intelligence layer, no chain-of-custody |
| Manual review teams | Watch footage, write reports | Does not scale, no tamper verification |
| Regure (UK) | Compliance audit trails for documents | Not built for video, no AI analysis |

**The gap:** Nobody provides tamper-evident ingest of multi-source dashcam/CCTV footage + AI fraud signal extraction + court-ready export. These are three separate tools stitched together manually, if at all.

---

## Video Wisdom Platform Fit

This maps directly to the 12–24 month platform direction:

```
Vendor-agnostic ingest    → dashcam footage from 40+ device brands
Tamper-evident layer      → chain-of-custody from clip retrieval to submission
AI analysis               → flag anomalies, surface fraud signals
Compliance export         → court-ready package for disputed claims
```

Video Wisdom does not need to manufacture a single new camera to serve this market. The video already exists. The platform is the product.

Deployment speed moat applies: insurers need this live before next claims cycle, not in 6 months.

---

## What We Don't Know

These must be answered before any build decision:

1. **Who controls the footage?** Does the insurer retrieve dashcam clips directly, or does the fleet operator submit them? The chain-of-custody problem is different depending on the answer.
2. **What is the fraud ROI threshold?** At what cost-per-claim does automated video analysis become a clear yes for a mid-sized UK insurer?
3. **Is there a regulatory trigger coming?** FCA Consumer Duty (live July 2023) requires insurers to prove fair claims handling — does this create a compliance mandate for video evidence management?
4. **Who is the buyer?** Head of Claims? Chief Risk Officer? Counter-Fraud team? The GTM motion depends on this.

---

## Recommended Next Step

One 45-minute call with a Head of Claims or Counter-Fraud lead at a UK commercial fleet insurer (Direct Line Commercial, Zurich Fleet, Aviva Fleet, or a broker like Towergate).

Goal: confirm or kill the chain-of-custody gap. If confirmed, this becomes a Stage 0 Signal Capture candidate.

Do not build anything before this call.
