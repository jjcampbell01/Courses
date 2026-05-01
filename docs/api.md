# API Contracts

## POST /v1/missions/{mission_id}/run-step

Runs the selected mission step with user input and optional selected agent.

### Request

```json
{
  "user_id": "u_123",
  "attempt_id": "a_456",
  "step_id": "s_collect",
  "user_input": "Analyze these emails and prioritize actions.",
  "selected_agent": "chief_of_staff"
}
```

### Response

```json
{
  "assistant_output": "...",
  "artifacts_generated": [
    { "artifact_id": "ar_1", "type": "task_table", "content": "..." }
  ],
  "step_status": "in_progress"
}
```

## POST /v1/missions/{mission_id}/inject-event

Injects a runtime event for scenario realism.

### Response

```json
{
  "event_id": "ev_deadline_shift_1",
  "event_type": "change_deadline",
  "urgency": "high",
  "message": "VP moved review from Friday to Wednesday 9 AM.",
  "affected_steps": ["s_reason", "s_execute"]
}
```

## POST /v1/missions/{mission_id}/evaluate

Grades attempt artifacts against rubric and pass rules.

### Response

```json
{
  "total_score": 81,
  "subscores": {
    "outcome": 85,
    "decision_quality": 78,
    "communication": 88,
    "risk": 72,
    "efficiency": 80,
    "automation_readiness": 79
  },
  "pass_fail": "pass",
  "strengths": ["Clear priorities", "Strong executive memo structure"],
  "gaps": ["Insufficient risk mitigation detail"],
  "risk_flags": ["Two claims missing evidence tags"],
  "improvement_actions": ["Add confidence labels to KPI assumptions"],
  "estimated_time_saved_hours": 3.1
}
```

## POST /v1/missions/{mission_id}/coach

Produces targeted retry guidance from evaluation data.

### Response

```json
{
  "focus_area": "Risk handling under deadline pressure",
  "why_it_matters": "Prevents executive rework and credibility loss.",
  "upgraded_sequence": [
    "Re-check assumptions",
    "Add risk table with owner+mitigation",
    "Rewrite stakeholder email with contingency option"
  ],
  "retry_plan": [
    "Re-run Step 2 with explicit risk extraction",
    "Update memo section 'Risks and Mitigation'",
    "Finalize with evidence tags"
  ]
}
```

