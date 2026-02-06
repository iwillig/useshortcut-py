"""Tests for Document (Doc) endpoints."""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
import requests

from useshortcut.client import APIClient
from useshortcut.models import CreateDocInput, Doc, DocSlim, UpdateDocInput


class TestDocs:
    """Test suite for Document endpoints."""

    @pytest.fixture
    def client(self):
        return APIClient(api_token="test-token")

    @pytest.fixture
    def mock_doc_response(self):
        """Sample doc response from API."""
        return {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Test Document",
            "content_markdown": "# Hello World\n\nThis is a test document.",
            "content_html": "<h1>Hello World</h1><p>This is a test document.</p>",
            "app_url": "https://app.shortcut.com/test/docs/123e4567-e89b-12d3-a456-426614174000",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T14:45:00Z",
            "archived": False,
        }

    @pytest.fixture
    def mock_doc_slim_response(self):
        """Sample doc slim response from API."""
        return {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Test Document",
            "app_url": "https://app.shortcut.com/test/docs/123e4567-e89b-12d3-a456-426614174000",
        }

    def test_list_docs(self, client, mock_doc_slim_response):
        """Test listing all documents."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: [mock_doc_slim_response],
                content=b'[{"id": "123e4567-e89b-12d3-a456-426614174000"}]',
            )

            docs = client.list_docs()

            assert len(docs) == 1
            assert isinstance(docs[0], DocSlim)
            assert docs[0].id == "123e4567-e89b-12d3-a456-426614174000"
            assert docs[0].title == "Test Document"
            mock_request.assert_called_once_with(
                "GET",
                "https://api.app.shortcut.com/api/v3/documents",
            )

    def test_get_doc(self, client, mock_doc_response):
        """Test getting a specific document."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: mock_doc_response,
                content=b"{}",
            )

            doc = client.get_doc("123e4567-e89b-12d3-a456-426614174000")

            assert isinstance(doc, Doc)
            assert doc.id == "123e4567-e89b-12d3-a456-426614174000"
            assert doc.title == "Test Document"
            assert doc.content_markdown == "# Hello World\n\nThis is a test document."
            assert doc.archived is False
            assert isinstance(doc.created_at, datetime)
            assert isinstance(doc.updated_at, datetime)
            mock_request.assert_called_once_with(
                "GET",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000",
                params=None,
            )

    def test_get_doc_with_html(self, client, mock_doc_response):
        """Test getting a document with HTML content included."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: mock_doc_response,
                content=b"{}",
            )

            doc = client.get_doc(
                "123e4567-e89b-12d3-a456-426614174000", include_html=True
            )

            assert isinstance(doc, Doc)
            assert (
                doc.content_html
                == "<h1>Hello World</h1><p>This is a test document.</p>"
            )
            mock_request.assert_called_once_with(
                "GET",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000",
                params={"include_html": "true"},
            )

    def test_create_doc(self, client, mock_doc_response):
        """Test creating a new document."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=201,
                json=lambda: mock_doc_response,
                content=b"{}",
            )

            input_data = CreateDocInput(
                title="Test Document",
                content="# Hello World\n\nThis is a test document.",
                content_format="markdown",
            )
            doc = client.create_doc(input_data)

            assert isinstance(doc, Doc)
            assert doc.id == "123e4567-e89b-12d3-a456-426614174000"
            assert doc.title == "Test Document"
            mock_request.assert_called_once_with(
                "POST",
                "https://api.app.shortcut.com/api/v3/documents",
                json={
                    "title": "Test Document",
                    "content": "# Hello World\n\nThis is a test document.",
                    "content_format": "markdown",
                },
            )

    def test_create_doc_minimal(self, client, mock_doc_response):
        """Test creating a document with minimal fields."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=201,
                json=lambda: mock_doc_response,
                content=b"{}",
            )

            input_data = CreateDocInput(
                title="Test Document",
                content="<h1>Hello</h1>",
            )
            doc = client.create_doc(input_data)

            assert isinstance(doc, Doc)
            mock_request.assert_called_once_with(
                "POST",
                "https://api.app.shortcut.com/api/v3/documents",
                json={
                    "title": "Test Document",
                    "content": "<h1>Hello</h1>",
                },
            )

    def test_update_doc(self, client, mock_doc_response):
        """Test updating an existing document."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: mock_doc_response,
                content=b"{}",
            )

            input_data = UpdateDocInput(
                title="Updated Document",
                content="Updated content",
            )
            doc = client.update_doc("123e4567-e89b-12d3-a456-426614174000", input_data)

            assert isinstance(doc, Doc)
            mock_request.assert_called_once_with(
                "PUT",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000",
                json={
                    "title": "Updated Document",
                    "content": "Updated content",
                },
            )

    def test_update_doc_partial(self, client, mock_doc_response):
        """Test updating only the title of a document."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: mock_doc_response,
                content=b"{}",
            )

            input_data = UpdateDocInput(title="New Title Only")
            doc = client.update_doc("123e4567-e89b-12d3-a456-426614174000", input_data)

            assert isinstance(doc, Doc)
            mock_request.assert_called_once_with(
                "PUT",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000",
                json={"title": "New Title Only"},
            )

    def test_delete_doc(self, client):
        """Test deleting a document."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=204,
                json=lambda: None,
                content=b"",
            )

            client.delete_doc("123e4567-e89b-12d3-a456-426614174000")

            mock_request.assert_called_once_with(
                "DELETE",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000",
            )

    def test_list_document_epics(self, client):
        """Test listing epics associated with a document."""
        epic_response = {
            "id": 123,
            "global_id": "epic:123",
            "name": "Test Epic",
            "app_url": "https://app.shortcut.com/test/epic/123",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T14:45:00Z",
        }

        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: [epic_response],
                content=b"[{}]",
            )

            epics = client.list_document_epics("123e4567-e89b-12d3-a456-426614174000")

            assert len(epics) == 1
            assert epics[0].id == 123
            assert epics[0].name == "Test Epic"
            mock_request.assert_called_once_with(
                "GET",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000/epics",
            )

    def test_link_document_to_epic(self, client):
        """Test linking a document to an epic."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: {},
                content=b"{}",
            )

            client.link_document_to_epic("123e4567-e89b-12d3-a456-426614174000", 123)

            mock_request.assert_called_once_with(
                "PUT",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000/epics/123",
            )

    def test_unlink_document_from_epic(self, client):
        """Test unlinking a document from an epic."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=204,
                json=lambda: None,
                content=b"",
            )

            client.unlink_document_from_epic(
                "123e4567-e89b-12d3-a456-426614174000", 123
            )

            mock_request.assert_called_once_with(
                "DELETE",
                "https://api.app.shortcut.com/api/v3/documents/123e4567-e89b-12d3-a456-426614174000/epics/123",
            )

    def test_doc_not_found(self, client):
        """Test handling 404 error when document is not found."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=404,
                raise_for_status=lambda: (_ for _ in ()).throw(
                    requests.exceptions.HTTPError(response=Mock(status_code=404))
                ),
            )

            with pytest.raises(requests.exceptions.HTTPError):
                client.get_doc("non-existent-doc-id")

    def test_doc_datetime_parsing(self, client):
        """Test that datetime fields are correctly parsed."""
        doc_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Test",
            "content_markdown": "Content",
            "app_url": "https://app.shortcut.com/test/docs/123",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-06-20T18:45:30Z",
            "archived": False,
        }

        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: doc_data,
                content=b"{}",
            )

            doc = client.get_doc("123e4567-e89b-12d3-a456-426614174000")

            assert doc.created_at == datetime(
                2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc
            )
            assert doc.updated_at == datetime(
                2024, 6, 20, 18, 45, 30, tzinfo=timezone.utc
            )

    def test_doc_empty_list(self, client):
        """Test listing documents when there are none."""
        with patch.object(client.session, "request") as mock_request:
            mock_request.return_value = Mock(
                status_code=200,
                json=lambda: [],
                content=b"[]",
            )

            docs = client.list_docs()

            assert docs == []
