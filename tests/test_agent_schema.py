import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_agent_output_contains_required_fields():
    schema = load_json(ROOT / "agent_schema.json")
    output = load_json(ROOT / "examples" / "agent_output.json")

    required_fields = schema["required"]

    for field in required_fields:
        assert field in output, f"Missing required field: {field}"


def test_agent_direction_is_valid():
    output = load_json(ROOT / "examples" / "agent_output.json")

    assert output["direction"] in {"LONG", "SHORT", "NEUTRAL"}


def test_agent_confidence_is_valid():
    output = load_json(ROOT / "examples" / "agent_output.json")

    assert 0 <= output["confidence"] <= 1
