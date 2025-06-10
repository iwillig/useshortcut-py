"""Simple API client tests that work with current model limitations."""

import pytest
import requests
from useshortcut.client import APIClient
from useshortcut import models


@pytest.fixture
def api_client():
    """Create an API client instance for testing."""
    return APIClient(api_token="test-token-123")


@pytest.fixture
def base_url():
    """Return the base URL for mocking."""
    return "https://api.app.shortcut.com/api/v3"


class TestStoryOperations:
    """Test story CRUD operations which have working models."""

    def test_create_story(self, requests_mock, api_client, base_url):
        """Test creating a story."""
        story_input = models.StoryInput(name="Test Story", workflow_state_id=500000)

        story_response = {"id": 1001, "name": "Test Story", "workflow_state_id": 500000}

        requests_mock.post(f"{base_url}/stories", json=story_response)

        story = api_client.create_story(story_input)

        assert isinstance(story, models.Story)
        assert story.id == 1001
        assert story.name == "Test Story"

    def test_get_story(self, requests_mock, api_client, base_url):
        """Test retrieving a story."""
        story_response = {"id": 1001, "name": "Existing Story"}

        requests_mock.get(f"{base_url}/stories/1001", json=story_response)

        story = api_client.get_story(1001)

        assert isinstance(story, models.Story)
        assert story.id == 1001
        assert story.name == "Existing Story"

    def test_update_story(self, requests_mock, api_client, base_url):
        """Test updating a story."""
        updated_story = models.Story(name="Updated Story")

        story_response = {"id": 1001, "name": "Updated Story"}

        requests_mock.put(f"{base_url}/stories/1001", json=story_response)

        story = api_client.update_story(1001, updated_story)

        assert story.name == "Updated Story"

    def test_delete_story(self, requests_mock, api_client, base_url):
        """Test deleting a story."""
        requests_mock.delete(f"{base_url}/stories/1001", status_code=204)

        # Should not raise an exception
        api_client.delete_story(1001)

        assert requests_mock.called

    def test_search_stories(self, requests_mock, api_client, base_url):
        """Test searching for stories."""
        search_params = models.SearchInputs(query="owner:testuser")

        search_response = {"total": 1, "data": [{"id": 1001, "name": "Found Story"}]}

        requests_mock.get(f"{base_url}/search/stories", json=search_response)

        result = api_client.search_stories(search_params)

        assert result.total == 1
        assert len(result.data) == 1


class TestAPIErrors:
    """Test error handling."""

    def test_404_not_found(self, requests_mock, api_client, base_url):
        """Test 404 error handling."""
        requests_mock.get(f"{base_url}/stories/9999", status_code=404)

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.get_story(9999)

        assert exc_info.value.response.status_code == 404

    def test_401_unauthorized(self, requests_mock, api_client, base_url):
        """Test 401 error handling."""
        requests_mock.get(f"{base_url}/member", status_code=401)

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.get_current_member()

        assert exc_info.value.response.status_code == 401

    def test_500_server_error(self, requests_mock, api_client, base_url):
        """Test 500 error handling."""
        requests_mock.post(f"{base_url}/stories", status_code=500)

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.create_story(models.StoryInput(name="Test", workflow_state_id=1))

        assert exc_info.value.response.status_code == 500


class TestLabelOperations:
    """Test label operations which have simpler models."""

    def test_create_label(self, requests_mock, api_client, base_url):
        """Test creating a label."""
        label_input = models.CreateLabelInput(name="bug", color="#ff0000")

        label_response = {
            "id": 4001,
            "global_id": "label-4001",
            "name": "bug",
            "color": "#ff0000",
            "archived": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "external_id": None,
            "stats": {},
            "entity_type": "label",
            "app_url": "https://app.shortcut.com/workspace/label/4001",
            "description": None,
        }

        requests_mock.post(f"{base_url}/labels", json=label_response)

        label = api_client.create_label(label_input)

        assert label.id == 4001
        assert label.name == "bug"
        assert label.color == "#ff0000"

    def test_delete_label(self, requests_mock, api_client, base_url):
        """Test deleting a label."""
        requests_mock.delete(f"{base_url}/labels/4001", status_code=204)

        api_client.delete_label(4001)

        assert requests_mock.called


class TestIterationOperations:
    """Test iteration operations."""

    def test_create_iteration(self, requests_mock, api_client, base_url):
        """Test creating an iteration."""
        iteration_input = models.CreateIterationInput(
            name="Sprint 1", start_date="2023-01-01", end_date="2023-01-14"
        )

        iteration_response = {
            "id": 5001,
            "name": "Sprint 1",
            "global_id": "spr-5001",
            "start_date": "2023-01-01T00:00:00Z",
            "end_date": "2023-01-14T00:00:00Z",
        }

        requests_mock.post(f"{base_url}/iterations", json=iteration_response)

        iteration = api_client.create_iteration(iteration_input)

        assert iteration.id == 5001
        assert iteration.name == "Sprint 1"

    def test_get_iteration(self, requests_mock, api_client, base_url):
        """Test retrieving an iteration."""
        iteration_response = {"id": 5001, "name": "Sprint 1", "global_id": "spr-5001"}

        requests_mock.get(f"{base_url}/iterations/5001", json=iteration_response)

        iteration = api_client.get_iteration(5001)

        assert iteration.id == 5001
        assert iteration.name == "Sprint 1"


class TestCategoryOperations:
    """Test category operations."""

    def test_create_category(self, requests_mock, api_client, base_url):
        """Test creating a category."""
        category_input = models.CreateCategoryInput(name="Q1 Goals")

        category_response = {
            "id": 6001,
            "global_id": "cat-6001",
            "name": "Q1 Goals",
            "type": "milestone",
            "color": "#0000ff",
            "archived": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "entity_type": "category",
            "external_id": None,
        }

        requests_mock.post(f"{base_url}/categories", json=category_response)

        category = api_client.create_category(category_input)

        assert category.id == 6001
        assert category.name == "Q1 Goals"
