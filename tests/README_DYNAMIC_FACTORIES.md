# Dynamic Factory System for Shortcut API Tests

## Overview

The dynamic factory system automatically generates mock data for tests by parsing the OpenAPI specification. This ensures that test data always matches the current API schema without manual maintenance.

## Key Features

### 1. **Automatic Schema Parsing**
- Reads the `shortcut-api-v3.yaml` OpenAPI specification
- Extracts model definitions, field types, constraints, and enums
- No hard-coded test data needed

### 2. **Smart Data Generation**
- **Enums**: Automatically uses valid enum values from the spec
- **Patterns**: Generates data matching regex patterns (e.g., hex colors)
- **Formats**: Handles special formats like UUID, date-time, email, URL
- **Constraints**: Respects minLength, maxLength, minimum, maximum
- **Types**: Properly generates strings, integers, booleans, arrays, objects

### 3. **Contextual Generation**
- Field names influence generated data (e.g., "email" fields get email addresses)
- Arrays have realistic sizes based on field purpose
- Related fields maintain consistency

## Usage Examples

### Basic Usage

```python
from tests.dynamic_factories import DynamicFactory

# Initialize with OpenAPI spec
factory = DynamicFactory("shortcut-api-v3.yaml")

# Generate a complete Story object
story = factory.create('Story')

# Generate with overrides
story = factory.create('Story', 
    name="My Custom Story",
    story_type="bug"
)

# Generate a list
stories = factory.create_list('Story', count=5)

# Generate search response
response = factory.create_search_response('StorySearchResult', total=100, page_size=20)
```

### In Tests

```python
def test_create_story_dynamic(self, requests_mock, api_client, factory):
    # Generate input from schema
    story_input_data = factory.create('CreateStoryParams')
    
    # Generate expected response
    story_response = factory.create('Story', id=1001)
    
    # Mock the API call
    requests_mock.post(f"{base_url}/stories", json=story_response)
    
    # Test the client
    story = api_client.create_story(story_input)
    assert story.id == 1001
```

## How It Works

### 1. Schema Parsing
The `OpenAPISchemaParser` class reads the YAML file and extracts:
- Model definitions from `definitions` section
- Path definitions from `paths` section
- Field types, formats, patterns, and constraints

### 2. Dynamic Generation
The `DynamicDataGenerator` class generates values based on:
- **Type**: string, integer, boolean, array, object
- **Format**: uuid, date-time, email, uri
- **Pattern**: Regular expressions like `^#[a-fA-F0-9]{6}$`
- **Constraints**: minLength, maxLength, enum values
- **Context**: Field names influence generation

### 3. Special Handling

#### Enums
```yaml
story_type:
  type: string
  enum: ["feature", "chore", "bug"]
```
Generated values will only be from the enum list.

#### Patterns
```yaml
color:
  type: string
  pattern: "^#[a-fA-F0-9]{6}$"
```
Generated values match the pattern (e.g., `#ff5733`).

#### Formats
```yaml
id:
  type: string
  format: uuid
```
Generated values use appropriate format (e.g., `550e8400-e29b-41d4-a716-446655440000`).

## Benefits

1. **Always Up-to-Date**: Test data automatically matches the current API schema
2. **No Maintenance**: No need to update test fixtures when API changes
3. **Realistic Data**: Generated data follows actual API constraints
4. **Flexible**: Easy to override specific fields while keeping others dynamic
5. **Comprehensive**: Handles all OpenAPI data types and constraints

## Files

- `dynamic_factories.py`: Core factory implementation
- `test_dynamic_api_client.py`: Tests using dynamic factories
- `test_factory_examples.py`: Examples and demonstrations
- `demo_dynamic_factory.py`: Standalone demo script

## Future Enhancements

1. **Relationship Consistency**: Ensure related IDs reference valid objects
2. **State Machines**: Generate valid state transitions
3. **Business Rules**: Apply domain-specific logic
4. **Performance**: Cache parsed schemas for faster generation
5. **Validation**: Validate generated data against schema