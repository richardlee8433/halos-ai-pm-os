# Workflow A — Stage 3: Compliance Annex
# Video Evidence Investigation · Review & Search · Investigator

**Version:** 1.0 · **Status:** Draft — awaiting Legal / QA sign-off
**Last updated:** 2026-04-27
**Sign-off required from:** Legal or QA stakeholder before Stage 4

---

## 1. Chain-of-Custody Documentation Requirements

**SHA-256 fingerprinting**
- Hash computed client-side before any transmission — establishes evidence origin at source
- Hash stored in evidence_record at upload; recomputable at any point for verification
- SHA-256 mismatch = hard stop: analysis blocked, IT Admin alerted, incident logged
- Any re-encoding or format conversion of the original file after upload must be flagged and logged separately — the original hash is never retroactively updated

**Record separation**
- evidence_record: immutable after upload. Contains original file + SHA-256 + uploader ID + timestamp. No AI process may write to this record.
- analysis_record: AI output only. Linked to evidence_record via evidence_id but stored separately. All AI writes carry { type: "ai_write", model, timestamp, confidence_avg }.
- correction_log: Human corrections only. Linked to analysis_record via analysis_id. Each entry carries { officer_id, timestamp, original_ai_output, corrected_value, confidence_at_time }.

**Audit trail**
- Every action on evidence (upload, analysis trigger, correction, export, access) must generate an immutable audit log entry
- Audit log entries must be append-only — no deletion, no editing
- Audit log must distinguish: ai_write / human_correction / system_event / access_event
- Audit log must be exportable alongside evidence package for court submission

---

## 2. GDPR / Data Sovereignty Constraints

**Applicable frameworks (HALOS Ireland base)**
- EU Law Enforcement Directive (LED) — governs processing of personal data by competent authorities for law enforcement purposes
- Irish Data Protection Act 2018 — transposes LED into Irish law
- GDPR (Regulation 2016/679) — applies to processing outside strict law enforcement scope (e.g. admin, HR, billing)

**Standard video analysis (v1.0–v8.0)**
- Body cam footage containing identifiable persons: processed under LED Art. 8 (lawfulness of processing) — processing must be necessary for the performance of a task in the public interest
- Data minimisation: only frames passing L1 filter are sent to AI — no unnecessary data transmission
- Retention: HALOS must support configurable retention periods per agency policy; no footage retained beyond agency-defined limits
- Data residency: EU-hosted processing required for EU law enforcement customers; cross-border transfer restrictions apply

**⚠ CRITICAL — Tactical-Link Re-ID (v7.0): BLOCKED**
- Feature uses GPT-4o Vision to describe physical characteristics of individuals across camera feeds
- This constitutes processing of biometric data under GDPR Art. 4(14) and LED Art. 10
- GDPR Art. 9 / LED Art. 10: biometric data processing requires an explicit legal basis
- No legal basis has been documented. Feature must not ship until one of the following is established:

  Option A — Substantial public interest (GDPR Art. 9(2)(g) / LED Art. 10(2))
    → Requires: Data Protection Impact Assessment (DPIA) completed
    → Requires: Consultation with Irish Data Protection Commission (DPC) if high risk
    → Timeline estimate: 8–16 weeks minimum

  Option B — Restrict scope to post-incident review only (no real-time processing)
    → Reduces regulatory exposure (real-time biometric processing triggers higher scrutiny)
    → Requires: explicit policy restriction enforced at API level (mode: "post_incident_only")
    → Requires: Legal sign-off on restricted scope definition
    → Timeline estimate: 2–4 weeks

  Recommended path: Option B as interim measure while Option A is pursued in parallel.

- Until legal basis is established: Tactical-Link Re-ID endpoint must return 403 in production. Demo/staging environments may use it with explicit consent from participants.

---

## 3. Audit Trail Specifications

**Minimum required fields per audit entry**

```
{
  entry_id:       uuid,
  evidence_id:    string,
  event_type:     "upload" | "analysis_triggered" | "ai_write" | "human_correction"
                  | "export" | "access" | "sha256_mismatch" | "system_event",
  actor_type:     "officer" | "investigator" | "system" | "ai_model",
  actor_id:       string (officer badge number or system identifier),
  timestamp:      ISO 8601 UTC,
  model:          string | null (populated for ai_write events only),
  confidence:     float | null (populated for ai_write events only),
  details:        object (event-specific payload)
}
```

**Court admissibility requirements**
- Audit log must be cryptographically tamper-evident (append-only structure with hash chaining recommended)
- Export format must be human-readable AND machine-parseable (JSON + PDF render)
- Timestamps must be UTC with timezone explicitly declared
- Officer ID in correction_log must map to a verified badge/credential — not a self-reported string

---

## 4. Edge Cases for Court Submission

**AI output labelling**
- Every AI-generated event must carry a visible "AI-generated — advisory only" label in any export or court-facing document
- AI output must never be presented as primary evidence without a human review step documented in the audit trail
- Correction_log entries must appear alongside original AI output in any court export — showing both what the AI said and what the investigator corrected it to

**Chain-of-custody gaps**
- If SHA-256 cannot be verified at export time (e.g. original file unavailable), export must include an explicit gap notice — court package must not be generated silently with unverifiable integrity
- If analysis was run on a re-encoded file (not the original), this must be flagged in the evidence package with the re-encoding event documented

**Proprietary format handling**
- Many body cam manufacturers use proprietary formats (.dav, .dat, .dga)
- If HALOS re-encodes to a standard format for analysis, the original proprietary file must be preserved alongside the re-encoded version
- Re-encoding event must be logged in audit trail with: original format, target format, tool used, operator ID

---

## 5. AI Training Data Coverage Gaps

**Known gaps in Gemini 1.5 Flash and GPT-4o Vision**

| Gap | Risk | Mitigation |
|-----|------|-----------|
| Night / low-light footage | Higher hallucination rate on scene description | Laplacian filter rejects most blurry low-light frames; flag low-confidence events |
| Extreme weather (rain, fog on lens) | Motion detection unreliable; pixel diff skewed | Add weather condition tag to analysis_record; lower auto-action threshold in poor conditions |
| Non-English audio (officer commands) | Audio-visual mismatch in non-English deployments | System prompt specifies visual-first reasoning; audio is secondary signal |
| Demographic coverage | Training data may underrepresent certain demographics in Re-ID accuracy | Tactical-Link blocked pending GDPR resolution — accuracy gap moot until legal basis established |
| Shift time variance | Night shift footage underrepresented in typical training sets | Golden test set must include ≥5 clips from night shifts (00:00–06:00) |
| Body cam orientation | Extreme angles (officer fallen, camera blocked) produce misleading frames | Laplacian filter catches most occluded/blurred frames; scene detection flags as anomalous |

**Golden test set composition requirements**
- ≥20 clips total
- ≥5 clips: night shift (00:00–06:00)
- ≥5 clips: high-motion / pursuit scenarios
- ≥5 clips: indoor environments (low contrast)
- ≥5 clips: multi-officer scenes (audio interference)
- Location: /tests/golden (version controlled)
- Pass criteria: ≥85% event recall across full set before Stage 4 sign-off

---

## 6. Sign-Off Checklist

| Item | Owner | Status |
|------|-------|--------|
| Chain-of-custody architecture reviewed | Legal / QA | ⬜ Pending |
| GDPR Art. 9 gap acknowledged and mitigation path selected | Legal | ⬜ Pending |
| Tactical-Link production block confirmed | Engineering | ⬜ Pending |
| Audit trail format approved for court submission | Legal / QA | ⬜ Pending |
| Golden test set composition approved | PM + QA | ⬜ Pending |
| AI confidence threshold (0.85) signed off | PM + Legal | ⬜ Pending |

**Stage 3 Exit Criteria cannot be met until all items above are checked.**
