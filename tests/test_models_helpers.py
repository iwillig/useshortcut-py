"""Helper functions to create mock data that works with current model limitations."""


def minimal_member_response():
    """Create a minimal member response that will work with the current models."""
    return {
        "id": "12345678-1234-1234-1234-123456789012",
        "role": "member",
        "disabled": False,
        "state": "full",
        "group_ids": ["87654321-4321-4321-4321-210987654321"],
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "profile": {
            "id": "12345678-1234-1234-1234-123456789012",
            "mention_name": "testuser",
            "name": "Test User",
            "email_address": "test@example.com",
            "is_owner": False,
            "deactivated": False,
            "two_factor_auth_activated": True,
            "gravatar_hash": None,  # Required but nullable
            "display_icon": None,  # Required but nullable
        },
    }


def minimal_workflow_state():
    """Create a minimal workflow state that will work with the current models."""
    return {
        "id": 500000,
        "global_id": "wf-state-500000",
        "name": "Unstarted",
        "type": "unstarted",
        "description": "",
        "verb": "start",
        "num_stories": 0,
        "num_story_templates": 0,
        "position": 0,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "entity_type": "workflow-state",  # Added required field
    }


def minimal_project_response():
    """Create a minimal project response that will work with the current models."""
    return {
        "id": 3001,
        "name": "Backend Project",
        "description": "Backend services",
        "abbreviation": "BE",
        "archived": False,
        "color": "#ff0000",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
    }


def minimal_group_response():
    """Create a minimal group response that will work with the current models."""
    return {
        "id": "12345678-1234-1234-1234-123456789012",
        "global_id": "grp-12345678",
        "name": "Engineering",
        "mention_name": "engineering",
        "description": "Engineering team",
        "archived": False,
        "color": "#0066cc",
        "color_key": "blue",
        "workflow_ids": [100],
        "member_ids": ["11111111-1111-1111-1111-111111111111"],
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "entity_type": "group",
        "app_url": "https://app.shortcut.com/workspace/group/12345678",
        "num_stories": 0,
        "num_stories_started": 0,
        "num_stories_backlog": 0,
        "num_epics_started": 0,
        "display_icon": None,
    }
