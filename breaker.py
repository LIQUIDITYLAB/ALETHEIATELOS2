"""
Breaker: independent challenge mechanism for agent claims.

The Breaker accepts an agent (the target), optional independent supporting
evidence, and optional independent challenging evidence. It returns a
structured challenge object that preserves the original claim and any
evidence/provenance supplied. The Breaker does NOT judge or overturn claims —
the "decision" remains "pending".
"""

from typing import Any, Dict, List, Optional


def break_claim(
    agent: Dict[str, Any],
    challenging_evidence: Optional[List[Dict[str, Any]]] = None,
    supporting_evidence: Optional[List[Dict[str, Any]]] = None,
    challenge_reason: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a structured challenge for a target agent claim.

    Parameters:
      - agent: the original agent dictionary (preserved unchanged).
      - challenging_evidence: list of evidence objects intended to challenge the claim.
      - supporting_evidence: list of evidence objects intended to support the claim (independent).
      - challenge_reason: optional short reason string supplied by the breaker.

    Returns a dict with at least:
      - target_agent_id
      - target_claim (keeps the core claim fields)
      - original_agent (the original agent dict preserved as-is)
      - challenge_status: 'unchallenged' or 'challenged'
      - challenge_reason
      - supporting_evidence
      - challenging_evidence
      - decision: 'pending' (no final decision yet)
    """

    # Preserve original agent claim fields (do not mutate agent)
    target_agent_id = agent.get("agent_id")
    # Represent the target_claim minimally but preserving values (direction/confidence/horizon)
    target_claim = {
        "direction": agent.get("direction"),
        "confidence": agent.get("confidence"),
        # accept both keys for compatibility
        "horizon": agent.get("horizon") or agent.get("time_horizon"),
    }

    # If no supporting_evidence explicitly supplied, include agent's own evidence (if any)
    agent_evidence = agent.get("evidence")
    preserved_supporting = supporting_evidence if supporting_evidence is not None else (agent_evidence if agent_evidence is not None else [])

    preserved_challenging = challenging_evidence if challenging_evidence is not None else []

    challenge_status = "challenged" if preserved_challenging else "unchallenged"

    reason_text = challenge_reason or (("independent challenging evidence supplied" if preserved_challenging else ""))

    result = {
        "target_agent_id": target_agent_id,
        "target_claim": target_claim,
        "original_agent": agent,  # preserve entire original agent dict unchanged
        "challenge_status": challenge_status,
        "challenge_reason": reason_text,
        "supporting_evidence": preserved_supporting,
        "challenging_evidence": preserved_challenging,
        "decision": "pending",
    }

    return result
