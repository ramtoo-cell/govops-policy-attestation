
"""Tests for the policy attestation campaign."""
import unittest
from datetime import date

from src.policy_attestation import AttestationCampaign

DUE = date(2026, 6, 30)


class TestAttestationCampaign(unittest.TestCase):
    def setUp(self):
        self.c = AttestationCampaign("AI Acceptable Use", "v3", DUE)
        self.c.assign_many(["amy", "bo", "cy"])

    def test_completion_rate(self):
        self.c.record_attestation("amy", date(2026, 6, 1))
        self.assertEqual(self.c.completion_rate(), 0.333)

    def test_pending(self):
        self.c.record_attestation("amy", date(2026, 6, 1))
        self.assertEqual(self.c.pending(), ["bo", "cy"])

    def test_overdue(self):
        self.assertEqual(self.c.overdue(date(2026, 6, 1)), [])
        self.assertEqual(self.c.overdue(date(2026, 7, 1)), ["amy", "bo", "cy"])

    def test_late_attestation_flagged(self):
        self.c.record_attestation("amy", date(2026, 7, 5))
        self.assertEqual(self.c.late_attestations(), ["amy"])

    def test_duplicate_attestation_raises(self):
        self.c.record_attestation("amy", date(2026, 6, 1))
        with self.assertRaises(ValueError):
            self.c.record_attestation("amy", date(2026, 6, 2))

    def test_unassigned_raises(self):
        with self.assertRaises(KeyError):
            self.c.record_attestation("zoe", date(2026, 6, 1))

    def test_duplicate_assign_raises(self):
        with self.assertRaises(ValueError):
            self.c.assign("amy")

    def test_nudge_list(self):
        self.assertEqual(self.c.nudge_list(date(2026, 6, 1)), [])
        self.c.record_attestation("amy", date(2026, 6, 1))
        self.assertEqual(self.c.nudge_list(date(2026, 7, 1)), ["bo", "cy"])

    def test_attested(self):
        self.assertFalse(self.c.attested("amy"))
        self.c.record_attestation("amy", date(2026, 6, 1))
        self.assertTrue(self.c.attested("amy"))

    def test_summary(self):
        summary = self.c.summary(date(2026, 7, 1))
        self.assertEqual(summary["assignees"], 3)
        self.assertEqual(summary["overdue"], ["amy", "bo", "cy"])


if __name__ == "__main__":
    unittest.main()
