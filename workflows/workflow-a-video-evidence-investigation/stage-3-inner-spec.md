# Workflow A — Stage 3: Inner Spec
# Video Evidence Investigation · Review & Search · Investigator

**Version:** 1.0 · **Status:** Draft — confidence threshold pending PM + Legal sign-off
**Last updated:** 2026-04-27

---

```
Problem:
  Investigators manually scrub hours of body cam footage to locate key moments.
  One 45-min incident generates 4+ hrs of footage; review costs 8–16 hrs/week per investigator.

Success Metrics:
  - Key moment located in <3 min for a 45-min body cam video
  - AI event recall rate ≥85% on golden test set
  - Evidence integrity: 0 SHA-256 mismatches in production
  - User correction rate <10% of auto-tagged events at steady state

Technical Contract:
  POST /evidence/upload
    body:    { file: binary, uploader_id: string }
    returns: { evidence_id, sha256, timestamp }
  POST /analysis/run
    body:    { evidence_id, mode: "body_cam"|"static_cctv", model: "gemini"|"gpt4o"|"parallel" }
    returns: { analysis_id, status: "queued"|"processing"|"complete" }
  GET  /analysis/{analysis_id}
    returns: { events: [{ timestamp, description, confidence, type }], model, cost_usd }
  POST /analysis/{analysis_id}/correct
    body:    { event_id, corrected_value, officer_id }
    returns: { correction_id, timestamp }
  GET  /search
    params:  { query: string, evidence_ids?: string[] }
    returns: { results: [{ evidence_id, timestamp, score, snippet }] }

Decision Rationale:
  Model choice:     Gemini 1.5 Flash because lowest cost-per-minute + native video input
                    eliminates frame extraction overhead; GPT-4o retained for comparison mode only
  Cost basis:       ~$0.005/video (45-min body cam at Gemini Flash rates);
                    <$30 per 1,000hr at two-layer architecture (6× headroom vs. ceiling)
  Compliance basis: chain-of-custody satisfied by client-side SHA-256 before transmission;
                    AI writes isolated to analysis_record — never touch evidence_record
  Golden test set:  /tests/golden — 20 body cam clips (mixed lighting, motion, shift times);
                    pass rate ≥85% event recall required before Stage 4 sign-off

AI Confidence Handling:
  Auto-action threshold:    ≥0.85 → event auto-tagged in analysis_record
                            [OPEN: needs PM + Legal sign-off — see stage-2-decomposition.md]
  Below-threshold behavior: surfaced to reviewer_queue; investigator confirms before logging;
                            queue is non-blocking — investigation continues regardless
  User correction path:     ≤1 action (flag icon) → correction_log written:
                            { officer_id, timestamp, original_ai_output, corrected_value }
  Confidence display:       always visible per event; visual flag on events below threshold;
                            never hidden from user under any display mode
```

---

**Line count: 40 — at limit. No additions permitted without removing existing content.**
