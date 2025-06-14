# useshortcut

A python REST API Client for the v3 of the Shortcut API.

## Installation

You can install `useshortcut` using pip:

```bash
pip install useshortcut
```

Or if you're using pipenv:

```bash
pipenv install useshortcut
```

## Quick Start

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

## Development

### Setting up the development environment

1. Clone the repository:
```bash
git clone https://github.com/your-username/useshortcut-py.git
cd useshortcut-py
```

2. Install pipenv if you haven't already:
```bash
pip install pipenv
```

3. Install development dependencies:
```bash
pipenv install --dev
```

4. Activate the virtual environment:
```bash
pipenv shell
```

### Running Tests

There are several ways to run the tests:

Using make:
```bash
make test
```

Using pipenv directly:
```bash
pipenv run pytest
```

Using invoke:
```bash
pipenv run invoke test
```

To run tests with coverage:
```bash
pipenv run pytest --cov=useshortcut
```

### Environment Variables

You'll need to set up the following environment variable for development:

- `SHORTCUT_API_TOKEN`: Your Shortcut API token

You can create a `.env` file in the project root (it will be ignored by git):
```bash
SHORTCUT_API_TOKEN=your_api_token_here
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
