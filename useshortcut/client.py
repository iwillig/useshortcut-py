from typing import Optional, Dict, Any, List, Union
import requests
import useshortcut.models as models

JSON = Union[Dict[str, Any], List[Dict[str, Any]]]


class APIClient:
    """Client for interacting with the Shortcut API v3."""

    BASE_URL = "https://api.app.shortcut.com/api/v3"

    def __init__(self, api_token: str, base_url: Optional[str] = None) -> None:

        self.api_token = api_token
        if base_url is None:
            self.base_url = self.BASE_URL
        else:
            self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json; charset=utf-8",
                "Shortcut-Token": api_token,
                "Accept": "application/json; charset=utf-8",
                "User-Agent": "useshortcut-py/0.0.1",
            }
        )

        super().__init__()

    def _make_request(self, method: str, path: str, **kwargs) -> JSON:
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
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else response

    def get_current_member(self):
        return models.Member.from_json(self._make_request("GET", "/member"))

    def search(self, params: models.SearchInputs):
        return self._make_request("GET", "/search", params=params.__dict__)

    def search_stories(self, params: models.SearchInputs):
        return models.SearchStoryResult.from_json(
            self._make_request("GET", "/search/stories", params=params.__dict__)
        )

    def create_story(self, story: models.StoryInput) -> models.Story:
        """Create a new story.
        Args:
            story: Story object with the story details
        Returns:
            Created Story object
        """
        data = self._make_request("POST", "/stories", json=story.__dict__)
        return models.Story.from_json(data)

    def get_story(self, story_id: int) -> models.Story:
        """Get a specific story by ID.
        Args:
            story_id: The ID of the story to retrieve
        Returns:
            Story object
        """
        data = self._make_request("GET", f"/stories/{story_id}")
        return models.Story.from_json(data)

    def update_story(self, story_id: int, story: models.Story) -> models.Story:
        """Update an existing story.
        Args:
            story_id: The ID of the story to update
            story: Story object with updated details

        Returns:
            Updated Story object
        """
        data = self._make_request("PUT", f"/stories/{story_id}", json=story.__dict__)
        return models.Story.from_json(data)

    # This delete method returns the response, helpful for debugging.
    # It also accepts the story model object instead of an ID. TODO: Revisit this.
    def delete_story(self, story: models.Story) -> Any:
        """Delete a story.
        Args:
            story: The story object to delete
        """
        story_id = story.id
        return self._make_request("DELETE", f"/stories/{story_id}")

    # Workflow endpoints
    def list_workflows(self):
        """List Workflows
        Returns: List of Workflow objects
        """
        data = self._make_request("GET", "/workflows")
        return [models.Workflow.from_json(x) for x in data]

    def get_workflow(self, workflow_id: str):
        """Get a specific workflow by ID.
        Args: workflow_id: The ID of the workflow
        Returns: Workflow object"""
        data = self._make_request("GET", f"/workflows/{workflow_id}")
        return models.Workflow.from_json(data)

    # Epic endpoints
    def list_epics(self) -> List[models.Epic]:
        """List all epics.
        Returns:
            List of Epic objects
        """
        data = self._make_request("GET", "/epics")
        return [models.Epic.from_json(epic) for epic in data]

    def get_epic(self, epic_id: int) -> models.Epic:
        """Get a specific epic by ID.
        Args:
            epic_id: The ID of the epic to retrieve

        Returns:
            Epic object
        """
        data = self._make_request("GET", f"/epics/{epic_id}")
        return models.Epic.from_json(data)

    def create_epic(self, epic: models.EpicInput) -> models.Epic:
        """Create a new epic.
        Args:
            epic: Epic object with the epic details

        Returns:
            Created Epic object
        """
        data = self._make_request("POST", "/epics", json=epic.__dict__)
        return models.Epic.from_json(data)

    def update_epic(self, epic_id: int, epic: models.Epic) -> models.Epic:
        """Update an existing epic.
        Args:
            epic_id: The ID of the epic to update
            epic: Epic object with updated details

        Returns:
            Updated Epic object
        """
        data = self._make_request("PUT", f"/epics/{epic_id}", json=epic.__dict__)
        return models.Epic.from_json(data)

    def delete_epic(self, epic_id: int) -> None:
        """Delete an epic.
        Args:
            epic_id: The ID of the epic to delete
        """
        self._make_request("DELETE", f"/epics/{epic_id}")

    # Iteration endpoints
    def list_iterations(self) -> List[models.Iteration]:
        """List all iterations.
        Returns:
            List of Iteration objects
        """
        data = self._make_request("GET", "/iterations")
        return [models.Iteration.from_json(iteration) for iteration in data]

    def get_iteration(self, iteration_id: int) -> models.Iteration:
        """Get a specific iteration by ID.
        Args:
            iteration_id: The ID of the iteration to retrieve

        Returns:
            Iteration object
        """
        data = self._make_request("GET", f"/iterations/{iteration_id}")
        return models.Iteration.from_json(data)

    def create_iteration(
        self, iteration: models.CreateIterationInput
    ) -> models.Iteration:
        """Create a new iteration.
        Args:
            iteration: Iteration object with the iteration details

        Returns:
            Created Iteration object
        """
        data = self._make_request("POST", "/iterations", json=iteration.__dict__)
        return models.Iteration.from_json(data)

    def update_iteration(
        self, iteration_id: int, iteration: models.UpdateIterationInput
    ) -> models.Iteration:
        """Update an existing iteration.
        Args:
            iteration_id: The ID of the iteration to update
            iteration: Iteration object with updated details

        Returns:
            Updated Iteration object
        """
        data = self._make_request(
            "PUT", f"/iterations/{iteration_id}", json=iteration.__dict__
        )
        return models.Iteration.from_json(data)

    def delete_iteration(self, iteration_id: int) -> None:
        """Delete an iteration.
        Args:
            iteration_id: The ID of the iteration to delete
        """
        self._make_request("DELETE", f"/iterations/{iteration_id}")

    ## Story Link (AKA Story Relationships)

    def create_story_link(
        self, params: models.StoryLinkInput
    ) -> List[models.StoryLink]:
        """
        Create a new story link
        Args:
            params: Story link parameters
        Returns
            Story Link object
        """
        data = self._make_request("POST", "/story-links", json=params.__dict__)
        return [models.StoryLink.from_json(story_link) for story_link in data]

    def get_story_link(self, story_link_id: int) -> models.StoryLink:
        """
        Get a specific story link by ID.
        Args
            story_link_id: The Story Link ID
        Returns
            The matching Story Link object
        """
        data = self._make_request("GET", f"/story-links/{story_link_id}")
        return models.StoryLink.from_json(data)

    def update_story_link(
        self, story_link_id: int, params: models.StoryLinkInput
    ) -> models.StoryLink:
        """Update an existing story link.
        Args:
            story_link_id: The ID of the story link to update
            params: Story Link parameters
        Returns
            Updated Story Link object
        """
        data = self._make_request(
            "PUT", f"/story-links/{story_link_id}", json=params.__dict__
        )
        return models.StoryLink.from_json(data)

    def delete_story_link(self, story_link_id: int) -> None:
        """
        Delete a story link by ID.
        Args
            story_link_id: The Story Link ID
        Returns None
        """
        self._make_request("DELETE", f"/story-links/{story_link_id}")

    ## Groups
    def list_groups(self) -> List[models.Group]:
        """
        List all groups.
        Returns:
            List of Group objects
        """
        data = self._make_request("GET", "/groups")
        return [models.Group.from_json(x) for x in data]

    def get_group(self, group_id: int) -> models.Group:
        """
        Get a specific group by ID.
        Args:
            group_id: The ID of the group to retrieve
        Returns:
            A Group object
        """
        return models.Group.from_json(self._make_request("GET", f"/groups/{group_id}"))

    def create_group(self, params: models.CreateGroupInput) -> models.Group:
        """
        Create a new group.
        Args:
            params: Group parameters
        Returns
            Group object
        """
        return models.Group.from_json(
            self._make_request("POST", "/groups", json=params.__dict__)
        )

    def update_group(self, params: models.UpdateGroupInput) -> models.Group:
        """Update an existing group.
        Args:
            params: Group parameters
        Returns:
            Group object
        """
        return models.Group.from_json(
            self._make_request("PUT", f"/groups/{params.id}", json=params.__dict__)
        )

    def delete_group(self, group_id: int) -> None:
        """
        Delete a specific group by ID.
        Args:
            group_id: The ID of the group to delete
        Returns
            None
        """
        self._make_request("DELETE", f"/groups/{group_id}")

    ## Key Results
    def get_key_result(self, key_result_id: int) -> models.KeyResult:
        """
        Get a specific key result by ID.
        Args:
            key_result_id: The ID of the key result to retrieve
        Returns:
            KeyResult object
        """
        data = self._make_request("GET", f"/key-results/{key_result_id}")
        return models.KeyResult.from_json(data)

    def update_key_result(
        self, key_result_id: int, params: models.KeyResultInput
    ) -> models.KeyResult:
        """
        Update a specific key result by ID.
        Args:
            key_result_id: The ID of the key result to update
            params: KeyResult parameters
        Returns:
            KeyResult object
        """
        data = self._make_request(
            "PUT", f"/key-results/{key_result_id}", json=params.__dict__
        )
        return models.KeyResult.from_json(data)

    ## Labels
    def list_labels(self) -> List[models.Label]:
        """
        List all labels.
        Returns:
                A list of Label objects
        """
        data = self._make_request("GET", "/labels")
        return [models.Label.from_json(x) for x in data]

    def get_label(self, label_id: int) -> models.Label:
        """
        Get a specific label by ID.
        Args:
            label_id: Label ID
        Returns:
                A Label object
        """
        return models.Label.from_json(self._make_request("GET", f"/labels/{label_id}"))

    def create_label(self, params: models.CreateLabelInput) -> models.Label:
        """
        Create a new label.
        Args:
            params: Label parameters
        Returns:
            The new Label object
        """
        data = self._make_request("POST", "/labels", json=params.__dict__)
        return models.Label.from_json(data)

    def delete_label(self, label_id: int) -> None:
        """
        Delete a specific label by ID.
        Args:
            label_id: The ID of the label to delete
        Returns:
            None
        """
        self._make_request("DELETE", f"/labels/{label_id}")

    ## Linked Files
    def list_linked_files(self) -> List[models.LinkedFiles]:
        """
        List all linked files.
        Returns:
                All linked files associated with a workspace
        """
        data = self._make_request("GET", "/linked-files")
        return [models.LinkedFiles.from_json(x) for x in data]

    def create_linked_file(
        self, params: models.CreateLinkedFilesInput
    ) -> models.LinkedFiles:
        """Create a new linked file.
        Args:
            params: LinkedFile parameters
        Returns:
            The new LinkedFile object
        """
        return models.LinkedFiles.from_json(
            self._make_request("POST", "/linked-files", json=params.__dict__)
        )

    def update_linked_file(
        self, linked_file_id: int, params: models.UpdatedLinkedFilesInput
    ):
        """
        Update a linked file.
        Args:
            linked_file_id: The ID of the linked file to update
            params: LinkedFile parameters

        Returns:
            Updated LinkedFile object
        """
        return models.LinkedFiles.from_json(
            self._make_request(
                "PUT", f"/linked-files/{linked_file_id}", json=params.__dict__
            )
        )

    def delete_linked_file(self, linked_file_id: int) -> None:
        """
        Delete a linked file.
        Args:
            linked_file_id: The ID of the linked file to delete
        Returns:
            None
        """
        self._make_request("DELETE", f"/linked-files/{linked_file_id}")

    ## Files
    def list_files(self) -> List[models.File]:
        """
        List all files.

        Returns:
            All Files associated with a workspace
        """
        return [models.File.from_json(x) for x in self._make_request("GET", "/files")]

    def get_file(self, file_id: int) -> models.File:
        """
        Get a specific file by ID.
        Args:
            file_id: The ID of the file to get
        Returns:
            File object
        """
        return models.File.from_json(self._make_request("GET", f"/files/{file_id}"))

    def update_file(self, file_id: int, params: models.CreateFileInput) -> models.File:
        """
        Update a specific file.
        Args:
            file_id: The ID of the file to update
            params: File parameters
        Returns:
            The updated File object
        """
        return models.File.from_json(
            self._make_request("PUT", f"/files/{file_id}", json=params.__dict__)
        )

    def delete_file(self, file_id: int) -> None:
        """
        Delete a specific file.
        Args:
            file_id: The ID of the file to delete
        Returns:
            None
        """
        self._make_request("DELETE", f"/files/{file_id}")

    ## Members
    def list_members(self) -> List[models.Member]:
        """
        List all members.
        Returns:
            All members associated with a workspace
        """
        data = self._make_request("GET", "/members")
        return [models.Member.from_json(x) for x in data]

    def get_member(self, member_id: str) -> models.Member:
        """
        Get a specific member by ID.
        Args:
            member_id: The ID of the member
        Returns:
            A Member object matching the given member_id
        """
        return models.Member.from_json(
            self._make_request("GET", f"/members/{member_id}")
        )

    ## Objectives
    def list_objectives(self) -> List[models.Objective]:
        data = self._make_request("GET", "/objectives")
        return [models.Objective.from_json(x) for x in data]

    def get_objective(self, objective_id: int) -> models.Objective:
        data = self._make_request("GET", f"/objectives/{objective_id}")
        return models.Objective.from_json(data)

    def create_objective(self, params: models.CreateObjectiveInput) -> models.Objective:
        data = self._make_request("POST", "/objectives", json=params.__dict__)
        return models.Objective.from_json(data)

    def update_objective(
        self, objective_id: int, params: models.UpdateObjectiveInput
    ) -> models.Objective:
        data = self._make_request(
            "PUT", f"/objectives/{objective_id}", json=params.__dict__
        )
        return models.Objective.from_json(data)

    def delete_objective(self, objective_id: int) -> None:
        self._make_request("DELETE", f"/objectives/{objective_id}")

    ## Projects

    def list_projects(self) -> List[models.Project]:
        data = self._make_request("GET", "/projects")
        return [models.Project.from_json(x) for x in data]

    def get_project(self, project_id: int) -> models.Project:
        return models.Project.from_json(
            self._make_request("GET", f"/projects/{project_id}")
        )

    def create_project(self, params) -> models.Project:
        data = self._make_request("POST", "/projects", json=params.__dict__)
        return models.Project.from_json(data)

    def update_project(
        self, project_id: int, params: models.UpdateProjectInput
    ) -> models.Project:
        data = self._make_request(
            "PUT", f"/projects/{project_id}", json=params.__dict__
        )
        return models.Project.from_json(data)

    def delete_project(self, project_id: int) -> None:
        self._make_request("DELETE", f"/projects/{project_id}")

    ## Repositories

    def list_repositories(self) -> List[models.Repository]:
        data = self._make_request("GET", "/repositories")
        return [models.Repository.from_json(x) for x in data]

    def get_repository(self, repository_id: int) -> models.Repository:
        data = self._make_request("GET", f"/repositories/{repository_id}")
        return models.Repository.from_json(data)

    ## Epic Workflow

    def get_epic_workflow(self) -> models.EpicWorkflow:
        data = self._make_request("GET", "/epic-workflow")
        return models.EpicWorkflow.from_json(data)

    ## Categories

    def list_categories(self) -> List[models.Category]:
        data = self._make_request("GET", "/categories")
        return [models.Category.from_json(x) for x in data]

    def get_category(self, category_id: int) -> models.Category:
        data = self._make_request("GET", f"/categories/{category_id}")
        return models.Category.from_json(data)

    def create_category(self, params: models.CreateCategoryInput) -> models.Category:
        data = self._make_request("POST", "/categories", json=params.__dict__)
        return models.Category.from_json(data)

    def update_category(
        self, category_id: int, params: models.UpdateCategoryInput
    ) -> models.Category:
        data = self._make_request(
            "PUT", f"/categories/{category_id}", json=params.__dict__
        )
        return models.Category.from_json(data)

    def delete_category(self, category_id: int) -> None:
        self._make_request("DELETE", f"/categories/{category_id}")

    ## Custom Fields
