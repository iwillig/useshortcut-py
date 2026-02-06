from useshortcut import client, models

client = client.APIClient(api_token="<>")

epic_id = 292772
print(client.get_epic(epic_id))
print(client.update_epic(epic_id, models.UpdateEpicInput(name="Risk Action Plans")))
