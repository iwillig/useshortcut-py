# Breaking Changes

## Version 0.0.2 (Upcoming)

### Changed Method Signatures

#### `delete_story` Method
The `delete_story` method signature has been changed to match other delete methods in the client.

**Before:**
```python
def delete_story(self, story: models.Story) -> Any:
    """Delete a story by passing the story object"""
    ...
```

**After:**
```python
def delete_story(self, story_id: int) -> None:
    """Delete a story by passing the story ID"""
    ...
```

**Migration Guide:**
```python
# Old usage
story = client.get_story(123)
client.delete_story(story)

# New usage
story = client.get_story(123)
client.delete_story(story.id)

# Or directly with ID
client.delete_story(123)
```

**Rationale:**
- Consistency with all other delete methods in the client (`delete_epic`, `delete_project`, etc.)
- Simpler API - no need to fetch the full story object just to delete it
- Aligns with REST API best practices where DELETE operations use resource IDs
- Matches the underlying API which expects `/api/v3/stories/{story-id}`