from copy import deepcopy

from breaker import break_claim


def make_evidence_item(eid: str) -> dict:
    return {
        "evidence_id": eid,
        "source": "news://provider/article/{}".format(eid),
        "claim": "Example claim from evidence {}".format(eid),
        "observed_at": "2026-08-30T09:12:00Z",
        "retrieved_at": "2026-08-30T09:12:05Z",
        "metadata": {"note": "test"}
    }


def test_breaker_unchallenged_preserves_claim():
    agent = {
        "agent_id": "agent-alpha",
        "direction": "LONG",
        "confidence": 0.8,
        "time_horizon": "short",
        "evidence": [make_evidence_item("ev-a1")],
        "strategy": "Example",
        "data_timestamp": "2026-08-30T09:00:00Z",
        "model_version": "v1",
        "regime_assumption": "normal",
        "capacity_constraint": None,
    }

    agent_copy = deepcopy(agent)
    result = break_claim(agent)

    # Original agent preserved exactly
    assert result["original_agent"] == agent_copy

    # No challenging evidence -> unchallenged
    assert result["challenge_status"] == "unchallenged"
    assert result["challenging_evidence"] == []
    assert result["decision"] == "pending"

    # supporting_evidence contains agent's own evidence by default
    assert result["supporting_evidence"] == agent["evidence"]


def test_breaker_challenged_records_challenge_and_preserves_claim():
    agent = {
        "agent_id": "agent-beta",
        "direction": "SHORT",
        "confidence": 0.6,
        "time_horizon": "medium",
        "evidence": [make_evidence_item("ev-b1")],
        "strategy": "Example2",
        "data_timestamp": "2026-08-30T09:00:00Z",
        "model_version": "v1",
        "regime_assumption": "normal",
        "capacity_constraint": None,
    }

    challenge_evidence = [make_evidence_item("ev-ch-1"), make_evidence_item("ev-ch-2")]
    supporting_evidence = [make_evidence_item("ev-sup-1")]
    agent_copy = deepcopy(agent)

    result = break_claim(
        agent,
        challenging_evidence=challenge_evidence,
        supporting_evidence=supporting_evidence,
        challenge_reason="Independent data suggests alternate interpretation"
    )

    # original claim preserved
    assert result["original_agent"] == agent_copy
    # challenge recorded
    assert result["challenge_status"] == "challenged"
    assert result["challenging_evidence"] == challenge_evidence
    assert result["supporting_evidence"] == supporting_evidence
    assert result["challenge_reason"] == "Independent data suggests alternate interpretation"
    # decision must remain pending
    assert result["decision"] == "pending"
    # must not auto-overturn: original direction remains present in target_claim
    assert result["target_claim"]["direction"] == agent["direction"]


def test_provenance_fields_preserved_in_challenging_evidence():
    agent = {
        "agent_id": "agent-gamma",
        "direction": "LONG",
        "confidence": 0.7,
        "time_horizon": "short",
        "strategy": "Example3",
    }

    ev = make_evidence_item("ev-prove-1")
    result = break_claim(agent, challenging_evidence=[ev])

    # Check the preserved evidence object has the provenance fields intact
    preserved = result["challenging_evidence"][0]
    for field in ("evidence_id", "source", "claim", "observed_at", "retrieved_at"):
        assert field in preserved
        assert preserved[field] == ev[field]


def test_empty_challenge_evidence_produces_unchallenged():
    agent = {
        "agent_id": "agent-delta",
        "direction": "NEUTRAL",
        "confidence": 0.5,
        "time_horizon": "short",
        "strategy": "Example4",
    }

    # explicitly pass empty list -> treated as unchallenged
    result = break_claim(agent, challenging_evidence=[])
    assert result["challenge_status"] == "unchallenged"
    assert result["challenging_evidence"] == []
    assert result["decision"] == "pending"
