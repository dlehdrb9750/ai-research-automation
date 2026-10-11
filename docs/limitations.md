# Verification and Limitations

## Reproduce the demonstration

```bash
python examples/research_demo.py
python -m unittest discover -s tests -v
```

The Python-only checks are deterministic and use synthetic data. GitHub Actions runs them from a clean checkout on push and pull request. Inspect the actual CI run status before claiming it passed.

## Explicit non-claims

- **No LLM or research retrieval:** the example does not generate factual research or validate the user-supplied note.
- **No unattended automation:** no actual ChatGPT task, cron process, webhook or background agent is triggered.
- **No GitHub write integration:** `publish()` changes only in-memory state; there is no branch CAS, remote commit or actual readback.
- **No genuine authorization:** `owner_authorized=True` is a caller assertion, not authentication or user approval.
- **No scientific validation:** citation metadata is not evidence the referenced publication exists or supports a claim.
- **No production durability:** checkpoint JSON is not saved to a persistent provider by this prototype.
- **No distributed consistency:** multiple concurrent writers, deduplication across processes and real races require separate engineering.
- **No production incident coverage:** deliberate simulated failures are not validated against a real host's permission, safety and transport states.

## Audit of disclosure

Only original descriptions and imaginary sources are present here. Private project research texts, financial decision models, sensitive political-economic findings, internal study records, account settings, authentic access tokens, and Owner-specific operational file paths are intentionally excluded.

This release is an **educational application architecture**, not the official operational specification for a private project.

## What to validate next

An independently consented trial could use public research inputs, a disposable repository, real publication/readback, reproducible retrieval, a separately authorized scheduler, and an external evaluator scoring factual support and research continuity. Those features remain future work.
