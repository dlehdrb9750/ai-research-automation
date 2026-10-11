"""Run: python -m unittest discover -s tests -v"""
import unittest

from examples.research_demo import ResearchError, ResearchStudio, Track


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.lab = ResearchStudio([Track("a", "Research a fictional question", "owner"),
                                   Track("b", "Research another question", "other")])
        self.lab.register_source("s1", "example://a", "2026-10-11", "Synthetic A")
        self.lab.register_source("s2", "example://b", "2026-10-11", "Synthetic B")

    def draft(self, aid="a1", track="a", route="interactive", method="original"):
        return self.lab.draft(aid, track, method, route=route,
                              source_ids=("s1",), research_note="Hypothesis only")

    def verify(self, aid="a1", base=0):
        self.lab.publish(aid, expected_frontier=base)
        self.lab.readback(aid, observed_checksum=self.lab.attempts[aid].checksum)

    def test_empty_track_or_duplicate_track_rejected(self):
        with self.assertRaises(ResearchError):
            ResearchStudio([])
        with self.assertRaises(ResearchError):
            ResearchStudio([Track("a", "x", "owner"), Track("a", "y", "owner")])

    def test_source_provenance_required(self):
        with self.assertRaises(ResearchError):
            self.lab.register_source("s1", "example://x", "date", "duplicate")
        with self.assertRaises(ResearchError):
            self.lab.register_source("s3", "", "date", "empty locator")

    def test_draft_with_missing_source_rejected(self):
        with self.assertRaises(ResearchError):
            self.lab.draft("x", "a", "method", route="interactive",
                           source_ids=("unregistered",), research_note="note")

    def test_draft_is_not_accepted(self):
        self.draft()
        self.assertEqual(self.lab.tracks["a"].accepted_frontier, 0)
        self.assertEqual(self.lab.attempts["a1"].status, "DRAFT")

    def test_scheduled_packet_is_not_canonical(self):
        self.draft(route="scheduled_producer")
        self.lab.produce_packet("a1")
        self.assertEqual(self.lab.attempts["a1"].status, "PRODUCER_PACKET")
        with self.assertRaises(ResearchError):
            self.lab.accept("a1", owner_authorized=True)
        self.assertEqual(self.lab.tracks["a"].accepted_frontier, 0)

    def test_scheduled_requires_explicit_packet_handoff(self):
        self.draft(route="scheduled_producer")
        with self.assertRaises(ResearchError):
            self.lab.publish("a1", expected_frontier=0)
        self.lab.produce_packet("a1")
        self.verify()
        self.assertEqual(self.lab.accept("a1", owner_authorized=True), "B001")

    def test_published_is_not_verified_or_accepted(self):
        self.draft()
        self.lab.publish("a1", expected_frontier=0)
        self.assertEqual(self.lab.tracks["a"].accepted_frontier, 0)
        with self.assertRaises(ResearchError):
            self.lab.accept("a1", owner_authorized=True)

    def test_mismatched_readback_rejected(self):
        self.draft()
        self.lab.publish("a1", expected_frontier=0)
        with self.assertRaises(ResearchError):
            self.lab.readback("a1", observed_checksum="wrong")
        self.assertEqual(self.lab.attempts["a1"].status, "PUBLISHED_UNVERIFIED")

    def test_owner_authorization_required(self):
        self.draft()
        self.verify()
        with self.assertRaises(ResearchError):
            self.lab.accept("a1", owner_authorized=False)
        self.assertEqual(self.lab.tracks["a"].accepted_frontier, 0)

    def test_batch_acceptance_never_promotes_hypothesis(self):
        self.draft()
        self.verify()
        self.assertEqual(self.lab.accept("a1", owner_authorized=True), "B001")
        self.assertFalse(self.lab.attempts["a1"].substantive_conclusion_accepted)

    def test_stale_frontier_blocks_older_candidate(self):
        self.draft("a1")
        self.draft("a2", method="another")
        self.verify("a1")
        self.lab.accept("a1", owner_authorized=True)
        with self.assertRaises(ResearchError):
            self.lab.publish("a2", expected_frontier=0)

    def test_duplicate_attempt_id_is_rejected(self):
        self.draft()
        with self.assertRaises(ResearchError):
            self.draft()

    def test_failure_is_local_to_another_track(self):
        self.draft("a1")
        self.draft("b1", track="b")
        self.lab.failure("a1", "TRANSIENT")
        self.verify("b1")
        self.lab.accept("b1", owner_authorized=True)
        self.assertEqual(self.lab.tracks["b"].accepted_frontier, 1)
        self.assertEqual(self.lab.tracks["a"].accepted_frontier, 0)

    def test_redefinition_requires_distinct_method_and_note(self):
        self.draft()
        self.lab.failure("a1", "TRANSIENT")
        with self.assertRaises(ResearchError):
            self.lab.redefine("a1", "a2", "original", new_source_ids=("s2",),
                              new_note="new note", distinct=True, within_scope=True)
        with self.assertRaises(ResearchError):
            self.lab.redefine("a1", "a2", "different", new_source_ids=("s2",),
                              new_note="new note", distinct=True, within_scope=False)
        self.lab.redefine("a1", "a2", "different", new_source_ids=("s2",),
                          new_note="new note", distinct=True, within_scope=True)
        self.assertEqual(self.lab.attempts["a2"].base_frontier, 0)

    def test_explicit_denial_not_redefinable(self):
        self.draft()
        self.lab.failure("a1", "EXPLICIT_DENIAL")
        with self.assertRaises(ResearchError):
            self.lab.redefine("a1", "a2", "renamed", new_source_ids=("s2",),
                              new_note="new note", distinct=True, within_scope=True)

    def test_unknown_effect_blocks_publish_and_accept(self):
        self.draft()
        self.lab.failure("a1", "UNKNOWN_EFFECT")
        with self.assertRaises(ResearchError):
            self.lab.publish("a1", expected_frontier=0)
        self.lab.reconcile("a1", applied=None)
        self.assertEqual(self.lab.attempts["a1"].status, "UNKNOWN_EFFECT")

    def test_unknown_effect_yes_requires_matching_readback(self):
        self.draft()
        self.lab.failure("a1", "UNKNOWN_EFFECT")
        with self.assertRaises(ResearchError):
            self.lab.reconcile("a1", applied=True, observed_checksum="wrong")
        self.lab.reconcile("a1", applied=True,
                           observed_checksum=self.lab.attempts["a1"].checksum)
        self.assertEqual(self.lab.accept("a1", owner_authorized=True), "B001")

    def test_unknown_effect_no_resumes_unpublished_state(self):
        self.draft()
        self.lab.failure("a1", "UNKNOWN_EFFECT")
        self.lab.reconcile("a1", applied=False)
        self.verify()
        self.assertEqual(self.lab.accept("a1", owner_authorized=True), "B001")

    def test_selective_recovery_never_moves_frontier(self):
        self.draft()
        self.lab.failure("a1", "TRANSIENT")
        self.assertIsNone(self.lab.optional_recovery("a1", irreplaceable=False))
        self.assertEqual(self.lab.recovery_packets, {})
        self.assertEqual(self.lab.optional_recovery("a1", irreplaceable=True), "a1")
        self.assertEqual(self.lab.tracks["a"].accepted_frontier, 0)

    def test_issue_is_noncanonical_coordination(self):
        self.lab.coordinate_issue("a", "fictional-issue-1")
        self.lab.coordinate_issue("a", "fictional-issue-1")
        self.assertEqual(self.lab.tracks["a"].issue_refs, ["fictional-issue-1"])
        self.assertEqual(self.lab.tracks["a"].accepted_frontier, 0)

    def test_checkpoint_restores_accepted_state(self):
        self.draft()
        self.verify()
        self.lab.accept("a1", owner_authorized=True)
        restored = ResearchStudio.resume(self.lab.checkpoint())
        self.assertEqual(restored.tracks["a"].accepted_frontier, 1)
        self.assertEqual(restored.attempts["a1"].status, "BATCH_ACCEPTED")
        self.assertFalse(restored.attempts["a1"].substantive_conclusion_accepted)
        restored.draft("a2", "a", "new method", route="interactive",
                       source_ids=("s2",), research_note="next question")
        self.assertEqual(restored.attempts["a2"].base_frontier, 1)


if __name__ == "__main__":
    unittest.main()
