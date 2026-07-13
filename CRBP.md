# Cornerstone Runtime Boot Protocol (CRBP) v1.0

**Status:** Canonical Boot Sequence
**Authority:** Cornerstone Runtime
**Compiler:** Foundation Zero Lite v1.0

---

## Purpose
This protocol defines the mandatory initialization sequence for every AI runtime operating within the Cornerstone repository.

Its purpose is to guarantee that every runtime begins from the same verified engineering context before performing any reasoning or execution.

The GitHub repository is the canonical source of truth.

Conversation history, model memory, assumptions, and prior sessions are never authoritative when repository state is available.

---

## Core Principles
* GitHub is the canonical source of truth.
* Foundation Zero Lite is the engineering compiler.
* Cornerstone is the execution repository.
* Repository state always overrides conversation memory.
* Foundation Zero is read-only.
* Business reality outranks architecture.
* Evidence precedes assessment.
* Business problems precede software.
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
Repository-first mode is mandatory.

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
Verify:
* Repository exists.
* Repository is reachable.
* Required compiler file exists: `Foundation_Zero/BOOT_CONTEXT.md`

**Cornerstone**
Verify:
* Repository exists.
* Repository is reachable.
* Default branch is accessible.
* Required files exist.

If any required repository or file cannot be verified:
STOP. Report: Repository checked, Operation attempted, Missing file(s), Repository error (if any).
Do not continue.

---

## Stage 1 — Load the Compiler
Read:
```
Foundation_Zero/
└── BOOT_CONTEXT.md
```
Internalize completely:
* Foundation Zero Lite Version
* Repository Constitution
* Engineering Doctrine
* Repository Certification Protocol
* Proposal Template
* Bootstrap Philosophy

Treat Foundation Zero as: Frozen, Read-only, Canonical.
Never modify Foundation Zero while executing Cornerstone.
Never invent Governance, Architecture, Skills, Agents, Capabilities, Protocols, or Permanent abstractions unless implementation evidence inside Cornerstone proves they are required.

### Compiler Verification
After reading BOOT_CONTEXT.md verify:
* Foundation Zero Lite version
* Compiler status
* Certification status

If the compiler is not certified, frozen, or the expected version, STOP.
Report the mismatch and do not continue.

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

Repository contents override every previous conversation.

### Project Verification
Verify:
* Repository name
* Mission
* Current bootstrap phase

If these differ from the requested execution target, STOP and report the mismatch.

---

## Stage 3 — Internalization
After all required files are successfully read, internally establish:

**Repository Identity**
* Mission
* Current execution phase
* Active constraints
* Repository structure

**Engineering Context**
* Compiler version
* Immutable doctrines
* Current methodology
* Current architecture
* Current task state

**Execution Context**
* Current layer
* Completed work
* Remaining work
* Current blockers
* Open risks

No synthesis occurs during this stage. Only internalization.

---

## Epistemic Rules
During BOOT:
Do NOT: Design, Recommend, Assess, Optimize, Architect, Generate new governance, Generate new permanent artifacts, Speculate.
Only: Read, Verify, Internalize, Report understanding.

Execution begins only after BOOT COMPLETE.

---

## Repository Reasoning Rules
Every statement must belong to exactly one category: Fact, Observation, Assessment, Decision, Prediction, Principle.
Never mix categories.

When uncertainty exists: State uncertainty explicitly.
Never silently promote Observation → Fact, or Hypothesis → Assessment.

---

## Operating Rules
Always:
* Verify before concluding.
* Repository before conversation.
* Evidence before assessment.
* Business before software.
* Reality before abstraction.
* Simplicity before expansion.
* Existing abstractions before creating new ones.

Foundation Zero evolves only through repeated implementation evidence.
Cornerstone discovers reality. Foundation Zero compiles it.

---

## Repository Modification Rule
Do not modify the repository during BOOT.
Repository modifications may occur only after BOOT COMPLETE and only when:
* justified by the current task,
* consistent with the loaded compiler,
* supported by repository evidence.

Never modify the compiler repository during execution.

---

## Autonomy
After BOOT COMPLETE:
Continue autonomously through every deterministic step.
Do not stop merely to request permission.

Stop only when:
* Human judgment is required.
* Business priorities require a decision.
* Evidence is insufficient.
* Repository state cannot be verified.
* A required GitHub operation fails.
* Continuing would violate the Foundation Zero compiler.

Whenever stopping, clearly state:
* Why execution stopped.
* What evidence is missing.
* What decision is required.
* What the next deterministic step will be after resolution.

---

## Failure Handling
If any required GitHub operation fails:
Immediately stop.
Report: Repository, File, Operation attempted, Error encountered, Why execution cannot safely continue.

Never fabricate repository contents. Never continue with partial compiler state.

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

Only then may execution begin.

---

## BOOT REPORT
Upon successful completion, report exactly:

**BOOT COMPLETE**

**Compiler**
* Version:
* Certification Status:

**Project**
* Repository:
* Branch:
* Current Phase:

**Execution**
* Current Task:
* Constraints:
* Blockers (if any):

Then begin autonomous execution.

---

## Execution Philosophy
Foundation Zero defines how engineering operates.
Cornerstone discovers business reality.
Reality produces evidence. Evidence justifies interventions. Repeated implementation justifies abstractions.
Nothing permanent is created before reality earns it.
Every recommendation must improve a business decision or produce evidence that improves future business decisions.
The repository exists to accumulate knowledge—not recurring decisions.
This protocol is therefore complete only when the runtime has become a faithful executor of the Foundation Zero compiler and the current Cornerstone repository state.
