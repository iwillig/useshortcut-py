"""Integration tests for the Shortcut API client.

These tests require a valid SHORTCUT_TOKEN environment variable.
"""

import os
import pytest
from datetime import datetime

from useshortcut.client import APIClient
import useshortcut.models as models
from faker import Faker

# Test data prefix to identify test-created resources
TEST_PREFIX = "TEST_INTEGRATION_"
TEST_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture
def api_client():
    """Create an API client instance."""
    token = os.environ.get("SHORTCUT_API_TOKEN")
    if not token:
        pytest.skip("SHORTCUT_API_TOKEN environment variable not set")
    return APIClient(api_token=token)


fake = Faker()


@pytest.fixture
def epic_name():
    return fake.text()


@pytest.fixture
def epic_input(epic_name):
    epic_input = models.CreateEpicInput(
        name=epic_name,
    )
    return epic_input


@pytest.fixture
def epic(api_client, epic_input):
    epic = api_client.create_epic(epic_input)
    yield epic
    api_client.delete_epic(epic.id)


@pytest.fixture
def default_workflow_state_id(api_client):
    """Get a default workflow state ID for story creation."""
    workflows = api_client.list_workflows()
    if not workflows:
        pytest.skip("No workflows available")

    # Get the first workflow's default state
    workflow = api_client.get_workflow(workflows[0].id)
    return workflow.default_state_id


@pytest.fixture
def test_story_name():
    return fake.text()


@pytest.fixture
def story_input(test_story_name, epic, default_workflow_state_id):
    story_input = models.CreateStoryParams(
        name=test_story_name,
        description="Test story created by integration tests",
        workflow_state_id=default_workflow_state_id,
        story_type="feature",
        epic_id=epic.id,
    )
    return story_input


@pytest.fixture
def story(api_client, story_input, test_story_name, default_workflow_state_id):
    story = api_client.create_story(story_input)
    yield story
    api_client.delete_story(story.id)


@pytest.fixture
def iteration_name():
    iteration_name = fake.word()
    return iteration_name

@pytest.fixture
def iteration_input(iteration_name):
    iteration_input = models.CreateIterationInput(
        name=iteration_name,
        start_date="2020-01-01",
        end_date="2020-01-31",
    )
    return iteration_input

@pytest.fixture
def iteration(api_client, iteration_input):
    iteration = api_client.create_iteration(iteration_input)
    yield iteration
    api_client.delete_iteration(iteration.id)


@pytest.mark.integration
class TestStories:

    def test_create_story(
        self, api_client, default_workflow_state_id, story, test_story_name
    ):
        """Test creating a story."""

        assert story is not None
        assert story.name == test_story_name
        assert story.description == "Test story created by integration tests"
        assert story.workflow_state_id == default_workflow_state_id
        assert story.story_type == "feature"

    def test_update_story(self, api_client, story):
        inputs = models.UpdateStoryInput(
            name="Updated Story name",
        )
        updated_story = api_client.update_story(story.id, inputs)
        assert updated_story.name == "Updated Story name"


@pytest.mark.integration
class TestEpics:

    def test_create_epic(self, api_client, epic_input):
        epic = api_client.create_epic(epic_input)
        assert epic is not None
        assert epic.name == epic_input.name

    def test_update_epic(self, api_client, epic):
        new_name = fake.word()
        epic_input = models.UpdateEpicInput(
            name=new_name,
        )
        updated_epic = api_client.update_epic(epic.id, epic_input)
        assert updated_epic.name == new_name

@pytest.mark.integration
class TestIterations:

    def test_create_iteration(self, api_client, iteration, iteration_input):
        assert iteration is not None
        assert iteration.name == iteration_input.name

    def test_update_iteration(self, api_client, iteration):
        new_name = fake.word()
        iteration_input = models.UpdateIterationInput(
            name=new_name,
        )
        updated_iteration = api_client.update_iteration(iteration.id, iteration_input)
        assert updated_iteration.name == new_name


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
