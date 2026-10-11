# Evidence, Recovery and Research Continuity

## Classify errors before acting

- **Transient or transport failure:** the calling system may retry when safe after establishing the operation's effect, or choose a different genuine research approach inside the approved goal.
- **Unknown write effect:** do not replay blindly. Re-fetch the exact intended target and verify whether the original write applied.
- **Explicit permission/safety/user denial:** obey the refusal. Renaming, splitting or moving the identical denied operation is not a legitimate recovery technique.
- **Version/frontier conflict:** query the Owner's accepted state and reconcile before acceptance; a timestamp or file existence cannot settle authority.

The Python example records `TRANSIENT`, `UNKNOWN_EFFECT` and `EXPLICIT_DENIAL` distinctly. Its `reconcile(..., applied=True, observed_checksum=...)` only demonstrates a transition *after an external system has supposedly verified a readback*. It does not independently perform the read.

## Redefine an unaccepted research attempt

If an unsuccessful attempt has no exclusive required finding and a different allowed method can advance the same research objective, a new attempt may be drafted.

The public function `redefine(..., distinct=True, within_scope=True)` assumes those decisions have already been established externally. It checks for a changed method and note, but **cannot semantically distinguish a safe new approach from a disguised replay**. This is not a permission override.

A denied attempt cannot enter the redefinition path in the example.

## Selective recovery packets

Not every failed draft must be stored permanently. `optional_recovery(..., irreplaceable=True)` demonstrates a noncanonical packet for material that requires later attention. No packet updates an accepted frontier or creates a future background task.

In real operations, a genuinely valuable recovery record needs a permitted storage location, its own successful readback, a lineage reference and an Owner decision about later admission.

## Evidence versus scientific admission

A research note can cite a known source ID and pass a simulated checksum readback while containing an **incorrect inference**. Batch admission in this package increments a progress marker but leaves `substantive_conclusion_accepted=False` by design.

Scientific conclusions, hypothesis rankings, new operating claims and downstream project states require their own validated domain-specific acceptance process.

## Repeatable testing

The included tests exercise stale frontier handling, scheduled packets, uncertain writes, local failures, issue references, checkpoint restoration, Owner gates and preservation of the scientific acceptance boundary.

No result from these tests should be interpreted as an empirically measured improvement in research quality or external scheduler reliability.
