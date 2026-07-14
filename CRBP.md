# Cornerstone Runtime Boot Protocol (CRBP) v1.0

**Status:** Canonical Boot Sequence
**Authority:** Cornerstone Runtime
**Compiler:** Foundation Zero Lite v1.0

---

## Purpose
This protocol defines the mandatory initialization sequence for every AI runtime operating within the Cornerstone repository.
Its purpose is to guarantee that every runtime begins from the same verified engineering context before performing any reasoning or execution.
Conversation history, model memory, assumptions, and prior sessions are never authoritative when repository state is available.

---

## Core Principles
* GitHub is the canonical source of truth.
* Foundation Zero Lite is the engineering compiler.
* Cornerstone is the execution repository.
* Repository state always overrides conversation memory.
* Foundation Zero is read-only.
* Every recommendation must comply with the loaded compiler.

---

## Canonical Source Priority
1. Repository state
2. Compiled context (BOOT_CONTEXT.md / BOOTSTRAP.md)
3. Canonical documents
4. Conversation
5. Model memory

Higher levels always override lower levels.

---

## Repository-First Mode
Whenever repository state is relevant:
* Read the repository before reasoning.
* Never infer repository contents.
* Never substitute conversation memory for repository evidence.
* Never fabricate missing files.
* Verify before concluding.

---

## Stage 0 — Repository Verification
Before reading any files, verify the repository itself.

**Foundation Zero**
* Repository exists.
* Repository is reachable.
* Required compiler file exists: `Foundation_Zero/BOOT_CONTEXT.md`

**Cornerstone**
* Repository exists.
* Repository is reachable.
* Default branch is accessible.
* Required files exist.

If any required repository or file cannot be verified, STOP. Report: Repository checked, Operation attempted, Missing file(s), Repository error (if any). Do not continue.

---

## Stage 1 — Load the Compiler
Read: `Foundation_Zero/BOOT_CONTEXT.md`
Internalize completely: Foundation Zero Lite Version, Repository Constitution, Engineering Doctrine, Repository Certification Protocol, Proposal Template, Bootstrap Philosophy.

Treat Foundation Zero as: Frozen, Read-only, Canonical. Never modify Foundation Zero while executing Cornerstone.

### Compiler Verification
After reading BOOT_CONTEXT.md verify:
* Foundation Zero Lite version
* Compiler status
* Certification status

If the compiler is not certified, frozen, or the expected version, STOP. Report the mismatch and do not continue.

---

## Stage 2 — Load the Project
Read from `mKouko-T/Cornerstone` in this order:
1. `README.md`
2. `BOOTSTRAP.md`

Then, if present: `CONTEXT.md` or `RUNTIME_CONTEXT.md`, read only that compiled context.
Otherwise read:
* `docs/Genesis_Methodology.md`
* `docs/CORNERSTONE_GENESIS_HANDOFF.md`
* `docs/Canonical_Model.md`
* `task.md`

### Project Verification
Verify: Repository name, Mission, Current bootstrap phase.
If these differ from the requested execution target, STOP and report the mismatch.

---

## Stage 3 — Internalization
After all required files are successfully read, internally establish:
* **Repository Identity**: Mission, Phase, Constraints, Structure.
* **Engineering Context**: Compiler version, Doctrines, Methodology, Architecture, Task state.
* **Execution Context**: Current layer, Completed work, Remaining work, Blockers, Risks.

No synthesis occurs during this stage. Only internalization.

---

## Epistemic Rules
During BOOT, Do NOT: Design, Recommend, Assess, Optimize, Architect, Generate new governance, Generate new permanent artifacts, Speculate.
Only: Read, Verify, Internalize, Report understanding.

---

## Repository Reasoning Rules
Every statement must belong to exactly one category: Fact, Observation, Assessment, Decision, Prediction, Principle. Never mix categories.
When uncertainty exists: State uncertainty explicitly. Never silently promote Observation → Fact, or Hypothesis → Assessment.

---

## BOOT COMPLETE Criteria
Declare **BOOT COMPLETE** only after all of the following are true:
* [x] GitHub connection verified
* [x] Foundation Zero repository verified
* [x] Cornerstone repository verified
* [x] Foundation Zero Lite compiler loaded
* [x] Cornerstone project context loaded
* [x] Required files successfully read
* [x] Current execution phase identified
* [x] Current task board understood
* [x] Constraints internalized
* [x] Repository state verified
* [x] No unresolved boot errors remain

---

## BOOT REPORT
Upon successful completion, report exactly:

```text
BOOT COMPLETE

Compiler
---------
Version:
Certification:
Status:

Project
-------
Repository:
Branch:
Commit:
Phase:

Execution
---------
Current Task:
Constraints:
Blocking Issues:

Verification
------------
Compiler Loaded: PASS
Repository Verified: PASS
Project Loaded: PASS
```

Then begin autonomous execution.

---

## Execution Philosophy
Execution after BOOT is governed by:
* Foundation Zero Lite
* Current Repository State
* [Runtime Contract](docs/Runtime_Contract.md)
