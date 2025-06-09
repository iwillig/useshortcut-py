# useshortcut - Python Client for Shortcut API

## Overview
This is a Python REST API client for Shortcut (formerly Clubhouse) API v3. The library provides a simple interface to interact with Shortcut's project management features.

## Project Structure
- `useshortcut/` - Main package directory
  - `client.py` - APIClient class that handles all API interactions
  - `models.py` - Data models representing Shortcut entities (Story, Epic, Project, etc.)
- `tests/` - Test files
  - `test_client.py` - Basic client tests

## Key Components

### APIClient (`useshortcut/client.py`)
The main client class that provides methods for all Shortcut API operations:
- Stories: create, update, delete, search
- Epics: list, create, update, delete
- Projects: list, create, update, delete
- Workflows: list, get specific workflow
- Labels, Categories, Iterations, etc.

### Models (`useshortcut/models.py`)
Dataclasses representing Shortcut entities:
- `Story`, `StoryInput` - Story management
- `Epic` - Epic tracking
- `Project` - Project organization
- `WorkflowState` - Workflow states
- `Member`, `Group` - User management
- And many more...

## Usage Example
```python
import os
from useshortcut.client import APIClient
import useshortcut.models as models

client = APIClient(api_token=os.environ.get("SHORTCUT_API_TOKEN"))

# Get current user
current_member = client.get_current_member()

# Search for stories
search_params = models.SearchInputs(
    query=f"owner:{current_member.mention_name}",
)
stories = client.search_stories(search_params)
```

## Testing
Run tests using the Makefile:
```bash
make test
```

Or using invoke:
```bash
pipenv run invoke test
```

This runs pytest through Pipenv.

## Building the Package
The project uses setuptools for building distributions. All package metadata is defined in `pyproject.toml` following PEP 517/518 standards.

To build the package:
```bash
python -m build
```

This will create both wheel and source distributions in the `dist/` directory.

Note: The project was migrated from Poetry to use standard setuptools with Pipenv for dependency management.

## Dependencies
- Python 3.x
- requests - HTTP client
- Pipenv - Dependency management

## Environment Variables
- `SHORTCUT_API_TOKEN` - Your Shortcut API token (required)

## Development Notes
- The client uses a session for connection pooling
- All API responses are converted to dataclass instances
- The base URL defaults to `https://api.app.shortcut.com/api/v3`
- Custom base URLs can be provided during client initialization

## Common Tasks
1. **Creating a story**:
   ```python
   story = client.create_story(models.StoryInput(
       name="New Feature",
       workflow_state_id=workflow_state_id
   ))
   ```

2. **Searching stories**:
   ```python
   results = client.search_stories(models.SearchInputs(
       query="project:backend state:in-progress"
   ))
   ```

3. **Managing projects**:
   ```python
   projects = client.list_projects()
   ```

## Known Issues/TODOs
- Some optional fields in models may need default values
- The `delete_story` method accepts a Story object instead of just an ID (needs revisiting)
- Type annotations could be improved in some areas