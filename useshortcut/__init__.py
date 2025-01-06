from typing import Optional, Dict, Any, List
import requests
import json

from .models import Story, Epic, Iteration, StoryInput, EpicInput, CreateIterationInput, UpdateIterationInput


class APIClient:
    """Client for interacting with the Shortcut API v3."""
    BASE_URL = "https://api.app.shortcut-staging.com/api/v3"

    def __init__(self, api_token: str) -> None:
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json; charset=utf-8",
            "Shortcut-Token": api_token,
            "Accept": "application/json; charset=utf-8",
            "User-Agent": "useshortcut-py/0.0.1",
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

        return response.json() if response.content else response

    def list_stories(self, **params) -> List[Story]:
        """List stories with optional filtering.

        Args:
            **params: Optional query parameters for filtering stories

        Returns:
            List of Story objects
        """
        data = self._make_request("GET", "/stories", params=params)
        return [Story.from_json(story) for story, value in data.items()]

    def create_story(self, story: StoryInput) -> Story:
        """Create a new story.

        Args:
            story: Story object with the story details

        Returns:
            Created Story object
        """
        data = self._make_request("POST", "/stories", json=story.__dict__)
        return Story.from_json(data)

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

    def delete_story(self, story: Story) -> Any:
        """Delete a story.

        Args:
            story: The story object to delete
        """
        story_id = story.id
        return self._make_request("DELETE", f"/stories/{story_id}")

    def list_workflows(self):
        return self._make_request("GET", "/workflows")

    def get_workflow(self, workflow_id: str):
        return self._make_request("GET", f"/workflows/{workflow_id}")

    # Epic endpoints
    def list_epics(self) -> List[Epic]:
        """List all epics.

        Returns:
            List of Epic objects
        """
        data = self._make_request("GET", "/epics")
        return [Epic.from_json(epic) for epic in data]

    def get_epic(self, epic_id: int) -> Epic:
        """Get a specific epic by ID.

        Args:
            epic_id: The ID of the epic to retrieve

        Returns:
            Epic object
        """
        data = self._make_request("GET", f"/epics/{epic_id}")
        return Epic.from_json(data)

    def create_epic(self, epic: EpicInput) -> Epic:
        """Create a new epic.

        Args:
            epic: Epic object with the epic details

        Returns:
            Created Epic object
        """
        data = self._make_request("POST", "/epics", json=epic.__dict__)
        return Epic.from_json(data)

    def update_epic(self, epic_id: int, epic: Epic) -> Epic:
        """Update an existing epic.

        Args:
            epic_id: The ID of the epic to update
            epic: Epic object with updated details

        Returns:
            Updated Epic object
        """
        data = self._make_request("PUT", f"/epics/{epic_id}", json=epic.__dict__)
        return Epic.from_json(data)

    def delete_epic(self, epic_id: int) -> None:
        """Delete an epic.

        Args:
            epic_id: The ID of the epic to delete
        """
        self._make_request("DELETE", f"/epics/{epic_id}")

    # Iteration endpoints
    def list_iterations(self) -> List[Iteration]:
        """List all iterations.

        Returns:
            List of Iteration objects
        """
        data = self._make_request("GET", "/iterations")
        return [Iteration.from_json(iteration) for iteration in data]

    def get_iteration(self, iteration_id: int) -> Iteration:
        """Get a specific iteration by ID.

        Args:
            iteration_id: The ID of the iteration to retrieve

        Returns:
            Iteration object
        """
        data = self._make_request("GET", f"/iterations/{iteration_id}")
        return Iteration.from_json(data)

    def create_iteration(self, iteration: CreateIterationInput) -> Iteration:
        """Create a new iteration.

        Args:
            iteration: Iteration object with the iteration details

        Returns:
            Created Iteration object
        """
        data = self._make_request("POST", "/iterations", json=iteration.__dict__)
        return Iteration.from_json(data)

    def update_iteration(self, iteration_id: int, iteration: UpdateIterationInput) -> Iteration:
        """Update an existing iteration.

        Args:
            iteration_id: The ID of the iteration to update
            iteration: Iteration object with updated details

        Returns:
            Updated Iteration object
        """
        data = self._make_request("PUT", f"/iterations/{iteration_id}", json=iteration.__dict__)
        return Iteration.from_json(data)

    def delete_iteration(self, iteration_id: int) -> None:
        """Delete an iteration.

        Args:
            iteration_id: The ID of the iteration to delete
        """
        self._make_request("DELETE", f"/iterations/{iteration_id}")