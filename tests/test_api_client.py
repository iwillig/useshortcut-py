import pytest
import requests
from datetime import datetime
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


class TestAPIClient:
    """Test the APIClient initialization and configuration."""

    def test_init_default_base_url(self):
        client = APIClient(api_token="test-token")
        assert client.base_url == "https://api.app.shortcut.com/api/v3"
        assert client.api_token == "test-token"

    def test_init_custom_base_url(self):
        client = APIClient(api_token="test-token", base_url="https://custom.url")
        assert client.base_url == "https://custom.url"

    def test_session_headers(self):
        client = APIClient(api_token="test-token")
        assert client.session.headers["Shortcut-Token"] == "test-token"
        assert (
            client.session.headers["Content-Type"] == "application/json; charset=utf-8"
        )
        assert client.session.headers["Accept"] == "application/json; charset=utf-8"
        assert client.session.headers["User-Agent"] == "useshortcut-py/0.0.1"


class TestMemberEndpoints:
    """Test Member-related endpoints."""

    def test_get_current_member(self, requests_mock, api_client, base_url):
        member_response = {
            "id": "12345678-1234-1234-1234-123456789012",
            "role": "member",
            "disabled": False,
            "state": "full",
            "group_ids": ["87654321-4321-4321-4321-210987654321"],
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "profile": {
                "id": "12345678-1234-1234-1234-123456789012",
                "mention_name": "testuser",
                "name": "Test User",
                "email_address": "test@example.com",
                "is_owner": False,
                "deactivated": False,
                "two_factor_auth_activated": True,
            },
        }

        requests_mock.get(f"{base_url}/member", json=member_response)

        member = api_client.get_current_member()

        assert isinstance(member, models.Member)
        assert member.id == "12345678-1234-1234-1234-123456789012"
        assert member.profile.mention_name == "testuser"
        assert member.profile.name == "Test User"

    def test_list_members(self, requests_mock, api_client, base_url):
        members_response = [
            {
                "id": "12345678-1234-1234-1234-123456789012",
                "role": "admin",
                "disabled": False,
                "state": "full",
                "profile": {
                    "id": "12345678-1234-1234-1234-123456789012",
                    "mention_name": "admin",
                    "name": "Admin User",
                    "email_address": "admin@example.com",
                    "is_owner": True,
                    "deactivated": False,
                },
            },
            {
                "id": "87654321-4321-4321-4321-210987654321",
                "role": "member",
                "disabled": False,
                "state": "full",
                "profile": {
                    "id": "87654321-4321-4321-4321-210987654321",
                    "mention_name": "member",
                    "name": "Member User",
                    "email_address": "member@example.com",
                    "is_owner": False,
                    "deactivated": False,
                },
            },
        ]

        requests_mock.get(f"{base_url}/members", json=members_response)

        members = api_client.list_members()

        assert len(members) == 2
        assert all(isinstance(member, models.Member) for member in members)
        assert members[0].role == "admin"
        assert members[1].role == "member"


class TestStoryEndpoints:
    """Test Story-related endpoints."""

    def test_create_story(self, requests_mock, api_client, base_url):
        story_input = models.CreateStoryParams(name="Test Story", workflow_state_id=500000)

        story_response = {
            "id": 1001,
            "name": "Test Story",
            "description": "",
            "app_url": "https://app.shortcut.com/workspace/story/1001",
            "story_type": "feature",
            "workflow_state_id": 500000,
            "workflow_id": 100,
            "project_id": None,
            "epic_id": None,
            "iteration_id": None,
            "position": 1.0,
            "archived": False,
            "started": False,
            "completed": False,
            "blocked": False,
            "blocker": False,
            "deadline": None,
            "external_id": None,
            "owner_ids": [],
            "follower_ids": [],
            "group_id": None,
            "requested_by_id": "12345678-1234-1234-1234-123456789012",
            "label_ids": [],
            "labels": [],
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "started_at": None,
            "completed_at": None,
            "moved_at": None,
            "lead_time": None,
            "cycle_time": None,
            "tasks": [],
            "comments": [],
            "files": [],
            "linked_files": [],
            "branches": [],
            "commits": [],
            "pull_requests": [],
            "story_links": [],
            "stats": {},
            "custom_fields": [],
        }

        requests_mock.post(f"{base_url}/stories", json=story_response)

        story = api_client.create_story(story_input)

        assert isinstance(story, models.Story)
        assert story.id == 1001
        assert story.name == "Test Story"
        assert story.workflow_state_id == 500000

    def test_get_story(self, requests_mock, api_client, base_url):
        story_response = {
            "id": 1001,
            "name": "Existing Story",
            "description": "Story description",
            "story_type": "bug",
            "workflow_state_id": 500001,
            "archived": False,
            "started": True,
            "completed": False,
        }

        requests_mock.get(f"{base_url}/stories/1001", json=story_response)

        story = api_client.get_story(1001)

        assert isinstance(story, models.Story)
        assert story.id == 1001
        assert story.name == "Existing Story"
        assert story.story_type == "bug"
        assert story.started is True

    def test_update_story(self, requests_mock, api_client, base_url):
        updated_story = models.Story(
            name="Updated Story Name", description="Updated description"
        )

        story_response = {
            "id": 1001,
            "name": "Updated Story Name",
            "description": "Updated description",
            "story_type": "feature",
            "workflow_state_id": 500000,
        }

        requests_mock.put(f"{base_url}/stories/1001", json=story_response)

        story = api_client.update_story(1001, updated_story)

        assert isinstance(story, models.Story)
        assert story.name == "Updated Story Name"
        assert story.description == "Updated description"

    def test_delete_story(self, requests_mock, api_client, base_url):
        requests_mock.delete(f"{base_url}/stories/1001", status_code=204)

        # Should not raise an exception
        api_client.delete_story(1001)

        # Verify the request was made
        assert requests_mock.called
        assert requests_mock.call_count == 1

    def test_search_stories(self, requests_mock, api_client, base_url):
        search_params = models.SearchInputs(query="owner:testuser")

        search_response = {
            "total": 2,
            "data": [
                {"id": 1001, "name": "First Story", "story_type": "feature"},
                {"id": 1002, "name": "Second Story", "story_type": "bug"},
            ],
            "next": None,
        }

        requests_mock.get(f"{base_url}/search/stories", json=search_response)

        result = api_client.search_stories(search_params)

        assert isinstance(result, models.SearchStoryResult)
        assert result.total == 2
        assert len(result.data) == 2
        assert result.data[0].id == 1001
        assert result.data[1].id == 1002


class TestEpicEndpoints:
    """Test Epic-related endpoints."""

    def test_list_epics(self, requests_mock, api_client, base_url):
        epics_response = [
            {
                "id": 2001,
                "global_id": "ep-2001",
                "name": "First Epic",
                "description": "Epic description",
                "epic_state_id": 100,
                "archived": False,
                "started": True,
                "completed": False,
                "project_ids": [1, 2],
            },
            {
                "id": 2002,
                "global_id": "ep-2002",
                "name": "Second Epic",
                "description": "",
                "epic_state_id": 101,
                "archived": False,
                "started": False,
                "completed": False,
                "project_ids": [3],
            },
        ]

        requests_mock.get(f"{base_url}/epics", json=epics_response)

        epics = api_client.list_epics()

        assert len(epics) == 2
        assert all(isinstance(epic, models.Epic) for epic in epics)
        assert epics[0].id == 2001
        assert epics[0].name == "First Epic"
        assert epics[1].id == 2002

    def test_create_epic(self, requests_mock, api_client, base_url):
        epic_input = models.EpicInput(name="New Epic")

        epic_response = {
            "id": 2003,
            "global_id": "ep-2003",
            "name": "New Epic",
            "description": "",
            "epic_state_id": 100,
            "archived": False,
            "started": False,
            "completed": False,
            "project_ids": [],
        }

        requests_mock.post(f"{base_url}/epics", json=epic_response)

        epic = api_client.create_epic(epic_input)

        assert isinstance(epic, models.Epic)
        assert epic.id == 2003
        assert epic.name == "New Epic"

    def test_delete_epic(self, requests_mock, api_client, base_url):
        requests_mock.delete(f"{base_url}/epics/2001", status_code=204)

        # Should not raise an exception
        api_client.delete_epic(2001)

        assert requests_mock.called


class TestProjectEndpoints:
    """Test Project-related endpoints."""

    def test_list_projects(self, requests_mock, api_client, base_url):
        projects_response = [
            {
                "id": 3001,
                "name": "Backend Project",
                "description": "Backend services",
                "abbreviation": "BE",
                "archived": False,
                "color": "#ff0000",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
            },
            {
                "id": 3002,
                "name": "Frontend Project",
                "description": "Frontend application",
                "abbreviation": "FE",
                "archived": False,
                "color": "#00ff00",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
            },
        ]

        requests_mock.get(f"{base_url}/projects", json=projects_response)

        projects = api_client.list_projects()

        assert len(projects) == 2
        assert all(isinstance(project, models.Project) for project in projects)
        assert projects[0].id == 3001
        assert projects[0].name == "Backend Project"


class TestWorkflowEndpoints:
    """Test Workflow-related endpoints."""

    def test_list_workflows(self, requests_mock, api_client, base_url):
        workflows_response = [
            {
                "id": 100,
                "name": "Default Workflow",
                "description": "Default workflow for stories",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "default_state_id": 500000,
                "states": [
                    {
                        "id": 500000,
                        "global_id": "wf-state-500000",
                        "name": "Unstarted",
                        "type": "unstarted",
                        "position": 0,
                        "description": "",
                        "verb": "start",
                        "num_stories": 0,
                        "num_story_templates": 0,
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-01T00:00:00Z",
                        "entity_type": "workflow-state",
                    },
                    {
                        "id": 500001,
                        "global_id": "wf-state-500001",
                        "name": "Started",
                        "type": "started",
                        "position": 1,
                        "description": "",
                        "verb": "continue",
                        "num_stories": 0,
                        "num_story_templates": 0,
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-01T00:00:00Z",
                        "entity_type": "workflow-state",
                    },
                ],
            }
        ]

        requests_mock.get(f"{base_url}/workflows", json=workflows_response)

        workflows = api_client.list_workflows()

        assert len(workflows) == 1
        assert isinstance(workflows[0], models.Workflow)
        assert workflows[0].id == 100
        assert workflows[0].name == "Default Workflow"
        assert workflows[0].default_state_id == 500000

    def test_get_workflow(self, requests_mock, api_client, base_url):
        workflow_response = {
            "id": 100,
            "name": "Default Workflow",
            "description": "Default workflow for stories",
            "default_state_id": 500000,
            "states": [
                {
                    "id": 500000,
                    "global_id": "wf-state-500000",
                    "name": "Unstarted",
                    "type": "unstarted",
                    "position": 0,
                    "description": "",
                    "verb": "start",
                    "num_stories": 0,
                    "num_story_templates": 0,
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:00:00Z",
                    "entity_type": "workflow-state",
                }
            ],
        }

        requests_mock.get(f"{base_url}/workflows/100", json=workflow_response)

        workflow = api_client.get_workflow("100")

        assert isinstance(workflow, models.Workflow)
        assert workflow.id == 100
        assert len(workflow.states) == 1


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_404_error(self, requests_mock, api_client, base_url):
        requests_mock.get(
            f"{base_url}/stories/9999",
            status_code=404,
            json={
                "error": "Resource not found",
                "message": "Story with ID 9999 not found",
            },
        )

        with pytest.raises(requests.exceptions.HTTPError):
            api_client.get_story(9999)

    def test_400_error(self, requests_mock, api_client, base_url):
        requests_mock.post(
            f"{base_url}/stories",
            status_code=400,
            json={"error": "Bad Request", "message": "Missing required field: name"},
        )

        with pytest.raises(requests.exceptions.HTTPError):
            api_client.create_story(
                models.CreateStoryParams(name="", workflow_state_id=500000)
            )

    def test_401_unauthorized(self, requests_mock, api_client, base_url):
        requests_mock.get(
            f"{base_url}/member",
            status_code=401,
            json={"error": "Unauthorized", "message": "Invalid API token"},
        )

        with pytest.raises(requests.exceptions.HTTPError):
            api_client.get_current_member()
