"""API client tests using dynamic factories based on OpenAPI spec."""

import pytest
import requests
from pathlib import Path
from useshortcut.client import APIClient
from useshortcut import models
from tests.dynamic_factories import DynamicFactory


@pytest.fixture
def factory():
    """Create a dynamic factory instance."""
    yaml_path = Path(__file__).parent.parent / "shortcut-api-v3.yaml"
    return DynamicFactory(str(yaml_path))


@pytest.fixture
def api_client():
    """Create an API client instance for testing."""
    return APIClient(api_token="test-token-123")


@pytest.fixture
def base_url():
    """Return the base URL for mocking."""
    return "https://api.app.shortcut.com/api/v3"


class TestDynamicStoryEndpoints:
    """Test Story endpoints with dynamically generated data."""

    def test_create_story_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test creating a story with dynamic data."""
        # Generate input data from CreateStoryParams schema
        story_input_data = factory.create("CreateStoryParams")
        story_input = models.StoryInput(
            name=story_input_data["name"],
            workflow_state_id=story_input_data.get("workflow_state_id", 500000),
        )

        # Generate response from Story schema
        story_response = factory.create(
            "Story",
            id=1001,
            name=story_input.name,
            workflow_state_id=story_input.workflow_state_id,
        )

        requests_mock.post(f"{base_url}/stories", json=story_response)

        story = api_client.create_story(story_input)

        assert isinstance(story, models.Story)
        assert story.id == 1001
        assert story.name == story_input.name

    def test_list_stories_from_path(self, requests_mock, api_client, base_url, factory):
        """Test listing stories using path-based response generation."""
        # This would work if we had a list stories endpoint
        # For now, use search as an example
        search_response = factory.create_search_response(
            "StorySearchResult", total=25, page_size=10
        )

        requests_mock.get(f"{base_url}/search/stories", json=search_response)

        result = api_client.search_stories(models.SearchInputs(query="test"))

        assert result.total == 25
        assert len(result.data) == 10
        assert result.next is not None

    def test_get_story_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test getting a story with full dynamic data."""
        story_id = 1234
        story_response = factory.create("Story", id=story_id)

        requests_mock.get(f"{base_url}/stories/{story_id}", json=story_response)

        story = api_client.get_story(story_id)

        assert isinstance(story, models.Story)
        assert story.id == story_id
        # Verify some dynamic fields exist
        assert hasattr(story, "name")
        assert hasattr(story, "created_at")

    def test_update_story_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test updating a story with dynamic data."""
        story_id = 1234
        update_data = factory.create("UpdateStory", name="Updated Dynamic Story")

        # Create a story object for update
        updated_story = models.Story(**update_data)

        # Generate response
        story_response = factory.create("Story", id=story_id, **update_data)

        requests_mock.put(f"{base_url}/stories/{story_id}", json=story_response)

        story = api_client.update_story(story_id, updated_story)

        assert isinstance(story, models.Story)
        assert story.id == story_id


class TestDynamicEpicEndpoints:
    """Test Epic endpoints with dynamically generated data."""

    def test_list_epics_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test listing epics with dynamic data."""
        epics_response = factory.create_list("EpicSlim", count=5)

        requests_mock.get(f"{base_url}/epics", json=epics_response)

        epics = api_client.list_epics()

        assert len(epics) == 5
        assert all(isinstance(epic, models.Epic) for epic in epics)
        # Verify dynamic data
        for epic in epics:
            assert hasattr(epic, "id")
            assert hasattr(epic, "name")

    def test_create_epic_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test creating an epic with dynamic data."""
        epic_input_data = factory.create("CreateEpic")
        epic_input = models.EpicInput(name=epic_input_data["name"])

        epic_response = factory.create("Epic", id=2001, name=epic_input.name)

        requests_mock.post(f"{base_url}/epics", json=epic_response)

        epic = api_client.create_epic(epic_input)

        assert isinstance(epic, models.Epic)
        assert epic.id == 2001
        assert epic.name == epic_input.name


class TestDynamicWorkflowEndpoints:
    """Test Workflow endpoints with dynamically generated data."""

    def test_list_workflows_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test listing workflows with dynamic data."""
        # Generate workflows with proper state arrays
        workflows_response = []
        for i in range(3):
            workflow = factory.create("Workflow")
            # Ensure states array exists and has proper structure
            if "states" not in workflow or not workflow["states"]:
                workflow["states"] = [
                    factory.create(
                        "WorkflowState",
                        id=500000 + i * 10,
                        position=j,
                        type=["unstarted", "started", "done"][j % 3],
                    )
                    for j in range(3)
                ]
            workflows_response.append(workflow)

        requests_mock.get(f"{base_url}/workflows", json=workflows_response)

        workflows = api_client.list_workflows()

        assert len(workflows) == 3
        # Note: This might fail due to model issues, but the mock data is correct


class TestDynamicLabelEndpoints:
    """Test Label endpoints with dynamically generated data."""

    def test_create_label_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test creating a label with dynamic data."""
        label_input_data = factory.create("CreateLabelParams")

        # Create input ensuring required fields
        label_input = models.CreateLabelInput(
            name=label_input_data.get("name", "Dynamic Label"),
            color=label_input_data.get("color", "#ff0000"),
        )

        label_response = factory.create(
            "Label", id=4001, name=label_input.name, color=label_input.color
        )

        requests_mock.post(f"{base_url}/labels", json=label_response)

        label = api_client.create_label(label_input)

        assert label.id == 4001
        assert label.name == label_input.name
        assert label.color == label_input.color

    def test_list_labels_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test listing labels with dynamic data."""
        labels_response = factory.create_list("Label", count=8)

        requests_mock.get(f"{base_url}/labels", json=labels_response)

        labels = api_client.list_labels()

        assert len(labels) == 8
        # Verify dynamic fields
        for label in labels:
            assert hasattr(label, "id")
            assert hasattr(label, "name")
            assert hasattr(label, "color")
            # Verify color format
            assert label.color.startswith("#")
            assert len(label.color) == 7


class TestDynamicIterationEndpoints:
    """Test Iteration endpoints with dynamically generated data."""

    def test_create_iteration_dynamic(
        self, requests_mock, api_client, base_url, factory
    ):
        """Test creating an iteration with dynamic data."""
        iteration_input_data = factory.create("CreateIterationParams")

        iteration_input = models.CreateIterationInput(
            name=iteration_input_data["name"],
            start_date=iteration_input_data["start_date"],
            end_date=iteration_input_data["end_date"],
        )

        iteration_response = factory.create(
            "Iteration",
            id=5001,
            name=iteration_input.name,
            start_date=iteration_input.start_date + "T00:00:00Z",
            end_date=iteration_input.end_date + "T23:59:59Z",
        )

        requests_mock.post(f"{base_url}/iterations", json=iteration_response)

        iteration = api_client.create_iteration(iteration_input)

        assert iteration.id == 5001
        assert iteration.name == iteration_input.name


class TestDynamicProjectEndpoints:
    """Test Project endpoints with dynamically generated data."""

    def test_list_projects_dynamic(self, requests_mock, api_client, base_url, factory):
        """Test listing projects with dynamic data."""
        projects_response = factory.create_list("Project", count=4)

        requests_mock.get(f"{base_url}/projects", json=projects_response)

        projects = api_client.list_projects()

        assert len(projects) == 4
        # Verify dynamic fields
        for project in projects:
            assert hasattr(project, "id")
            assert hasattr(project, "name")
            # Verify color is hex format
            if hasattr(project, "color"):
                assert project.color.startswith("#")


class TestErrorHandlingWithDynamicData:
    """Test error handling with dynamic error responses."""

    def test_404_with_dynamic_error(self, requests_mock, api_client, base_url, factory):
        """Test 404 error with dynamic error message."""
        error_response = {
            "error": "Resource not found",
            "message": f"Story with ID {factory.generator._id_counter} not found",
        }

        requests_mock.get(
            f"{base_url}/stories/99999", status_code=404, json=error_response
        )

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.get_story(99999)

        assert exc_info.value.response.status_code == 404

    def test_validation_error_dynamic(
        self, requests_mock, api_client, base_url, factory
    ):
        """Test validation error with dynamic field names."""
        # Generate a CreateStoryParams to know what fields exist
        story_params = factory.create("CreateStoryParams")
        field_name = list(story_params.keys())[0]  # Get first field name

        error_response = {
            "error": "Validation Error",
            "message": f"Invalid value for field '{field_name}'",
        }

        requests_mock.post(f"{base_url}/stories", status_code=422, json=error_response)

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.create_story(models.StoryInput(name="", workflow_state_id=1))

        assert exc_info.value.response.status_code == 422
