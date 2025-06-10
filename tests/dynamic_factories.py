"""Dynamic factory system that generates mock data from OpenAPI schema."""

import yaml
import random
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union
from faker import Faker


fake = Faker()


class OpenAPISchemaParser:
    """Parse OpenAPI schema and generate mock data based on definitions."""

    def __init__(self, yaml_path: str):
        """Initialize with OpenAPI YAML file."""
        with open(yaml_path, "r") as f:
            self.spec = yaml.safe_load(f)

        self.definitions = self.spec.get("definitions", {})
        self.paths = self.spec.get("paths", {})

    def get_definition(self, name: str) -> Dict[str, Any]:
        """Get a definition by name."""
        return self.definitions.get(name, {})

    def get_enum_values(self, property_schema: Dict[str, Any]) -> Optional[List[str]]:
        """Extract enum values from a property schema."""
        return property_schema.get("enum")

    def get_pattern(self, property_schema: Dict[str, Any]) -> Optional[str]:
        """Extract pattern from a property schema."""
        return property_schema.get("pattern")

    def get_format(self, property_schema: Dict[str, Any]) -> Optional[str]:
        """Extract format from a property schema."""
        return property_schema.get("format")

    def get_constraints(self, property_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Extract constraints like minLength, maxLength, etc."""
        constraints = {}
        for key in [
            "minLength",
            "maxLength",
            "minimum",
            "maximum",
            "minItems",
            "maxItems",
        ]:
            if key in property_schema:
                constraints[key] = property_schema[key]
        return constraints


class DynamicDataGenerator:
    """Generate mock data based on OpenAPI schema types and constraints."""

    def __init__(self, schema_parser: OpenAPISchemaParser):
        self.parser = schema_parser
        self._id_counter = 1000

    def generate_value(
        self, property_schema: Dict[str, Any], property_name: str = ""
    ) -> Any:
        """Generate a value based on property schema."""
        # Check for enum first
        enum_values = self.parser.get_enum_values(property_schema)
        if enum_values:
            return random.choice(enum_values)

        # Check for $ref
        if "$ref" in property_schema:
            ref_name = property_schema["$ref"].split("/")[-1]
            return self.generate_from_definition(ref_name)

        # Get type and format
        prop_type = property_schema.get("type", "string")
        prop_format = property_schema.get("format")
        pattern = property_schema.get("pattern")
        constraints = self.parser.get_constraints(property_schema)

        # Handle based on type
        if prop_type == "string":
            return self._generate_string(
                property_name, prop_format, pattern, constraints
            )
        elif prop_type == "integer":
            return self._generate_integer(property_name, prop_format, constraints)
        elif prop_type == "number":
            return self._generate_number(property_name, prop_format, constraints)
        elif prop_type == "boolean":
            return self._generate_boolean(property_name)
        elif prop_type == "array":
            return self._generate_array(property_schema, property_name)
        elif prop_type == "object":
            return self._generate_object(property_schema)

        return None

    def _generate_string(
        self,
        name: str,
        format: Optional[str],
        pattern: Optional[str],
        constraints: Dict[str, Any],
    ) -> str:
        """Generate string based on format, pattern, and constraints."""
        # Handle specific formats
        if format == "uuid":
            return str(fake.uuid4())
        elif format == "date-time":
            return fake.date_time_between(
                start_date="-1y", end_date="now", tzinfo=timezone.utc
            ).isoformat()
        elif format == "date":
            return fake.date_between(start_date="-1y", end_date="+1y").isoformat()
        elif format == "email":
            return fake.email()
        elif format == "uri" or format == "url":
            return fake.url()

        # Handle patterns
        if pattern:
            return self._generate_from_pattern(pattern)

        # Handle based on property name
        if "color" in name.lower():
            return f"#{fake.random_int(0, 16777215):06x}"
        elif "name" in name.lower():
            if "mention" in name.lower():
                return fake.user_name().lower().replace("-", "_")
            elif "story" in name.lower() or "epic" in name.lower():
                return fake.catch_phrase()
            else:
                return fake.word().capitalize()
        elif "description" in name.lower():
            max_length = constraints.get("maxLength", 500)
            return fake.text(max_nb_chars=min(max_length, 500))
        elif "url" in name.lower() or "link" in name.lower():
            return fake.url()
        elif "email" in name.lower():
            return fake.email()
        elif "hash" in name.lower():
            return fake.md5()
        elif "id" in name.lower() and "external" in name.lower():
            return f"ext-{fake.lexify('????')}-{fake.lexify('????')}"

        # Default string generation with constraints
        min_length = constraints.get("minLength", 1)
        max_length = constraints.get("maxLength", 50)

        if max_length <= 20:
            return fake.word()[:max_length]
        else:
            return fake.text(max_nb_chars=max_length)[:max_length]

    def _generate_integer(
        self, name: str, format: Optional[str], constraints: Dict[str, Any]
    ) -> int:
        """Generate integer based on format and constraints."""
        minimum = constraints.get("minimum", 1)
        maximum = constraints.get("maximum", 999999)

        # Handle specific property names
        if "id" in name.lower() and format == "int64":
            self._id_counter += 1
            return self._id_counter
        elif "position" in name.lower():
            return fake.random_int(1000, 100000)
        elif "estimate" in name.lower():
            return random.choice([0, 1, 2, 3, 5, 8, 13, 21])  # Fibonacci
        elif "count" in name.lower() or "num" in name.lower():
            return fake.random_int(0, 100)
        elif "time" in name.lower() and (
            "lead" in name.lower() or "cycle" in name.lower()
        ):
            return fake.random_int(3600, 604800)  # 1 hour to 1 week in seconds

        return fake.random_int(minimum, maximum)

    def _generate_number(
        self, name: str, format: Optional[str], constraints: Dict[str, Any]
    ) -> float:
        """Generate number based on format and constraints."""
        minimum = constraints.get("minimum", 0.0)
        maximum = constraints.get("maximum", 1000.0)
        return round(random.uniform(minimum, maximum), 2)

    def _generate_boolean(self, name: str) -> bool:
        """Generate boolean based on property name."""
        # Adjust probability based on property name
        if "archived" in name.lower() or "disabled" in name.lower():
            return fake.boolean(chance_of_getting_true=10)
        elif "completed" in name.lower() or "started" in name.lower():
            return fake.boolean(chance_of_getting_true=50)
        elif "blocked" in name.lower() or "blocker" in name.lower():
            return fake.boolean(chance_of_getting_true=15)

        return fake.boolean()

    def _generate_array(
        self, property_schema: Dict[str, Any], property_name: str
    ) -> List[Any]:
        """Generate array based on items schema."""
        items_schema = property_schema.get("items", {})
        constraints = self.parser.get_constraints(property_schema)

        min_items = constraints.get("minItems", 0)
        max_items = constraints.get("maxItems", 5)

        # Adjust array size based on property name
        if "owner" in property_name.lower():
            count = fake.random_int(1, min(3, max_items))
        elif "label" in property_name.lower() or "tag" in property_name.lower():
            count = fake.random_int(0, min(5, max_items))
        else:
            count = fake.random_int(min_items, min(max_items, 10))

        return [self.generate_value(items_schema, property_name) for _ in range(count)]

    def _generate_object(self, property_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate object based on properties schema."""
        properties = property_schema.get("properties", {})
        required = property_schema.get("required", [])
        result = {}

        for prop_name, prop_schema in properties.items():
            # Include required fields and optional fields with some probability
            if prop_name in required or fake.boolean(chance_of_getting_true=70):
                result[prop_name] = self.generate_value(prop_schema, prop_name)

        return result

    def _generate_from_pattern(self, pattern: str) -> str:
        """Generate string matching a regex pattern."""
        # Handle common patterns
        if pattern == r"^#[a-fA-F0-9]{6}$":
            return f"#{fake.random_int(0, 16777215):06x}"
        elif pattern == r"^https?://.+$":
            return fake.url()
        elif pattern == r"^[a-z0-9\-\_\.]+$":
            return fake.slug()

        # For other patterns, return a simple matching string
        return fake.lexify("????????")

    def generate_from_definition(
        self, definition_name: str, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate data for a specific definition from the OpenAPI spec."""
        definition = self.parser.get_definition(definition_name)
        if not definition:
            raise ValueError(
                f"Definition '{definition_name}' not found in OpenAPI spec"
            )

        properties = definition.get("properties", {})
        required = definition.get("required", [])
        result = {}

        # Generate each property
        for prop_name, prop_schema in properties.items():
            # Skip if x-nullable is true and randomly decide to omit
            if prop_schema.get("x-nullable") and fake.boolean(
                chance_of_getting_true=30
            ):
                continue

            # Include required fields always, optional fields with probability
            if prop_name in required or fake.boolean(chance_of_getting_true=70):
                result[prop_name] = self.generate_value(prop_schema, prop_name)

        # Apply any overrides
        if overrides:
            result.update(overrides)

        return result


class DynamicFactory:
    """Factory that uses OpenAPI spec to generate mock data."""

    def __init__(self, yaml_path: str = "shortcut-api-v3.yaml"):
        self.parser = OpenAPISchemaParser(yaml_path)
        self.generator = DynamicDataGenerator(self.parser)

    def create(self, model_name: str, **overrides) -> Dict[str, Any]:
        """Create a mock instance of a model."""
        return self.generator.generate_from_definition(model_name, overrides)

    def create_list(
        self, model_name: str, count: int = 5, **overrides
    ) -> List[Dict[str, Any]]:
        """Create a list of mock instances."""
        return [self.create(model_name, **overrides) for _ in range(count)]

    def create_search_response(
        self, model_name: str, total: int = 10, page_size: int = 10
    ) -> Dict[str, Any]:
        """Create a paginated search response."""
        data = self.create_list(model_name, min(total, page_size))

        return {
            "total": total,
            "data": data,
            "next": (
                f"/api/v3/search?next={fake.uuid4()}" if total > page_size else None
            ),
        }

    def create_response_from_path(
        self, path: str, method: str
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Create a response based on the OpenAPI path definition."""
        path_def = self.parser.paths.get(path, {}).get(method.lower(), {})
        responses = path_def.get("responses", {})

        # Look for successful response (200, 201, etc.)
        success_response = None
        for status_code in ["200", "201", "202"]:
            if status_code in responses:
                success_response = responses[status_code]
                break

        if not success_response:
            raise ValueError(f"No success response found for {method} {path}")

        schema = success_response.get("schema", {})

        # Handle array responses
        if schema.get("type") == "array":
            items_ref = schema.get("items", {}).get("$ref")
            if items_ref:
                model_name = items_ref.split("/")[-1]
                return self.create_list(model_name, fake.random_int(1, 10))

        # Handle object responses with $ref
        elif "$ref" in schema:
            model_name = schema["$ref"].split("/")[-1]
            return self.create(model_name)

        # Handle inline schemas
        else:
            return self.generator._generate_object(schema)

        return {}


# Example usage functions
def create_story_from_spec(factory: DynamicFactory, **overrides) -> Dict[str, Any]:
    """Create a story using the OpenAPI spec."""
    story = factory.create("Story", **overrides)

    # Ensure logical consistency
    if not story.get("started", False):
        story["started_at"] = None
        story["completed"] = False
        story["completed_at"] = None

    if not story.get("completed", False):
        story["completed_at"] = None
        story["lead_time"] = None
        story["cycle_time"] = None

    return story


def create_member_from_spec(factory: DynamicFactory, **overrides) -> Dict[str, Any]:
    """Create a member using the OpenAPI spec."""
    member = factory.create("Member", **overrides)

    # Ensure profile is properly nested
    if "profile" not in member:
        member["profile"] = factory.create("Profile")

    return member
