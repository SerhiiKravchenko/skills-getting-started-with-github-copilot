import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


class TestActivitiesAPI:
    def test_get_activities(self, client):
        # Arrange: No specific setup needed as data is in-memory

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Check response status and structure
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "participants" in data["Chess Club"]
        assert "max_participants" in data["Chess Club"]

    def test_signup_success(self, client):
        # Arrange: Choose an activity and new email
        activity = "Programming Class"
        email = "newstudent@mergington.edu"

        # Act: Make POST request to signup
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert: Check success response and that email was added
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]

        # Verify in activities data
        get_response = client.get("/activities")
        data = get_response.json()
        assert email in data[activity]["participants"]

    def test_signup_duplicate(self, client):
        # Arrange: Use an existing participant
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act: Attempt to signup again
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert: Should return 400 error
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"]

    def test_signup_activity_not_found(self, client):
        # Arrange: Use non-existent activity
        activity = "NonExistent Activity"
        email = "test@mergington.edu"

        # Act: Attempt to signup
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert: Should return 404 error
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_unregister_success(self, client):
        # Arrange: Choose an activity and existing participant
        activity = "Gym Class"
        email = "john@mergington.edu"  # Already in participants

        # Act: Make DELETE request to unregister
        response = client.delete(f"/activities/{activity}/signup?email={email}")

        # Assert: Check success response
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]

        # Verify removed from activities data
        get_response = client.get("/activities")
        data = get_response.json()
        assert email not in data[activity]["participants"]

    def test_unregister_not_signed_up(self, client):
        # Arrange: Use an email not in the activity
        activity = "Chess Club"
        email = "notsignedup@mergington.edu"

        # Act: Attempt to unregister
        response = client.delete(f"/activities/{activity}/signup?email={email}")

        # Assert: Should return 400 error
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "not signed up" in result["detail"]

    def test_unregister_activity_not_found(self, client):
        # Arrange: Use non-existent activity
        activity = "NonExistent Activity"
        email = "test@mergington.edu"

        # Act: Attempt to unregister
        response = client.delete(f"/activities/{activity}/signup?email={email}")

        # Assert: Should return 404 error
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]