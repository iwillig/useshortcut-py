import pytest

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


class TestLabelEndpoints:
    """Test Label-related endpoints."""

    def test_list_labels(self, requests_mock, api_client, base_url):
        labels_response = [
            {
                "id": 4001,
                "global_id": "label-4001",
                "name": "bug",
                "color": "#ff0000",
                "archived": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "external_id": None,
                "stats": {},
                "entity_type": "label",
                "app_url": "https://app.shortcut.com/workspace/label/4001",
                "description": None,
            },
            {
                "id": 4002,
                "global_id": "label-4002",
                "name": "feature",
                "color": "#00ff00",
                "archived": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "external_id": None,
                "stats": {},
                "entity_type": "label",
                "app_url": "https://app.shortcut.com/workspace/label/4002",
                "description": None,
            },
        ]

        requests_mock.get(f"{base_url}/labels", json=labels_response)

        labels = api_client.list_labels()

        assert len(labels) == 2
        assert all(isinstance(label, models.Label) for label in labels)
        assert labels[0].id == 4001
        assert labels[0].name == "bug"
        assert labels[0].color == "#ff0000"

    def test_create_label(self, requests_mock, api_client, base_url):
        label_input = models.CreateLabelInput(name="urgent", color="#ff9900")

        label_response = {
            "id": 4003,
            "global_id": "label-4003",
            "name": "urgent",
            "color": "#ff9900",
            "archived": False,
            "created_at": "2023-01-03T00:00:00Z",
            "updated_at": "2023-01-03T00:00:00Z",
            "external_id": None,
            "stats": {},
            "entity_type": "label",
            "app_url": "https://app.shortcut.com/workspace/label/4003",
            "description": None,
        }

        requests_mock.post(f"{base_url}/labels", json=label_response)

        label = api_client.create_label(label_input)

        assert isinstance(label, models.Label)
        assert label.id == 4003
        assert label.name == "urgent"
        assert label.color == "#ff9900"

    def test_delete_label(self, requests_mock, api_client, base_url):
        requests_mock.delete(f"{base_url}/labels/4001", status_code=204)

        api_client.delete_label(4001)
        assert requests_mock.called


class TestIterationEndpoints:
    """Test Iteration-related endpoints."""

    def test_list_iterations(self, requests_mock, api_client, base_url):
        iterations_response = [
            {
                "id": 5001,
                "name": "Sprint 1",
                "global_id": "spr-5001",
                "start_date": "2023-01-01T00:00:00Z",
                "end_date": "2023-01-14T00:00:00Z",
                "status": "started",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "app_url": "https://app.shortcut.com/workspace/iteration/5001",
                "labels": [],
                "follower_ids": [],
                "group_ids": [],
                "entity_type": "iteration",
                "stats": {},
            },
            {
                "id": 5002,
                "name": "Sprint 2",
                "global_id": "spr-5002",
                "start_date": "2023-01-15T00:00:00Z",
                "end_date": "2023-01-28T00:00:00Z",
                "status": "unstarted",
            },
        ]

        requests_mock.get(f"{base_url}/iterations", json=iterations_response)

        iterations = api_client.list_iterations()

        assert len(iterations) == 2
        assert all(isinstance(iteration, models.Iteration) for iteration in iterations)
        assert iterations[0].id == 5001
        assert iterations[0].name == "Sprint 1"
        assert iterations[0].status == "started"

    def test_create_iteration(self, requests_mock, api_client, base_url):
        iteration_input = models.CreateIterationInput(
            name="Sprint 3", start_date="2023-01-29", end_date="2023-02-11"
        )

        iteration_response = {
            "id": 5003,
            "name": "Sprint 3",
            "global_id": "spr-5003",
            "start_date": "2023-01-29T00:00:00Z",
            "end_date": "2023-02-11T00:00:00Z",
            "status": "unstarted",
        }

        requests_mock.post(f"{base_url}/iterations", json=iteration_response)

        iteration = api_client.create_iteration(iteration_input)

        assert isinstance(iteration, models.Iteration)
        assert iteration.id == 5003
        assert iteration.name == "Sprint 3"


class TestGroupEndpoints:
    """Test Group-related endpoints."""

    def test_list_groups(self, requests_mock, api_client, base_url):
        groups_response = [
            {
                "id": "12345678-1234-1234-1234-123456789012",
                "global_id": "grp-12345678",
                "name": "Engineering",
                "mention_name": "engineering",
                "description": "Engineering team",
                "archived": False,
                "color": "#0066cc",
                "color_key": "blue",
                "workflow_ids": [100],
                "member_ids": ["11111111-1111-1111-1111-111111111111"],
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "entity_type": "group",
                "app_url": "https://app.shortcut.com/workspace/group/12345678",
                "num_stories": 0,
                "num_stories_started": 0,
                "num_stories_backlog": 0,
                "num_epics_started": 0,
                "display_icon": None,
            },
            {
                "id": "87654321-4321-4321-4321-210987654321",
                "global_id": "grp-87654321",
                "name": "Product",
                "mention_name": "product",
                "description": "Product team",
                "archived": False,
                "color": "#00cc66",
                "color_key": "green",
                "workflow_ids": [100],
                "member_ids": [],
                "entity_type": "group",
                "app_url": "https://app.shortcut.com/workspace/group/87654321",
                "num_stories": 0,
                "num_stories_started": 0,
                "num_stories_backlog": 0,
                "num_epics_started": 0,
                "display_icon": None,
            },
        ]

        requests_mock.get(f"{base_url}/groups", json=groups_response)

        groups = api_client.list_groups()

        assert len(groups) == 2
        assert all(isinstance(group, models.Group) for group in groups)
        assert groups[0].name == "Engineering"
        assert groups[0].mention_name == "engineering"

    def test_create_group(self, requests_mock, api_client, base_url):
        group_input = models.CreateGroupInput(name="Design", mention_name="design")

        group_response = {
            "id": "99999999-9999-9999-9999-999999999999",
            "global_id": "grp-99999999",
            "name": "Design",
            "mention_name": "design",
            "description": "",
            "archived": False,
            "color": "#ff9900",
            "color_key": "orange",
            "workflow_ids": [],
            "member_ids": [],
            "entity_type": "group",
            "app_url": "https://app.shortcut.com/workspace/group/99999999",
            "num_stories": 0,
            "num_stories_started": 0,
            "num_stories_backlog": 0,
            "num_epics_started": 0,
            "display_icon": None,
        }

        requests_mock.post(f"{base_url}/groups", json=group_response)

        group = api_client.create_group(group_input)

        assert isinstance(group, models.Group)
        assert group.name == "Design"
        assert group.mention_name == "design"


class TestCategoryEndpoints:
    """Test Category-related endpoints."""

    def test_list_categories(self, requests_mock, api_client, base_url):
        categories_response = [
            {
                "id": 6001,
                "global_id": "cat-6001",
                "name": "Q1 Goals",
                "type": "milestone",
                "color": "#ff0000",
                "archived": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "entity_type": "category",
                "external_id": None,
            },
            {
                "id": 6002,
                "global_id": "cat-6002",
                "name": "Q2 Goals",
                "type": "milestone",
                "color": "#00ff00",
                "archived": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "entity_type": "category",
                "external_id": None,
            },
        ]

        requests_mock.get(f"{base_url}/categories", json=categories_response)

        categories = api_client.list_categories()

        assert len(categories) == 2
        assert all(isinstance(category, models.Category) for category in categories)
        assert categories[0].id == 6001
        assert categories[0].name == "Q1 Goals"

    def test_create_category(self, requests_mock, api_client, base_url):
        category_input = models.CreateCategoryInput(name="Q3 Goals")

        category_response = {
            "id": 6003,
            "global_id": "cat-6003",
            "name": "Q3 Goals",
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

        assert isinstance(category, models.Category)
        assert category.id == 6003
        assert category.name == "Q3 Goals"


class TestObjectiveEndpoints:
    """Test Objective-related endpoints."""

    def test_list_objectives(self, requests_mock, api_client, base_url):
        objectives_response = [
            {
                "id": 7001,
                "global_id": "obj-7001",
                "name": "Improve Performance",
                "description": "Improve app performance by 50%",
                "position": 1,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "completed": False,
                "archived": False,
                "entity_type": "objective",
                "stats": {},
            }
        ]

        requests_mock.get(f"{base_url}/objectives", json=objectives_response)

        objectives = api_client.list_objectives()

        assert len(objectives) == 1
        assert isinstance(objectives[0], models.Objective)
        assert objectives[0].id == 7001
        assert objectives[0].name == "Improve Performance"


class TestFileEndpoints:
    """Test File-related endpoints."""

    def test_list_files(self, requests_mock, api_client, base_url):
        files_response = [
            {
                "id": 8001,
                "name": "screenshot.png",
                "description": "UI screenshot",
                "filename": "screenshot.png",
                "content_type": "image/png",
                "size": 1024000,
                "uploader_id": "12345678-1234-1234-1234-123456789012",
                "thumbnail_url": "https://example.com/thumb.png",
                "url": "https://example.com/screenshot.png",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "entity_type": "file",
                "external_id": None,
                "story_ids": [],
                "mention_ids": [],
                "member_mention_ids": [],
                "group_mention_ids": [],
            }
        ]

        requests_mock.get(f"{base_url}/files", json=files_response)

        files = api_client.list_files()

        assert len(files) == 1
        assert isinstance(files[0], models.File)
        assert files[0].id == 8001
        assert files[0].name == "screenshot.png"

    def test_delete_file(self, requests_mock, api_client, base_url):
        requests_mock.delete(f"{base_url}/files/8001", status_code=204)

        api_client.delete_file(8001)
        assert requests_mock.called


class TestStoryLinkEndpoints:
    """Test StoryLink-related endpoints."""

    def test_create_story_link(self, requests_mock, api_client, base_url):
        story_link_input = models.StoryLinkInput(
            object_id=1001, subject_id=1002, verb="blocks"
        )

        story_link_response = [
            {
                "id": 9001,
                "object_id": 1001,
                "subject_id": 1002,
                "verb": "blocks",
                "entity_type": "story-link",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            }
        ]

        requests_mock.post(f"{base_url}/story-links", json=story_link_response)

        story_links = api_client.create_story_link(story_link_input)

        assert len(story_links) == 1
        assert isinstance(story_links[0], models.StoryLink)
        assert story_links[0].id == 9001
        assert story_links[0].verb == "blocks"


class TestRepositoryEndpoints:
    """Test Repository-related endpoints."""

    def test_list_repositories(self, requests_mock, api_client, base_url):
        repositories_response = [
            {
                "id": 10001,
                "name": "backend-api",
                "type": "github",
                "url": "https://github.com/org/backend-api",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "external_id": "12345",
                "full_name": "org/backend-api",
                "entity_type": "repository",
            }
        ]

        requests_mock.get(f"{base_url}/repositories", json=repositories_response)

        repositories = api_client.list_repositories()

        assert len(repositories) == 1
        assert isinstance(repositories[0], models.Repository)
        assert repositories[0].id == 10001
        assert repositories[0].name == "backend-api"


class TestEpicWorkflowEndpoint:
    """Test Epic Workflow endpoint."""

    def test_get_epic_workflow(self, requests_mock, api_client, base_url):
        epic_workflow_response = {
            "id": 200,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "default_epic_state_id": 600000,
            "epic_states": [
                {"id": 600000, "name": "To Do", "type": "unstarted", "position": 0},
                {"id": 600001, "name": "In Progress", "type": "started", "position": 1},
                {"id": 600002, "name": "Done", "type": "done", "position": 2},
            ],
        }

        requests_mock.get(f"{base_url}/epic-workflow", json=epic_workflow_response)

        epic_workflow = api_client.get_epic_workflow()

        assert isinstance(epic_workflow, models.EpicWorkflow)
        assert epic_workflow.id == 200
