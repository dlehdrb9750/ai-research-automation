# Architecture — Continuous Research Without False Acceptance

## Responsibility model

This public prototype models research state transitions in a **single process**. It is not a live implementation of a research engine or a scheduler.

| Role | Owns | Does not own |
| --- | --- | --- |
| **Research track / Owner** | Research objective, evidence requirements, local accepted frontier | Another track's conclusions or credentials |
| **Source register** | Source identifiers, locator, inspection timestamp and title | Automatic source authenticity or factual truth |
| **Research attempt** | Method, evidence IDs, proposed research note, observed execution route | Automatic Owner acceptance |
| **Publication path** | Simulated candidate publication, digest readback and version constraint | Actual remote Git consistency or authentication |
| **Accepted frontier** | Ordered record of admitted research batches for one track | Substantive approval of any scientific claim |
| **Issue-like follow-up** | Coordination reminders for later investigation | Immutable research ledger or a second accepted frontier |

## Critical distinctions

```text
Source metadata → research draft
                      |
             +--------+----------+
             |                   |
   Interactive candidate    Scheduled producer packet
             |                   |
             |             Separate handoff
             +---------+---------+
                       |
             Candidate publication
                       |
                 Digest readback
                       |
              Owner batch admission
                       |
              Track accepted frontier
                       |
                  Next objective

    Research-hypothesis admission: NOT AUTOMATIC
```

**Attempt ≠ stored artifact ≠ accepted batch ≠ accepted substantive finding**.

A note may be durably stored without being accepted; an accepted batch may merely establish that a research step completed, without proving the proposed hypothesis.

## Track isolation

Each track has its own objective, Owner and accepted frontier. A failure in Track A must not move Track B's frontier or impose a global block on independent authorized work. The example demonstrates a per-track frontier check but **does not implement cross-process atomic compare-and-swap**.

## Source provenance

Every synthetic research note cites registered source IDs; a source includes a locator, inspection timestamp and title. No semantic quality or reliability judgment follows automatically from this metadata. Production research requires actual source retrieval, quote-to-source comparison, freshness checks and disclosure of uncertainty.

## Coordination and GitHub Issues

The example tracks optional Issue references separately. An Issue can describe an unresolved obligation, but its existence, label or closure does not verify research, publish a note or advance the accepted frontier. The model does not call the GitHub Issues API.

## Scope of the public reference

The example uses imaginary research topics and `example://` locators. It has no private repository references, active schedules, actual scientific findings, operational timestamps or account-specific configuration.
