# Policy Attestation Campaign

Runs policy attestation campaigns with assignee tracking, due dates, overdue lists, and completion rates.

**Stack:** Python 3.12 · stdlib only · unittest

## Problem

Campaigns assign a policy version to employees with a due date;
record_attestation() marks completion with a timestamp; overdue()
lists stragglers; completion_rate() reports progress; nudge_list()
returns who still needs a reminder.

## Design decisions

- One campaign per (policy, version); assignees are added once and
- Duplicate attestations raise: attesting twice is a data error, not
- overdue(as_of) covers assigned-but-unattested assignees past the due

## Layout

- `README.md`
- `src/policy_attestation.py`
- `tests/test_policy_attestation.py`
- `LICENSE`
- `.gitignore`

## Setup

No third-party dependencies — Python 3.11+ standard library only.

```bash
cd govops-policy-attestation
python -m unittest discover -s tests -v
```

## Usage

```python
from datetime import date
from src.policy_attestation import AttestationCampaign

c = AttestationCampaign("AI Acceptable Use", "v3", date(2026, 6, 30))
c.assign_many(["amy", "bo"])
c.record_attestation("amy", date(2026, 6, 1))
print(c.summary(date(2026, 7, 1)))
```

## License

MIT — see [LICENSE](LICENSE).
