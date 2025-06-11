import pytest
from datetime import datetime
from useshortcut import models
from useshortcut.client import APIClient


@pytest.fixture
def api_client():
    """Create an API client instance for testing."""
    return APIClient(api_token="test-token-123")


@pytest.fixture
def base_url():
    """Return the base URL for mocking."""
    return "https://api.app.shortcut.com/api/v3"


@pytest.fixture
def milestone_stats_data():
    """Sample milestone stats data."""
    return {
        "num_related_documents": 5,
        "average_cycle_time": 86400,
        "average_lead_time": 172800,
    }


@pytest.fixture
def category_data():
    """Sample category data."""
    return {
        "id": 100,
        "global_id": "category-100",
        "name": "Engineering",
        "type": "team",
        "color": "#ff0000",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "entity_type": "category",
        "archived": False,
    }


@pytest.fixture
def milestone_data(milestone_stats_data, category_data):
    """Sample milestone data."""
    return {
        "id": 111,
        "name": "Q1 2024 Release",
        "description": "First quarter release milestone",
        "state": "in progress",
        "position": 1,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z",
        "entity_type": "milestone",
        "app_url": "https://app.shortcut.com/workspace/milestone/111",
        "global_id": "milestone-111",
        "archived": False,
        "started": True,
        "completed": False,
        "started_at": "2024-01-01T00:00:00Z",
        "completed_at": None,
        "started_at_override": None,
        "completed_at_override": None,
        "key_result_ids": ["kr-123", "kr-456"],
        "stats": milestone_stats_data,
        "categories": [category_data],
    }


@pytest.fixture
def epic_data():
    """Sample epic data for milestone epics endpoint."""
    return {
        "id": 222,
        "global_id": "epic-222",
        "name": "Authentication System",
        "description": "Implement OAuth2 authentication",
        "state": "in progress",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z",
        "started": True,
        "completed": False,
        "archived": False,
        "labels": [],
        "milestone_id": 111,
    }


class TestMilestones:
    """Test milestone endpoints."""

    def test_list_milestones(self, requests_mock, api_client, base_url, milestone_data):
        """Test listing all milestones."""
        requests_mock.get(f"{base_url}/milestones", json=[milestone_data])

        milestones = api_client.list_milestones()

        assert len(milestones) == 1
        assert isinstance(milestones[0], models.Milestone)
        assert milestones[0].id == 111
        assert milestones[0].name == "Q1 2024 Release"
        assert milestones[0].state == "in progress"

    def test_get_milestone(self, requests_mock, api_client, base_url, milestone_data):
        """Test fetching a specific milestone."""
        milestone_id = 111

        requests_mock.get(f"{base_url}/milestones/{milestone_id}", json=milestone_data)

        milestone = api_client.get_milestone(milestone_id)

        assert isinstance(milestone, models.Milestone)
        assert milestone.id == 111
        assert milestone.description == "First quarter release milestone"
        assert milestone.started is True
        assert milestone.completed is False

    def test_create_milestone(
        self, requests_mock, api_client, base_url, milestone_data
    ):
        """Test creating a new milestone."""
        milestone_input = models.CreateMilestoneInput(
            name="Q2 2024 Release", description="Second quarter release"
        )

        requests_mock.post(f"{base_url}/milestones", json=milestone_data)

        milestone = api_client.create_milestone(milestone_input)

        assert isinstance(milestone, models.Milestone)
        assert milestone.id == 111

    def test_create_milestone_with_categories(
        self, requests_mock, api_client, base_url, milestone_data
    ):
        """Test creating milestone with categories."""
        category_params = models.CreateCategoryParams(
            name="Engineering", color="#ff0000"
        )

        milestone_input = models.CreateMilestoneInput(
            name="Q2 2024 Release",
            description="Second quarter release",
            categories=[category_params],
        )

        requests_mock.post(f"{base_url}/milestones", json=milestone_data)

        milestone = api_client.create_milestone(milestone_input)

        assert len(milestone.categories) == 1
        assert milestone.categories[0].name == "Engineering"

    def test_update_milestone(self, requests_mock, api_client, base_url):
        """Test updating milestone properties."""
        milestone_id = 111
        updated_data = {
            "id": 111,
            "name": "Q1 2024 Release - Updated",
            "description": "Updated description",
            "state": "in progress",
            "position": 1,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-20T00:00:00Z",
            "entity_type": "milestone",
            "app_url": "https://app.shortcut.com/workspace/milestone/111",
            "global_id": "milestone-111",
            "archived": False,
            "started": True,
            "completed": False,
            "stats": {"num_related_documents": 5},
            "categories": [],
        }

        update_input = models.UpdateMilestoneInput(
            name="Q1 2024 Release - Updated", description="Updated description"
        )

        requests_mock.put(f"{base_url}/milestones/{milestone_id}", json=updated_data)

        milestone = api_client.update_milestone(milestone_id, update_input)

        assert milestone.name == "Q1 2024 Release - Updated"
        assert milestone.description == "Updated description"

    def test_update_milestone_state(
        self, requests_mock, api_client, base_url, milestone_data
    ):
        """Test changing milestone state."""
        milestone_id = 111
        completed_data = milestone_data.copy()
        completed_data.update(
            {"state": "done", "completed": True, "completed_at": "2024-03-31T00:00:00Z"}
        )

        update_input = models.UpdateMilestoneInput(state="done")

        requests_mock.put(f"{base_url}/milestones/{milestone_id}", json=completed_data)

        milestone = api_client.update_milestone(milestone_id, update_input)

        assert milestone.state == "done"
        assert milestone.completed is True

    def test_update_milestone_reorder(
        self, requests_mock, api_client, base_url, milestone_data
    ):
        """Test reordering milestones."""
        milestone_id = 111
        reordered_data = milestone_data.copy()
        reordered_data["position"] = 3

        update_input = models.UpdateMilestoneInput(after_id=112)

        requests_mock.put(f"{base_url}/milestones/{milestone_id}", json=reordered_data)

        milestone = api_client.update_milestone(milestone_id, update_input)

        assert milestone.position == 3

    def test_delete_milestone(self, requests_mock, api_client, base_url):
        """Test deleting a milestone."""
        milestone_id = 111

        requests_mock.delete(f"{base_url}/milestones/{milestone_id}", status_code=204)

        # Should not raise an exception
        api_client.delete_milestone(milestone_id)

    def test_milestone_stats_parsing(
        self, requests_mock, api_client, base_url, milestone_data
    ):
        """Test MilestoneStats model parsing."""
        milestone_id = 111

        requests_mock.get(f"{base_url}/milestones/{milestone_id}", json=milestone_data)

        milestone = api_client.get_milestone(milestone_id)

        assert isinstance(milestone.stats, models.MilestoneStats)
        assert milestone.stats.num_related_documents == 5
        assert milestone.stats.average_cycle_time == 86400
        assert milestone.stats.average_lead_time == 172800

    def test_list_milestone_epics(self, requests_mock, api_client, base_url, epic_data):
        """Test fetching epics for a milestone."""
        milestone_id = 111

        requests_mock.get(
            f"{base_url}/milestones/{milestone_id}/epics", json=[epic_data]
        )

        epics = api_client.list_milestone_epics(milestone_id)

        assert len(epics) == 1
        assert isinstance(epics[0], models.Epic)
        assert epics[0].id == 222
        assert epics[0].name == "Authentication System"

    def test_list_category_milestones(
        self, requests_mock, api_client, base_url, milestone_data
    ):
        """Test fetching milestones in a category."""
        category_id = 100

        requests_mock.get(
            f"{base_url}/categories/{category_id}/milestones", json=[milestone_data]
        )

        milestones = api_client.list_category_milestones(category_id)

        assert len(milestones) == 1
        assert isinstance(milestones[0], models.Milestone)
        assert milestones[0].id == 111

    def test_milestone_datetime_parsing(
        self, requests_mock, api_client, base_url, milestone_data
    ):
        """Test that datetime fields are properly parsed."""
        milestone_id = 111

        requests_mock.get(f"{base_url}/milestones/{milestone_id}", json=milestone_data)

        milestone = api_client.get_milestone(milestone_id)

        assert isinstance(milestone.created_at, datetime)
        assert isinstance(milestone.updated_at, datetime)
        assert isinstance(milestone.started_at, datetime)
        assert milestone.created_at.year == 2023
        assert milestone.started_at.year == 2024
        assert milestone.completed_at is None

    def test_milestone_not_found(self, requests_mock, api_client, base_url):
        """Test 404 error handling."""
        milestone_id = 999

        requests_mock.get(
            f"{base_url}/milestones/{milestone_id}",
            status_code=404,
            json={"message": "Milestone not found", "error": "NotFound"},
        )

        with pytest.raises(Exception):  # Will be HTTPError
            api_client.get_milestone(milestone_id)
