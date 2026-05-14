# Opportunity Brief: Healthcare Video Evidence Management
**For:** CTPO
**Date:** 2026-05-14
**Status:** Unvalidated — based on regulatory signals and market inference, not customer conversations

---

## The Opportunity in One Sentence

US and UK hospitals are running extensive CCTV infrastructure with no HIPAA-compliant (or UK GDPR-compliant) video evidence management layer — and regulators are closing in.

---

## Why Now

Three forces are converging in 2025–2026:

**1. HIPAA enforcement on video is no longer theoretical**
OCR (HHS Office for Civil Rights) guidance is explicit: if footage can identify an individual and relates to care, payment, or health status, it is Protected Health Information under HIPAA. Most hospital CCTV operations are not currently managed under HIPAA-compliant controls. Enforcement actions and settlement agreements referencing physical and facility surveillance are increasing. The compliance gap is documented — it is no longer a grey area.

**2. Workplace violence reporting mandates are creating a video evidence paper trail requirement**
The Joint Commission (US) and NHS Trusts (UK) are tightening requirements for incident documentation. Workplace violence in clinical settings — a recognised epidemic — requires detailed incident records including video. Hospitals need footage they can submit to HR, legal, and law enforcement in a chain-of-custody format. Today they cannot do this reliably.

**3. Healthcare cybersecurity and privacy scrutiny has reached board level**
Post-Change Healthcare breach (2024), HIPAA enforcement budgets increased and OCR signalled broader enforcement scope, including physical security controls. Hospital boards are now asking whether their surveillance infrastructure is a liability. This creates a procurement window for solutions framed as compliance infrastructure, not IT projects.

---

## The Customer Pain

*In their words, not Video Wisdom language — note: all indirect, sourced from public regulatory guidance, healthcare trade press, and incident reports. Needs direct validation:*

- "We have cameras everywhere but no way to pull footage securely when there's an incident — it goes through the facilities team, not compliance."
- "When we need to respond to an OCR audit, we can't produce a clean chain of custody for surveillance footage the way we can for EHR access logs."
- "Legal holds on video are informal. Someone saves a clip to a USB. That's not defensible."
- "After a patient assault, we need footage for the police report and the HR investigation — those go through completely different people and neither process is documented."

*(Sources: Joint Commission sentinel event advisories, OCR settlement summaries, healthcare security forum discussions, HIPAA Journal reporting — all indirect. No first-party customer quotes in hand.)*

---

## What Exists Today and Why It Fails

| Tool | What it does | Why it fails here |
|------|-------------|-------------------|
| Milestone / Genetec (VMS) | Video management system — view, record, store CCTV | No HIPAA compliance layer, no chain-of-custody, no audit trail for evidence export |
| Avigilon (Motorola Solutions) | Enterprise CCTV management | Same gap as Milestone/Genetec — built for physical security, not regulated evidence |
| Hospital EHR systems (Epic, Cerner) | Patient record management | Does not ingest video; chain-of-custody designed for clinical data, not surveillance footage |
| Manual incident workflows | Facilities pulls clip, emails to HR/Legal | No tamper verification, no audit trail, not court-ready, not HIPAA-documented |
| Body-worn camera vendors (Axon, Motorola) | Captures video, provides basic evidence management | Built for law enforcement chain-of-custody, not healthcare compliance workflows; high hardware cost |

**The gap:** No vendor provides HIPAA-compliant ingest of existing hospital CCTV footage + tamper-evident chain-of-custody + documented export for legal, HR, and law enforcement use cases — without requiring a hospital to replace its existing camera infrastructure.

---

## Video Wisdom Platform Fit

This maps directly to the 12–24 month platform direction:

```
Vendor-agnostic ingest    → pull from existing Milestone, Genetec, Avigilon, or any CCTV/S3 source
                            no hardware replacement required
Tamper-evident layer      → SHA-256 chain-of-custody from ingest to export
                            satisfies HIPAA physical safeguard documentation requirements
AI-assisted tagging       → incident flagging, PII redaction before disclosure
                            supports HIPAA minimum necessary standard
Compliance export         → packaged evidence for OCR audits, legal holds, police submissions
                            audit log format aligned to HIPAA §164.312 audit controls
```

Video Wisdom does not need to sell a single camera into a hospital. The CCTV infrastructure already exists. The platform closes the compliance gap between the physical security layer and the regulated evidence layer.

UK relevance: NHS Trusts and private healthcare operators fall under UK GDPR + Data Security and Protection Toolkit (DSPT) requirements. The same vendor-agnostic ingest + chain-of-custody architecture applies; the compliance export layer needs a UK variant.

---

## What We Don't Know

These are blocking questions. A 30-minute call with the right role would answer most of them:

1. **Who owns the footage today?** Is it Facilities, IT, Legal, or a third-party VMS vendor? If it is a third-party vendor, the chain-of-custody problem starts earlier than the software layer — and Video Wisdom's integration story changes.
2. **Has any hospital in this segment received an OCR enforcement action specifically citing surveillance video?** If yes, this is a proven procurement trigger. If not, the regulatory pressure is real but the buyer urgency may lag.
3. **What is the incident volume that drives the ROI case?** How many times per month does a large hospital need to produce regulated video evidence (for HR, legal, or law enforcement)? The per-incident cost of manual retrieval vs. platform cost determines the sale.
4. **Is the buyer in Legal, Compliance, or Physical Security?** These are different budget owners with different procurement cycles and different definitions of "done." The GTM motion is entirely different depending on the answer.
5. **UK DSPT requirement specificity:** Does the NHS Data Security and Protection Toolkit explicitly require chain-of-custody controls on surveillance footage, or is this an interpretive gap? This determines whether UK is a soft-sell compliance argument or a hard regulatory mandate.

---

## Recommended Next Step

One 30-minute call with a **Chief Compliance Officer or Privacy Officer at a US health system with 200+ beds** (not an IT contact — this is a compliance and legal risk conversation, not a technology evaluation).

Target organisations to approach cold: mid-sized regional health systems where HIPAA enforcement risk is high and dedicated video compliance infrastructure is unlikely to already exist. Avoid the top-10 academic medical centres — they will have bespoke solutions or active vendor relationships that slow the discovery signal.

UK equivalent: NHS Trust Data Protection Officer or Head of Legal Services at a mid-sized acute trust.

**Do not build anything before this call.** The regulatory case is credible. The buyer identity and procurement trigger are unconfirmed. Stage 0 Signal Capture cannot start without at least 3 independent voices describing the same friction point.
