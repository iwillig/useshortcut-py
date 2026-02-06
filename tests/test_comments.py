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
def story_comment_data():
    """Sample story comment data."""
    return {
        "id": 123,
        "text": "This is a test comment",
        "author_id": "12345678-1234-1234-1234-123456789012",
        "created_at": "2023-01-01T00:00:00Z",
        "entity_type": "story-comment",
        "story_id": 456,
        "position": 1,
        "app_url": "https://app.shortcut.com/workspace/story/456/comment/123",
        "deleted": False,
        "updated_at": "2023-01-02T00:00:00Z",
        "blocker": False,
        "unblocks_parent": False,
        "linked_to_slack": False,
        "parent_id": None,
        "external_id": None,
        "member_mention_ids": ["87654321-4321-4321-4321-210987654321"],
        "group_mention_ids": [],
        "reactions": [
            {"emoji": "👍", "permission_ids": ["user-123", "user-456"]},
            {"emoji": "🚀", "permission_ids": ["user-789"]},
        ],
    }


@pytest.fixture
def threaded_comment_data():
    """Sample threaded comment data for epics."""
    return {
        "id": 789,
        "text": "Epic discussion comment",
        "author_id": "12345678-1234-1234-1234-123456789012",
        "created_at": "2023-01-01T00:00:00Z",
        "entity_type": "epic-comment",
        "app_url": "https://app.shortcut.com/workspace/epic/111/comment/789",
        "deleted": False,
        "updated_at": "2023-01-02T00:00:00Z",
        "member_mention_ids": [],
        "group_mention_ids": [],
        "comments": [
            {
                "id": 790,
                "text": "Nested reply",
                "author_id": "87654321-4321-4321-4321-210987654321",
                "created_at": "2023-01-03T00:00:00Z",
                "entity_type": "epic-comment",
                "app_url": "https://app.shortcut.com/workspace/epic/111/comment/790",
                "deleted": False,
                "member_mention_ids": [],
                "group_mention_ids": [],
                "comments": [],
            }
        ],
    }


class TestStoryComments:
    """Test story comment endpoints."""

    def test_list_story_comments(
        self, requests_mock, api_client, base_url, story_comment_data
    ):
        """Test listing all comments for a story."""
        story_id = 456
        requests_mock.get(
            f"{base_url}/stories/{story_id}/comments", json=[story_comment_data]
        )

        comments = api_client.list_story_comments(story_id)

        assert len(comments) == 1
        assert isinstance(comments[0], models.StoryComment)
        assert comments[0].id == 123
        assert comments[0].text == "This is a test comment"
        assert comments[0].story_id == 456
        assert len(comments[0].reactions) == 2
        assert comments[0].reactions[0].emoji == "👍"

    def test_create_story_comment(
        self, requests_mock, api_client, base_url, story_comment_data
    ):
        """Test creating a new comment on a story."""
        story_id = 456
        comment_input = models.CreateStoryCommentInput(text="New comment text")

        requests_mock.post(
            f"{base_url}/stories/{story_id}/comments", json=story_comment_data
        )

        comment = api_client.create_story_comment(story_id, comment_input)

        assert isinstance(comment, models.StoryComment)
        assert comment.id == 123
        assert comment.story_id == 456

    def test_create_story_comment_with_parent(
        self, requests_mock, api_client, base_url
    ):
        """Test creating a threaded comment."""
        story_id = 456
        parent_comment_data = {
            "id": 124,
            "text": "Reply to parent",
            "author_id": "12345678-1234-1234-1234-123456789012",
            "created_at": "2023-01-01T00:00:00Z",
            "entity_type": "story-comment",
            "story_id": 456,
            "position": 2,
            "parent_id": 123,
            "reactions": [],
        }

        comment_input = models.CreateStoryCommentInput(
            text="Reply to parent", parent_id=123
        )

        requests_mock.post(
            f"{base_url}/stories/{story_id}/comments", json=parent_comment_data
        )

        comment = api_client.create_story_comment(story_id, comment_input)

        assert comment.parent_id == 123

    def test_get_story_comment(
        self, requests_mock, api_client, base_url, story_comment_data
    ):
        """Test fetching a specific comment."""
        story_id = 456
        comment_id = 123

        requests_mock.get(
            f"{base_url}/stories/{story_id}/comments/{comment_id}",
            json=story_comment_data,
        )

        comment = api_client.get_story_comment(story_id, comment_id)

        assert isinstance(comment, models.StoryComment)
        assert comment.id == 123
        assert comment.text == "This is a test comment"

    def test_update_story_comment(self, requests_mock, api_client, base_url):
        """Test updating comment text."""
        story_id = 456
        comment_id = 123
        updated_data = {
            "id": 123,
            "text": "Updated comment text",
            "author_id": "12345678-1234-1234-1234-123456789012",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-03T00:00:00Z",
            "entity_type": "story-comment",
            "story_id": 456,
            "position": 1,
            "reactions": [],
        }

        update_input = models.UpdateStoryCommentInput(text="Updated comment text")

        requests_mock.put(
            f"{base_url}/stories/{story_id}/comments/{comment_id}", json=updated_data
        )

        comment = api_client.update_story_comment(story_id, comment_id, update_input)

        assert comment.text == "Updated comment text"
        assert comment.updated_at is not None

    def test_delete_story_comment(self, requests_mock, api_client, base_url):
        """Test deleting a comment."""
        story_id = 456
        comment_id = 123

        requests_mock.delete(
            f"{base_url}/stories/{story_id}/comments/{comment_id}", status_code=204
        )

        # Should not raise an exception
        api_client.delete_story_comment(story_id, comment_id)

    def test_story_comment_datetime_parsing(
        self, requests_mock, api_client, base_url, story_comment_data
    ):
        """Test that datetime fields are properly parsed."""
        story_id = 456

        requests_mock.get(
            f"{base_url}/stories/{story_id}/comments", json=[story_comment_data]
        )

        comments = api_client.list_story_comments(story_id)

        assert isinstance(comments[0].created_at, datetime)
        assert isinstance(comments[0].updated_at, datetime)
        assert comments[0].created_at.year == 2023
        assert comments[0].created_at.month == 1
        assert comments[0].created_at.day == 1

    def test_story_comment_not_found(self, requests_mock, api_client, base_url):
        """Test 404 error handling."""
        story_id = 456
        comment_id = 999

        requests_mock.get(
            f"{base_url}/stories/{story_id}/comments/{comment_id}",
            status_code=404,
            json={"message": "Comment not found", "error": "NotFound"},
        )

        with pytest.raises(requests.exceptions.HTTPError):
            api_client.get_story_comment(story_id, comment_id)


class TestEpicComments:
    """Test epic comment endpoints."""

    def test_list_epic_comments(
        self, requests_mock, api_client, base_url, threaded_comment_data
    ):
        """Test listing all comments for an epic."""
        epic_id = 111

        requests_mock.get(
            f"{base_url}/epics/{epic_id}/comments", json=[threaded_comment_data]
        )

        comments = api_client.list_epic_comments(epic_id)

        assert len(comments) == 1
        assert isinstance(comments[0], models.ThreadedComment)
        assert comments[0].id == 789
        assert comments[0].text == "Epic discussion comment"
        assert len(comments[0].comments) == 1
        assert comments[0].comments[0].text == "Nested reply"

    def test_create_epic_comment(
        self, requests_mock, api_client, base_url, threaded_comment_data
    ):
        """Test creating a new comment on an epic."""
        epic_id = 111
        comment_input = models.CreateStoryCommentInput(text="New epic comment")

        requests_mock.post(
            f"{base_url}/epics/{epic_id}/comments", json=threaded_comment_data
        )

        comment = api_client.create_epic_comment(epic_id, comment_input)

        assert isinstance(comment, models.ThreadedComment)
        assert comment.id == 789

    def test_get_epic_comment(
        self, requests_mock, api_client, base_url, threaded_comment_data
    ):
        """Test fetching a specific epic comment."""
        epic_id = 111
        comment_id = 789

        requests_mock.get(
            f"{base_url}/epics/{epic_id}/comments/{comment_id}",
            json=threaded_comment_data,
        )

        comment = api_client.get_epic_comment(epic_id, comment_id)

        assert isinstance(comment, models.ThreadedComment)
        assert comment.id == 789

    def test_update_epic_comment(self, requests_mock, api_client, base_url):
        """Test updating epic comment text."""
        epic_id = 111
        comment_id = 789
        updated_data = {
            "id": 789,
            "text": "Updated epic comment",
            "author_id": "12345678-1234-1234-1234-123456789012",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-03T00:00:00Z",
            "entity_type": "epic-comment",
            "comments": [],
        }

        update_input = models.UpdateStoryCommentInput(text="Updated epic comment")

        requests_mock.put(
            f"{base_url}/epics/{epic_id}/comments/{comment_id}", json=updated_data
        )

        comment = api_client.update_epic_comment(epic_id, comment_id, update_input)

        assert comment.text == "Updated epic comment"

    def test_delete_epic_comment(self, requests_mock, api_client, base_url):
        """Test deleting an epic comment."""
        epic_id = 111
        comment_id = 789

        requests_mock.delete(
            f"{base_url}/epics/{epic_id}/comments/{comment_id}", status_code=204
        )

        # Should not raise an exception
        api_client.delete_epic_comment(epic_id, comment_id)

    def test_threaded_comment_parsing(
        self, requests_mock, api_client, base_url, threaded_comment_data
    ):
        """Test nested comment structure parsing."""
        epic_id = 111

        requests_mock.get(
            f"{base_url}/epics/{epic_id}/comments", json=[threaded_comment_data]
        )

        comments = api_client.list_epic_comments(epic_id)

        assert len(comments[0].comments) == 1
        nested = comments[0].comments[0]
        assert isinstance(nested, models.ThreadedComment)
        assert nested.id == 790
        assert nested.author_id == "87654321-4321-4321-4321-210987654321"
