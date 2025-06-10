"""Demo script showing how the dynamic factory generates data from OpenAPI spec."""
from pathlib import Path
from tests.dynamic_factories import DynamicFactory
import json


def main():
    # Initialize factory with OpenAPI spec
    yaml_path = Path(__file__).parent.parent / "shortcut-api-v3.yaml"
    factory = DynamicFactory(str(yaml_path))
    
    print("=== Dynamic Factory Demo ===\n")
    
    # 1. Show available definitions
    print("1. Sample of available model definitions from OpenAPI spec:")
    definitions = sorted(factory.parser.definitions.keys())
    print(f"   Total definitions: {len(definitions)}")
    print(f"   Examples: {', '.join(definitions[:10])}...\n")
    
    # 2. Generate a Story dynamically
    print("2. Generate a Story from OpenAPI definition:")
    story = factory.create('Story')
    print(f"   Generated story with {len(story)} fields")
    print("   Sample fields:")
    for key in ['id', 'name', 'story_type', 'workflow_state_id', 'created_at']:
        if key in story:
            print(f"     - {key}: {story[key]}")
    print()
    
    # 3. Show how enums are respected
    print("3. Enum values are automatically respected:")
    stories = [factory.create('Story') for _ in range(5)]
    story_types = set(s.get('story_type') for s in stories if 'story_type' in s)
    print(f"   Generated story types: {story_types}")
    print("   (These match the enum in the OpenAPI spec)\n")
    
    # 4. Show pattern matching
    print("4. Patterns are automatically matched:")
    labels = factory.create_list('Label', count=3)
    for i, label in enumerate(labels):
        if 'color' in label:
            print(f"   Label {i+1} color: {label['color']} (matches hex pattern)")
    print()
    
    # 5. Show date-time format
    print("5. Date formats are properly generated:")
    iteration = factory.create('Iteration')
    for key in ['start_date', 'end_date', 'created_at']:
        if key in iteration:
            print(f"   {key}: {iteration[key]}")
    print()
    
    # 6. Show UUID generation
    print("6. UUIDs are generated for appropriate fields:")
    member = factory.create('Member')
    if 'id' in member:
        print(f"   Member ID: {member['id']} (UUID format)")
    if 'group_ids' in member:
        print(f"   Group IDs: {member['group_ids'][:2]}...")
    print()
    
    # 7. Show constraint handling
    print("7. Field constraints are respected:")
    story_params = factory.create('CreateStoryParams')
    if 'name' in story_params:
        print(f"   Story name length: {len(story_params['name'])} characters")
        print("   (Spec defines: minLength: 1, maxLength: 512)")
    print()
    
    # 8. Show search response generation
    print("8. Complex responses like search results:")
    search = factory.create_search_response('StorySearchResult', total=50, page_size=3)
    print(f"   Total results: {search['total']}")
    print(f"   Items returned: {len(search['data'])}")
    print(f"   Has pagination: {'next' in search and search['next'] is not None}")
    print()
    
    # 9. Show how to override values
    print("9. Override specific values while keeping others dynamic:")
    custom_story = factory.create('Story', 
        name="My Custom Story",
        story_type="bug",
        completed=True
    )
    print(f"   Name: {custom_story['name']} (overridden)")
    print(f"   Type: {custom_story['story_type']} (overridden)")
    print(f"   Completed: {custom_story['completed']} (overridden)")
    print(f"   ID: {custom_story.get('id')} (dynamically generated)")
    print(f"   Created: {custom_story.get('created_at')} (dynamically generated)")


if __name__ == '__main__':
    main()