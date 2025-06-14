"""Integration tests for the Shortcut API client.

These tests require a valid SHORTCUT_TOKEN environment variable.
"""

import os
import pytest
import time
from datetime import datetime
from typing import List, Set

from useshortcut.client import APIClient
import useshortcut.models as models


# Test data prefix to identify test-created resources
TEST_PREFIX = "TEST_INTEGRATION_"
TEST_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


class TestDataTracker:
    """Track created resources for cleanup."""

    def __init__(self):
        self.stories: Set[int] = set()
        self.epics: Set[int] = set()
        self.projects: Set[int] = set()
        self.labels: Set[int] = set()
        self.iterations: Set[int] = set()
        self.categories: Set[int] = set()
        self.milestones: Set[int] = set()
        self.objectives: Set[int] = set()

    def add_story(self, story_id: int):
        self.stories.add(story_id)

    def add_epic(self, epic_id: int):
        self.epics.add(epic_id)

    def add_project(self, project_id: int):
        self.projects.add(project_id)

    def add_label(self, label_id: int):
        self.labels.add(label_id)

    def add_iteration(self, iteration_id: int):
        self.iterations.add(iteration_id)

    def add_category(self, category_id: int):
        self.categories.add(category_id)

    def add_milestone(self, milestone_id: int):
        self.milestones.add(milestone_id)

    def add_objective(self, objective_id: int):
        self.objectives.add(objective_id)


@pytest.fixture(scope="session")
def api_client():
    """Create an API client instance."""
    token = os.environ.get("SHORTCUT_API_TOKEN")
    if not token:
        pytest.skip("SHORTCUT_API_TOKEN environment variable not set")
    return APIClient(api_token=token)


@pytest.fixture(scope="session")
def test_data_tracker():
    """Create a test data tracker for cleanup."""
    return TestDataTracker()


@pytest.fixture(scope="session")
def default_workflow_state_id(api_client):
    """Get a default workflow state ID for story creation."""
    workflows = api_client.list_workflows()
    if not workflows:
        pytest.skip("No workflows available")

    # Get the first workflow's default state
    workflow = api_client.get_workflow(workflows[0].id)
    return workflow.default_state_id


@pytest.fixture(scope="session")
def test_project(api_client, test_data_tracker):
    """Create a test project for stories."""
    project_name = f"{TEST_PREFIX}Project_{TEST_TIMESTAMP}"
    project = api_client.create_project(
        models.CreateProjectInput(
            name=project_name, description="Integration test project"
        )
    )
    test_data_tracker.add_project(project.id)
    return project


@pytest.fixture(scope="session", autouse=True)
def cleanup(api_client, test_data_tracker):
    """Clean up test data after all tests."""
    yield

    # Clean up in reverse order of dependencies
    errors = []

    # Delete stories
    for story_id in test_data_tracker.stories:
        try:
            api_client.delete_story(story_id)
        except Exception as e:
            errors.append(f"Failed to delete story {story_id}: {e}")

    # Delete epics
    for epic_id in test_data_tracker.epics:
        try:
            api_client.delete_epic(epic_id)
        except Exception as e:
            errors.append(f"Failed to delete epic {epic_id}: {e}")

    # Delete milestones
    for milestone_id in test_data_tracker.milestones:
        try:
            api_client.delete_milestone(milestone_id)
        except Exception as e:
            errors.append(f"Failed to delete milestone {milestone_id}: {e}")

    # Delete objectives
    for objective_id in test_data_tracker.objectives:
        try:
            api_client.delete_objective(objective_id)
        except Exception as e:
            errors.append(f"Failed to delete objective {objective_id}: {e}")

    # Delete iterations
    for iteration_id in test_data_tracker.iterations:
        try:
            api_client.delete_iteration(iteration_id)
        except Exception as e:
            errors.append(f"Failed to delete iteration {iteration_id}: {e}")

    # Delete projects
    for project_id in test_data_tracker.projects:
        try:
            api_client.delete_project(project_id)
        except Exception as e:
            errors.append(f"Failed to delete project {project_id}: {e}")

    # Delete labels
    for label_id in test_data_tracker.labels:
        try:
            api_client.delete_label(label_id)
        except Exception as e:
            errors.append(f"Failed to delete label {label_id}: {e}")

    # Delete categories
    for category_id in test_data_tracker.categories:
        try:
            api_client.delete_category(category_id)
        except Exception as e:
            errors.append(f"Failed to delete category {category_id}: {e}")

    if errors:
        print(f"\nCleanup errors:\n" + "\n".join(errors))


@pytest.mark.integration
class TestAPIClientConnection:
    """Test basic API client connectivity."""

    def test_get_current_member(self, api_client):
        """Test getting the current authenticated member."""
        member = api_client.get_current_member()
        assert member is not None
        assert hasattr(member, "id")
        assert hasattr(member, "mention_name")
        assert hasattr(member, "profile")


@pytest.mark.integration
class TestWorkflows:
    """Test workflow-related operations."""

    def test_list_workflows(self, api_client):
        """Test listing workflows."""
        workflows = api_client.list_workflows()
        assert isinstance(workflows, list)
        assert len(workflows) > 0

        # Check workflow structure
        workflow = workflows[0]
        assert hasattr(workflow, "id")
        assert hasattr(workflow, "name")
        assert hasattr(workflow, "default_state_id")

    def test_get_workflow(self, api_client):
        """Test getting a specific workflow."""
        workflows = api_client.list_workflows()
        workflow_id = workflows[0].id

        workflow = api_client.get_workflow(workflow_id)
        assert workflow is not None
        assert workflow.id == workflow_id
        assert hasattr(workflow, "states")
        assert len(workflow.states) > 0

        # Check workflow state structure
        state = workflow.states[0]
        assert hasattr(state, "id")
        assert hasattr(state, "name")
        assert hasattr(state, "type")

    def test_get_epic_workflow(self, api_client):
        """Test getting the epic workflow."""
        epic_workflow = api_client.get_epic_workflow()
        assert epic_workflow is not None
        assert hasattr(epic_workflow, "id")
        assert hasattr(epic_workflow, "default_epic_state_id")
        assert hasattr(epic_workflow, "epic_states")


@pytest.mark.integration
class TestStories:
    """Test story CRUD operations."""

    def test_create_story(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test creating a story."""
        story_name = f"{TEST_PREFIX}Story_{TEST_TIMESTAMP}"
        story_input = models.CreateStoryParams(
            name=story_name,
            description="Test story created by integration tests",
            workflow_state_id=default_workflow_state_id,
            story_type="feature",
        )

        story = api_client.create_story(story_input)
        test_data_tracker.add_story(story.id)

        assert story is not None
        assert story.name == story_name
        assert story.description == "Test story created by integration tests"
        assert story.workflow_state_id == default_workflow_state_id
        assert story.story_type == "feature"

    def test_get_story(self, api_client, default_workflow_state_id, test_data_tracker):
        """Test getting a specific story."""
        # Create a story first
        story_name = f"{TEST_PREFIX}GetStory_{TEST_TIMESTAMP}"
        created_story = api_client.create_story(
            models.CreateStoryParams(
                name=story_name, workflow_state_id=default_workflow_state_id
            )
        )
        test_data_tracker.add_story(created_story.id)

        # Get the story
        story = api_client.get_story(created_story.id)
        assert story is not None
        assert story.id == created_story.id
        assert story.name == story_name

    def test_update_story(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test updating a story."""
        # Create a story first
        original_name = f"{TEST_PREFIX}UpdateStory_Original_{TEST_TIMESTAMP}"
        story = api_client.create_story(
            models.CreateStoryParams(
                name=original_name, workflow_state_id=default_workflow_state_id
            )
        )
        test_data_tracker.add_story(story.id)

        # Update the story
        updated_name = f"{TEST_PREFIX}UpdateStory_Updated_{TEST_TIMESTAMP}"
        update_input = models.UpdateStoryInput(
            name=updated_name, description="Updated description"
        )

        updated_story = api_client.update_story(story.id, update_input)
        assert updated_story is not None
        assert updated_story.name == updated_name
        assert updated_story.description == "Updated description"

    def test_delete_story(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test deleting a story."""
        # Create a story first
        story_name = f"{TEST_PREFIX}DeleteStory_{TEST_TIMESTAMP}"
        story = api_client.create_story(
            models.CreateStoryParams(
                name=story_name, workflow_state_id=default_workflow_state_id
            )
        )
        story_id = story.id

        # Delete the story
        api_client.delete_story(story_id)

        # Verify it's deleted by trying to get it
        with pytest.raises(Exception):
            api_client.get_story(story_id)

    def test_search_stories(self, api_client):
        """Test searching for stories."""
        current_member = api_client.get_current_member()
        search_params = models.SearchInputs(
            query=f"owner:{current_member.mention_name}", page_size=10
        )

        result = api_client.search_stories(search_params)
        assert result is not None
        assert hasattr(result, "data")
        assert isinstance(result.data, list)

        # If there are results, check the structure
        if result.data:
            story = result.data[0]
            assert hasattr(story, "id")
            assert hasattr(story, "name")
            assert hasattr(story, "workflow_state_id")

    def test_story_with_labels(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test creating a story with labels."""
        # Create a test label
        label_name = f"{TEST_PREFIX}Label_{TEST_TIMESTAMP}"
        label = api_client.create_label(
            models.CreateLabelInput(name=label_name, color="#ff0000")
        )
        test_data_tracker.add_label(label.id)

        # Create a story with the label
        story_name = f"{TEST_PREFIX}StoryWithLabel_{TEST_TIMESTAMP}"
        story = api_client.create_story(
            models.CreateStoryParams(
                name=story_name,
                workflow_state_id=default_workflow_state_id,
                label_ids=[label.id],
            )
        )
        test_data_tracker.add_story(story.id)

        assert story is not None
        assert label.id in story.label_ids

    def test_story_with_project(
        self, api_client, default_workflow_state_id, test_project, test_data_tracker
    ):
        """Test creating a story in a specific project."""
        story_name = f"{TEST_PREFIX}StoryInProject_{TEST_TIMESTAMP}"
        story = api_client.create_story(
            models.CreateStoryParams(
                name=story_name,
                workflow_state_id=default_workflow_state_id,
                project_id=test_project.id,
            )
        )
        test_data_tracker.add_story(story.id)

        assert story is not None
        assert story.project_id == test_project.id


@pytest.mark.integration
class TestEpics:
    """Test epic CRUD operations."""

    def test_list_epics(self, api_client):
        """Test listing epics."""
        epics = api_client.list_epics()
        assert isinstance(epics, list)

        # If there are epics, check the structure
        if epics:
            epic = epics[0]
            assert hasattr(epic, "id")
            assert hasattr(epic, "name")
            assert hasattr(epic, "state")

    def test_create_epic(self, api_client, test_data_tracker):
        """Test creating an epic."""
        epic_name = f"{TEST_PREFIX}Epic_{TEST_TIMESTAMP}"
        epic_input = models.CreateEpicInput(
            name=epic_name, description="Test epic created by integration tests"
        )

        epic = api_client.create_epic(epic_input)
        test_data_tracker.add_epic(epic.id)

        assert epic is not None
        assert epic.name == epic_name
        assert epic.description == "Test epic created by integration tests"

    def test_get_epic(self, api_client, test_data_tracker):
        """Test getting a specific epic."""
        # Create an epic first
        epic_name = f"{TEST_PREFIX}GetEpic_{TEST_TIMESTAMP}"
        created_epic = api_client.create_epic(models.CreateEpicInput(name=epic_name))
        test_data_tracker.add_epic(created_epic.id)

        # Get the epic
        epic = api_client.get_epic(created_epic.id)
        assert epic is not None
        assert epic.id == created_epic.id
        assert epic.name == epic_name

    def test_update_epic(self, api_client, test_data_tracker):
        """Test updating an epic."""
        # Create an epic first
        original_name = f"{TEST_PREFIX}UpdateEpic_Original_{TEST_TIMESTAMP}"
        epic = api_client.create_epic(models.CreateEpicInput(name=original_name))
        test_data_tracker.add_epic(epic.id)

        # Update the epic
        updated_name = f"{TEST_PREFIX}UpdateEpic_Updated_{TEST_TIMESTAMP}"
        update_input = models.UpdateEpicInput(
            name=updated_name, description="Updated epic description"
        )

        updated_epic = api_client.update_epic(epic.id, update_input)
        assert updated_epic is not None
        assert updated_epic.name == updated_name
        assert updated_epic.description == "Updated epic description"

    def test_delete_epic(self, api_client, test_data_tracker):
        """Test deleting an epic."""
        # Create an epic first
        epic_name = f"{TEST_PREFIX}DeleteEpic_{TEST_TIMESTAMP}"
        epic = api_client.create_epic(models.CreateEpicInput(name=epic_name))
        epic_id = epic.id

        # Delete the epic
        api_client.delete_epic(epic_id)

        # Verify it's deleted by trying to get it
        with pytest.raises(Exception):
            api_client.get_epic(epic_id)


@pytest.mark.integration
class TestProjects:
    """Test project operations."""

    def test_list_projects(self, api_client):
        """Test listing projects."""
        projects = api_client.list_projects()
        assert isinstance(projects, list)

        # Check project structure if there are projects
        if projects:
            project = projects[0]
            assert hasattr(project, "id")
            assert hasattr(project, "name")
            assert hasattr(project, "description")

    def test_create_project(self, api_client, test_data_tracker):
        """Test creating a project."""
        project_name = f"{TEST_PREFIX}CreateProject_{TEST_TIMESTAMP}"
        project_input = models.CreateProjectInput(
            name=project_name,
            description="Test project for integration tests",
            color="#0000ff",
        )

        project = api_client.create_project(project_input)
        test_data_tracker.add_project(project.id)

        assert project is not None
        assert project.name == project_name
        assert project.description == "Test project for integration tests"
        assert project.color == "#0000ff"

    def test_get_project(self, api_client, test_data_tracker):
        """Test getting a specific project."""
        # Create a project first
        project_name = f"{TEST_PREFIX}GetProject_{TEST_TIMESTAMP}"
        created_project = api_client.create_project(
            models.CreateProjectInput(name=project_name)
        )
        test_data_tracker.add_project(created_project.id)

        # Get the project
        project = api_client.get_project(created_project.id)
        assert project is not None
        assert project.id == created_project.id
        assert project.name == project_name

    def test_update_project(self, api_client, test_data_tracker):
        """Test updating a project."""
        # Create a project first
        original_name = f"{TEST_PREFIX}UpdateProject_Original_{TEST_TIMESTAMP}"
        project = api_client.create_project(
            models.CreateProjectInput(name=original_name)
        )
        test_data_tracker.add_project(project.id)

        # Update the project
        updated_name = f"{TEST_PREFIX}UpdateProject_Updated_{TEST_TIMESTAMP}"
        update_input = models.UpdateProjectInput(
            name=updated_name, description="Updated project description"
        )

        updated_project = api_client.update_project(project.id, update_input)
        assert updated_project is not None
        assert updated_project.name == updated_name
        assert updated_project.description == "Updated project description"


@pytest.mark.integration
class TestLabels:
    """Test label operations."""

    def test_list_labels(self, api_client):
        """Test listing labels."""
        labels = api_client.list_labels()
        assert isinstance(labels, list)

        # Check label structure if there are labels
        if labels:
            label = labels[0]
            assert hasattr(label, "id")
            assert hasattr(label, "name")
            assert hasattr(label, "color")

    def test_create_label(self, api_client, test_data_tracker):
        """Test creating a label."""
        label_name = f"{TEST_PREFIX}Label_{TEST_TIMESTAMP}"
        label_input = models.CreateLabelInput(
            name=label_name,
            color="#00ff00",
            description="Test label for integration tests",
        )

        label = api_client.create_label(label_input)
        test_data_tracker.add_label(label.id)

        assert label is not None
        assert label.name == label_name
        assert label.color == "#00ff00"
        assert label.description == "Test label for integration tests"

    def test_get_label(self, api_client, test_data_tracker):
        """Test getting a specific label."""
        # Create a label first
        label_name = f"{TEST_PREFIX}GetLabel_{TEST_TIMESTAMP}"
        created_label = api_client.create_label(
            models.CreateLabelInput(name=label_name, color="#ff00ff")
        )
        test_data_tracker.add_label(created_label.id)

        # Get the label
        label = api_client.get_label(created_label.id)
        assert label is not None
        assert label.id == created_label.id
        assert label.name == label_name

    def test_update_label(self, api_client, test_data_tracker):
        """Test updating a label."""
        # Create a label first
        original_name = f"{TEST_PREFIX}UpdateLabel_Original_{TEST_TIMESTAMP}"
        label = api_client.create_label(
            models.CreateLabelInput(name=original_name, color="#000000")
        )
        test_data_tracker.add_label(label.id)

        # Update the label
        updated_name = f"{TEST_PREFIX}UpdateLabel_Updated_{TEST_TIMESTAMP}"
        update_input = models.UpdateLabelInput(name=updated_name, color="#ffffff")

        updated_label = api_client.update_label(label.id, update_input)
        assert updated_label is not None
        assert updated_label.name == updated_name
        assert updated_label.color == "#ffffff"


@pytest.mark.integration
class TestCategories:
    """Test category operations."""

    def test_list_categories(self, api_client):
        """Test listing categories."""
        categories = api_client.list_categories()
        assert isinstance(categories, list)

        # Check category structure if there are categories
        if categories:
            category = categories[0]
            assert hasattr(category, "id")
            assert hasattr(category, "name")
            assert hasattr(category, "type")

    def test_create_category(self, api_client, test_data_tracker):
        """Test creating a category."""
        category_name = f"{TEST_PREFIX}Category_{TEST_TIMESTAMP}"
        category_input = models.CreateCategoryInput(
            name=category_name, type="milestone"
        )

        category = api_client.create_category(category_input)
        test_data_tracker.add_category(category.id)

        assert category is not None
        assert category.name == category_name
        assert category.type == "milestone"

    def test_get_category(self, api_client, test_data_tracker):
        """Test getting a specific category."""
        # Create a category first
        category_name = f"{TEST_PREFIX}GetCategory_{TEST_TIMESTAMP}"
        created_category = api_client.create_category(
            models.CreateCategoryInput(name=category_name, type="milestone")
        )
        test_data_tracker.add_category(created_category.id)

        # Get the category
        category = api_client.get_category(created_category.id)
        assert category is not None
        assert category.id == created_category.id
        assert category.name == category_name


@pytest.mark.integration
class TestMilestones:
    """Test milestone operations."""

    def test_list_milestones(self, api_client):
        """Test listing milestones."""
        milestones = api_client.list_milestones()
        assert isinstance(milestones, list)

        # Check milestone structure if there are milestones
        if milestones:
            milestone = milestones[0]
            assert hasattr(milestone, "id")
            assert hasattr(milestone, "name")
            assert hasattr(milestone, "state")

    def test_create_milestone(self, api_client, test_data_tracker):
        """Test creating a milestone."""
        # First create a category for the milestone
        category_name = f"{TEST_PREFIX}MilestoneCategory_{TEST_TIMESTAMP}"
        category = api_client.create_category(
            models.CreateCategoryInput(name=category_name, type="milestone")
        )
        test_data_tracker.add_category(category.id)

        milestone_name = f"{TEST_PREFIX}Milestone_{TEST_TIMESTAMP}"
        milestone_input = models.CreateMilestoneInput(
            name=milestone_name,
            description="Test milestone for integration tests",
            state="in progress",
            categories=[models.CreateCategoryInput(id=category.id)],
        )

        milestone = api_client.create_milestone(milestone_input)
        test_data_tracker.add_milestone(milestone.id)

        assert milestone is not None
        assert milestone.name == milestone_name
        assert milestone.description == "Test milestone for integration tests"
        assert milestone.state == "in progress"

    def test_get_milestone(self, api_client, test_data_tracker):
        """Test getting a specific milestone."""
        # Create a milestone first
        milestone_name = f"{TEST_PREFIX}GetMilestone_{TEST_TIMESTAMP}"
        created_milestone = api_client.create_milestone(
            models.CreateMilestoneInput(name=milestone_name, state="to do")
        )
        test_data_tracker.add_milestone(created_milestone.id)

        # Get the milestone
        milestone = api_client.get_milestone(created_milestone.id)
        assert milestone is not None
        assert milestone.id == created_milestone.id
        assert milestone.name == milestone_name

    def test_update_milestone(self, api_client, test_data_tracker):
        """Test updating a milestone."""
        # Create a milestone first
        original_name = f"{TEST_PREFIX}UpdateMilestone_Original_{TEST_TIMESTAMP}"
        milestone = api_client.create_milestone(
            models.CreateMilestoneInput(name=original_name, state="to do")
        )
        test_data_tracker.add_milestone(milestone.id)

        # Update the milestone
        updated_name = f"{TEST_PREFIX}UpdateMilestone_Updated_{TEST_TIMESTAMP}"
        update_input = models.UpdateMilestoneInput(name=updated_name, state="done")

        updated_milestone = api_client.update_milestone(milestone.id, update_input)
        assert updated_milestone is not None
        assert updated_milestone.name == updated_name
        assert updated_milestone.state == "done"


@pytest.mark.integration
class TestIterations:
    """Test iteration operations."""

    def test_list_iterations(self, api_client):
        """Test listing iterations."""
        iterations = api_client.list_iterations()
        assert isinstance(iterations, list)

        # Check iteration structure if there are iterations
        if iterations:
            iteration = iterations[0]
            assert hasattr(iteration, "id")
            assert hasattr(iteration, "name")
            assert hasattr(iteration, "status")

    def test_create_iteration(self, api_client, test_data_tracker):
        """Test creating an iteration."""
        iteration_name = f"{TEST_PREFIX}Iteration_{TEST_TIMESTAMP}"
        iteration_input = models.CreateIterationInput(
            name=iteration_name,
            description="Test iteration for integration tests",
            start_date="2024-01-01",
            end_date="2024-01-14",
        )

        iteration = api_client.create_iteration(iteration_input)
        test_data_tracker.add_iteration(iteration.id)

        assert iteration is not None
        assert iteration.name == iteration_name
        assert iteration.description == "Test iteration for integration tests"

    def test_get_iteration(self, api_client, test_data_tracker):
        """Test getting a specific iteration."""
        # Create an iteration first
        iteration_name = f"{TEST_PREFIX}GetIteration_{TEST_TIMESTAMP}"
        created_iteration = api_client.create_iteration(
            models.CreateIterationInput(
                name=iteration_name, start_date="2024-02-01", end_date="2024-02-14"
            )
        )
        test_data_tracker.add_iteration(created_iteration.id)

        # Get the iteration
        iteration = api_client.get_iteration(created_iteration.id)
        assert iteration is not None
        assert iteration.id == created_iteration.id
        assert iteration.name == iteration_name

    def test_update_iteration(self, api_client, test_data_tracker):
        """Test updating an iteration."""
        # Create an iteration first
        original_name = f"{TEST_PREFIX}UpdateIteration_Original_{TEST_TIMESTAMP}"
        iteration = api_client.create_iteration(
            models.CreateIterationInput(
                name=original_name, start_date="2024-03-01", end_date="2024-03-14"
            )
        )
        test_data_tracker.add_iteration(iteration.id)

        # Update the iteration
        updated_name = f"{TEST_PREFIX}UpdateIteration_Updated_{TEST_TIMESTAMP}"
        update_input = models.UpdateIterationInput(
            name=updated_name, description="Updated iteration description"
        )

        updated_iteration = api_client.update_iteration(iteration.id, update_input)
        assert updated_iteration is not None
        assert updated_iteration.name == updated_name
        assert updated_iteration.description == "Updated iteration description"


@pytest.mark.integration
class TestObjectives:
    """Test objective operations."""

    def test_list_objectives(self, api_client):
        """Test listing objectives."""
        objectives = api_client.list_objectives()
        assert isinstance(objectives, list)

        # Check objective structure if there are objectives
        if objectives:
            objective = objectives[0]
            assert hasattr(objective, "id")
            assert hasattr(objective, "name")
            assert hasattr(objective, "state")


@pytest.mark.integration
class TestMembers:
    """Test member operations."""

    def test_list_members(self, api_client):
        """Test listing members."""
        members = api_client.list_members()
        assert isinstance(members, list)
        assert len(members) > 0  # There should be at least the current member

        # Check member structure
        member = members[0]
        assert hasattr(member, "id")
        assert hasattr(member, "profile")
        assert hasattr(member, "mention_name")
        assert hasattr(member.profile, "name")
        assert hasattr(member.profile, "email_address")

    def test_get_member(self, api_client):
        """Test getting a specific member."""
        # Get current member first
        current_member = api_client.get_current_member()

        # Get the same member by ID
        member = api_client.get_member(current_member.id)
        assert member is not None
        assert member.id == current_member.id
        assert member.mention_name == current_member.mention_name


@pytest.mark.integration
class TestGroups:
    """Test group operations."""

    def test_list_groups(self, api_client):
        """Test listing groups."""
        groups = api_client.list_groups()
        assert isinstance(groups, list)

        # Check group structure if there are groups
        if groups:
            group = groups[0]
            assert hasattr(group, "id")
            assert hasattr(group, "name")
            assert hasattr(group, "member_ids")


@pytest.mark.integration
class TestSearchAndPagination:
    """Test search functionality and pagination."""

    def test_search_with_pagination(self, api_client):
        """Test searching with pagination parameters."""
        search_params = models.SearchInputs(query="type:story", page_size=5)

        result = api_client.search_stories(search_params)
        assert result is not None
        assert hasattr(result, "data")
        assert hasattr(result, "next_page_token")

        # If there are more results, test pagination
        if result.next_page_token:
            next_search_params = models.SearchInputs(
                query="type:story", page_size=5, next_page_token=result.next_page_token
            )

            next_result = api_client.search_stories(next_search_params)
            assert next_result is not None
            assert hasattr(next_result, "data")

    def test_search_epics(self, api_client):
        """Test searching for epics."""
        search_params = models.SearchInputs(query="type:epic", page_size=10)

        result = api_client.search_epics(search_params)
        assert result is not None
        assert hasattr(result, "data")
        assert isinstance(result.data, list)

    def test_list_stories_paginated(
        self, api_client, test_project, default_workflow_state_id, test_data_tracker
    ):
        """Test listing stories for a project with pagination."""
        # Create a few stories for the test
        for i in range(3):
            story = api_client.create_story(
                models.CreateStoryParams(
                    name=f"{TEST_PREFIX}PaginatedStory_{i}_{TEST_TIMESTAMP}",
                    workflow_state_id=default_workflow_state_id,
                    project_id=test_project.id,
                )
            )
            test_data_tracker.add_story(story.id)

        # Small delay to ensure stories are indexed
        time.sleep(1)

        # List stories for the project
        stories = api_client.list_stories_for_project(test_project.id, limit=2)
        assert isinstance(stories, list)
        # We created 3 stories, but limited to 2
        assert len(stories) <= 2


@pytest.mark.integration
class TestFiles:
    """Test file operations."""

    def test_list_files(self, api_client):
        """Test listing files."""
        files = api_client.list_files()
        assert isinstance(files, list)

        # Check file structure if there are files
        if files:
            file = files[0]
            assert hasattr(file, "id")
            assert hasattr(file, "name")
            assert hasattr(file, "size")

    def test_list_linked_files(self, api_client):
        """Test listing linked files."""
        linked_files = api_client.list_linked_files()
        assert isinstance(linked_files, list)

        # Check linked file structure if there are linked files
        if linked_files:
            linked_file = linked_files[0]
            assert hasattr(linked_file, "id")
            assert hasattr(linked_file, "name")
            assert hasattr(linked_file, "url")


@pytest.mark.integration
class TestTasks:
    """Test task operations within stories."""

    def test_create_story_task(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test creating a task within a story."""
        # Create a story first
        story_name = f"{TEST_PREFIX}StoryWithTask_{TEST_TIMESTAMP}"
        story = api_client.create_story(
            models.CreateStoryParams(
                name=story_name, workflow_state_id=default_workflow_state_id
            )
        )
        test_data_tracker.add_story(story.id)

        # Create a task
        task_input = models.CreateTaskInput(
            description="Test task description", complete=False
        )

        task = api_client.create_story_task(story.id, task_input)
        assert task is not None
        assert task.description == "Test task description"
        assert task.complete is False
        assert task.story_id == story.id

    def test_get_story_task(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test getting a specific task."""
        # Create a story and task first
        story = api_client.create_story(
            models.CreateStoryParams(
                name=f"{TEST_PREFIX}StoryGetTask_{TEST_TIMESTAMP}",
                workflow_state_id=default_workflow_state_id,
            )
        )
        test_data_tracker.add_story(story.id)

        task = api_client.create_story_task(
            story.id, models.CreateTaskInput(description="Task to retrieve")
        )

        # Get the task
        retrieved_task = api_client.get_story_task(story.id, task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.description == "Task to retrieve"

    def test_update_story_task(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test updating a task."""
        # Create a story and task first
        story = api_client.create_story(
            models.CreateStoryParams(
                name=f"{TEST_PREFIX}StoryUpdateTask_{TEST_TIMESTAMP}",
                workflow_state_id=default_workflow_state_id,
            )
        )
        test_data_tracker.add_story(story.id)

        task = api_client.create_story_task(
            story.id,
            models.CreateTaskInput(description="Original task", complete=False),
        )

        # Update the task
        update_input = models.UpdateTaskInput(description="Updated task", complete=True)

        updated_task = api_client.update_story_task(story.id, task.id, update_input)
        assert updated_task is not None
        assert updated_task.description == "Updated task"
        assert updated_task.complete is True

    def test_delete_story_task(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test deleting a task."""
        # Create a story and task first
        story = api_client.create_story(
            models.CreateStoryParams(
                name=f"{TEST_PREFIX}StoryDeleteTask_{TEST_TIMESTAMP}",
                workflow_state_id=default_workflow_state_id,
            )
        )
        test_data_tracker.add_story(story.id)

        task = api_client.create_story_task(
            story.id, models.CreateTaskInput(description="Task to delete")
        )

        # Delete the task
        api_client.delete_story_task(story.id, task.id)

        # Verify it's deleted by trying to get it
        with pytest.raises(Exception):
            api_client.get_story_task(story.id, task.id)


@pytest.mark.integration
class TestComments:
    """Test comment operations on stories."""

    def test_create_story_comment(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test creating a comment on a story."""
        # Create a story first
        story_name = f"{TEST_PREFIX}StoryWithComment_{TEST_TIMESTAMP}"
        story = api_client.create_story(
            models.CreateStoryParams(
                name=story_name, workflow_state_id=default_workflow_state_id
            )
        )
        test_data_tracker.add_story(story.id)

        # Create a comment
        comment_input = models.CreateCommentInput(text="This is a test comment")

        comment = api_client.create_story_comment(story.id, comment_input)
        assert comment is not None
        assert comment.text == "This is a test comment"
        assert comment.story_id == story.id

    def test_get_story_comment(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test getting a specific comment."""
        # Create a story and comment first
        story = api_client.create_story(
            models.CreateStoryParams(
                name=f"{TEST_PREFIX}StoryGetComment_{TEST_TIMESTAMP}",
                workflow_state_id=default_workflow_state_id,
            )
        )
        test_data_tracker.add_story(story.id)

        comment = api_client.create_story_comment(
            story.id, models.CreateCommentInput(text="Comment to retrieve")
        )

        # Get the comment
        retrieved_comment = api_client.get_story_comment(story.id, comment.id)
        assert retrieved_comment is not None
        assert retrieved_comment.id == comment.id
        assert retrieved_comment.text == "Comment to retrieve"

    def test_update_story_comment(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test updating a comment."""
        # Create a story and comment first
        story = api_client.create_story(
            models.CreateStoryParams(
                name=f"{TEST_PREFIX}StoryUpdateComment_{TEST_TIMESTAMP}",
                workflow_state_id=default_workflow_state_id,
            )
        )
        test_data_tracker.add_story(story.id)

        comment = api_client.create_story_comment(
            story.id, models.CreateCommentInput(text="Original comment")
        )

        # Update the comment
        update_input = models.UpdateCommentInput(text="Updated comment")

        updated_comment = api_client.update_story_comment(
            story.id, comment.id, update_input
        )
        assert updated_comment is not None
        assert updated_comment.text == "Updated comment"

    def test_delete_story_comment(
        self, api_client, default_workflow_state_id, test_data_tracker
    ):
        """Test deleting a comment."""
        # Create a story and comment first
        story = api_client.create_story(
            models.CreateStoryParams(
                name=f"{TEST_PREFIX}StoryDeleteComment_{TEST_TIMESTAMP}",
                workflow_state_id=default_workflow_state_id,
            )
        )
        test_data_tracker.add_story(story.id)

        comment = api_client.create_story_comment(
            story.id, models.CreateCommentInput(text="Comment to delete")
        )

        # Delete the comment
        api_client.delete_story_comment(story.id, comment.id)

        # Note: Shortcut API might still return deleted comments with a flag
        # so we can't reliably test with a get request


@pytest.mark.integration
class TestCustomFields:
    """Test custom field operations."""

    def test_list_custom_fields(self, api_client):
        """Test listing custom fields."""
        custom_fields = api_client.list_custom_fields()
        assert isinstance(custom_fields, list)

        # Check custom field structure if there are custom fields
        if custom_fields:
            custom_field = custom_fields[0]
            assert hasattr(custom_field, "id")
            assert hasattr(custom_field, "name")
            assert hasattr(custom_field, "field_type")

    def test_get_custom_field(self, api_client):
        """Test getting a specific custom field."""
        # First list custom fields to get an ID
        custom_fields = api_client.list_custom_fields()
        if not custom_fields:
            pytest.skip("No custom fields available")

        custom_field_id = custom_fields[0].id

        # Get the custom field
        custom_field = api_client.get_custom_field(custom_field_id)
        assert custom_field is not None
        assert custom_field.id == custom_field_id


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
