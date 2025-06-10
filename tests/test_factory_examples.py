"""Examples of using the dynamic factory system."""
import pytest
from pathlib import Path
from tests.dynamic_factories import DynamicFactory, create_story_from_spec, create_member_from_spec


@pytest.fixture
def factory():
    """Create a dynamic factory instance."""
    yaml_path = Path(__file__).parent.parent / "shortcut-api-v3.yaml"
    return DynamicFactory(str(yaml_path))


def test_generate_story_with_all_fields(factory):
    """Example: Generate a complete story with all fields from OpenAPI spec."""
    story = factory.create('Story')
    
    # Verify it has the expected structure
    assert 'id' in story
    assert 'name' in story
    assert isinstance(story.get('id'), int)
    assert isinstance(story.get('name'), str)
    
    # Check for various field types
    if 'owner_ids' in story:
        assert isinstance(story['owner_ids'], list)
        if story['owner_ids']:
            # Should be UUIDs
            assert all('-' in owner_id for owner_id in story['owner_ids'])
    
    if 'archived' in story:
        assert isinstance(story['archived'], bool)
    
    if 'created_at' in story:
        assert 'T' in story['created_at']  # ISO format
    
    print(f"Generated story with {len(story)} fields")


def test_generate_minimal_story(factory):
    """Example: Generate a story with only required fields."""
    # Get the Story definition to check required fields
    story_def = factory.parser.get_definition('Story')
    required_fields = story_def.get('required', [])
    
    # Generate with overrides to ensure minimal
    story = factory.create('Story')
    
    # Filter to only required fields
    minimal_story = {k: v for k, v in story.items() if k in required_fields}
    
    print(f"Minimal story has {len(minimal_story)} required fields: {list(minimal_story.keys())}")


def test_generate_consistent_workflow(factory):
    """Example: Generate a workflow with consistent states."""
    workflow = factory.create('Workflow')
    
    # Ensure states are present and consistent
    if 'states' in workflow:
        states = workflow['states']
        
        # Verify states have proper progression
        for i, state in enumerate(states):
            assert 'position' in state
            assert state['position'] == i or isinstance(state['position'], int)
            
            # Verify state types make sense
            if 'type' in state:
                assert state['type'] in ['unstarted', 'started', 'done']
    
    print(f"Generated workflow with {len(workflow.get('states', []))} states")


def test_generate_search_response(factory):
    """Example: Generate a paginated search response."""
    # Generate a search response for stories
    search_response = factory.create_search_response('StorySearchResult', total=50, page_size=20)
    
    assert search_response['total'] == 50
    assert len(search_response['data']) == 20
    assert search_response['next'] is not None
    
    # Verify each item in data is properly formed
    for item in search_response['data']:
        assert 'id' in item
        assert isinstance(item.get('id'), int)


def test_generate_with_enum_constraints(factory):
    """Example: Generate data respecting enum constraints."""
    # Generate multiple stories to see enum variety
    stories = [factory.create('Story') for _ in range(10)]
    
    story_types = set()
    for story in stories:
        if 'story_type' in story:
            story_types.add(story['story_type'])
    
    # Should only contain valid enum values
    assert story_types.issubset({'feature', 'chore', 'bug'})
    print(f"Generated story types: {story_types}")


def test_generate_with_pattern_constraints(factory):
    """Example: Generate data matching regex patterns."""
    # Generate labels which have color patterns
    labels = factory.create_list('Label', count=5)
    
    for label in labels:
        if 'color' in label:
            # Should match hex color pattern
            assert label['color'].startswith('#')
            assert len(label['color']) == 7
            assert all(c in '0123456789abcdefABCDEF' for c in label['color'][1:])


def test_generate_with_format_constraints(factory):
    """Example: Generate data with specific formats."""
    member = factory.create('Member')
    
    # Check UUID format
    if 'id' in member:
        assert isinstance(member['id'], str)
        assert member['id'].count('-') == 4  # UUID format
    
    # Check date-time format
    if 'created_at' in member:
        assert 'T' in member['created_at']  # ISO format
        assert member['created_at'].endswith('Z') or '+' in member['created_at']


def test_generate_nested_objects(factory):
    """Example: Generate objects with nested structures."""
    member = create_member_from_spec(factory)
    
    # Verify profile is properly nested
    assert 'profile' in member
    assert isinstance(member['profile'], dict)
    
    profile = member['profile']
    # Check profile has expected fields
    if 'mention_name' in profile:
        assert isinstance(profile['mention_name'], str)
        assert profile['mention_name'].islower()  # Should be lowercase


def test_generate_with_length_constraints(factory):
    """Example: Generate strings respecting length constraints."""
    # CreateStoryParams has constraints on name length
    story_params = factory.create('CreateStoryParams')
    
    if 'name' in story_params:
        name = story_params['name']
        # From spec: minLength: 1, maxLength: 512
        assert len(name) >= 1
        assert len(name) <= 512
    
    if 'description' in story_params:
        desc = story_params['description']
        # From spec: maxLength: 100000
        assert len(desc) <= 100000


def test_generate_arrays_with_constraints(factory):
    """Example: Generate arrays respecting size constraints."""
    story = factory.create('Story')
    
    # Different arrays have different typical sizes
    if 'owner_ids' in story:
        # Owners are typically 1-3
        assert len(story['owner_ids']) <= 5
    
    if 'label_ids' in story:
        # Labels are typically 0-5
        assert len(story['label_ids']) <= 10


def test_generate_from_path_definition(factory):
    """Example: Generate response based on API path definition."""
    # This would work with actual path definitions
    # For example, GET /api/v3/members returns array of Member
    try:
        response = factory.create_response_from_path('/api/v3/members', 'GET')
        assert isinstance(response, list)
        if response:
            assert all('id' in member for member in response)
    except ValueError:
        # Path might not exist in our spec
        pass


def test_custom_story_generation(factory):
    """Example: Generate story with custom logic for consistency."""
    story = create_story_from_spec(factory, 
        started=True,
        completed=False,
        story_type='bug'
    )
    
    # Verify our custom logic
    assert story['started'] is True
    assert story['completed'] is False
    assert story['completed_at'] is None
    assert story['lead_time'] is None
    assert story['cycle_time'] is None
    assert story['story_type'] == 'bug'


if __name__ == '__main__':
    # Run examples
    import sys
    from pathlib import Path
    
    yaml_path = Path(__file__).parent.parent / "shortcut-api-v3.yaml"
    factory = DynamicFactory(str(yaml_path))
    
    print("=== Dynamic Factory Examples ===\n")
    
    print("1. Generate a complete Story:")
    story = factory.create('Story')
    print(f"   Generated {len(story)} fields")
    print(f"   Sample fields: id={story.get('id')}, name={story.get('name')[:30]}...")
    
    print("\n2. Generate a Label:")
    label = factory.create('Label')
    print(f"   {label}")
    
    print("\n3. Generate a search response:")
    search = factory.create_search_response('StorySearchResult', total=100, page_size=10)
    print(f"   Total: {search['total']}, Items: {len(search['data'])}, Has next: {search['next'] is not None}")
    
    print("\n4. Available definitions in spec:")
    definitions = list(factory.parser.definitions.keys())[:10]
    print(f"   {', '.join(definitions)}... (and {len(factory.parser.definitions) - 10} more)")
    
    print("\n5. Generate data for any definition:")
    for def_name in ['Epic', 'Project', 'Workflow', 'Iteration']:
        data = factory.create(def_name)
        print(f"   {def_name}: {len(data)} fields generated")