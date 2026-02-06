from collections.abc import Iterator
from typing import Any, Optional, Union

import requests

import useshortcut.models as models

JSON = Union[dict[str, Any], list[dict[str, Any]]]


def _clean_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Remove None values from a dictionary."""
    return {k: v for k, v in data.items() if v is not None}


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
                "User-Agent": "useshortcut-py/0.0.5",
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

    def _paginate_results(
        self, initial_response: models.SearchStoryResult, params: models.SearchInputs
    ) -> Iterator[models.Story]:
        """Iterate through all pages of search results.

        Args:
            initial_response: The first page of results
            params: The search parameters

        Yields:
            Individual Story objects from all pages
        """
        # Yield items from first page
        for item in initial_response.data:
            yield item

        # Follow pagination links
        next_url = initial_response.next
        while next_url:
            # Extract just the path and query from the next URL
            if next_url.startswith("http"):
                # Full URL provided
                next_path = next_url.split(self.base_url)[-1]
            else:
                next_path = next_url

            response = self._make_request("GET", next_path)
            result = models.SearchStoryResult.from_json(response)

            for item in result.data:
                yield item

            next_url = result.next

    def get_current_member(self):
        return models.Member.from_json(self._make_request("GET", "/member"))

    def search(self, params: models.SearchInputs):
        return self._make_request("GET", "/search", params=params.__dict__)

    def search_stories(self, params: models.SearchInputs):
        return models.SearchStoryResult.from_json(
            self._make_request("GET", "/search/stories", params=params.__dict__)
        )

    def search_stories_iter(
        self, params: models.SearchInputs
    ) -> Iterator[models.Story]:
        """Search for stories with automatic pagination.

        Args:
            params: Search parameters

        Yields:
            Individual Story objects from all pages of results
        """
        initial_response = self.search_stories(params)
        return self._paginate_results(initial_response, params)

    def create_story(self, story: models.CreateStoryParams) -> models.Story:
        """Create a new story.
        Args:
            story: Story object with the story details
        Returns:
            Created Story object
        """
        data = self._make_request("POST", "/stories", json=_clean_dict(story.__dict__))
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

    def update_story(
        self, story_id: int, story: models.UpdateStoryInput
    ) -> models.Story:
        """Update an existing story.
        Args:
            story_id: The ID of the story to update
            story: UpdateStoryInput object with updated details

        Returns:
            Updated Story object
        """
        data = self._make_request(
            "PUT", f"/stories/{story_id}", json=_clean_dict(story.__dict__)
        )
        return models.Story.from_json(data)

    def delete_story(self, story_id: int) -> None:
        """Delete a story.
        Args:
            story_id: The ID of the story to delete
        """
        self._make_request("DELETE", f"/stories/{story_id}")

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
    def list_epics(self) -> list[models.Epic]:
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

    def create_epic(self, epic: models.CreateEpicInput) -> models.Epic:
        """Create a new epic.
        Args:
            epic: Epic object with the epic details

        Returns:
            Created Epic object
        """
        data = self._make_request("POST", "/epics", json=_clean_dict(epic.__dict__))
        return models.Epic.from_json(data)

    def update_epic(self, epic_id: int, epic: models.UpdateEpicInput) -> models.Epic:
        """Update an existing epic.
        Args:
            epic_id: The ID of the epic to update
            epic: UpdateEpicInput object with updated details

        Returns:
            Updated Epic object
        """
        data = self._make_request(
            "PUT", f"/epics/{epic_id}", json=_clean_dict(epic.__dict__)
        )
        return models.Epic.from_json(data)

    def delete_epic(self, epic_id: int) -> None:
        """Delete an epic.
        Args:
            epic_id: The ID of the epic to delete
        """
        self._make_request("DELETE", f"/epics/{epic_id}")

    # Iteration endpoints
    def list_iterations(self) -> list[models.Iteration]:
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
        data = self._make_request(
            "POST", "/iterations", json=_clean_dict(iteration.__dict__)
        )
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
            "PUT",
            f"/iterations/{iteration_id}",
            json=_clean_dict(iteration.__dict__),
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
    ) -> list[models.StoryLink]:
        """
        Create a new story link
        Args:
            params: Story link parameters
        Returns
            Story Link object
        """
        data = self._make_request(
            "POST", "/story-links", json=_clean_dict(params.__dict__)
        )
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
            "PUT",
            f"/story-links/{story_link_id}",
            json=_clean_dict(params.__dict__),
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
    def list_groups(self) -> list[models.Group]:
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
            self._make_request("POST", "/groups", json=_clean_dict(params.__dict__))
        )

    def update_group(
        self, group_id: int, params: models.UpdateGroupInput
    ) -> models.Group:
        """Update an existing group.
        Args:
            group_id: The ID of the group to update
            params: Group parameters
        Returns:
            Group object
        """
        return models.Group.from_json(
            self._make_request(
                "PUT", f"/groups/{group_id}", json=_clean_dict(params.__dict__)
            )
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
            "PUT",
            f"/key-results/{key_result_id}",
            json=_clean_dict(params.__dict__),
        )
        return models.KeyResult.from_json(data)

    ## Labels
    def list_labels(self) -> list[models.Label]:
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
        data = self._make_request("POST", "/labels", json=_clean_dict(params.__dict__))
        return models.Label.from_json(data)

    def update_label(
        self, label_id: int, params: models.UpdateLabelInput
    ) -> models.Label:
        """
        Update an existing label.
        Args:
            label_id: The ID of the label to update
            params: UpdateLabelInput object with updated details
        Returns:
            Updated Label object
        """
        data = self._make_request(
            "PUT", f"/labels/{label_id}", json=_clean_dict(params.__dict__)
        )
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
    def list_linked_files(self) -> list[models.LinkedFiles]:
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
            self._make_request(
                "POST", "/linked-files", json=_clean_dict(params.__dict__)
            )
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
                "PUT",
                f"/linked-files/{linked_file_id}",
                json=_clean_dict(params.__dict__),
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
    def list_files(self) -> list[models.File]:
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
            self._make_request(
                "PUT", f"/files/{file_id}", json=_clean_dict(params.__dict__)
            )
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
    def list_members(self) -> list[models.Member]:
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
    def list_objectives(self) -> list[models.Objective]:
        data = self._make_request("GET", "/objectives")
        return [models.Objective.from_json(x) for x in data]

    def get_objective(self, objective_id: int) -> models.Objective:
        data = self._make_request("GET", f"/objectives/{objective_id}")
        return models.Objective.from_json(data)

    def create_objective(self, params: models.CreateObjectiveInput) -> models.Objective:
        data = self._make_request(
            "POST", "/objectives", json=_clean_dict(params.__dict__)
        )
        return models.Objective.from_json(data)

    def update_objective(
        self, objective_id: int, params: models.UpdateObjectiveInput
    ) -> models.Objective:
        data = self._make_request(
            "PUT", f"/objectives/{objective_id}", json=_clean_dict(params.__dict__)
        )
        return models.Objective.from_json(data)

    def delete_objective(self, objective_id: int) -> None:
        self._make_request("DELETE", f"/objectives/{objective_id}")

    ## Projects

    def list_projects(self) -> list[models.Project]:
        data = self._make_request("GET", "/projects")
        return [models.Project.from_json(x) for x in data]

    def get_project(self, project_id: int) -> models.Project:
        return models.Project.from_json(
            self._make_request("GET", f"/projects/{project_id}")
        )

    def create_project(self, params: models.CreateProjectInput) -> models.Project:
        # Filter out None values from the request
        payload = {k: v for k, v in params.__dict__.items() if v is not None}
        data = self._make_request("POST", "/projects", json=payload)
        return models.Project.from_json(data)

    def update_project(
        self, project_id: int, params: models.UpdateProjectInput
    ) -> models.Project:
        data = self._make_request(
            "PUT", f"/projects/{project_id}", json=_clean_dict(params.__dict__)
        )
        return models.Project.from_json(data)

    def delete_project(self, project_id: int) -> None:
        self._make_request("DELETE", f"/projects/{project_id}")

    ## Repositories

    def list_repositories(self) -> list[models.Repository]:
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

    def list_categories(self) -> list[models.Category]:
        data = self._make_request("GET", "/categories")
        return [models.Category.from_json(x) for x in data]

    def get_category(self, category_id: int) -> models.Category:
        data = self._make_request("GET", f"/categories/{category_id}")
        return models.Category.from_json(data)

    def create_category(self, params: models.CreateCategoryInput) -> models.Category:
        data = self._make_request(
            "POST", "/categories", json=_clean_dict(params.__dict__)
        )
        return models.Category.from_json(data)

    def update_category(
        self, category_id: int, params: models.UpdateCategoryInput
    ) -> models.Category:
        data = self._make_request(
            "PUT", f"/categories/{category_id}", json=_clean_dict(params.__dict__)
        )
        return models.Category.from_json(data)

    def delete_category(self, category_id: int) -> None:
        self._make_request("DELETE", f"/categories/{category_id}")

    ## Custom Fields

    def list_custom_fields(self) -> list[models.CustomField]:
        """List all custom fields.
        Returns:
            List of CustomField objects
        """
        data = self._make_request("GET", "/custom-fields")
        return [models.CustomField.from_json(x) for x in data]

    def get_custom_field(self, custom_field_id: str) -> models.CustomField:
        """Get a specific custom field by ID.
        Args:
            custom_field_id: The UUID of the custom field
        Returns:
            CustomField object
        """
        data = self._make_request("GET", f"/custom-fields/{custom_field_id}")
        return models.CustomField.from_json(data)

    def update_custom_field(
        self, custom_field_id: str, custom_field: models.UpdateCustomFieldInput
    ) -> models.CustomField:
        """Update an existing custom field.
        Args:
            custom_field_id: The UUID of the custom field to update
            custom_field: Updated custom field parameters
        Returns:
            Updated CustomField object
        """
        # Filter out None values and convert values list
        update_data = {k: v for k, v in custom_field.__dict__.items() if v is not None}
        ## TOD (Ivan) Review this
        if "values" in update_data and update_data["values"]:
            update_data["values"] = [
                {k: v for k, v in val.__dict__.items() if v is not None}
                for val in update_data["values"]
            ]

        data = self._make_request(
            "PUT", f"/custom-fields/{custom_field_id}", json=update_data
        )
        return models.CustomField.from_json(data)

    def delete_custom_field(self, custom_field_id: str) -> None:
        """Delete a custom field.
        Args:
            custom_field_id: The UUID of the custom field to delete
        """
        self._make_request("DELETE", f"/custom-fields/{custom_field_id}")

    ## Documents (Docs)

    def list_docs(self) -> list[models.DocSlim]:
        """List all documents.
        Returns:
            List of DocSlim objects
        """
        data = self._make_request("GET", "/documents")
        return [models.DocSlim.from_json(x) for x in data]

    def get_doc(self, doc_id: str, include_html: bool = False) -> models.Doc:
        """Get a specific document by ID.
        Args:
            doc_id: The UUID of the document
            include_html: Whether to include HTML content in the response
        Returns:
            Doc object
        """
        params = {"include_html": "true"} if include_html else None
        data = self._make_request("GET", f"/documents/{doc_id}", params=params)
        return models.Doc.from_json(data)

    def create_doc(self, doc: models.CreateDocInput) -> models.Doc:
        """Create a new document.
        Args:
            doc: Document parameters
        Returns:
            Created Doc object
        """
        data = self._make_request("POST", "/documents", json=_clean_dict(doc.__dict__))
        return models.Doc.from_json(data)

    def update_doc(self, doc_id: str, doc: models.UpdateDocInput) -> models.Doc:
        """Update an existing document.
        Args:
            doc_id: The UUID of the document to update
            doc: Updated document parameters
        Returns:
            Updated Doc object
        """
        data = self._make_request(
            "PUT", f"/documents/{doc_id}", json=_clean_dict(doc.__dict__)
        )
        return models.Doc.from_json(data)

    def delete_doc(self, doc_id: str) -> None:
        """Delete a document.
        Args:
            doc_id: The UUID of the document to delete
        """
        self._make_request("DELETE", f"/documents/{doc_id}")

    def list_document_epics(self, doc_id: str) -> list[models.Epic]:
        """List all epics associated with a document.
        Args:
            doc_id: The UUID of the document
        Returns:
            List of Epic objects
        """
        data = self._make_request("GET", f"/documents/{doc_id}/epics")
        return [models.Epic.from_json(x) for x in data]

    def link_document_to_epic(self, doc_id: str, epic_id: int) -> None:
        """Link a document to an epic.
        Args:
            doc_id: The UUID of the document
            epic_id: The ID of the epic to link to
        """
        self._make_request("PUT", f"/documents/{doc_id}/epics/{epic_id}")

    def unlink_document_from_epic(self, doc_id: str, epic_id: int) -> None:
        """Unlink a document from an epic.
        Args:
            doc_id: The UUID of the document
            epic_id: The ID of the epic to unlink from
        """
        self._make_request("DELETE", f"/documents/{doc_id}/epics/{epic_id}")

    ## Story Comments

    def list_story_comments(self, story_id: int) -> list[models.StoryComment]:
        """List all comments for a story.
        Args:
            story_id: The ID of the story
        Returns:
            List of StoryComment objects
        """
        data = self._make_request("GET", f"/stories/{story_id}/comments")
        return [models.StoryComment.from_json(x) for x in data]

    def create_story_comment(
        self, story_id: int, comment: models.CreateStoryCommentInput
    ) -> models.StoryComment:
        """Create a new comment on a story.
        Args:
            story_id: The ID of the story
            comment: Comment parameters
        Returns:
            Created StoryComment object
        """
        data = self._make_request(
            "POST",
            f"/stories/{story_id}/comments",
            json=_clean_dict(comment.__dict__),
        )
        return models.StoryComment.from_json(data)

    def get_story_comment(self, story_id: int, comment_id: int) -> models.StoryComment:
        """Get a specific comment on a story.
        Args:
            story_id: The ID of the story
            comment_id: The ID of the comment
        Returns:
            StoryComment object
        """
        data = self._make_request("GET", f"/stories/{story_id}/comments/{comment_id}")
        return models.StoryComment.from_json(data)

    def update_story_comment(
        self, story_id: int, comment_id: int, comment: models.UpdateStoryCommentInput
    ) -> models.StoryComment:
        """Update a comment on a story.
        Args:
            story_id: The ID of the story
            comment_id: The ID of the comment
            comment: Updated comment parameters
        Returns:
            Updated StoryComment object
        """
        data = self._make_request(
            "PUT",
            f"/stories/{story_id}/comments/{comment_id}",
            json=_clean_dict(comment.__dict__),
        )
        return models.StoryComment.from_json(data)

    def delete_story_comment(self, story_id: int, comment_id: int) -> None:
        """Delete a comment from a story.
        Args:
            story_id: The ID of the story
            comment_id: The ID of the comment
        """
        self._make_request("DELETE", f"/stories/{story_id}/comments/{comment_id}")

    ## Epic Comments

    def list_epic_comments(self, epic_id: int) -> list[models.ThreadedComment]:
        """List all comments for an epic.
        Args:
            epic_id: The ID of the epic
        Returns:
            List of ThreadedComment objects
        """
        data = self._make_request("GET", f"/epics/{epic_id}/comments")
        return [models.ThreadedComment.from_json(x) for x in data]

    def create_epic_comment(
        self, epic_id: int, comment: models.CreateStoryCommentInput
    ) -> models.ThreadedComment:
        """Create a new comment on an epic.
        Args:
            epic_id: The ID of the epic
            comment: Comment parameters
        Returns:
            Created ThreadedComment object
        """
        data = self._make_request(
            "POST",
            f"/epics/{epic_id}/comments",
            json=_clean_dict(comment.__dict__),
        )
        return models.ThreadedComment.from_json(data)

    def get_epic_comment(self, epic_id: int, comment_id: int) -> models.ThreadedComment:
        """Get a specific comment on an epic.
        Args:
            epic_id: The ID of the epic
            comment_id: The ID of the comment
        Returns:
            ThreadedComment object
        """
        data = self._make_request("GET", f"/epics/{epic_id}/comments/{comment_id}")
        return models.ThreadedComment.from_json(data)

    def update_epic_comment(
        self, epic_id: int, comment_id: int, comment: models.UpdateStoryCommentInput
    ) -> models.ThreadedComment:
        """Update a comment on an epic.
        Args:
            epic_id: The ID of the epic
            comment_id: The ID of the comment
            comment: Updated comment parameters
        Returns:
            Updated ThreadedComment object
        """
        data = self._make_request(
            "PUT",
            f"/epics/{epic_id}/comments/{comment_id}",
            json=_clean_dict(comment.__dict__),
        )
        return models.ThreadedComment.from_json(data)

    def delete_epic_comment(self, epic_id: int, comment_id: int) -> None:
        """Delete a comment from an epic.
        Args:
            epic_id: The ID of the epic
            comment_id: The ID of the comment
        """
        self._make_request("DELETE", f"/epics/{epic_id}/comments/{comment_id}")

    ## Story Tasks

    def list_story_tasks(self, story_id: int) -> list[models.Task]:
        """List all tasks for a story.
        Args:
            story_id: The ID of the story
        Returns:
            List of Task objects
        """
        data = self._make_request("GET", f"/stories/{story_id}/tasks")
        return [models.Task.from_json(x) for x in data]

    def create_story_task(
        self, story_id: int, task: models.CreateTaskInput
    ) -> models.Task:
        """Create a new task on a story.
        Args:
            story_id: The ID of the story
            task: Task parameters
        Returns:
            Created Task object
        """
        data = self._make_request(
            "POST", f"/stories/{story_id}/tasks", json=_clean_dict(task.__dict__)
        )
        return models.Task.from_json(data)

    def get_story_task(self, story_id: int, task_id: int) -> models.Task:
        """Get a specific task on a story.
        Args:
            story_id: The ID of the story
            task_id: The ID of the task
        Returns:
            Task object
        """
        data = self._make_request("GET", f"/stories/{story_id}/tasks/{task_id}")
        return models.Task.from_json(data)

    def update_story_task(
        self, story_id: int, task_id: int, task: models.UpdateTaskInput
    ) -> models.Task:
        """Update a task on a story.
        Args:
            story_id: The ID of the story
            task_id: The ID of the task
            task: Updated task parameters
        Returns:
            Updated Task object
        """
        # Filter out None values from the update
        update_data = {k: v for k, v in task.__dict__.items() if v is not None}
        data = self._make_request(
            "PUT", f"/stories/{story_id}/tasks/{task_id}", json=update_data
        )
        return models.Task.from_json(data)

    def delete_story_task(self, story_id: int, task_id: int) -> None:
        """Delete a task from a story.
        Args:
            story_id: The ID of the story
            task_id: The ID of the task
        """
        self._make_request("DELETE", f"/stories/{story_id}/tasks/{task_id}")

    ## Milestones

    def list_milestones(self) -> list[models.Milestone]:
        """List all milestones.
        Returns:
            List of Milestone objects
        """
        data = self._make_request("GET", "/milestones")
        return [models.Milestone.from_json(x) for x in data]

    def get_milestone(self, milestone_id: int) -> models.Milestone:
        """Get a specific milestone by ID.
        Args:
            milestone_id: The ID of the milestone
        Returns:
            Milestone object
        """
        data = self._make_request("GET", f"/milestones/{milestone_id}")
        return models.Milestone.from_json(data)

    def create_milestone(
        self, milestone: models.CreateMilestoneInput
    ) -> models.Milestone:
        """Create a new milestone.
        Args:
            milestone: Milestone parameters
        Returns:
            Created Milestone object
        """
        # Convert categories to dict format
        request_data = _clean_dict(milestone.__dict__.copy())
        if "categories" in request_data and request_data["categories"]:
            request_data["categories"] = [
                _clean_dict(cat.__dict__) for cat in request_data["categories"]
            ]

        data = self._make_request("POST", "/milestones", json=request_data)
        return models.Milestone.from_json(data)

    def update_milestone(
        self, milestone_id: int, milestone: models.UpdateMilestoneInput
    ) -> models.Milestone:
        """Update an existing milestone.
        Args:
            milestone_id: The ID of the milestone to update
            milestone: Updated milestone parameters
        Returns:
            Updated Milestone object
        """
        # Filter out None values and convert categories
        update_data = {k: v for k, v in milestone.__dict__.items() if v is not None}
        if "categories" in update_data and update_data["categories"]:
            update_data["categories"] = [
                cat.__dict__ for cat in update_data["categories"]
            ]

        data = self._make_request(
            "PUT", f"/milestones/{milestone_id}", json=update_data
        )
        return models.Milestone.from_json(data)

    def delete_milestone(self, milestone_id: int) -> None:
        """Delete a milestone.
        Args:
            milestone_id: The ID of the milestone to delete
        """
        self._make_request("DELETE", f"/milestones/{milestone_id}")

    def list_milestone_epics(self, milestone_id: int) -> list[models.Epic]:
        """List all epics associated with a milestone.
        Args:
            milestone_id: The ID of the milestone
        Returns:
            List of Epic objects
        """
        data = self._make_request("GET", f"/milestones/{milestone_id}/epics")
        return [models.Epic.from_json(x) for x in data]

    def list_category_milestones(self, category_id: int) -> list[models.Milestone]:
        """List all milestones in a category.
        Args:
            category_id: The ID of the category
        Returns:
            List of Milestone objects
        """
        data = self._make_request("GET", f"/categories/{category_id}/milestones")
        return [models.Milestone.from_json(x) for x in data]

    def list_category_objectives(self, category_id: int) -> List[models.Objective]:
        """List all objectives in a category.
        Args:
            category_id: The ID of the category
        Returns:
            List of Objective objects
        """
        data = self._make_request("GET", f"/categories/{category_id}/objectives")
        return [models.Objective.from_json(x) for x in data]

    ## Documents (Docs)

    def list_docs(self) -> List[models.DocSlim]:
        """List all docs.
        Returns:
            List of DocSlim objects
        """
        data = self._make_request("GET", "/documents")
        return [models.DocSlim.from_json(x) for x in data]

    def get_doc(self, doc_id: str, content_format: Optional[str] = None) -> models.Doc:
        """Get a specific doc by ID.
        Args:
            doc_id: The UUID of the doc
            content_format: Format of content to return ("markdown" or "html")
        Returns:
            Doc object
        """
        params = {}
        if content_format:
            params["content_format"] = content_format
        data = self._make_request("GET", f"/documents/{doc_id}", params=params)
        return models.Doc.from_json(data)

    def create_doc(self, doc: models.CreateDocInput) -> models.DocSlim:
        """Create a new doc.
        Args:
            doc: Doc parameters
        Returns:
            Created DocSlim object
        """
        data = self._make_request("POST", "/documents", json=_clean_dict(doc.__dict__))
        return models.DocSlim.from_json(data)

    def update_doc(self, doc_id: str, doc: models.UpdateDocInput) -> models.Doc:
        """Update an existing doc.
        Args:
            doc_id: The UUID of the doc to update
            doc: Updated doc parameters
        Returns:
            Updated Doc object
        """
        data = self._make_request(
            "PUT", f"/documents/{doc_id}", json=_clean_dict(doc.__dict__)
        )
        return models.Doc.from_json(data)

    def delete_doc(self, doc_id: str) -> None:
        """Delete a doc.
        Args:
            doc_id: The UUID of the doc to delete
        """
        self._make_request("DELETE", f"/documents/{doc_id}")

    def list_document_epics(self, doc_id: str) -> List[models.EpicSlim]:
        """List all epics related to a document.
        Args:
            doc_id: The UUID of the document
        Returns:
            List of EpicSlim objects
        """
        data = self._make_request("GET", f"/documents/{doc_id}/epics")
        return [models.EpicSlim.from_json(x) for x in data]

    def link_document_to_epic(self, doc_id: str, epic_id: int) -> None:
        """Link a document to an epic.
        Args:
            doc_id: The UUID of the document
            epic_id: The ID of the epic
        """
        self._make_request("PUT", f"/documents/{doc_id}/epics/{epic_id}")

    def unlink_document_from_epic(self, doc_id: str, epic_id: int) -> None:
        """Unlink a document from an epic.
        Args:
            doc_id: The UUID of the document
            epic_id: The ID of the epic
        """
        self._make_request("DELETE", f"/documents/{doc_id}/epics/{epic_id}")

    ## Entity Templates

    def list_entity_templates(self) -> List[models.EntityTemplate]:
        """List all entity templates.
        Returns:
            List of EntityTemplate objects
        """
        data = self._make_request("GET", "/entity-templates")
        return [models.EntityTemplate.from_json(x) for x in data]

    def get_entity_template(self, template_id: str) -> models.EntityTemplate:
        """Get a specific entity template by ID.
        Args:
            template_id: The UUID of the template
        Returns:
            EntityTemplate object
        """
        data = self._make_request("GET", f"/entity-templates/{template_id}")
        return models.EntityTemplate.from_json(data)

    def create_entity_template(
        self, template: models.CreateEntityTemplateInput
    ) -> models.EntityTemplate:
        """Create a new entity template.
        Args:
            template: EntityTemplate parameters
        Returns:
            Created EntityTemplate object
        """
        data = self._make_request(
            "POST", "/entity-templates", json=_clean_dict(template.__dict__)
        )
        return models.EntityTemplate.from_json(data)

    def update_entity_template(
        self, template_id: str, template: models.UpdateEntityTemplateInput
    ) -> models.EntityTemplate:
        """Update an existing entity template.
        Args:
            template_id: The UUID of the template to update
            template: Updated template parameters
        Returns:
            Updated EntityTemplate object
        """
        data = self._make_request(
            "PUT", f"/entity-templates/{template_id}", json=_clean_dict(template.__dict__)
        )
        return models.EntityTemplate.from_json(data)

    def delete_entity_template(self, template_id: str) -> None:
        """Delete an entity template.
        Args:
            template_id: The UUID of the template to delete
        """
        self._make_request("DELETE", f"/entity-templates/{template_id}")

    def enable_story_templates(self) -> None:
        """Enable the Story Template feature for the Workspace."""
        self._make_request("PUT", "/entity-templates/enable")

    def disable_story_templates(self) -> None:
        """Disable the Story Template feature for the Workspace."""
        self._make_request("PUT", "/entity-templates/disable")

    ## Epic Health

    def get_epic_health(self, epic_id: int) -> models.Health:
        """Get the current health for an epic.
        Args:
            epic_id: The ID of the epic
        Returns:
            Health object
        """
        data = self._make_request("GET", f"/epics/{epic_id}/health")
        return models.Health.from_json(data)

    def create_epic_health(
        self, epic_id: int, health: models.CreateHealthInput
    ) -> models.Health:
        """Create a new health status for an epic.
        Args:
            epic_id: The ID of the epic
            health: Health parameters
        Returns:
            Created Health object
        """
        data = self._make_request(
            "POST", f"/epics/{epic_id}/health", json=_clean_dict(health.__dict__)
        )
        return models.Health.from_json(data)

    def list_epic_health_history(self, epic_id: int) -> List[models.Health]:
        """List the health history for an epic.
        Args:
            epic_id: The ID of the epic
        Returns:
            List of Health objects
        """
        data = self._make_request("GET", f"/epics/{epic_id}/health-history")
        return [models.Health.from_json(x) for x in data]

    def update_health(self, health_id: str, health: models.UpdateHealthInput) -> models.Health:
        """Update an existing health record.
        Args:
            health_id: The UUID of the health record
            health: Updated health parameters
        Returns:
            Updated Health object
        """
        data = self._make_request(
            "PUT", f"/health/{health_id}", json=_clean_dict(health.__dict__)
        )
        return models.Health.from_json(data)

    ## Epic Stories

    def list_epic_stories(
        self, epic_id: int, includes_description: Optional[bool] = None
    ) -> List[models.StorySlim]:
        """List all stories in an epic.
        Args:
            epic_id: The ID of the epic
            includes_description: Whether to include story descriptions
        Returns:
            List of StorySlim objects
        """
        params = {}
        if includes_description is not None:
            params["includes_description"] = "true" if includes_description else "false"
        data = self._make_request("GET", f"/epics/{epic_id}/stories", params=params)
        return [models.StorySlim.from_json(x) for x in data]

    def list_epics_paginated(
        self,
        includes_description: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List epics with pagination.
        Args:
            includes_description: Whether to include epic descriptions
            page: The page number to return
            page_size: The number of epics to return per page
        Returns:
            Paginated response with epics
        """
        params = {}
        if includes_description is not None:
            params["includes_description"] = includes_description
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        return self._make_request("GET", "/epics/paginated", params=params)

    def list_epic_documents(self, epic_id: int) -> List[models.DocSlim]:
        """List all documents related to an epic.
        Args:
            epic_id: The ID of the epic
        Returns:
            List of DocSlim objects
        """
        data = self._make_request("GET", f"/epics/{epic_id}/documents")
        return [models.DocSlim.from_json(x) for x in data]

    def unlink_productboard_from_epic(self, epic_id: int) -> None:
        """Unlink a productboard epic.
        Args:
            epic_id: The ID of the epic
        """
        self._make_request("POST", f"/epics/{epic_id}/unlink-productboard")

    def create_epic_comment_comment(
        self, epic_id: int, comment_id: int, comment: models.CreateStoryCommentInput
    ) -> models.ThreadedComment:
        """Create a nested comment reply to an existing epic comment.
        Args:
            epic_id: The ID of the epic
            comment_id: The ID of the parent comment
            comment: Comment parameters
        Returns:
            Created ThreadedComment object
        """
        data = self._make_request(
            "POST",
            f"/epics/{epic_id}/comments/{comment_id}",
            json=_clean_dict(comment.__dict__),
        )
        return models.ThreadedComment.from_json(data)

    ## External Link Stories

    def get_external_link_stories(self, external_link: str) -> List[models.StorySlim]:
        """Get stories which have a given external link associated with them.
        Args:
            external_link: The external link URL
        Returns:
            List of StorySlim objects
        """
        data = self._make_request(
            "GET", "/external-link/stories", params={"external_link": external_link}
        )
        return [models.StorySlim.from_json(x) for x in data]

    ## Group Stories

    def list_group_stories(
        self, group_id: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[models.StorySlim]:
        """List stories assigned to a group.
        Args:
            group_id: The UUID of the group
            limit: Maximum number of results to return
            offset: Offset at which to begin returning results
        Returns:
            List of StorySlim objects
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._make_request("GET", f"/groups/{group_id}/stories", params=params)
        return [models.StorySlim.from_json(x) for x in data]

    ## Iteration Stories

    def list_iteration_stories(
        self, iteration_id: int, includes_description: Optional[bool] = None
    ) -> List[models.StorySlim]:
        """List all stories in an iteration.
        Args:
            iteration_id: The ID of the iteration
            includes_description: Whether to include story descriptions
        Returns:
            List of StorySlim objects
        """
        params = {}
        if includes_description is not None:
            params["includes_description"] = includes_description
        data = self._make_request(
            "GET", f"/iterations/{iteration_id}/stories", params=params
        )
        return [models.StorySlim.from_json(x) for x in data]

    def enable_iterations(self) -> None:
        """Enable iterations for the current workspace."""
        self._make_request("PUT", "/iterations/enable")

    def disable_iterations(self) -> None:
        """Disable iterations for the current workspace."""
        self._make_request("PUT", "/iterations/disable")

    ## Label Epics and Stories

    def list_label_epics(self, label_id: int) -> List[models.EpicSlim]:
        """List all epics with a label.
        Args:
            label_id: The ID of the label
        Returns:
            List of EpicSlim objects
        """
        data = self._make_request("GET", f"/labels/{label_id}/epics")
        return [models.EpicSlim.from_json(x) for x in data]

    def list_label_stories(
        self, label_id: int, includes_description: Optional[bool] = None
    ) -> List[models.StorySlim]:
        """List all stories with a label.
        Args:
            label_id: The ID of the label
            includes_description: Whether to include story descriptions
        Returns:
            List of StorySlim objects
        """
        params = {}
        if includes_description is not None:
            params["includes_description"] = includes_description
        data = self._make_request("GET", f"/labels/{label_id}/stories", params=params)
        return [models.StorySlim.from_json(x) for x in data]

    ## Linked Files

    def get_linked_file(self, linked_file_id: int) -> models.LinkedFiles:
        """Get a specific linked file by ID.
        Args:
            linked_file_id: The ID of the linked file
        Returns:
            LinkedFiles object
        """
        data = self._make_request("GET", f"/linked-files/{linked_file_id}")
        return models.LinkedFiles.from_json(data)

    ## Objective Epics

    def list_objective_epics(self, objective_id: int) -> List[models.EpicSlim]:
        """List all epics related to an objective.
        Args:
            objective_id: The ID of the objective
        Returns:
            List of EpicSlim objects
        """
        data = self._make_request("GET", f"/objectives/{objective_id}/epics")
        return [models.EpicSlim.from_json(x) for x in data]

    ## Project Stories

    def list_project_stories(
        self, project_id: int, includes_description: Optional[bool] = None
    ) -> List[models.StorySlim]:
        """List all stories in a project.
        Args:
            project_id: The ID of the project
            includes_description: Whether to include story descriptions
        Returns:
            List of StorySlim objects
        """
        params = {}
        if includes_description is not None:
            params["includes_description"] = includes_description
        data = self._make_request(
            "GET", f"/projects/{project_id}/stories", params=params
        )
        return [models.StorySlim.from_json(x) for x in data]

    ## Story History

    def get_story_history(self, story_id: int) -> List[models.StoryHistory]:
        """Get the history of a story.
        Args:
            story_id: The ID of the story
        Returns:
            List of StoryHistory objects
        """
        data = self._make_request("GET", f"/stories/{story_id}/history")
        return [models.StoryHistory.from_json(x) for x in data]

    ## Story Sub-tasks

    def list_story_sub_tasks(self, story_id: int) -> List[models.StorySlim]:
        """List all sub-tasks for a story.
        Args:
            story_id: The ID of the story
        Returns:
            List of StorySlim objects
        """
        data = self._make_request("GET", f"/stories/{story_id}/sub-tasks")
        return [models.StorySlim.from_json(x) for x in data]

    ## Story Reactions

    def create_story_reaction(
        self, story_id: int, comment_id: int, emoji: str
    ) -> None:
        """Create a reaction on a story comment.
        Args:
            story_id: The ID of the story
            comment_id: The ID of the comment
            emoji: The emoji shortcode (e.g., ":thumbsup:")
        """
        self._make_request(
            "POST",
            f"/stories/{story_id}/comments/{comment_id}/reactions",
            json={"emoji": emoji},
        )

    def delete_story_reaction(
        self, story_id: int, comment_id: int, emoji: str
    ) -> None:
        """Delete a reaction from a story comment.
        Args:
            story_id: The ID of the story
            comment_id: The ID of the comment
            emoji: The emoji shortcode (e.g., ":thumbsup:")
        """
        self._make_request(
            "DELETE",
            f"/stories/{story_id}/comments/{comment_id}/reactions",
            json={"emoji": emoji},
        )

    def unlink_comment_thread_from_slack(
        self, story_id: int, comment_id: int
    ) -> None:
        """Unlink a comment thread from Slack.
        Args:
            story_id: The ID of the story
            comment_id: The ID of the comment
        """
        self._make_request(
            "POST", f"/stories/{story_id}/comments/{comment_id}/unlink-from-slack"
        )

    ## Bulk Story Operations

    def create_multiple_stories(
        self, stories: List[models.CreateStoryParams]
    ) -> List[models.StorySlim]:
        """Create multiple stories at once.
        Args:
            stories: List of story parameters
        Returns:
            List of created StorySlim objects
        """
        data = self._make_request(
            "POST", "/stories/bulk", json={"stories": [_clean_dict(s.__dict__) for s in stories]}
        )
        return [models.StorySlim.from_json(x) for x in data]

    def update_multiple_stories(self, update_input: models.UpdateStoriesInput) -> None:
        """Update multiple stories at once.
        Args:
            update_input: Update parameters including story_ids and fields to update
        """
        self._make_request("PUT", "/stories/bulk", json=_clean_dict(update_input.__dict__))

    def delete_multiple_stories(self, story_ids: List[int]) -> None:
        """Delete multiple stories at once.
        Args:
            story_ids: List of story IDs to delete
        """
        self._make_request("DELETE", "/stories/bulk", json={"story_ids": story_ids})

    def create_story_from_template(
        self, params: models.CreateStoryFromTemplateInput
    ) -> models.StorySlim:
        """Create a story from a template.
        Args:
            params: Story from template parameters
        Returns:
            Created StorySlim object
        """
        data = self._make_request(
            "POST", "/stories/from-template", json=_clean_dict(params.__dict__)
        )
        return models.StorySlim.from_json(data)

    def query_stories(self, query_input: models.QueryStoriesInput) -> models.StorySearchResults:
        """Query stories using advanced search via POST.
        Args:
            query_input: Query parameters
        Returns:
            StorySearchResults object
        """
        data = self._make_request(
            "POST", "/stories/search", json=_clean_dict(query_input.__dict__)
        )
        return models.StorySearchResults.from_json(data)

    ## Search Endpoints

    def search_epics(self, query: str, detail: str = "slim", page_size: int = 25) -> models.EpicSearchResults:
        """Search for epics.
        Args:
            query: Search query string
            detail: Level of detail ("slim" or "full")
            page_size: Number of results per page
        Returns:
            EpicSearchResults object
        """
        params = {"query": query, "detail": detail, "page_size": page_size}
        data = self._make_request("GET", "/search/epics", params=params)
        return models.EpicSearchResults.from_json(data)

    def search_iterations(self, query: str, detail: str = "slim", page_size: int = 25) -> models.IterationSearchResults:
        """Search for iterations.
        Args:
            query: Search query string
            detail: Level of detail ("slim" or "full")
            page_size: Number of results per page
        Returns:
            IterationSearchResults object
        """
        params = {"query": query, "detail": detail, "page_size": page_size}
        data = self._make_request("GET", "/search/iterations", params=params)
        return models.IterationSearchResults.from_json(data)

    def search_milestones(self, query: str, detail: str = "slim", page_size: int = 25) -> models.ObjectiveSearchResults:
        """Search for milestones (objectives).
        Args:
            query: Search query string
            detail: Level of detail ("slim" or "full")
            page_size: Number of results per page
        Returns:
            ObjectiveSearchResults object
        """
        params = {"query": query, "detail": detail, "page_size": page_size}
        data = self._make_request("GET", "/search/milestones", params=params)
        return models.ObjectiveSearchResults.from_json(data)

    def search_objectives(self, query: str, detail: str = "slim", page_size: int = 25) -> models.ObjectiveSearchResults:
        """Search for objectives.
        Args:
            query: Search query string
            detail: Level of detail ("slim" or "full")
            page_size: Number of results per page
        Returns:
            ObjectiveSearchResults object
        """
        params = {"query": query, "detail": detail, "page_size": page_size}
        data = self._make_request("GET", "/search/objectives", params=params)
        return models.ObjectiveSearchResults.from_json(data)

    def search_documents(self, query: str, detail: str = "slim", page_size: int = 25) -> models.DocumentSearchResults:
        """Search for documents.
        Args:
            query: Search query string
            detail: Level of detail ("slim" or "full")
            page_size: Number of results per page
        Returns:
            DocumentSearchResults object
        """
        params = {"query": query, "detail": detail, "page_size": page_size}
        data = self._make_request("GET", "/search/documents", params=params)
        return models.DocumentSearchResults.from_json(data)

    ## Generic Integrations (Webhooks)

    def create_generic_integration(
        self, integration: models.CreateGenericIntegrationInput
    ) -> None:
        """Create a generic integration (webhook).
        Args:
            integration: Integration parameters
        """
        self._make_request(
            "POST", "/integrations/webhook", json=_clean_dict(integration.__dict__)
        )

    def get_generic_integration(self, integration_id: int) -> Dict[str, Any]:
        """Get a generic integration by ID.
        Args:
            integration_id: The ID of the integration
        Returns:
            Integration data
        """
        return self._make_request("GET", f"/integrations/webhook/{integration_id}")

    def delete_generic_integration(self, integration_id: int) -> None:
        """Delete a generic integration.
        Args:
            integration_id: The ID of the integration to delete
        """
        self._make_request("DELETE", f"/integrations/webhook/{integration_id}")

    ## File Uploads

    def upload_files(
        self, files: Dict[str, Any], story_id: Optional[int] = None
    ) -> List[models.UploadedFile]:
        """Upload files to Shortcut.
        Args:
            files: Dictionary of file objects to upload (file0, file1, etc.)
            story_id: Optional story ID to associate files with
        Returns:
            List of UploadedFile objects
        """
        # This requires multipart/form-data, which is different from normal JSON requests
        url = f"{self.base_url}/files"
        data = {"story_id": story_id} if story_id else {}
        response = self.session.post(url, data=data, files=files)
        response.raise_for_status()
        return [models.UploadedFile.from_json(x) for x in response.json()]

    def update_uploaded_file(
        self, file_id: int, file_update: models.UpdateFileInput
    ) -> models.UploadedFile:
        """Update an uploaded file.
        Args:
            file_id: The ID of the file to update
            file_update: Updated file parameters
        Returns:
            Updated UploadedFile object
        """
        data = self._make_request(
            "PUT", f"/files/{file_id}", json=_clean_dict(file_update.__dict__)
        )
        return models.UploadedFile.from_json(data)
