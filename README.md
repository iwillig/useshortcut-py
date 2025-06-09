# useshortcut

A python REST API Client for the v3 of the Shortcut API.

```python
import os
from useshortcut.client import APIClient
import useshortcut.models as models

client = APIClient(api_token=os.environ.get("SHORTCUT_API_TOKEN"))

# Get the current user
current_member = client.get_current_member()

# Find all the stories that I own
search_params = models.SearchInputs(
    query=f"owner:{current_member.mention_name}",
)
# Print all the story ids that I own.
stories = client.search_stories(search_params)
for story in stories.data:
    print(story.id)
```
