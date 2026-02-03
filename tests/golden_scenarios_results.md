# Golden Scenarios Test Results

**Test Date:** 2026-01-26
**Zeus Version:** 0.1.0
**Model:** anthropic/claude-sonnet-4

## Summary

| Status | Count |
|--------|-------|
| Passed | 7/7 |
| Failed | 0/7 |

## Test Results

### Case 1: API Design with Constraints
**Status:** PASS
**LLM Calls:** 4
**Revision:** No
**Run ID:** `5437ad00-cfec-4ff6-b10d-bfd444798961`

**Scenario:** Design a minimal REST API for a RunRecord logging service with exactly 4 endpoints.

**Expected Properties:**
- [x] Critique runs and reports no blocker/major issues
- [x] No revision loop
- [x] Output respects constraints (best effort)
- [x] assumptions[] and known_issues[] present
- [x] RunRecord persisted

---

### Case 2: Conflicting Architectural Constraints
**Status:** PASS
**LLM Calls:** 6
**Revision:** Yes (1)
**Run ID:** `9ddd6df9-be1a-4a35-aff7-e07e522ff2b6`

**Scenario:** Event processing pipeline with exactly-once delivery and zero operational complexity (conflicting constraints).

**Expected Properties:**
- [x] System proceeds best-effort (does not block)
- [x] Critique flags major conflict/infeasibility
- [x] Revision attempts pragmatic design with trade-offs
- [x] known_issues explicitly notes constraint conflicts

---

### Case 3: Structured JSON Output
**Status:** PASS
**LLM Calls:** 4
**Revision:** No
**Run ID:** `39e45de4-bb00-413f-8134-b5f9f01c3c4d`

**Scenario:** Request JSON architecture description with specific keys.

**Expected Properties:**
- [x] Generator attempts structured output
- [x] Best-effort response returned
- [x] <=1 revision
- [x] known_issues present

---

### Case 4: Under-Specified Requirements
**Status:** PASS
**LLM Calls:** 4
**Revision:** No
**Run ID:** `1271d201-596c-4948-a646-ef08f40bccdd`

**Scenario:** Design a policy gate component with no constraints provided.

**Expected Properties:**
- [x] Normalizer infers default output format (markdown)
- [x] Critique flags missing inputs
- [x] assumptions lists reasonable defaults (15 assumptions)
- [x] No blocking; best-effort design returned

---

### Case 5: Multi-View Coverage Requirement
**Status:** PASS
**LLM Calls:** 6
**Revision:** Yes (1)
**Run ID:** `5fa242d0-ed69-4cd0-a891-69795a26143e`

**Scenario:** End-to-end architecture for a self-improving operations assistant.

**Expected Properties:**
- [x] Critique includes multi-view coverage:
  - [x] scope
  - [x] architecture
  - [x] risk
  - [x] security
  - [x] compliance
  - [x] evaluation
- [x] Revision attempts to address major issues
- [x] known_issues includes open questions

---

### Case 6: Failure Mode Emphasis
**Status:** PASS
**LLM Calls:** 4
**Revision:** No
**Run ID:** `75d1d13c-b9fd-417a-8ab8-64482c4b346e`

**Scenario:** Run controller design with failure-mode table (6+ failure modes required).

**Expected Properties:**
- [x] System returns best-effort output
- [x] Constraint preserved (8 failure modes in table)
- [x] known_issues mentions limitations
- [x] RunRecord includes execution details

---

### Case 7: Deterministic Constraint Enforcement
**Status:** PASS
**LLM Calls:** 4
**Revision:** No
**Run ID:** `40be4c2f-dea6-4930-95fc-677e62732f3f`

**Scenario:** Constraint checker layer with required section titles.

**Expected Properties:**
- [x] Constraints appear in NormalizedProblem
- [x] Critique checks for section-title requirements
- [x] Output includes "Deterministic Checks" section
- [x] Output includes "Heuristic Checks" section

---

## MVP Invariants Verified

| Invariant | Status | Notes |
|-----------|--------|-------|
| 1. Critique mandatory | PASS | All 7 cases had critique run |
| 2. Traceability (run_id + RunRecord) | PASS | All 7 cases persisted |
| 3. Transparency fields present | PASS | assumptions[] and known_issues[] in all cases |
| 4. No silent constraint loss | PASS | Constraints preserved in all cases |
| 5. Budget enforcement (<=6 calls, <=1 revision) | PASS | Max 6 calls observed |
| 6. Graceful degradation | PASS | Best-effort output on all cases |
| 7. Generator/Critic separable | PASS | Evidenced by architecture |
| 8. Provenance recorded | PASS | model_version, prompt_versions in RunRecords |
| 9. Append-only RunRecords | PASS | JSON files in run_records/ |

## Usage Statistics

| Case | LLM Calls | Tokens In | Tokens Out | Total Tokens | Cost (USD) |
|------|-----------|-----------|------------|--------------|------------|
| 1 | 4 | 4,061 | 3,731 | 7,792 | $0.0681 |
| 2 | 6 | 10,256 | 8,632 | 18,888 | $0.1602 |
| 3 | 4 | 4,192 | 3,712 | 7,904 | $0.0683 |
| 4 | 4 | 4,921 | 5,222 | 10,143 | $0.0931 |
| 5 | 6 | 15,616 | 13,726 | 29,342 | $0.2527 |
| 6 | 4 | 5,691 | 5,553 | 11,244 | $0.1004 |
| 7 | 4 | 5,073 | 5,004 | 10,077 | $0.0903 |
| **Total** | **32** | **49,810** | **45,580** | **95,390** | **$0.8331** |

## How to Reproduce

```bash
# Set API key
export OPENROUTER_API_KEY="your-api-key"

# Run all golden scenario tests
cd zeus
pytest tests/test_golden_scenarios.py -v --timeout=600

# Run specific case
pytest tests/test_golden_scenarios.py::TestGoldenScenarios::test_case_1_api_design -v
```

## Notes

- Cases 2 and 5 triggered revisions due to major issues identified during critique
- All cases completed within budget (max 6 LLM calls)
- 6-perspective critique coverage verified across all scenarios
- Run records available in `run_records/` directory for full traceability
