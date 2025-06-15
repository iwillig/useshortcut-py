"""Integration tests for the Shortcut API client.

These tests require a valid SHORTCUT_TOKEN environment variable.
"""

import os
import pytest
from datetime import datetime

import requests

from useshortcut.client import APIClient
import useshortcut.models as models


# Test data prefix to identify test-created resources
TEST_PREFIX = "TEST_INTEGRATION_"
TEST_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

@pytest.fixture(scope="session")
def api_client():
    """Create an API client instance."""
    token = os.environ.get("SHORTCUT_API_TOKEN")
    if not token:
        pytest.skip("SHORTCUT_API_TOKEN environment variable not set")
    return APIClient(api_token=token)

@pytest.fixture(scope="session")
def default_workflow_state_id(api_client):
    """Get a default workflow state ID for story creation."""
    workflows = api_client.list_workflows()
    if not workflows:
        pytest.skip("No workflows available")

    # Get the first workflow's default state
    workflow = api_client.get_workflow(workflows[0].id)
    return workflow.default_state_id

@pytest.mark.integration
class TestStories:
    """Test story CRUD operations."""

    def test_create_story(
        self, api_client, default_workflow_state_id,
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

        assert story is not None
        assert story.name == story_name
        assert story.description == "Test story created by integration tests"
        assert story.workflow_state_id == default_workflow_state_id
        assert story.story_type == "feature"

        api_client.delete_story(story.id)
        try:
            api_client.get_story(story.id)
        except requests.exceptions.HTTPError as e:
            assert e.response.status_code == 404




if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
