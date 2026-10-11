"""Synthetic research continuity reference: no scheduler, LLM or remote writes.

All evidence, owner approval, and readback observations are external assertions,
not independently verified facts. This is an educational state model.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
import json
from typing import Dict, List, Tuple


class ResearchError(ValueError):
    """A transition is invalid or lacks the required evidence."""


@dataclass
class Source:
    source_id: str
    locator: str
    inspected_at: str
    title: str


@dataclass
class Track:
    track_id: str
    objective: str
    owner: str
    accepted_frontier: int = 0
    accepted_attempt_ids: List[str] = field(default_factory=list)
    issue_refs: List[str] = field(default_factory=list)


@dataclass
class Attempt:
    attempt_id: str
    track_id: str
    method: str
    route: str
    source_ids: Tuple[str, ...]
    research_note: str
    base_frontier: int
    checksum: str
    status: str = "DRAFT"
    readback_verified: bool = False
    failure_kind: str = ""
    substantive_conclusion_accepted: bool = False


class ResearchStudio:
    """Models research attempts, producer packets and separate owner admission.

    It intentionally does not call GitHub, authenticate users, or submit jobs.
    """

    def __init__(self, tracks: List[Track]) -> None:
        if not tracks or any(not t.track_id.strip() or not t.objective.strip()
                             or not t.owner.strip() for t in tracks):
            raise ResearchError("tracks need a unique ID, objective and owner")
        self.tracks: Dict[str, Track] = {t.track_id: t for t in tracks}
        if len(self.tracks) != len(tracks):
            raise ResearchError("duplicate track ID")
        self.sources: Dict[str, Source] = {}
        self.attempts: Dict[str, Attempt] = {}
        self.recovery_packets: Dict[str, str] = {}

    @staticmethod
    def digest(text: str) -> str:
        return sha256(text.encode("utf-8")).hexdigest()

    def register_source(self, source_id: str, locator: str,
                        inspected_at: str, title: str) -> None:
        if source_id in self.sources or not all(
                value.strip() for value in (source_id, locator, inspected_at, title)):
            raise ResearchError("source record must have unique, nonempty provenance")
        self.sources[source_id] = Source(source_id, locator, inspected_at, title)

    def draft(self, attempt_id: str, track_id: str, method: str, *,
              route: str, source_ids: Tuple[str, ...], research_note: str) -> str:
        if track_id not in self.tracks:
            raise ResearchError("unknown track")
        if attempt_id in self.attempts or not attempt_id.strip():
            raise ResearchError("unique attempt ID required")
        if route not in {"interactive", "scheduled_producer"}:
            raise ResearchError("route must be declared explicitly")
        if not method.strip() or not research_note.strip() or not source_ids:
            raise ResearchError("method, note and supporting source IDs required")
        if len(set(source_ids)) != len(source_ids):
            raise ResearchError("duplicate sources within an attempt")
        if any(source_id not in self.sources for source_id in source_ids):
            raise ResearchError("source must be registered before a note cites it")
        base = self.tracks[track_id].accepted_frontier
        checksum = self.digest(repr((track_id, method, source_ids, research_note, base)))
        self.attempts[attempt_id] = Attempt(
            attempt_id, track_id, method, route, source_ids, research_note,
            base, checksum,
        )
        return attempt_id

    def produce_packet(self, attempt_id: str) -> None:
        a = self.attempts[attempt_id]
        if a.route != "scheduled_producer" or a.status != "DRAFT":
            raise ResearchError("only fresh scheduled drafts can produce a packet")
        a.status = "PRODUCER_PACKET"

    def publish(self, attempt_id: str, *, expected_frontier: int) -> None:
        """Simulate a guarded publication candidate, not an actual Git write."""
        a = self.attempts[attempt_id]
        required_status = "DRAFT" if a.route == "interactive" else "PRODUCER_PACKET"
        if a.status != required_status:
            raise ResearchError("unexpected state; cannot blindly republish")
        if expected_frontier != a.base_frontier:
            raise ResearchError("supplied publication base did not match the draft")
        if self.tracks[a.track_id].accepted_frontier != a.base_frontier:
            raise ResearchError("stale frontier requires explicit reconciliation")
        a.status = "PUBLISHED_UNVERIFIED"

    def readback(self, attempt_id: str, *, observed_checksum: str) -> None:
        """Assert independent readback. This code does not fetch a remote object."""
        a = self.attempts[attempt_id]
        if a.status != "PUBLISHED_UNVERIFIED":
            raise ResearchError("readback requires a published candidate")
        if observed_checksum != a.checksum:
            raise ResearchError("readback content mismatch")
        a.status = "VERIFIED_UNACCEPTED"
        a.readback_verified = True

    def accept(self, attempt_id: str, *, owner_authorized: bool) -> str:
        """Accept batch progress, never automatically a scientific conclusion."""
        a = self.attempts[attempt_id]
        track = self.tracks[a.track_id]
        if not owner_authorized:
            raise ResearchError("owner authorization not established")
        if a.status != "VERIFIED_UNACCEPTED" or not a.readback_verified:
            raise ResearchError("verified publication is required")
        if a.base_frontier != track.accepted_frontier:
            raise ResearchError("stale frontier; cannot accept out of order")
        track.accepted_frontier += 1
        track.accepted_attempt_ids.append(attempt_id)
        a.status = "BATCH_ACCEPTED"
        assert not a.substantive_conclusion_accepted
        return f"B{track.accepted_frontier:03d}"

    def failure(self, attempt_id: str, kind: str) -> None:
        a = self.attempts[attempt_id]
        if a.status not in {"DRAFT", "PRODUCER_PACKET", "PUBLISHED_UNVERIFIED"}:
            raise ResearchError("failure applies only to a pending attempt")
        if kind not in {"TRANSIENT", "UNKNOWN_EFFECT", "EXPLICIT_DENIAL"}:
            raise ResearchError("unknown failure class")
        a.status, a.failure_kind = kind, kind

    def reconcile(self, attempt_id: str, *, applied: bool | None,
                  observed_checksum: str = "") -> None:
        """Caller must independently establish the actual external write effect."""
        a = self.attempts[attempt_id]
        if a.status != "UNKNOWN_EFFECT":
            raise ResearchError("no unknown effect to reconcile")
        if applied is None:
            return
        if applied:
            if observed_checksum != a.checksum:
                raise ResearchError("a confirmed write needs exact matching readback")
            a.status = "VERIFIED_UNACCEPTED"
            a.readback_verified = True
        else:
            a.status = ("DRAFT" if a.route == "interactive"
                        else "PRODUCER_PACKET")
            a.failure_kind = ""

    def redefine(self, failed_id: str, new_id: str, new_method: str, *,
                 new_source_ids: Tuple[str, ...], new_note: str,
                 distinct: bool, within_scope: bool) -> str:
        """Create an independent, permitted successor; flags are external claims."""
        a = self.attempts[failed_id]
        if (a.status != "TRANSIENT" or not distinct or not within_scope
                or new_method == a.method or new_note == a.research_note):
            raise ResearchError("new batch must be meaningfully distinct, permitted and unaccepted")
        if self.tracks[a.track_id].accepted_frontier != a.base_frontier:
            raise ResearchError("accepted frontier moved; reconcile the task first")
        return self.draft(new_id, a.track_id, new_method, route=a.route,
                          source_ids=new_source_ids, research_note=new_note)

    def optional_recovery(self, attempt_id: str, *,
                          irreplaceable: bool) -> str | None:
        """A noncanonical in-memory packet, never a publication or acceptance."""
        a = self.attempts[attempt_id]
        if a.status not in {"TRANSIENT", "EXPLICIT_DENIAL", "UNKNOWN_EFFECT"}:
            raise ResearchError("recovery packets are for unresolved attempts")
        if not irreplaceable:
            return None
        self.recovery_packets[attempt_id] = a.research_note
        return attempt_id

    def coordinate_issue(self, track_id: str, issue_ref: str) -> None:
        """Track a fictional obligation; does not advance the accepted frontier."""
        if track_id not in self.tracks or not issue_ref.strip():
            raise ResearchError("valid track and issue reference needed")
        refs = self.tracks[track_id].issue_refs
        if issue_ref not in refs:
            refs.append(issue_ref)

    def checkpoint(self) -> str:
        """In-memory JSON only; actual persistence belongs to the host Owner."""
        return json.dumps({
            "tracks": [asdict(t) for t in self.tracks.values()],
            "sources": [asdict(s) for s in self.sources.values()],
            "attempts": [asdict(a) for a in self.attempts.values()],
            "recovery_packets": self.recovery_packets,
        }, sort_keys=True)

    @classmethod
    def resume(cls, checkpoint_json: str) -> "ResearchStudio":
        """Trusted, locally generated checkpoint only; untrusted input unsupported."""
        obj = json.loads(checkpoint_json)
        studio = cls([Track(**t) for t in obj["tracks"]])
        studio.sources = {s["source_id"]: Source(**s) for s in obj["sources"]}
        studio.attempts = {}
        for raw in obj["attempts"]:
            raw["source_ids"] = tuple(raw["source_ids"])
            studio.attempts[raw["attempt_id"]] = Attempt(**raw)
        studio.recovery_packets = dict(obj["recovery_packets"])
        return studio


def demonstration() -> None:
    lab = ResearchStudio([
        Track("public-trend", "Produce a public-domain trends note", "fictional-owner-a"),
        Track("public-method", "Produce a reproducibility-method note", "fictional-owner-b"),
    ])
    lab.register_source("s1", "example://fictional-statistic", "2026-10-11",
                        "Fictional public indicator")
    lab.register_source("s2", "example://synthetic-method", "2026-10-11",
                        "Fictional methodology")
    lab.draft("t1", "public-trend", "compare indicator versions",
              route="interactive", source_ids=("s1",),
              research_note="Hypothesis: definitions might differ")
    lab.publish("t1", expected_frontier=0)
    lab.readback("t1", observed_checksum=lab.attempts["t1"].checksum)
    print("Interactive batch:", lab.accept("t1", owner_authorized=True))

    lab.draft("t2", "public-method", "inspect synthetic research method",
              route="scheduled_producer", source_ids=("s2",),
              research_note="Unconfirmed method comparison")
    lab.produce_packet("t2")
    print("Scheduled producer status:", lab.attempts["t2"].status)
    lab.publish("t2", expected_frontier=0)
    lab.readback("t2", observed_checksum=lab.attempts["t2"].checksum)
    print("Accepted handoff:", lab.accept("t2", owner_authorized=True))

    lab.draft("t3", "public-trend", "retrieve fragile draft",
              route="interactive", source_ids=("s1",),
              research_note="Draft based on another inspection")
    lab.failure("t3", "TRANSIENT")
    lab.redefine("t3", "t4", "analyze a different open method",
                 new_source_ids=("s2",), new_note="New independent comparison",
                 distinct=True, within_scope=True)
    lab.publish("t4", expected_frontier=1)
    lab.readback("t4", observed_checksum=lab.attempts["t4"].checksum)
    lab.accept("t4", owner_authorized=True)
    lab.coordinate_issue("public-trend", "example-issue-42")
    resumed = ResearchStudio.resume(lab.checkpoint())
    print("Recovered accepted frontier:", resumed.tracks["public-trend"].accepted_frontier)
    print("Scientific hypothesis promoted?", resumed.attempts["t4"].substantive_conclusion_accepted)
    print("Synthetic research continuity demonstration succeeded.")


if __name__ == "__main__":
    demonstration()
