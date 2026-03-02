"""
Pytest configuration and shared fixtures for FastAPI tests.
Provides TestClient and fresh app state for each test.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient for testing FastAPI endpoints.
    Returns a fresh client for each test.
    """
    # Arrange: Create a test client
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture: Reset activities to initial state before each test.
    This ensures test isolation and prevents test interdependencies.
    Runs automatically for every test (autouse=True).
    """
    # Arrange: Define initial state
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for school tournaments",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Improve tennis skills and compete in matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and visual arts",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Join the school band and perform in concerts",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["sophia@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
            "max_participants": 22,
            "participants": ["ryan@mergington.edu", "maya@mergington.edu"]
        }
    }
    
    # Clear current activities and restore initial state
    activities.clear()
    activities.update(initial_activities)
    
    yield  # Test runs here
    
    # Cleanup: Reset after test completes
    activities.clear()
    activities.update(initial_activities)


@pytest.fixture
def sample_activity():
    """
    Fixture: Provides sample activity data for use in tests.
    Useful for testing edge cases and validation.
    """
    return {
        "name": "Chess Club",
        "new_participant": "newstudent@mergington.edu",
        "existing_participant": "michael@mergington.edu"
    }
