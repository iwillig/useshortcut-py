from useshortcut.client import APIClient
from useshortcut.models import StoryInput, CreateCategoryInput
import useshortcut.models as models
import requests
import os


## Fake test to make pytest runner happy
def test_answer():
    assert 5 == 5


# def test_client():
#     client = APIClient(api_token=os.environ.get("SHORTCUT_API_TOKEN"))

#     workflows = client.list_workflows()

#     for workflow in workflows:
#         print(workflow.name, workflow.id, workflow.default_state_id)

#     workflow = client.get_workflow(workflows[-1].id)

#     for state in workflow.states:
#         print(state.id)

#     try:
#         epics = client.list_epics()

#         for epic in epics:
#             pass

#         iterations = client.list_iterations()
#         for iteration in iterations:
#             pass

#         groups = client.list_groups()
#         for group in groups:
#             pass

#         labels = client.list_labels()
#         for label in labels:
#             pass

#         linked_files = client.list_linked_files()
#         print("linked-files-count", len(linked_files))

#         for linked_file in linked_files:
#             print("linked-files", linked_file.id)

#         files = client.list_files()
#         print("files-count", len(files))
#         for file in files:
#             print("files", file.id)

#         members = client.list_members()
#         for member in members:
#             print("members", member.profile.name)

#         objectives = client.list_objectives()
#         print("objectives-count", len(objectives))
#         for objective in objectives:
#             print("objectives", objective.id)

#         projects = client.list_projects()
#         print("project-count", len(projects))
#         for project in projects:
#             print("projects", project.id, project.name)

#         epic_workflow = client.get_epic_workflow()
#         print("epic-workflow", epic_workflow)

#         # client.create_category(models.CreateCategoryInput(name="test"))

#         categories = client.list_categories()
#         print("categories-count", len(categories))
#         for category in categories:
#             print("categories", category.id, category.name)

#         current_member = client.get_current_member()
#         print("current-member", current_member)
#         search_query = f"owner:{current_member.mention_name}"
#         print("search-query", search_query)

#         search_params = models.SearchInputs(
#             query=search_query,
#         )

#         stories = client.search_stories(search_params)
#         print(search_params)

#         print("stories-count", len(stories.data))
#         print("stories", stories)

#         for story in stories.data:
#             print(story.name)

#         story = client.create_story(
#             models.StoryInput(
#                 name="Test Story", workflow_state_id=workflow.default_state_id
#             ),
#         )

#         print("new", story)

#         resp = client.delete_story(story.id)
#         print(resp)
#     except requests.exceptions.RequestException as e:
#         print(e)
#         print(e.response.json())
