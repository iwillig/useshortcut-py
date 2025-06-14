# Test Plan for New Shortcut API Endpoints

## Overview
This plan outlines the testing strategy for the newly implemented endpoints in Phase 1: Comments, Tasks, Milestones, and Custom Fields.

## Testing Approach

### 1. Unit Tests
Each endpoint will have unit tests using `pytest` and `requests_mock` to mock API responses. Tests will follow the existing pattern in the codebase.

### 2. Test Structure
- **Fixtures**: Reusable test data and mock responses
- **Mocking**: Use `requests_mock` to mock HTTP responses
- **Assertions**: Verify correct models are returned and data is properly parsed

## Test Implementation Plan

### 1. Comments System Tests (`test_comments.py`)

#### Story Comments Tests
- `test_list_story_comments()` - Test listing all comments for a story
- `test_create_story_comment()` - Test creating a new comment
- `test_create_story_comment_with_parent()` - Test creating a threaded comment
- `test_get_story_comment()` - Test fetching a specific comment
- `test_update_story_comment()` - Test updating comment text
- `test_delete_story_comment()` - Test deleting a comment
- `test_story_comment_with_reactions()` - Test comment with emoji reactions
- `test_story_comment_datetime_parsing()` - Test datetime field parsing

#### Epic Comments Tests
- `test_list_epic_comments()` - Test listing all comments for an epic
- `test_create_epic_comment()` - Test creating a new comment
- `test_get_epic_comment()` - Test fetching a specific comment
- `test_update_epic_comment()` - Test updating comment text
- `test_delete_epic_comment()` - Test deleting a comment
- `test_threaded_comment_parsing()` - Test nested comment structure

### 2. Tasks System Tests (`test_tasks.py`)

#### Story Tasks Tests
- `test_list_story_tasks()` - Test listing all tasks for a story
- `test_create_story_task()` - Test creating a new task
- `test_create_story_task_with_owners()` - Test creating task with owner assignments
- `test_get_story_task()` - Test fetching a specific task
- `test_update_story_task()` - Test updating task properties
- `test_update_story_task_complete_status()` - Test marking task as complete
- `test_update_story_task_reorder()` - Test reordering tasks (before_id/after_id)
- `test_delete_story_task()` - Test deleting a task
- `test_task_datetime_parsing()` - Test datetime field parsing

### 3. Milestones System Tests (`test_milestones.py`)

#### Milestone CRUD Tests
- `test_list_milestones()` - Test listing all milestones
- `test_get_milestone()` - Test fetching a specific milestone
- `test_create_milestone()` - Test creating a new milestone
- `test_create_milestone_with_categories()` - Test creating with categories
- `test_update_milestone()` - Test updating milestone properties
- `test_update_milestone_state()` - Test changing milestone state
- `test_update_milestone_reorder()` - Test reordering milestones
- `test_delete_milestone()` - Test deleting a milestone
- `test_milestone_stats_parsing()` - Test MilestoneStats model parsing

#### Related Endpoints Tests
- `test_list_milestone_epics()` - Test fetching epics for a milestone
- `test_list_category_milestones()` - Test fetching milestones in a category

### 4. Custom Fields Tests (`test_custom_fields.py`)

#### Custom Field Tests
- `test_list_custom_fields()` - Test listing all custom fields
- `test_get_custom_field()` - Test fetching a specific custom field
- `test_update_custom_field()` - Test updating custom field properties
- `test_update_custom_field_values()` - Test updating enum values
- `test_update_custom_field_reorder()` - Test reordering custom fields
- `test_delete_custom_field()` - Test deleting a custom field
- `test_custom_field_enum_values_parsing()` - Test parsing enum values

## Test Data Fixtures

### Comment Fixtures
```python
@pytest.fixture
def story_comment_data():
    return {
        "id": 123,
        "text": "This is a test comment",
        "author_id": "12345678-1234-1234-1234-123456789012",
        "created_at": "2023-01-01T00:00:00Z",
        "entity_type": "story-comment",
        "story_id": 456,
        "position": 1,
        "reactions": [
            {"emoji": "👍", "permission_ids": ["user-123", "user-456"]}
        ]
    }
```

### Task Fixtures
```python
@pytest.fixture
def task_data():
    return {
        "id": 789,
        "description": "Complete unit tests",
        "complete": False,
        "story_id": 456,
        "entity_type": "task",
        "position": 1,
        "created_at": "2023-01-01T00:00:00Z",
        "owner_ids": ["12345678-1234-1234-1234-123456789012"]
    }
```

### Milestone Fixtures
```python
@pytest.fixture
def milestone_data():
    return {
        "id": 111,
        "name": "Q1 2024 Release",
        "description": "First quarter release",
        "state": "in progress",
        "position": 1,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z",
        "entity_type": "milestone",
        "app_url": "https://app.shortcut.com/workspace/milestone/111",
        "global_id": "milestone-111",
        "stats": {
            "num_related_documents": 5,
            "average_cycle_time": 86400,
            "average_lead_time": 172800
        },
        "categories": []
    }
```

### Custom Field Fixtures
```python
@pytest.fixture
def custom_field_data():
    return {
        "id": "cf-12345678-1234-1234-1234-123456789012",
        "name": "Priority",
        "field_type": "enum",
        "position": 1,
        "enabled": True,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z",
        "entity_type": "custom-field",
        "values": [
            {
                "id": "cfv-1",
                "value": "High",
                "position": 1,
                "color_key": "red",
                "entity_type": "custom-field-enum-value",
                "enabled": True
            },
            {
                "id": "cfv-2",
                "value": "Medium",
                "position": 2,
                "color_key": "yellow",
                "entity_type": "custom-field-enum-value",
                "enabled": True
            }
        ]
    }
```

## Error Handling Tests

Each test module should include error handling tests:
- Test 404 responses (resource not found)
- Test 401 responses (unauthorized)
- Test 400 responses (bad request)
- Test 500 responses (server error)

Example:
```python
def test_get_story_comment_not_found(requests_mock, api_client, base_url):
    requests_mock.get(
        f"{base_url}/stories/456/comments/999",
        status_code=404,
        json={"message": "Comment not found"}
    )
    
    with pytest.raises(requests.exceptions.HTTPError):
        api_client.get_story_comment(456, 999)
```

## Integration Tests

Mark integration tests that require a real API token:
```python
@pytest.mark.integration
def test_create_and_delete_comment_integration(api_client_with_real_token):
    # This test would run against the real API
    pass
```

## Test Execution Strategy

1. **Run unit tests first** (fast, no API required):
   ```bash
   pytest tests/test_comments.py tests/test_tasks.py tests/test_milestones.py tests/test_custom_fields.py -v
   ```

2. **Run integration tests separately** (requires API token):
   ```bash
   pytest -m integration -v
   ```

3. **Coverage report**:
   ```bash
   pytest --cov=useshortcut --cov-report=html
   ```

## Success Criteria

- All new endpoints have at least one happy path test
- All model parsing is tested, especially datetime conversions
- Error cases are covered (404, 401, etc.)
- Code coverage for new code is >90%
- All tests pass in CI/CD pipeline