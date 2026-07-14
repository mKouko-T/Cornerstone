# Cornerstone Runtime Boot Protocol (CRBP) v2.0

**Status:** Canonical Boot Sequence
**Authority:** Cornerstone Runtime
**Architecture:** Foundation Zero Compiler Pipeline

---

## Purpose
This protocol defines the mandatory initialization sequence for every AI runtime operating within the Cornerstone repository.

By design, the runtime **never parses raw repository documents**. It solely consumes the deterministic compiled artifact (`BOOT_PACKAGE.md`) and verifies its cryptographic provenance against the machine-readable manifest (`BOOT_MANIFEST.json`).

---

## Core Principles
* The compiler builds reality; the runtime executes it.
* The `BOOT_MANIFEST.json` is the sole source of truth for certification and provenance.
* A mismatch between the Package's `BOOT_ID` and the Manifest's `boot_id` is a fatal architectural violation.
* Every recommendation after boot must comply with the loaded Canonical IR.

---

## Stage 1 — Load the Compiled Package
Read the executable artifact:
`BOOT_PACKAGE.md`

Extract the `BOOT_ID` from the header.
Internalize all sections of the package (Compiler, Rules, Mission, Canonical Model, Methodology, Task State).

---

## Stage 2 — Verify the Manifest
Read the machine-readable source of truth:
`BOOT_MANIFEST.json`

Verify the following:
1. **Schema Check**: Ensure the manifest schema is supported (e.g., `v1`).
2. **Boot Identity Match**: Compare the `BOOT_ID` from `BOOT_PACKAGE.md` against the `boot_id` inside the `certification` block of the JSON manifest. They must match exactly.
3. **Cryptographic Integrity**: Verify that the `certification` block explicitly declares the `compiler_identity`, `repository_commit`, and `manifest_hash`.

If the IDs do not match, or if the certification block is invalid, STOP. Do not continue. The compiled package is tainted.

---

## Stage 3 — Epistemic Internalization
After verification, internally establish:
* **Repository Identity**: Mission, Phase, Constraints.
* **Engineering Context**: Compiler version, Doctrines, Methodology, Architecture, Task state.
* **Execution Context**: Current layer, Completed work, Remaining work, Blockers.

During BOOT, Do NOT: Design, Recommend, Assess, Optimize, Architect, Generate new governance, Speculate.
Only: Read, Verify, Internalize.

---

## Repository Reasoning Rules
Every statement must belong to exactly one category: Fact, Observation, Assessment, Decision, Prediction, Principle. Never mix categories.
When uncertainty exists: State uncertainty explicitly. Never silently promote Observation → Fact, or Hypothesis → Assessment.

---

## BOOT COMPLETE Criteria
Declare **BOOT COMPLETE** only after all of the following are true:
* [x] `BOOT_PACKAGE.md` successfully loaded.
* [x] `BOOT_MANIFEST.json` successfully loaded.
* [x] `BOOT_ID` match verified.
* [x] Cryptographic/Hash Certification flags verified as PASS.
* [x] Current execution phase identified.
* [x] Current task board understood.

---

## BOOT REPORT
Upon successful completion, report exactly:

```text
BOOT COMPLETE

Compiler
---------
Version: [From Manifest]
Remote Commit: [From Manifest]

Package Identity
----------------
BOOT_ID: [Verified ID]
Generated: [From Manifest]

Execution
---------
Current Task: [From Package]
Phase: [From Package]

Verification
------------
Manifest Verified: PASS
ID Match: PASS
Certification Valid: PASS
```

Then begin autonomous execution as governed by the `Runtime_Contract.md`.
