"""
Tests for signup and participant removal endpoints.
Tests POST /activities/{activity_name}/signup and DELETE /activities/{activity_name}/participants/{email}
Uses AAA (Arrange-Act-Assert) pattern for clear test structure.
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and new student email
        Act: Sign up new student for Chess Club
        Assert: Verify signup is successful and status is 200
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["new_participant"]

        # Act: Submit signup request
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Check successful response
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and verify initial participants
        Act: Sign up new student
        Assert: Verify participant was added to activity
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["new_participant"]
        
        # Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])

        # Act: Sign up new participant
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Verify participant was added
        response = client.get("/activities")
        updated_count = len(response.json()[activity_name]["participants"])
        assert updated_count == initial_count + 1
        assert email in response.json()[activity_name]["participants"]

    def test_signup_duplicate_email_rejected(self, client, sample_activity):
        """
        Arrange: Prepare existing participant from sample_activity
        Act: Attempt to sign up with same email twice
        Assert: Verify duplicate signup is rejected with 400 status
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["existing_participant"]

        # Act: Try to sign up with existing participant email
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Check that signup is rejected
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_rejected(self, client):
        """
        Arrange: Prepare TestClient and invalid activity name
        Act: Attempt to sign up for non-existent activity
        Assert: Verify request is rejected with 404 status
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act: Try to sign up for activity that doesn't exist
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Check that request is rejected
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_full_activity_rejected(self, client):
        """
        Arrange: Create activity with minimal capacity and fill it
        Act: Attempt to sign up when activity is full
        Assert: Verify signup is rejected with 400 status
        """
        # Arrange: Use Basketball Team which has max_participants=15 with 1 participant
        # We'll fill it with multiple signups
        activity_name = "Basketball Team"
        
        # Get current participant count
        response = client.get("/activities")
        current_count = len(response.json()[activity_name]["participants"])
        max_participants = response.json()[activity_name]["max_participants"]
        
        # Sign up students until activity is full
        for i in range(max_participants - current_count):
            email = f"student{i}@mergington.edu"
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Act: Try to sign up when activity is full
        email_over_capacity = "overcapacity@mergington.edu"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email_over_capacity}
        )

        # Assert: Check that signup is rejected
        assert response.status_code == 400
        assert "full" in response.json()["detail"]

    def test_signup_multiple_different_users(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and multiple unique emails
        Act: Sign up multiple different students for same activity
        Assert: Verify all signups succeed and participants are added
        """
        # Arrange
        activity_name = sample_activity["name"]
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]

        # Act: Sign up multiple students
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            # Assert each signup succeeds
            assert response.status_code == 200

        # Assert: All participants are in the activity
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        for email in emails:
            assert email in participants


class TestRemoveParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_remove_participant_successful(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and existing participant
        Act: Remove participant from activity
        Assert: Verify removal is successful and status is 200
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["existing_participant"]

        # Act: Remove participant
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert: Check successful response
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]

    def test_remove_participant_removes_from_activity(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and verify initial participants
        Act: Remove participant from activity
        Assert: Verify participant was removed from activity
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["existing_participant"]
        
        # Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])

        # Act: Remove participant
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert: Verify participant was removed
        response = client.get("/activities")
        updated_count = len(response.json()[activity_name]["participants"])
        assert updated_count == initial_count - 1
        assert email not in response.json()[activity_name]["participants"]

    def test_remove_nonexistent_participant_rejected(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and non-existent participant email
        Act: Attempt to remove participant that doesn't exist
        Assert: Verify request is rejected with 404 status
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = "nonexistent@mergington.edu"

        # Act: Try to remove participant that doesn't exist
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert: Check that request is rejected
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_from_nonexistent_activity_rejected(self, client):
        """
        Arrange: Prepare TestClient and invalid activity name
        Act: Attempt to remove from non-existent activity
        Assert: Verify request is rejected with 404 status
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act: Try to remove from activity that doesn't exist
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert: Check that request is rejected
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_and_rejoin(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and participant to remove
        Act: Remove participant, then sign them up again
        Assert: Verify participant can rejoin after removal
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = "rejoin@mergington.edu"

        # Act 1: Sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        # Act 2: Remove
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        assert response.status_code == 200

        # Act 3: Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Rejoin is successful
        assert response.status_code == 200

    def test_remove_participant_twice_rejected(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and participant to remove
        Act: Remove participant twice
        Assert: Verify second removal is rejected with 404 status
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["existing_participant"]

        # Act 1: Remove participant first time
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        assert response.status_code == 200

        # Act 2: Try to remove same participant again
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert: Second removal is rejected
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
