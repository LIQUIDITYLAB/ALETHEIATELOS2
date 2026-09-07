from orchestrator import orchestrate


def test_same_horizon_conflict():
    agents = [
        {
            "agent_id": "trend_agent",
            "direction": "bullish",
            "confidence": 0.72,
            "time_horizon": "short",
        },
        {
            "agent_id": "risk_agent",
            "direction": "bearish",
            "confidence": 0.81,
            "time_horizon": "short",
        },
    ]

    result = orchestrate(agents)

    assert result["agent_count"] == 2
    assert result["conflict_count"] == 1
    assert result.get("horizon_divergence_count", 0) == 0
    assert result["status"] == "conflict_detected"
    # original agent dicts must be preserved exactly
    assert result["agents"] == agents

    conflict = result["conflicts"][0]
    assert set(conflict["agents"]) == {"trend_agent", "risk_agent"}
    assert set(conflict["directions"]) == {"bullish", "bearish"}
    assert conflict.get("time_horizon") == "short"


def test_different_horizon_divergence():
    agents = [
        {
            "agent_id": "trend_agent",
            "direction": "bullish",
            "confidence": 0.72,
            "time_horizon": "short",
        },
        {
            "agent_id": "risk_agent",
            "direction": "bearish",
            "confidence": 0.81,
            "time_horizon": "medium",
        },
    ]

    result = orchestrate(agents)

    assert result["agent_count"] == 2
    assert result["conflict_count"] == 0
    assert result["horizon_divergence_count"] == 1
    # Per requirement: horizon divergences do NOT change status from 'aligned'
    assert result["status"] == "aligned"
    # original agent dicts must be preserved exactly
    assert result["agents"] == agents

    divergence = result["horizon_divergences"][0]
    assert set(divergence["agents"]) == {"trend_agent", "risk_agent"}
    assert set(divergence["directions"]) == {"bullish", "bearish"}
    assert set(divergence["time_horizons"]) == {"short", "medium"}


def test_preserves_agent_outputs_multiple():
    agents = [
        {
            "agent_id": "a1",
            "direction": "bullish",
            "confidence": 0.7,
            "time_horizon": "short",
        },
        {
            "agent_id": "a2",
            "direction": "bullish",
            "confidence": 0.6,
            "time_horizon": "short",
        },
        {
            "agent_id": "a3",
            "direction": "bullish",
            "confidence": 0.8,
            "time_horizon": "medium",
        },
    ]

    result = orchestrate(agents)
    # exact preservation of original list value
    assert result["agents"] == agents


def test_aligned_agents_no_conflict():
    agents = [
        {
            "agent_id": "trend_agent",
            "direction": "bullish",
            "confidence": 0.72,
            "time_horizon": "short",
        },
        {
            "agent_id": "other_agent",
            "direction": "bullish",
            "confidence": 0.5,
            "time_horizon": "short",
        },
    ]

    result = orchestrate(agents)

    assert result["conflict_count"] == 0
    assert result.get("horizon_divergence_count", 0) == 0
    assert result["status"] == "aligned"
