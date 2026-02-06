from datetime import datetime

import pytest
import requests

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
def task_data():
    """Sample task data."""
    return {
        "id": 789,
        "description": "Complete unit tests",
        "complete": False,
        "story_id": 456,
        "entity_type": "task",
        "position": 1,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "completed_at": None,
        "external_id": None,
        "global_id": "task-789",
        "owner_ids": ["12345678-1234-1234-1234-123456789012"],
        "member_mention_ids": [],
        "group_mention_ids": [],
        "mention_ids": [],
    }


@pytest.fixture
def completed_task_data():
    """Sample completed task data."""
    return {
        "id": 790,
        "description": "Review PR",
        "complete": True,
        "story_id": 456,
        "entity_type": "task",
        "position": 2,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-03T00:00:00Z",
        "completed_at": "2023-01-03T00:00:00Z",
        "external_id": None,
        "global_id": "task-790",
        "owner_ids": ["87654321-4321-4321-4321-210987654321"],
        "member_mention_ids": [],
        "group_mention_ids": [],
        "mention_ids": [],
    }


class TestStoryTasks:
    """Test story task endpoints."""

    def test_list_story_tasks(
        self, requests_mock, api_client, base_url, task_data, completed_task_data
    ):
        """Test listing all tasks for a story."""
        story_id = 456

        requests_mock.get(
            f"{base_url}/stories/{story_id}/tasks",
            json=[task_data, completed_task_data],
        )

        tasks = api_client.list_story_tasks(story_id)

        assert len(tasks) == 2
        assert isinstance(tasks[0], models.Task)
        assert tasks[0].id == 789
        assert tasks[0].description == "Complete unit tests"
        assert tasks[0].complete is False
        assert tasks[1].complete is True

    def test_create_story_task(self, requests_mock, api_client, base_url, task_data):
        """Test creating a new task on a story."""
        story_id = 456
        task_input = models.CreateTaskInput(description="New task description")

        requests_mock.post(f"{base_url}/stories/{story_id}/tasks", json=task_data)

        task = api_client.create_story_task(story_id, task_input)

        assert isinstance(task, models.Task)
        assert task.id == 789
        assert task.story_id == 456
        assert task.complete is False

    def test_create_story_task_with_owners(self, requests_mock, api_client, base_url):
        """Test creating a task with owner assignments."""
        story_id = 456
        task_with_owners = {
            "id": 791,
            "description": "Task with multiple owners",
            "complete": False,
            "story_id": 456,
            "entity_type": "task",
            "position": 3,
            "created_at": "2023-01-01T00:00:00Z",
            "owner_ids": [
                "12345678-1234-1234-1234-123456789012",
                "87654321-4321-4321-4321-210987654321",
            ],
            "member_mention_ids": [],
            "group_mention_ids": [],
        }

        task_input = models.CreateTaskInput(
            description="Task with multiple owners",
            owner_ids=[
                "12345678-1234-1234-1234-123456789012",
                "87654321-4321-4321-4321-210987654321",
            ],
        )

        requests_mock.post(
            f"{base_url}/stories/{story_id}/tasks", json=task_with_owners
        )

        task = api_client.create_story_task(story_id, task_input)

        assert len(task.owner_ids) == 2
        assert "12345678-1234-1234-1234-123456789012" in task.owner_ids

    def test_get_story_task(self, requests_mock, api_client, base_url, task_data):
        """Test fetching a specific task."""
        story_id = 456
        task_id = 789

        requests_mock.get(
            f"{base_url}/stories/{story_id}/tasks/{task_id}", json=task_data
        )

        task = api_client.get_story_task(story_id, task_id)

        assert isinstance(task, models.Task)
        assert task.id == 789
        assert task.description == "Complete unit tests"

    def test_update_story_task(self, requests_mock, api_client, base_url):
        """Test updating task properties."""
        story_id = 456
        task_id = 789
        updated_data = {
            "id": 789,
            "description": "Updated task description",
            "complete": False,
            "story_id": 456,
            "entity_type": "task",
            "position": 1,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-04T00:00:00Z",
            "owner_ids": ["12345678-1234-1234-1234-123456789012"],
            "member_mention_ids": [],
            "group_mention_ids": [],
        }

        update_input = models.UpdateTaskInput(description="Updated task description")

        requests_mock.put(
            f"{base_url}/stories/{story_id}/tasks/{task_id}", json=updated_data
        )

        task = api_client.update_story_task(story_id, task_id, update_input)

        assert task.description == "Updated task description"

    def test_update_story_task_complete_status(
        self, requests_mock, api_client, base_url
    ):
        """Test marking task as complete."""
        story_id = 456
        task_id = 789
        completed_data = {
            "id": 789,
            "description": "Complete unit tests",
            "complete": True,
            "story_id": 456,
            "entity_type": "task",
            "position": 1,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-04T00:00:00Z",
            "completed_at": "2023-01-04T00:00:00Z",
            "owner_ids": ["12345678-1234-1234-1234-123456789012"],
            "member_mention_ids": [],
            "group_mention_ids": [],
        }

        update_input = models.UpdateTaskInput(complete=True)

        requests_mock.put(
            f"{base_url}/stories/{story_id}/tasks/{task_id}", json=completed_data
        )

        task = api_client.update_story_task(story_id, task_id, update_input)

        assert task.complete is True
        assert task.completed_at is not None

    def test_update_story_task_reorder(self, requests_mock, api_client, base_url):
        """Test reordering tasks using before_id/after_id."""
        story_id = 456
        task_id = 789
        reordered_data = {
            "id": 789,
            "description": "Complete unit tests",
            "complete": False,
            "story_id": 456,
            "entity_type": "task",
            "position": 3,  # Changed position
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-04T00:00:00Z",
            "owner_ids": ["12345678-1234-1234-1234-123456789012"],
            "member_mention_ids": [],
            "group_mention_ids": [],
        }

        update_input = models.UpdateTaskInput(after_id=790)

        requests_mock.put(
            f"{base_url}/stories/{story_id}/tasks/{task_id}", json=reordered_data
        )

        task = api_client.update_story_task(story_id, task_id, update_input)

        assert task.position == 3

    def test_delete_story_task(self, requests_mock, api_client, base_url):
        """Test deleting a task."""
        story_id = 456
        task_id = 789

        requests_mock.delete(
            f"{base_url}/stories/{story_id}/tasks/{task_id}", status_code=204
        )

        # Should not raise an exception
        api_client.delete_story_task(story_id, task_id)

    def test_task_datetime_parsing(
        self, requests_mock, api_client, base_url, task_data, completed_task_data
    ):
        """Test that datetime fields are properly parsed."""
        story_id = 456

        requests_mock.get(
            f"{base_url}/stories/{story_id}/tasks",
            json=[task_data, completed_task_data],
        )

        tasks = api_client.list_story_tasks(story_id)

        # Check first task
        assert isinstance(tasks[0].created_at, datetime)
        assert isinstance(tasks[0].updated_at, datetime)
        assert tasks[0].completed_at is None

        # Check completed task
        assert isinstance(tasks[1].created_at, datetime)
        assert isinstance(tasks[1].updated_at, datetime)
        assert isinstance(tasks[1].completed_at, datetime)
        assert tasks[1].completed_at.year == 2023
        assert tasks[1].completed_at.month == 1
        assert tasks[1].completed_at.day == 3

    def test_task_not_found(self, requests_mock, api_client, base_url):
        """Test 404 error handling."""
        story_id = 456
        task_id = 999

        requests_mock.get(
            f"{base_url}/stories/{story_id}/tasks/{task_id}",
            status_code=404,
            json={"message": "Task not found", "error": "NotFound"},
        )

        with pytest.raises(requests.exceptions.HTTPError):
            api_client.get_story_task(story_id, task_id)
