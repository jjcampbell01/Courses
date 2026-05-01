from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
MISSION_ID = "mgr_m01_inbox_command"


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_run_step_and_evaluate_and_coach() -> None:
    run_resp = client.post(
        f"/v1/missions/{MISSION_ID}/run-step",
        json={
            "user_id": "u_1",
            "attempt_id": "a_1",
            "step_id": "s_collect",
            "user_input": "Prioritize inbox items",
            "selected_agent": "chief_of_staff",
        },
    )
    assert run_resp.status_code == 200
    artifacts = run_resp.json()["artifacts_generated"]
    assert artifacts

    eval_resp = client.post(
        f"/v1/missions/{MISSION_ID}/evaluate",
        json={"user_id": "u_1", "attempt_id": "a_1", "artifacts": artifacts},
    )
    assert eval_resp.status_code == 200
    evaluation = eval_resp.json()
    assert "total_score" in evaluation
    assert "pass_fail" in evaluation

    coach_resp = client.post(
        f"/v1/missions/{MISSION_ID}/coach",
        json={"user_id": "u_1", "attempt_id": "a_1", "evaluation": evaluation},
    )
    assert coach_resp.status_code == 200
    assert "focus_area" in coach_resp.json()
