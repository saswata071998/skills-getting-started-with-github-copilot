"""
Tests for the activities endpoint (/activities).
Uses AAA (Arrange-Act-Assert) pattern for clear test structure.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Prepare TestClient
        Act: Call GET /activities endpoint
        Assert: Verify response contains all 9 activities
        """
        # Act: Make request to get all activities
        response = client.get("/activities")

        # Assert: Check status code is 200 OK
        assert response.status_code == 200
        
        # Assert: Response is a dictionary with 9 activities
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 9

    def test_get_activities_includes_chess_club(self, client, sample_activity):
        """
        Arrange: Prepare TestClient
        Act: Call GET /activities endpoint
        Assert: Verify Chess Club is in the response
        """
        # Act: Get activities
        response = client.get("/activities")
        activities = response.json()

        # Assert: Chess Club exists in activities
        assert sample_activity["name"] in activities

    def test_get_activities_has_required_fields(self, client):
        """
        Arrange: Prepare TestClient
        Act: Call GET /activities endpoint
        Assert: Verify each activity has required fields
        """
        # Act: Get activities
        response = client.get("/activities")
        activities = response.json()

        # Assert: Each activity has required fields
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in {activity_name}"

    def test_get_activities_participants_is_list(self, client):
        """
        Arrange: Prepare TestClient
        Act: Call GET /activities endpoint
        Assert: Verify participants field is a list
        """
        # Act: Get activities
        response = client.get("/activities")
        activities = response.json()

        # Assert: participants field is a list in each activity
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_max_participants_is_integer(self, client):
        """
        Arrange: Prepare TestClient
        Act: Call GET /activities endpoint
        Assert: Verify max_participants is an integer
        """
        # Act: Get activities
        response = client.get("/activities")
        activities = response.json()

        # Assert: max_participants is an integer
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_activity_has_initial_participants(self, client, sample_activity):
        """
        Arrange: Prepare TestClient and sample activity
        Act: Call GET /activities endpoint
        Assert: Verify Chess Club has initial participants
        """
        # Act: Get activities
        response = client.get("/activities")
        chess_club = response.json()[sample_activity["name"]]

        # Assert: Chess Club has 2 initial participants
        assert len(chess_club["participants"]) == 2
        assert sample_activity["existing_participant"] in chess_club["participants"]
