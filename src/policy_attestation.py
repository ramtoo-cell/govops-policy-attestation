
"""Policy attestation campaign.

Campaigns assign a policy version to employees with a due date;
record_attestation() marks completion with a timestamp; overdue()
lists stragglers; completion_rate() reports progress; nudge_list()
returns who still needs a reminder.

Design:
- One campaign per (policy, version); assignees are added once and
  cannot be removed: the record of who was asked is itself evidence.
- Duplicate attestations raise: attesting twice is a data error, not
  extra diligence.
- overdue(as_of) covers assigned-but-unattested assignees past the due
  date; attested-late assignees stay in the history.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Attestation:
    """One completed attestation."""
    employee: str
    attested: date
    late: bool


class AttestationCampaign:
    """One policy attestation drive."""

    def __init__(self, policy, version, due):
        self.policy = policy
        self.version = version
        if not isinstance(due, date):
            raise TypeError("due must be a datetime.date")
        self.due = due
        self._assignees = set()
        self._attestations = {}

    def assign(self, employee):
        if employee in self._assignees:
            raise ValueError("already assigned: %r" % (employee,))
        self._assignees.add(employee)

    def assign_many(self, employees):
        for employee in employees:
            self.assign(employee)

    def record_attestation(self, employee, attested):
        if employee not in self._assignees:
            raise KeyError("not assigned: %r" % (employee,))
        if employee in self._attestations:
            raise ValueError("already attested: %r" % (employee,))
        if not isinstance(attested, date):
            raise TypeError("attested must be a datetime.date")
        record = Attestation(employee, attested, attested > self.due)
        self._attestations[employee] = record
        return record

    def attested(self, employee):
        return employee in self._attestations

    def pending(self):
        """Assigned employees who have not attested, sorted."""
        return sorted(self._assignees - set(self._attestations))

    def overdue(self, as_of):
        """Pending assignees past the due date."""
        if as_of <= self.due:
            return []
        return self.pending()

    def completion_rate(self):
        if not self._assignees:
            return 1.0
        return round(len(self._attestations) / len(self._assignees), 3)

    def late_attestations(self):
        return sorted(e for e, a in self._attestations.items() if a.late)

    def nudge_list(self, as_of):
        """Who needs a reminder: pending, overdue first."""
        pending = self.pending()
        if as_of > self.due:
            return pending
        return []

    def assignee_count(self):
        return len(self._assignees)

    def summary(self, as_of):
        return {
            "policy": self.policy,
            "version": self.version,
            "due": self.due.isoformat(),
            "assignees": len(self._assignees),
            "attested": len(self._attestations),
            "completion_rate": self.completion_rate(),
            "overdue": self.overdue(as_of),
        }
