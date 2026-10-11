# Interactive Execution, Scheduled Production and Handoff

## Why routes differ

A general-purpose research workflow may use a direct interactive writer or a scheduled producer operating through a different host/data interface. **The fact that a scheduled job ran does not imply its output became the current accepted research.**

The public example declares one of two routes per attempt:

- `interactive` — a draft can become a simulated publication candidate, then a readback-verified candidate.
- `scheduled_producer` — a draft first produces a **noncanonical packet**, which must be separately published, read back and accepted.

The two-route convention is a teaching abstraction, not a rule that GitHub is always the scheduled writer or that any current ChatGPT scheduled task is running.

## State transitions

| Origin | Operation | Outcome | Important limitation |
| --- | --- | --- | --- |
| DRAFT (interactive) | publish with expected frontier | PUBLISHED_UNVERIFIED | Not an actual Git commit |
| DRAFT (scheduled) | produce_packet | PRODUCER_PACKET | Not a canonical result |
| PRODUCER_PACKET (scheduled) | explicit publish with expected frontier | PUBLISHED_UNVERIFIED | Handoff still requires host permissions |
| PUBLISHED_UNVERIFIED | readback with matching digest | VERIFIED_UNACCEPTED | Caller supplies observed digest |
| VERIFIED_UNACCEPTED | Owner authorization and frontier match | BATCH_ACCEPTED | Scientific conclusion remains unaccepted |

## Source-of-truth boundary

The real system's Owner must decide the selected writer and accepted frontier. Branch HEAD, source copies, checkpoints, Issue comments and scheduled-run metadata are **not sufficient** to override a live Owner selector.

The code's `owner_authorized=True` is only a synthetic signal to the state machine. It is **not an access-control system**.

## Scheduling claims

There is deliberately **no cron job, scheduled API call, unattended background worker or automatic future research** in this package. The synthetic scheduled path demonstrates a data handoff contract, not a functioning scheduling provider.

A real scheduled deployment would separately need:

1. A supported scheduler and explicit user authorization.
2. A documented route for receiving the scheduled producer's packet.
3. Exact input/Owner/clock context and version binding.
4. Idempotent handling of duplicate job deliveries.
5. Verified persistence and Owner-specific acceptance.
6. Monitoring of host limitations, permissions and runtime failures.

None of these external capabilities is claimed to be implemented by this repository.

## Multi-session handoff

`checkpoint()` emits JSON that can be reconstructed with `resume()`. It includes registered sources, accepted track frontiers, work attempts and their status, optional recovery packets and coordination references. The model is intentionally not hardened against untrusted checkpoint data, and the JSON is **not durably stored** unless an external writer persists it.
