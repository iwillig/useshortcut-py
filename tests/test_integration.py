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


@pytest.fixture
def label_name():
    return fake.word()


@pytest.fixture
def label_input(label_name):
    label_input = models.CreateLabelInput(
        name=label_name,
        color="#ff0000",
    )
    return label_input


@pytest.fixture
def label(api_client, label_input):
    label = api_client.create_label(label_input)
    yield label
    api_client.delete_label(label.id)


@pytest.fixture
def milestone_name():
    return fake.text()


@pytest.fixture
def milestone_input(milestone_name):
    milestone_input = models.CreateMilestoneInput(
        name=milestone_name,
        description="Test milestone created by integration tests",
    )
    return milestone_input


@pytest.fixture
def milestone(api_client, milestone_input):
    milestone = api_client.create_milestone(milestone_input)
    yield milestone
    api_client.delete_milestone(milestone.id)


@pytest.fixture
def group(api_client):
    """Get the first available group for testing."""
    groups = api_client.list_groups()
    if not groups:
        pytest.skip("No groups available")
    return groups[0]


@pytest.fixture
def task_description():
    return fake.text()


@pytest.fixture
def task_input(task_description):
    task_input = models.CreateTaskInput(
        description=task_description,
        complete=False,
    )
    return task_input


@pytest.fixture
def task(api_client, story, task_input):
    task = api_client.create_story_task(story.id, task_input)
    yield task
    api_client.delete_story_task(story.id, task.id)


@pytest.fixture
def comment_text():
    return fake.text()


@pytest.fixture
def comment_input(comment_text):
    comment_input = models.CreateCommentInput(
        text=comment_text,
    )
    return comment_input


@pytest.fixture
def comment(api_client, story, comment_input):
    comment = api_client.create_story_comment(story.id, comment_input)
    yield comment
    api_client.delete_story_comment(story.id, comment.id)


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


@pytest.mark.integration
class TestLabels:

    def test_create_label(self, api_client, label, label_input):
        assert label is not None
        assert label.name == label_input.name
        assert label.color == "#ff0000"

    def test_update_label(self, api_client, label):
        new_name = fake.word()
        label_input = models.UpdateLabelInput(
            name=new_name,
            color="#00ff00",
        )
        updated_label = api_client.update_label(label.id, label_input)
        assert updated_label.name == new_name
        assert updated_label.color == "#00ff00"


@pytest.mark.integration
class TestMilestones:

    def test_create_milestone(self, api_client, milestone, milestone_input):
        assert milestone is not None
        assert milestone.name == milestone_input.name
        assert milestone.description == "Test milestone created by integration tests"

    def test_update_milestone(self, api_client, milestone):
        new_name = fake.word()
        milestone_input = models.UpdateMilestoneInput(
            name=new_name,
        )
        updated_milestone = api_client.update_milestone(milestone.id, milestone_input)
        assert updated_milestone.name == new_name


@pytest.mark.integration
class TestTasks:

    def test_create_task(self, api_client, task, task_input):
        assert task is not None
        assert task.description == task_input.description
        assert task.complete == False

    def test_update_task(self, api_client, story, task):
        new_description = fake.text()
        task_input = models.UpdateTaskInput(
            description=new_description,
            complete=True,
        )
        updated_task = api_client.update_story_task(story.id, task.id, task_input)
        assert updated_task.description == new_description
        assert updated_task.complete == True


@pytest.mark.integration
class TestComments:

    def test_create_comment(self, api_client, comment, comment_input):
        assert comment is not None
        assert comment.text == comment_input.text

    def test_update_comment(self, api_client, story, comment):
        new_text = fake.text()
        comment_input = models.UpdateCommentInput(
            text=new_text,
        )
        updated_comment = api_client.update_story_comment(story.id, comment.id, comment_input)
        assert updated_comment.text == new_text


@pytest.mark.integration
class TestGroups:

    def test_list_groups(self, api_client, group):
        assert group is not None
        assert hasattr(group, 'id')
        assert hasattr(group, 'name')


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
