"""
AletheiaTelos
Basic orchestration layer.

The orchestrator does not force independent agents into consensus.
It preserves their individual outputs, identifies conflicts,
and produces a structured synthesis.
"""

from typing import Any, Dict, List


def detect_conflicts(agents: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Identify disagreements between agent directions.

    Time-horizon aware:
    - If two agents disagree on direction but share the same time_horizon, it's a true conflict.
    - If they disagree on direction but have different time_horizon values, it's recorded as a horizon divergence.

    Returns a dict with two lists: "conflicts" and "horizon_divergences".
    """

    conflicts: List[Dict[str, Any]] = []
    horizon_divergences: List[Dict[str, Any]] = []

    for i, agent_a in enumerate(agents):
        for agent_b in agents[i + 1:]:
            direction_a = agent_a.get("direction")
            direction_b = agent_b.get("direction")
            # Backwards-compatible: support both "time_horizon" and "horizon" keys
            horizon_a = agent_a.get("time_horizon") or agent_a.get("horizon")
            horizon_b = agent_b.get("time_horizon") or agent_b.get("horizon")

            if direction_a and direction_b and direction_a != direction_b:
                if horizon_a == horizon_b:
                    # True directional conflict on the same horizon
                    conflicts.append(
                        {
                            "agents": [
                                agent_a.get("agent_id"),
                                agent_b.get("agent_id"),
                            ],
                            "directions": [direction_a, direction_b],
                            "time_horizon": horizon_a,
                        }
                    )
                else:
                    # Different horizons: record as a divergence rather than a conflict
                    horizon_divergences.append(
                        {
                            "agents": [
                                agent_a.get("agent_id"),
                                agent_b.get("agent_id"),
                            ],
                            "directions": [direction_a, direction_b],
                            "time_horizons": [horizon_a, horizon_b],
                        }
                    )

    return {"conflicts": conflicts, "horizon_divergences": horizon_divergences}


def orchestrate(agents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Preserve independent agent outputs and produce
    a structured orchestration result.

    Backwards-compatible keys preserved:
    - "agents"
    - "conflicts" (only same-horizon directional conflicts)
    - "conflict_count"

    Additional keys:
    - "horizon_divergences"
    - "horizon_divergence_count"

    Status semantics:
    - "conflict_detected" when there is at least one same-horizon conflict.
    - "aligned" when there are no same-horizon conflicts (even if horizon divergences exist).
    """

    detection = detect_conflicts(agents)
    conflicts = detection["conflicts"]
    horizon_divergences = detection["horizon_divergences"]

    status = "conflict_detected" if conflicts else "aligned"

    return {
        "agent_count": len(agents),
        "agents": agents,
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
        "horizon_divergences": horizon_divergences,
        "horizon_divergence_count": len(horizon_divergences),
        "status": status,
    }


if __name__ == "__main__":
    example_agents = [
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

    result = orchestrate(example_agents)

    print(result)
