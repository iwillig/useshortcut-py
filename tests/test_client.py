from useshortcut.client import APIClient
from useshortcut.models import Story, StoryInput
import requests
import os


def test_client():
    client = APIClient(api_token=os.environ.get("SHORTCUT_API_TOKEN"))

    ## assert client.list_workflows() is None

    # for workflow in client.list_workflows():
    #     print(workflow["name"], workflow["id"])

    workflow = client.get_workflow("1488")

    ##print(workflow)
    ##print(workflow.keys())

    # for state in workflow["states"]:
    #     print(state["id"])

    try:
        epics = client.list_epics()

        for epic in epics:
            print("epic", epic.id, epic.name)

        iterations = client.list_iterations()
        for iteration in iterations:
            print("iteration", iteration.id, iteration.name)

        story = client.create_story(
            StoryInput(name="Test Story", workflow_state_id=500104846),
        )

        print("new", story)

        resp = client.delete_story(story)
        print(resp)
    except requests.exceptions.RequestException as e:
        print(e)
        print(e.response.json())

    assert client is None
    assert {} is None