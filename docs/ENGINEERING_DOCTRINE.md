---
Authority: Doctrine
Lifecycle State: Permanent
Owner: Core Maintainers
Permanence Justification: Removing this destroys the operational law of the repository.
---

# Engineering Doctrine

This is the engineering constitution. It contains the immutable rules for Foundation Zero execution. Every future implementation agent reads this before touching code.

## Foundational Principle
**Repositories accumulate knowledge. They should not accumulate decisions.**
Knowledge should remain. Repeated decisions should disappear into automation, contracts, or defaults.

## The 6-Layer Architectural Backbone
Foundation Zero operates on a strict, stable architectural backbone. The runtime (AI model) is explicitly the outermost layer.
* **Layer 0:** Kernel (Frozen)
* **Layer 1:** Capabilities (Requires justification to expand)
* **Layer 2:** Playbooks (Routine to expand)
* **Layer 3:** Execution State (Ephemeral data driving the current task)
* **Layer 4:** Operational Memory (Short-term context retained between execution steps)
* **Layer 5:** Runtime (The interchangeable execution engine, e.g., LLM)

## Foundational Interpretation

### Epistemic Clarity
Every repository statement must belong to exactly one category: Fact (physical reality), Observation (measurement), Assessment (evaluation), Decision (action), Prediction (hypothesis), or Principle (invariant rule). Mixing categories destroys analytical integrity.

### Business Priority Rule
Until implementation evidence demonstrates a constitutional deficiency, repository work must primarily improve business workflows rather than repository structure.

## Immutable Doctrines


1. **Never overwrite events.** [Test: `tests/governance/test_event_immutability.py`] Mistakes must be corrected with compensating events, never deletions.
2. **Evidence precedes assessment.** [Test: `tests/governance/test_evidence_first.py`] Semantic evaluation may only occur on strictly parsed physical evidence.
3. **Identity is eternal.** [Test: `tests/governance/test_identity_immutability.py`] Once an identity is minted, its meaning is permanently fixed.
4. **Projections are disposable.** [Test: `tests/governance/test_projection_rebuild.py`] The Event Ledger is truth. Any projection, graph, or database built from the ledger can and will be deleted and recomputed.
5. **Kernel earns abstractions only through repeated implementation.** [Test: `tests/governance/test_kernel_expansion.py`] A pattern becomes a capability only after it is successfully implemented at least twice in the application layer.
6. **Every irreversible operation occurs exactly once.** [Test: `tests/governance/test_idempotency.py`]
7. **Every semantic operation remains reversible.** [Test: `tests/governance/test_reversibility.py`]
8. **Repository is the source of truth.** [CI Check: `verify_no_external_state`] Not the conversation. Not external chat logs.
9. **ADR before architectural change.** [Test: `tests/governance/test_adr_coverage.py`] Code changes must be justified by published architectural decisions.
10. **No Level 0/1 expansion without implementation failure.** [Test: `tests/governance/test_architecture_freeze.py`] The foundation expands only when execution demonstrates an unsolvable flaw in the current architecture.
11. **Governance as Code.** [Test: `tests/governance/test_governance_coverage.py`] Governance documents are executable contracts whenever possible. They must eventually become tests or CI checks.
12. **The Disagreement Defect.** [Test: `tests/governance/test_documentation_drift.py`] When implementation and documentation disagree, the disagreement itself is a defect.
13. **The Verification Postcondition.** [Test: `tests/governance/test_verification_postcondition.py`] No operation may report SUCCESS without verifying the resulting external state against its postconditions.
14. **Justify Existence.** [Test: `tests/governance/test_repository_economics.py`] Every permanent file must explicitly justify its own existence with the required Metadata header.
15. **Ban "We'll Remember."** [CI Check: `verify_no_memory_assumptions`] Human memory is not infrastructure. Anything requiring memory must become evidence, a playbook, an ADR, or state.
16. **The Ultimate Test.** [Test: `tests/governance/test_decision_friction.py`] A repository should become easier to understand as it grows, not harder. Evaluates the `Decision Friction` KPI.
17. **Information Ownership.** Before creating a new artifact, identify the rightful owner of the information. If an existing artifact can own it without losing clarity, extend that artifact instead of creating a new one.
18. **Abstraction Leverage.** Every permanent abstraction must remove more future decisions than it creates. Otherwise it is accidental complexity.
19. **Complexity Types.** Distinguish strictly between Necessary Complexity (e.g., append-only ledgers) and Accidental Complexity (e.g., overlapping playbooks). Actively eradicate the latter.
20. **Earned Agent Abstractions.** [ADR-007] A Skill exists only when maintaining it costs less than repeatedly rediscovering the transformation it performs.

## Governance Freeze
No further governance changes are proposed until at least three independent business implementation projects have been completed using Foundation Zero.
