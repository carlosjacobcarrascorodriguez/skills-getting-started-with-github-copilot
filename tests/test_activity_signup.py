from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_activity_full_prevents_signup():
    activity_name = "Basketball Team"
    original_participants = activities[activity_name]["participants"][:]

    try:
        activities[activity_name]["participants"] = [
            f"student{i}@mergington.edu"
            for i in range(activities[activity_name]["max_participants"])
        ]

        response = client.post(
            f"/activities/{activity_name}/signup?email=extra@mergington.edu"
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
    finally:
        activities[activity_name]["participants"] = original_participants
