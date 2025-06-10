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
            "gravatar_hash": "hash123",  # Required field
            "display_icon": None,  # Required field
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
