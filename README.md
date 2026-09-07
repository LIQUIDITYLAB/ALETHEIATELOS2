# AletheiaTelos

AletheiaTelos is an experimental decision-intelligence terminal designed around a simple principle:

> Independent intelligence should not be destroyed by forced consensus.

Instead of averaging conflicting strategies into a meaningless signal, AletheiaTelos preserves their individual reasoning, identifies conflicts, accounts for different time horizons, detects regime changes, and allows an orchestration layer to determine how the signals should coexist.

## Core Architecture

### Aletheia — Intelligence

The Aletheia layer contains independent strategy agents.

Each agent produces its own:

- Direction
- Confidence
- Time horizon
- Evidence
- Reasoning
- Regime assumptions

Agents are not required to agree.

### Conflict & Coexistence Engine

Conflicting signals are treated as information rather than errors.

The orchestration layer evaluates:

- Directional conflicts
- Time-horizon differences
- Confidence
- Strategy correlation
- Market regime
- Liquidity conditions
- Risk constraints

The objective is not fake consensus.

The objective is preserving useful independent information.

### Telos — Decision & Execution

Telos converts the surviving intelligence into an actionable portfolio structure.

This includes:

- Position sizing
- Exposure management
- Conflict-aware allocation
- Regime-conditioned scaling
- Capacity constraints
- Trading costs
- Risk budgets
- Auditability

Every major decision should have a reason.

## Research Principle

Five independent strategies should not automatically become one averaged strategy.

If one agent is LONG and another is SHORT, the system should first ask:

**Why do they disagree?**

A disagreement may represent:

- Different time horizons
- Different information sets
- Different market assumptions
- Different risk models
- Different regime expectations

The orchestration layer exists to understand those differences before collapsing them.

## Current Prototype

The current terminal demonstrates:

- Five independent strategy agents
- Independent confidence scores
- Multiple trading horizons
- Conflict detection
- Simple averaging comparison
- Orchestrated allocation
- Regime switching
- Market stress testing
- Agent failure simulation
- Audit trail
- System-context export

## Research Direction

AletheiaTelos is currently a research prototype.

The next stages will focus on testing whether orchestration actually improves decision quality rather than merely producing more complicated outputs.

Evaluation should compare the orchestrated system against a single-agent or simple-aggregation baseline using:

- Out-of-sample performance
- Calibration
- Abstention quality
- Regime-specific errors
- Drawdown
- Risk-adjusted returns
- Transaction costs
- Capacity
- Robustness to agent failure
- Information added by independent challenges

## Design Principle

The system should earn the right to act.

Signals are evidence.

Agents are hypotheses.

The orchestrator is the referee.

Execution is constrained by risk.

And every important decision should remain auditable.

---

**Status:** Experimental / Research Prototype

**Version:** 1.0
## Agent Contract

Every Aletheia agent must return a structured decision object.

The agent does not simply produce a prediction.

It must expose the reasoning required for the orchestration layer to evaluate, challenge, compare, and govern that prediction.

Each agent should provide:

- **Direction** — LONG, SHORT, or NEUTRAL
- **Confidence** — calibrated confidence score
- **Time Horizon** — expected duration of the signal
- **Evidence** — observations supporting the decision
- **Contradictory Evidence** — information that argues against the decision
- **Invalidation Conditions** — what would make the thesis wrong
- **Data Timestamp** — when the underlying information was available
- **Model Version** — which agent/model produced the decision
- **Regime Assumption** — the market conditions under which the decision is expected to work
- **Capacity / Liquidity Constraint** — whether the strategy can realistically be expressed at scale

### Example

```json
{
  "agent_id": "A",
  "strategy": "Trend / Momentum",
  "direction": "LONG",
  "confidence": 0.85,
  "horizon": "4-12d",
  "evidence": [],
  "contradictory_evidence": [],
  "invalidation_conditions": [],
  "data_timestamp": "2026-08-29T00:00:00Z",
  "model_version": "A-v1",
  "regime_assumption": "High-IV / Mean Reversion",
  "capacity_constraint": null
}

