# Cornerstone Runtime Contract v1.0

This contract governs the continuous execution phase of any AI runtime operating within the Cornerstone repository, immediately following a successful BOOT COMPLETE.

## 1. Operating Rules
Always:
* Verify before concluding.
* Repository before conversation.
* Evidence before assessment.
* Business before software.
* Reality before abstraction.
* Simplicity before expansion.
* Existing abstractions before creating new ones.

## 2. Repository Modification Rule
Repository modifications may occur only after BOOT COMPLETE and only when:
* justified by the current task,
* consistent with the loaded compiler,
* supported by repository evidence.

Never modify the compiler repository during execution.

## 3. Autonomy
After BOOT COMPLETE:
Continue autonomously through every deterministic step. Do not stop merely to request permission.

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

## 4. Failure Handling
If any required GitHub operation fails:
Immediately stop.
Report: Repository, File, Operation attempted, Error encountered, Why execution cannot safely continue.

Never fabricate repository contents. Never continue with partial compiler state.

## 5. Continuous Verification
Verification is not limited to boot. It is the execution heartbeat:
`EXECUTE -> VERIFY -> REPORT -> CORRECT (if needed) -> VERIFY -> CONTINUE`

Every action must be verified against repository state and compiler rules before the next action is taken.
