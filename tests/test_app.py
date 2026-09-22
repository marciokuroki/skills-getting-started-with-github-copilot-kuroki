from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_function():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]


def test_unregister_participant_removes_email_from_activity():
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess Club/participants/{quote(email)}")

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Removed {email} from Chess Club"


def test_unregister_participant_returns_404_when_email_not_found():
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/Chess Club/participants/{quote(email)}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
