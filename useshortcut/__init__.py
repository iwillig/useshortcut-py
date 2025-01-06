from typing import Optional, Dict, Any, List
import requests

from .models import Story, Epic, Iteration


class APIClient:
    """Client for interacting with the Shortcut API v3."""
    BASE_URL = "https://api.app.shortcut.com/api/v3"

    def __init__(self, api_token: str) -> None:
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Shortcut-Token": api_token
        })

        super().__init__()

    def _make_request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the Shortcut API.

        Args:
                method: HTTP method (GET, POST, PUT, DELETE)
                path: API endpoint path
                **kwargs: Additional arguments to pass to requests

        Returns:
                Response data as dictionary

        Raises:
                requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.BASE_URL}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def list_stories(self, **params) -> List[Story]:
        """List stories with optional filtering.

        Args:
            **params: Optional query parameters for filtering stories

        Returns:
            List of Story objects
        """
        data = self._make_request("GET", "/stories", params=params)
        return [Story.from_json(story) for story in data]

    def get_story(self, story_id: int) -> Story:
        """Get a specific story by ID.

        Args:
            story_id: The ID of the story to retrieve

        Returns:
            Story object
        """
        data = self._make_request("GET", f"/stories/{story_id}")
        return Story.from_json(data)

    def update_story(self, story_id: int, story: Story) -> Story:
        """Update an existing story.

        Args:
            story_id: The ID of the story to update
            story: Story object with updated details

        Returns:
            Updated Story object
        """
        data = self._make_request("PUT", f"/stories/{story_id}", json=story.__dict__)
        return Story.from_json(data)

    def delete_story(self, story_id: int) -> None:
        """Delete a story.

        Args:
            story_id: The ID of the story to delete
        """
        self._make_request("DELETE", f"/stories/{story_id}")
