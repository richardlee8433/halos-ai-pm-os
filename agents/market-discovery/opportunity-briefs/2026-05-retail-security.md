# Opportunity Brief: Retail Security
**For:** CTPO
**Date:** 2026-05-14
**Status:** Unvalidated — based on market signals, not customer conversations

---

## The Opportunity in One Sentence

Retailers are sitting on thousands of hours of CCTV footage they cannot use for prosecution — theft is at a political flashpoint on both sides of the Atlantic, violent incidents are rising, and the gap between capturing footage and submitting court-ready evidence remains entirely manual and stitched together.

---

## Why Now

Four forces converged in 2024–2026:

**1. Retail crime is a legislative priority in both target markets**
In the US, Organized Retail Crime (ORC) has escalated to federal-level attention. Legislation is being discussed to treat coordinated theft rings as a federal offense, meaning retailers will face pressure to produce prosecution-grade evidence — not just incident reports. In the UK, retail crime became an explicit political issue in 2023–2025, with government pressure on the Crown Prosecution Service and retailers to increase prosecution rates. Both governments are creating demand for evidence that actually reaches court.

**2. The scale of loss has crossed the "tolerate and write off" threshold**
UK retailers suffered more than 20 million theft incidents last year, costing £2.2 billion. At that scale, shrinkage is no longer absorbed as a cost of business — it is a P&L line that requires an operational response. Loss prevention leaders are being asked to demonstrate prosecution pipelines, not just detection rates.

**3. Rising violent incidents are forcing a surveillance upgrade cycle**
Growing violent incidents in retail environments — including staff assaults — are pushing retailers to move beyond deterrence-only CCTV. This creates a new buyer: the retailer who has already invested in camera hardware but cannot extract prosecution-usable evidence from it. The camera is sunk cost. The software layer is the open problem.

**4. Existing systems were not built to produce evidence — they were built to deter**
Retail CCTV infrastructure was designed for loss prevention monitoring, not for the evidence chain. When prosecution is the goal, the process breaks down: footage retrieval is manual, format compatibility is inconsistent across store systems, and chain-of-custody documentation is absent or ad hoc. No incumbent retail security vendor owns the prosecution workflow.

---

## The Customer Pain

*In their own words where available, noted as indirect/inferred where not directly sourced:*

- "We have cameras in every aisle. But by the time we've pulled the clip, converted it, and handed it to the police, they say it's not in a format they can use." *(Inferred from operational pattern — needs direct validation)*
- "We don't have a standard process. Each store manager handles it differently." *(Inferred from distributed retail operations — needs direct validation)*
- "The police need chain-of-custody paperwork. We've never had to produce that before." *(Inferred from prosecution process requirements — needs direct validation)*
- "Most incidents we just write off because prosecution takes too long and costs more than the stolen goods." *(Indirect — sourced from UK retail trade association commentary on low prosecution rates)*
- "We can catch them on camera every time. We just can't do anything about it." *(Indirect — sourced from retail loss prevention community forums)*

*(All quotes are indirect or inferred. No direct customer conversations have been conducted. These must be validated in Stage 0 before any build decision.)*

---

## What Exists Today and Why It Fails

| Tool | What it does | Why it fails here |
|------|-------------|-------------------|
| Genetec / Milestone (VMS) | Centralized CCTV management, live monitoring | Records and monitors footage; no chain-of-custody layer, no prosecution-export workflow |
| Verkada | Cloud CCTV with basic AI tagging | Closed hardware ecosystem; footage export is manual; no tamper-evidence or court-format output |
| Checkpoint / Sensormatic | EAS tags, loss prevention hardware | Detects theft events; does not capture or process video evidence for prosecution |
| In-house LP teams | Pull clips, write incident reports, liaise with police | Manual, unscalable, inconsistent across stores; no audit trail on the evidence handling process itself |
| Police digital submission portals (UK: Digital Evidence Management systems) | Receive evidence from third parties | Require specific formats and metadata; retailers rarely know what's required until submission fails |

**The gap:** No tool in the current retail security stack owns the moment between "footage captured" and "evidence submitted to police or court." That workflow — retrieve, authenticate tamper-evidence, format to jurisdiction requirements, generate chain-of-custody documentation, export — is entirely manual. It fails silently: most incidents are written off rather than prosecuted because the evidence submission process is too expensive and uncertain.

---

## Video Wisdom Platform Fit

This maps directly to the 12–24 month platform direction:

```
Vendor-agnostic ingest    → pull footage from Genetec, Milestone, Verkada, any CCTV 
                            source or S3 bucket; no camera replacement required
Tamper-evident layer      → SHA-256 or equivalent hash on ingest; chain-of-custody 
                            from clip retrieval through submission
AI-assisted tagging       → flag incident footage automatically; reduce manual review 
                            time for LP teams handling high-volume incidents
Compliance export         → court-ready package in jurisdiction-specific formats 
                            (UK Crown Court, US federal/state submission)
Audit trail               → full documentation of who accessed, exported, and submitted 
                            each piece of evidence
```

Video Wisdom does not need to displace the camera infrastructure. The cameras are already in every store. The platform is the missing software layer between the camera and the prosecution.

The vendor-agnostic ingest direction is the specific moat here: retail environments run three to five different camera brands across a single chain. Any solution that requires camera replacement will not be bought.

---

## What We Don't Know

These are the blocking questions a single 30-minute call would begin to answer:

1. **What does the current video evidence submission process actually look like?** When a UK retailer decides to prosecute, who pulls the footage, in what format, how is it handed to police, and what documentation is required? The answer determines whether Video Wisdom's compliance export is a feature or the entire product. *(This is the single most important unknown.)*

2. **Who is the buyer and what is their budget authority?** Is this a Loss Prevention Director decision, a Head of Security decision, or does it require sign-off from Legal? The procurement path determines GTM. In large chains (Tesco, M&S, Walmart) these may be entirely separate functions.

3. **Is prosecution actually the goal, or is deterrence still the primary outcome sought?** If retailers have given up on prosecution and are only seeking deterrence, the evidence-chain framing is wrong. The brief above assumes prosecution intent — this must be confirmed directly.

4. **What is the IT constraint?** Does retail LP have the authority to procure a SaaS tool, or does it go through central IT / procurement? The CCTV infrastructure is typically owned by IT, not Loss Prevention. Who controls the camera feed access?

5. **How does ORC differ from opportunistic theft in terms of evidence requirements?** ORC cases involve multiple incidents, multiple stores, and federal-level coordination. The evidence packaging requirement is fundamentally different from a single-store theft. Does this create a premium tier, or is it a different buyer entirely (federal law enforcement vs. retail LP)?

6. **What are the UK Police Digital Submission requirements?** UK police forces have specific digital evidence submission standards. Does existing retail CCTV footage meet those standards by default, or does it systematically fail? If it fails, that is a validated, recurring pain point.

---

## Recommended Next Step

Two parallel calls in the same week — one UK, one US:

**UK — Target:** Head of Loss Prevention or Head of Security at a UK grocery or high-street retailer running 100+ stores. Specific organizations: Tesco, Marks & Spencer, Sainsbury's, Boots, or John Lewis. UK retail LP is a relatively small professional community — the British Retail Consortium (BRC) Retail Crime Survey team is a credible warm introduction path.

**US — Target:** Director of Asset Protection or VP of Loss Prevention at a large-format US retailer. Specific organizations: Walmart Asset Protection, Target Loss Prevention, Home Depot LP (known for ORC focus), or Walgreens (documented ORC problem). The National Retail Federation (NRF) Loss Prevention Council is the direct access point.

**Call goal:** Validate or kill the evidence submission gap. Ask them to walk through the last three prosecutions they attempted. Where did the process break down? What did the police or prosecutor ask for that they could not provide?

Do not pitch Video Wisdom on the first call. Map the process. The prosecution workflow is either a validated recurring failure or it is not — that finding determines whether this becomes a Stage 0 Signal Capture candidate.

Do not build anything before these calls.
