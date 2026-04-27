# Workflow A — Stage 2: Decomposition

**Status:** Complete · 1 open item (confidence threshold sign-off pending)
**Last updated:** 2026-04-27
**Source demo:** v8.1 (Gemini Flash + GPT-4o parallel, Body Cam Adaptive Mode)

---

## Context Chain

### Primary Flow — Single Video Analysis

```
[1] USER UPLOADS VIDEO
    → Frontend computes SHA-256 hash client-side
    → Evidence record created: { id, sha256, timestamp, uploader_id }
    → Original file locked (read-only after hash)

[2] SCENE DETECTION
    → System classifies video type:
      Body Cam:     high motion variance + first-person POV signals
      Static CCTV:  fixed frame, low baseline motion
      Unknown:      defaults to Body Cam mode (conservative)

[3] L1 FILTER (CPU — zero AI cost)
    Body Cam path:
      → Laplacian sharpness filter applied at 1/5s sampling rate
      → Blurry frames rejected (sharpness score below threshold)
      → Sharp frames queued for L2
    Static CCTV path:
      → Pixel difference computed per frame
      → Motion > 15% → frame queued for L2
      → Motion ≤ 15% → frame discarded (no AI call)

[4] ROUTING DECISION
    → If queued frames exist → proceed to L2
    → If no frames pass L1 → return "No significant activity detected"
      (logged in audit trail, not treated as analysis failure)

[5] L2 AI ANALYSIS
    Preferred path (Gemini 1.5 Flash):
      → Native video upload (no frame extraction)
      → System prompt: time-series reasoning + landmark tracking
        + first-person POV reconstruction (Body Cam mode)
      → Returns: events[] { timestamp, description, confidence, type }
    Comparison path (GPT-4o Vision):
      → Frame-sampled input (Laplacian-filtered frames)
      → Same system prompt structure
      → Runs in parallel with Gemini when comparison mode active

[6] RESULT STORAGE
    → AI output written to analysis_record (separate from evidence_record)
    → Audit log entry: { type: "ai_write", model, timestamp, confidence_avg }
    → AI writes flagged as distinct from human writes — never merged into
      original evidence record

[7] RESULTS DISPLAYED
    → Confidence score always visible per event (never hidden)
    → Model toggle available (Gemini / GPT-4o) — switches display only,
      no re-analysis required
    → Events timeline rendered with timestamp anchors

[8] INVESTIGATOR ACTIONS
    → Semantic search across all analyzed videos (cosine similarity)
    → Correction / flag on any AI event → 1 action
      writes: { correction_log_id, officer_id, timestamp, original, corrected }
    → Export package available (events + audit log + SHA-256 chain)
```

### Secondary Flow — Multi-Camera Tactical-Link (v7.0)

```
[1–6] Same as Primary Flow, run independently per camera feed

[7] CROSS-CAMERA RE-ID
    → GPT-4o Vision describes target characteristics per camera
    → Descriptions vectorised (text-embedding-3-small)
    → Cosine similarity computed across camera feeds
    → Matches above threshold → linked in subject_track record

[8] TOPOLOGY RESOLUTION
    → Camera topology graph consulted for physical adjacency
    → Implausible matches (wrong geography, impossible timing) filtered
    → Subject movement path reconstructed

[9] FORENSIC REPORT GENERATED
    → AI assembles: movement timeline, appearance at each camera,
      gaps / occlusion events, confidence per link
    → Report flagged as AI-generated advisory (not primary evidence)
```

### Failure Paths

```
F1: API timeout (Gemini or GPT-4o)
    → Queue retry (max 2 attempts)
    → If retry fails: surface to investigator as "Analysis pending"
    → Original evidence and SHA-256 chain preserved — never at risk

F2: Low confidence output (below auto-action threshold)
    → Event surfaced to reviewer queue
    → NOT written to evidence record
    → Confidence score displayed with visual flag

F3: Corrupted or unsupported file format
    → Rejected at upload stage
    → Attempt logged in audit trail
    → User notified with specific error

F4: SHA-256 mismatch detected post-upload
    → Hard stop — analysis blocked
    → Alert raised to IT Admin
    → Incident logged

F5: L1 filter rejects all frames (no activity detected)
    → "No significant activity" result returned
    → Logged — not treated as system failure
    → Investigator can override and force full analysis
```

---

## Routing Logic

```
INPUT: video file + scene_type

L1 DECISION (CPU, no cost):
  if scene_type == BODY_CAM:
    apply Laplacian filter at 1/5s → pass sharp frames to L2
  if scene_type == STATIC_CCTV:
    apply pixel_diff per frame → pass frames where diff > 15% to L2
  if no frames pass L1:
    return NO_ACTIVITY (skip L2 entirely — $0 cost)

L2 DECISION (AI cost incurred):
  if video_duration ≤ 60min:
    → Gemini 1.5 Flash native upload (preferred)
  if video_duration > 60min:
    → Chunk into 60min segments → parallel Gemini calls
  if comparison_mode == ON:
    → Gemini + GPT-4o run in parallel
    → Cost doubles — only activate on investigator request

COST OUTCOME:
  L1 filters ~90% of static footage → L2 called on ~10% of frames
  Target: <$30 per 1,000hr at production scale
```

---

## AI Feasibility Check

```
Problem type: Pattern recognition + summarization + temporal reasoning
→ AI fits. Not a deterministic rule-based problem.

Evidence: v8.0 failure mode ("food inquiry" misclassification) was caused
by wrong sampling rate + audio over-reliance, not AI unsuitability.
Fix (Laplacian + scene detection) resolved output quality.
```

---

## AI Confidence Handling (Three Mandatory Questions)

```
1. Auto-action threshold:
   Proposed: ≥ 0.85 confidence → event auto-tagged in analysis record
   Below 0.85 → surfaced to reviewer queue, not auto-written

   [GAP — needs PM + Legal sign-off before Stage 3]
   Rationale: 0.85 is proposed based on v8.1 output quality observation.
   No formal golden test set exists yet to validate this threshold.

2. Below-threshold behaviour:
   → Event added to reviewer_queue with confidence score displayed
   → Investigator must manually confirm or reject before event is logged
   → System does not block investigation — queue is non-blocking

3. User correction path (≤ 1 action):
   → Flag icon on each AI event (single tap / click)
   → Correction modal: original AI text pre-filled, investigator edits
   → On confirm: correction_log written { officer_id, timestamp,
     original_ai_output, corrected_value, confidence_at_time }
   → Correction feeds back to improvement queue (Stage 5)

   [GAP — correction UI exists in concept but not validated with
   real investigator in v8.1. Must be tested in Stage 4.]
```

---

## User Stories

### US-01 — Single Video Analysis (Core)
**As an** investigator
**I want to** upload a body cam video and receive a timestamped event summary
**So that** I can identify key moments without scrubbing the full footage

**Acceptance criterion:** AI returns ≥1 event with timestamp and confidence score within 3 minutes of upload for a 45-minute video

**Edge cases:**
- EC-01a: Video contains no significant activity → L1 filters all frames → system returns "No activity detected" with option to force full analysis
- EC-01b: Video file is corrupted → rejected at upload, audit log entry created, user notified
- EC-01c: AI confidence < 0.85 on all events → all events surfaced to reviewer queue, none auto-tagged

---

### US-02 — Model Comparison
**As an** investigator
**I want to** toggle between Gemini and GPT-4o analysis results for the same footage
**So that** I can identify which model captured details the other missed

**Acceptance criterion:** Toggle switches displayed result without re-triggering analysis; both results available within the same session

**Edge cases:**
- EC-02a: GPT-4o API unavailable → Gemini result shown by default, toggle disabled with explanatory message
- EC-02b: Investigator in low-bandwidth environment → comparison mode not available (cost + latency constraint), single-model result shown

---

### US-03 — Semantic Search
**As an** investigator
**I want to** search across all analyzed videos using natural language (e.g. "use of force")
**So that** I can find relevant footage without knowing the exact words in the transcript

**Acceptance criterion:** Search returns ranked results with timestamp anchors; "use of force" matches "suspect was restrained" and similar semantic equivalents

**Edge cases:**
- EC-03a: Search query returns no matches → empty state with suggested alternative queries shown
- EC-03b: Video not yet analyzed → excluded from search results, flagged as "pending analysis"
- EC-03c: Search term matches redacted content → result suppressed, redaction flag shown to investigator

---

### US-04 — AI Result Correction
**As an** investigator
**I want to** correct a wrong AI event description in ≤ 1 action
**So that** inaccurate AI output is never used as evidence without human review

**Acceptance criterion:** Correction logged with officer ID and timestamp; original AI output preserved alongside correction; ≤ 1 action to initiate correction from results view

**Edge cases:**
- EC-04a: Investigator closes session before confirming correction → correction discarded, original AI output retained, no partial write
- EC-04b: Two investigators correct the same event simultaneously → last-write-wins with both corrections logged

---

### US-05 — Evidence Integrity Verification
**As a** legal / QA reviewer
**I want to** verify that a video file has not been altered since upload
**So that** the evidence is admissible in court

**Acceptance criterion:** SHA-256 hash computed client-side at upload; hash recomputable at any point; mismatch triggers hard stop and alert

**Edge cases:**
- EC-05a: File re-encoded by third-party player before upload → hash mismatch detected, upload blocked
- EC-05b: AI analysis metadata written to original file (instead of analysis_record) → this must be architecturally impossible; AI writes only touch analysis_record, never evidence_record

---

### US-06 — Multi-Camera Subject Tracking (Tactical-Link)
**As an** investigator
**I want to** track a subject across multiple camera feeds automatically
**So that** I can reconstruct a movement timeline without manually reviewing each feed

**Acceptance criterion:** System links subject appearances across ≥2 cameras using semantic Re-ID; movement path displayed with timestamps and confidence per link

**Edge cases:**
- EC-06a: Subject appearance changes significantly (e.g. removes jacket) → Re-ID confidence drops; low-confidence links surfaced for human review
- EC-06b: Camera topology not configured → system warns that physical adjacency cannot be validated; links shown with lower confidence
- EC-06c: Subject never appears in second camera → no link created; gap flagged in forensic report as "subject not located after [timestamp]"

---

## Agent Review Notes

### Cost Analysis Agent
```
Context Chain reviewed: 2026-04-26

Routing logic validated:
  L1 filtering estimated to reduce L2 calls by ~90% on static CCTV
  Body cam: all frames pass L1 (Laplacian), cost reduction via
  Gemini native video vs frame-sampled GPT-4o (~80% cost saving)

Cost basis confirmed:
  Single video (45min body cam): ~$0.004–0.006 at Gemini Flash rates
  1,000hr at two-layer architecture: <$30 target achievable

Open item:
  Per-version cost estimates for v1.0–v8.0 not yet backfilled.
  Required before Stage 3 Decision Rationale is finalised.
```

### User Analysis Agent
```
Context Chain reviewed: 2026-04-26

Primary User (Investigator) alignment:
  Context Chain matches investigator workflow: upload → review summary
  → search → correct → export. Sequence is logical.

Concern flagged:
  US-04 correction flow (≤1 action) has not been validated with a
  real investigator. v8.1 demo did not include this interaction.
  Must be tested in Stage 4 with ≥5 investigators before release.

Concern flagged:
  Comparison mode (US-02) adds cognitive load. Investigator must
  know which model to trust and when. Needs UX guidance in the UI —
  not just a toggle. Recommend: add "when to use each model" tooltip
  or contextual recommendation in Stage 3 spec.
```

### Trust & Compliance Agent
```
Context Chain reviewed: 2026-04-26

Chain-of-custody architecture: PASS
  AI writes to analysis_record only. evidence_record is immutable
  post-upload. SHA-256 in F4 failure path is correctly defined.

Compliance gap confirmed (from Stage 0):
  v7.0 Tactical-Link Re-ID uses GPT-4o Vision to describe person
  characteristics. This constitutes biometric data processing under
  GDPR Art. 9. No legal basis documented. This feature must not
  ship without explicit legal basis established in Compliance Annex.

  Recommended legal basis options:
    a) Substantial public interest (Art. 9(2)(g)) — requires DPA consultation
    b) Restrict Re-ID to post-incident review only (not real-time)
       which reduces regulatory exposure

AI advisory labelling gap confirmed:
  AI output is not explicitly labelled as advisory in current UI.
  Must be added before Stage 3. Hard Line #2 applies.
```

---

## Profile Revision Window

No revision to Use Case Profile required at this stage.

```
Current Profile:
  Cluster:          Review & Search
  Primary User:     Investigator
  Evidence Node:    Tag → Review
  Decision Nature:  Async Review

Assessment: Profile remains valid. All User Stories and Context Chain
are consistent with this profile. No revision triggered.
```

---

## Exit Criteria

| Criteria | Status |
|----------|--------|
| Context Chain covers ≥1 failure path | ✓ Five failure paths documented (F1–F5) |
| Every User Story has acceptance criterion + ≥1 named edge case | ✓ US-01 to US-06 |
| AI confidence questions answered | △ Proposed answers documented; threshold (0.85) needs PM + Legal sign-off |
| All Required agents reviewed Context Chain | ✓ Cost Analysis, User Analysis, Trust & Compliance |

**Status: Stage 2 Exit Criteria met with one open item.**
Open item: AI confidence threshold (0.85) must be formally signed off by PM + Legal before Stage 3 Inner Spec is finalised.

---

## Output Summary

- Context Chain: Primary flow (9 states) + Tactical-Link flow + 5 failure paths ✓
- User Stories: US-01 to US-06 with edge cases tagged ✓
- Routing logic: L1 (Laplacian / pixel diff) → L2 (Gemini preferred) documented ✓
- Agent review notes: 3 Required agents completed ✓
- Profile revision: Not required ✓

→ **Next: Stage 3 — Dual Specification**
