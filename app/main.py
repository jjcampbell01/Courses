from __future__ import annotations

from pathlib import Path
from typing import Any
import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
MISSIONS_DIR = ROOT / "missions"

app = FastAPI(title="AI WorkOS Academy API", version="0.1.0")

ATTEMPTS: dict[str, dict[str, Any]] = {}
DIMENSIONS = [
    "outcome",
    "decision_quality",
    "communication",
    "risk",
    "efficiency",
    "automation_readiness",
]


def load_mission(mission_id: str) -> dict[str, Any]:
    for path in MISSIONS_DIR.rglob("*.json"):
        import json

        mission = json.loads(path.read_text())
        if mission.get("mission_id") == mission_id:
            return mission
    raise HTTPException(status_code=404, detail=f"Mission '{mission_id}' not found")


class RunStepRequest(BaseModel):
    user_id: str
    attempt_id: str
    step_id: str
    user_input: str
    selected_agent: str | None = None


class EvaluateRequest(BaseModel):
    user_id: str
    attempt_id: str
    artifacts: list[dict[str, Any]]


class CoachRequest(BaseModel):
    user_id: str
    attempt_id: str
    evaluation: dict[str, Any]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/missions/{mission_id}/run-step")
def run_step(mission_id: str, request: RunStepRequest) -> dict[str, Any]:
    mission = load_mission(mission_id)
    step = next((s for s in mission["steps"] if s["step_id"] == request.step_id), None)
    if not step:
        raise HTTPException(status_code=400, detail=f"Invalid step_id '{request.step_id}'")

    attempt = ATTEMPTS.setdefault(request.attempt_id, {"mission_id": mission_id, "artifacts": []})
    artifact = {
        "artifact_id": f"ar_{len(attempt['artifacts']) + 1}",
        "type": "step_output",
        "content": f"[{step['name']}] {request.user_input[:240]}",
    }
    attempt["artifacts"].append(artifact)

    return {
        "assistant_output": f"Processed {step['name']} step using {request.selected_agent or step.get('recommended_agent', 'default_assistant')}",
        "artifacts_generated": [artifact],
        "step_status": "completed" if request.step_id == "s_automate" else "in_progress",
    }


@app.post("/v1/missions/{mission_id}/inject-event")
def inject_event(mission_id: str) -> dict[str, Any]:
    mission = load_mission(mission_id)
    events = mission.get("events", [])
    if not events:
        return {
            "event_id": "ev_none",
            "event_type": "none",
            "urgency": "low",
            "message": "No dynamic events configured.",
            "affected_steps": [],
        }

    event = random.choice(events)
    return {
        "event_id": event["event_id"],
        "event_type": event.get("effect", {}).get("type", "unknown"),
        "urgency": "high",
        "message": f"Runtime event injected: {event['event_id']}",
        "affected_steps": ["s_reason", "s_execute"],
    }


@app.post("/v1/missions/{mission_id}/evaluate")
def evaluate(mission_id: str, request: EvaluateRequest) -> dict[str, Any]:
    mission = load_mission(mission_id)
    rubric_weights = mission.get("rubric", {}).get("weights", {})

    base = min(95, 60 + len(request.artifacts) * 7)
    subscores = {
        d: max(50, min(98, int(base + (i - 2) * 2))) for i, d in enumerate(DIMENSIONS)
    }
    weighted_total = sum(subscores[d] * rubric_weights.get(d, 1 / len(DIMENSIONS)) for d in DIMENSIONS)
    total_score = int(round(weighted_total))

    min_score = mission.get("pass_rules", {}).get("min_total_score", 75)
    gaps = [] if total_score >= min_score else ["Improve evidence and risk mitigation depth"]

    return {
        "total_score": total_score,
        "subscores": subscores,
        "pass_fail": "pass" if total_score >= min_score else "fail",
        "strengths": ["Clear structure", "Action-oriented outputs"],
        "gaps": gaps,
        "risk_flags": ["One claim may need evidence tag"] if request.artifacts else ["No artifacts submitted"],
        "improvement_actions": ["Add confidence labels", "Expand mitigation table"],
        "estimated_time_saved_hours": round(len(request.artifacts) * 0.7, 1),
    }


@app.post("/v1/missions/{mission_id}/coach")
def coach(mission_id: str, request: CoachRequest) -> dict[str, Any]:
    load_mission(mission_id)
    passed = request.evaluation.get("pass_fail") == "pass"

    return {
        "focus_area": "Scale what worked" if passed else "Risk handling under deadline pressure",
        "why_it_matters": "Consistent quality reduces rework and improves trust.",
        "upgraded_sequence": [
            "Re-check assumptions",
            "Add risk table with owner+mitigation",
            "Rewrite stakeholder email with contingency option",
        ],
        "retry_plan": [
            "Re-run Step 2 with explicit risk extraction",
            "Update memo section 'Risks and Mitigation'",
            "Finalize with evidence tags",
        ],
    }
