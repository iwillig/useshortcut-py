from datetime import datetime

import pytest
import requests

from useshortcut import models
from useshortcut.client import APIClient


@pytest.fixture
def api_client():
    """Create an API client instance for testing."""
    return APIClient(api_token="test-token-123")


@pytest.fixture
def base_url():
    """Return the base URL for mocking."""
    return "https://api.app.shortcut.com/api/v3"


@pytest.fixture
def custom_field_enum_value_data():
    """Sample custom field enum value data."""
    return [
        {
            "id": "cfv-12345678-1234-1234-1234-123456789001",
            "value": "High",
            "position": 1,
            "color_key": "red",
            "entity_type": "custom-field-enum-value",
            "enabled": True,
        },
        {
            "id": "cfv-12345678-1234-1234-1234-123456789002",
            "value": "Medium",
            "position": 2,
            "color_key": "yellow",
            "entity_type": "custom-field-enum-value",
            "enabled": True,
        },
        {
            "id": "cfv-12345678-1234-1234-1234-123456789003",
            "value": "Low",
            "position": 3,
            "color_key": "green",
            "entity_type": "custom-field-enum-value",
            "enabled": True,
        },
    ]


@pytest.fixture
def custom_field_data(custom_field_enum_value_data):
    """Sample custom field data."""
    return {
        "id": "cf-12345678-1234-1234-1234-123456789012",
        "name": "Priority",
        "field_type": "enum",
        "position": 1,
        "enabled": True,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z",
        "entity_type": "custom-field",
        "description": "Task priority level",
        "icon_set_identifier": "priority",
        "canonical_name": None,
        "fixed_position": False,
        "story_types": ["feature", "bug", "chore"],
        "values": custom_field_enum_value_data,
    }


@pytest.fixture
def custom_field_simple_data():
    """Sample custom field with minimal data."""
    return {
        "id": "cf-87654321-4321-4321-4321-210987654321",
        "name": "Team",
        "field_type": "enum",
        "position": 2,
        "enabled": True,
        "created_at": "2023-02-01T00:00:00Z",
        "updated_at": "2023-02-15T00:00:00Z",
        "entity_type": "custom-field",
        "values": [
            {
                "id": "cfv-team-1",
                "value": "Frontend",
                "position": 1,
                "entity_type": "custom-field-enum-value",
                "enabled": True,
            },
            {
                "id": "cfv-team-2",
                "value": "Backend",
                "position": 2,
                "entity_type": "custom-field-enum-value",
                "enabled": True,
            },
        ],
    }


class TestCustomFields:
    """Test custom field endpoints."""

    def test_list_custom_fields(
        self,
        requests_mock,
        api_client,
        base_url,
        custom_field_data,
        custom_field_simple_data,
    ):
        """Test listing all custom fields."""
        requests_mock.get(
            f"{base_url}/custom-fields",
            json=[custom_field_data, custom_field_simple_data],
        )

        custom_fields = api_client.list_custom_fields()

        assert len(custom_fields) == 2
        assert isinstance(custom_fields[0], models.CustomField)
        assert custom_fields[0].id == "cf-12345678-1234-1234-1234-123456789012"
        assert custom_fields[0].name == "Priority"
        assert custom_fields[0].field_type == "enum"
        assert len(custom_fields[0].values) == 3

    def test_get_custom_field(
        self, requests_mock, api_client, base_url, custom_field_data
    ):
        """Test fetching a specific custom field."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"

        requests_mock.get(
            f"{base_url}/custom-fields/{custom_field_id}", json=custom_field_data
        )

        custom_field = api_client.get_custom_field(custom_field_id)

        assert isinstance(custom_field, models.CustomField)
        assert custom_field.id == custom_field_id
        assert custom_field.description == "Task priority level"
        assert custom_field.enabled is True

    def test_update_custom_field(self, requests_mock, api_client, base_url):
        """Test updating custom field properties."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"
        updated_data = {
            "id": custom_field_id,
            "name": "Priority Level",
            "field_type": "enum",
            "position": 1,
            "enabled": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-20T00:00:00Z",
            "entity_type": "custom-field",
            "description": "Updated priority level description",
            "values": [],
        }

        update_input = models.UpdateCustomFieldInput(
            name="Priority Level", description="Updated priority level description"
        )

        requests_mock.put(
            f"{base_url}/custom-fields/{custom_field_id}", json=updated_data
        )

        custom_field = api_client.update_custom_field(custom_field_id, update_input)

        assert custom_field.name == "Priority Level"
        assert custom_field.description == "Updated priority level description"

    def test_update_custom_field_values(
        self, requests_mock, api_client, base_url, custom_field_data
    ):
        """Test updating custom field enum values."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"
        updated_data = custom_field_data.copy()
        updated_data["values"][0]["value"] = "Critical"
        updated_data["values"][0]["color_key"] = "purple"

        update_values = [
            models.UpdateCustomFieldEnumValue(
                id="cfv-12345678-1234-1234-1234-123456789001",
                value="Critical",
                color_key="purple",
            )
        ]

        update_input = models.UpdateCustomFieldInput(values=update_values)

        requests_mock.put(
            f"{base_url}/custom-fields/{custom_field_id}", json=updated_data
        )

        custom_field = api_client.update_custom_field(custom_field_id, update_input)

        assert custom_field.values[0].value == "Critical"
        assert custom_field.values[0].color_key == "purple"

    def test_update_custom_field_reorder(
        self, requests_mock, api_client, base_url, custom_field_data
    ):
        """Test reordering custom fields."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"
        reordered_data = custom_field_data.copy()
        reordered_data["position"] = 3

        update_input = models.UpdateCustomFieldInput(
            after_id="cf-87654321-4321-4321-4321-210987654321"
        )

        requests_mock.put(
            f"{base_url}/custom-fields/{custom_field_id}", json=reordered_data
        )

        custom_field = api_client.update_custom_field(custom_field_id, update_input)

        assert custom_field.position == 3

    def test_delete_custom_field(self, requests_mock, api_client, base_url):
        """Test deleting a custom field."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"

        requests_mock.delete(
            f"{base_url}/custom-fields/{custom_field_id}", status_code=204
        )

        # Should not raise an exception
        api_client.delete_custom_field(custom_field_id)

    def test_custom_field_enum_values_parsing(
        self, requests_mock, api_client, base_url, custom_field_data
    ):
        """Test parsing of custom field enum values."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"

        requests_mock.get(
            f"{base_url}/custom-fields/{custom_field_id}", json=custom_field_data
        )

        custom_field = api_client.get_custom_field(custom_field_id)

        assert len(custom_field.values) == 3

        # Check first value
        high_priority = custom_field.values[0]
        assert isinstance(high_priority, models.CustomFieldEnumValue)
        assert high_priority.value == "High"
        assert high_priority.color_key == "red"
        assert high_priority.position == 1
        assert high_priority.enabled is True

        # Check all values are properly ordered
        assert custom_field.values[0].position == 1
        assert custom_field.values[1].position == 2
        assert custom_field.values[2].position == 3

    def test_custom_field_datetime_parsing(
        self, requests_mock, api_client, base_url, custom_field_data
    ):
        """Test that datetime fields are properly parsed."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"

        requests_mock.get(
            f"{base_url}/custom-fields/{custom_field_id}", json=custom_field_data
        )

        custom_field = api_client.get_custom_field(custom_field_id)

        assert isinstance(custom_field.created_at, datetime)
        assert isinstance(custom_field.updated_at, datetime)
        assert custom_field.created_at.year == 2023
        assert custom_field.created_at.month == 1
        assert custom_field.created_at.day == 1

    def test_custom_field_not_found(self, requests_mock, api_client, base_url):
        """Test 404 error handling."""
        custom_field_id = "cf-99999999-9999-9999-9999-999999999999"

        requests_mock.get(
            f"{base_url}/custom-fields/{custom_field_id}",
            status_code=404,
            json={"message": "Custom field not found", "error": "NotFound"},
        )

        with pytest.raises(requests.exceptions.HTTPError):
            api_client.get_custom_field(custom_field_id)

    def test_update_custom_field_disabled(
        self, requests_mock, api_client, base_url, custom_field_data
    ):
        """Test disabling a custom field."""
        custom_field_id = "cf-12345678-1234-1234-1234-123456789012"
        disabled_data = custom_field_data.copy()
        disabled_data["enabled"] = False

        update_input = models.UpdateCustomFieldInput(enabled=False)

        requests_mock.put(
            f"{base_url}/custom-fields/{custom_field_id}", json=disabled_data
        )

        custom_field = api_client.update_custom_field(custom_field_id, update_input)

        assert custom_field.enabled is False
