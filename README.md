# AI Research Automation & Continuity

**A public reference architecture for multi-cycle, evidence-aware AI research**

**Release:** 0.1.0 · Independently written educational prototype · 2026-10-11

> Research should survive interruptions without confusing an attempted batch, a stored note, an accepted result, and a new substantive conclusion.

## What this solves

A one-off AI answer is different from research conducted across days, tools and sessions. A credible long-running system must preserve the **research objective**, trace which sources were used, continue after recoverable failures, and avoid inventing a conclusion or a completed batch when storage is incomplete.

This reference separates five concerns:

| Concern | Purpose | Boundary |
| --- | --- | --- |
| **Research objective** | The approved question and scope for each track | A change of purpose requires independent authorization |
| **Evidence provenance** | Which independently identified sources support each research note | Citation metadata is not proof the source or claim is true |
| **Execution attempt** | Method, batch attempt, route and observed outcome | Failed or generated attempts are not accepted research |
| **Publication & acceptance** | Producer packet, candidate publication, verification and Owner admission | Storage/readback ≠ scientific conclusion approval |
| **Continuity & coordination** | Accepted frontier, checkpoint, independent next actions and optional Issue references | Issue closure and scheduler events are not canonical state |

## Operating model

```text
Approved research goal and Owner
      |
      v
Source register -> batch attempt (interactive / scheduled producer)
      |
      +---- Interactive candidate -----+
      |                                |
      +---- Scheduled producer packet -+--> canonical publication (simulated)
                                             |
                                             v
                                      verified readback (simulated)
                                             |
                                             v
                                      Owner batch acceptance
                                             |
                                             v
                                    checkpoint + next research
```

A scheduled **producer** packet does not automatically become accepted research merely because a scheduled run occurred. The public model only simulates the *handoff*; it neither creates nor operates real ChatGPT scheduled tasks.

## Key architectural distinctions

- **Attempt ≠ batch acceptance ≠ substantive research conclusion.** A confirmed storage operation never automatically confirms a causal model or hypothesis.
- **One accepted frontier per track.** Work that was prepared from an outdated frontier must be reconciled before acceptance.
- **Interactive versus scheduled routes.** The demonstration uses different simulated pathways for a direct publication candidate and a noncanonical scheduled producer packet.
- **Localize failures.** A transient problem with one attempt does not stop an independent track.
- **Never repeat an unknown-effect write blindly.** Check the actual target before deciding whether any retry is appropriate.
- **Redefine unaccepted attempts carefully.** The permitted next method must genuinely differ and stay within approved scope; a denied action cannot be disguised as a fresh batch.
- **Retain only valuable recovery material.** Ordinary failed drafts need not generate permanent duplicate recovery work.
- **GitHub Issues are coordination, not accepted results.** A linked Issue is a reminder or follow-up obligation; it cannot move the research frontier.

## Reproduce the synthetic example

Python **3.10+**, standard library only:

```bash
python examples/research_demo.py
python -m unittest discover -s tests -v
```

The example runs two fictional tracks. One prepares an **interactive** evidence note; another produces a **scheduled-route packet** that must be explicitly published and read back. An attempted failure and a selective redefinition are demonstrated without any real research service, API key, background scheduler or remote write.

## Repository guide

- [Research lifecycle and authority boundaries](docs/architecture.md)
- [Producer routes, scheduling and handoff](docs/routes-and-handoff.md)
- [Failure recovery and provenance](docs/recovery-and-evidence.md)
- [Verification, limitations and security](docs/limitations.md)
- [Executable simulation](examples/research_demo.py)
- [Tests](tests/test_research_demo.py)
- [Change log](CHANGELOG.md)

## Evidence and maturity

The synthetic engine is intentionally small. Passing tests can show that **its local state machine behaves as specified**, not that an AI is autonomously researching, that a scheduler is running, that sources have been checked, or that findings are correct.

Actual research-workflow experience informed this design, but **no private data, operational schedules, investment strategy, sensitive research output, or internal repository configuration** is copied here.

## Related public architecture

- [AI Workflow Orchestration (AWPS)](https://github.com/dlehdrb9750/ai-workflow-orchestration) — goal/WP/batch execution, interruptions and recovery
- [AI State Governance (DLS)](https://github.com/dlehdrb9750/ai-state-governance) — persistent authority and accepted state
- [AI Audit & Recursive Improvement (AUDS/RIS)](https://github.com/dlehdrb9750/ai-audit-and-improvement) — evidence-based audit and improvement proposals
- [AI Systems Portfolio](https://github.com/dlehdrb9750/ai-systems-portfolio) — the public overview

**Publication is not operational cutover.** This independent public reference cannot grant authority over internal Owners, modify scheduled tasks or approve research conclusions.

**License:** No open-source license grant has yet been selected.
