"""Tests for tools, parsing, and monitoring functionality."""

import pytest
import respx
from httpx import Response

from albert import (
    AlbertClient,
    FileResponse,
    OCRResponse,
    ParsedDocument,
    UsageList,
)


@pytest.fixture
def client(api_key, base_url):
    """Create test client."""
    return AlbertClient(api_key=api_key, base_url=base_url)


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary test file."""
    f = tmp_path / "test.txt"
    f.write_text("Test document content for parsing.")
    return f


class TestUsageTracking:
    """Test get_usage method."""

    @pytest.fixture
    def mock_usage_list(self):
        """Mock usage data."""
        return {
            "object": "list",
            "data": [
                {
                    "object": "me.usage",
                    "created": 1705276800,  # 2024-01-15
                    "model": "gpt-4",
                    "usage": {
                        "total_tokens": 1500,
                        "cost": 0.05,
                    },
                },
                {
                    "object": "me.usage",
                    "created": 1705363200,  # 2024-01-16
                    "model": "gpt-4",
                    "usage": {
                        "total_tokens": 3000,
                        "cost": 0.10,
                    },
                },
            ],
        }

    @respx.mock
    def test_get_usage_all(self, client, base_url, mock_usage_list):
        """Test getting all usage statistics."""
        respx.get(f"{base_url.rstrip('/')}/me/usage").mock(
            return_value=Response(200, json=mock_usage_list)
        )

        result = client.get_usage()

        assert isinstance(result, UsageList)
        assert result.object == "list"
        assert len(result.data) == 2
        assert result.data[0].created == 1705276800
        assert result.data[0].usage.total_tokens == 1500
        assert result.data[0].usage.cost == 0.05

    @respx.mock
    def test_get_usage_with_time_range(self, client, base_url, mock_usage_list):
        """Test getting usage with time filters."""
        mock_route = respx.get(f"{base_url.rstrip('/')}/me/usage").mock(
            return_value=Response(200, json=mock_usage_list)
        )

        result = client.get_usage(start_time=1705276800, end_time=1705363200)

        # Verify query params
        assert (
            mock_route.calls.last.request.url.params.get("start_time") == "1705276800"
        )
        assert mock_route.calls.last.request.url.params.get("end_time") == "1705363200"

        assert isinstance(result, UsageList)

    @respx.mock
    def test_get_usage_empty(self, client, base_url):
        """Test getting usage when no data exists."""
        respx.get(f"{base_url.rstrip('/')}/me/usage").mock(
            return_value=Response(200, json={"object": "list", "data": []})
        )

        result = client.get_usage()

        assert isinstance(result, UsageList)
        assert len(result.data) == 0


class TestOCR:
    """Test OCR methods."""

    @pytest.fixture
    def mock_ocr_response(self):
        """Mock OCR response data."""
        return {
            "pages": [
                {
                    "index": 0,
                    "markdown": "This is the extracted text from page 1.",
                    "images": [],
                }
            ],
            "id": "ocr_123",
            "model": "doctr",
        }

    @respx.mock
    def test_ocr_with_url_string(self, client, base_url, mock_ocr_response):
        """Test OCR with a URL string."""
        respx.post(f"{base_url.rstrip('/')}/ocr").mock(
            return_value=Response(200, json=mock_ocr_response)
        )

        result = client.ocr(document="https://example.com/doc.pdf")

        assert isinstance(result, OCRResponse)
        assert len(result.pages) == 1
        assert result.pages[0].markdown == "This is the extracted text from page 1."
        assert result.model == "doctr"

    @respx.mock
    def test_ocr_with_document_dict(self, client, base_url, mock_ocr_response):
        """Test OCR with a document dictionary."""
        respx.post(f"{base_url.rstrip('/')}/ocr").mock(
            return_value=Response(200, json=mock_ocr_response)
        )

        result = client.ocr(document={"document_url": "https://example.com/doc.pdf"})

        assert isinstance(result, OCRResponse)
        assert len(result.pages) == 1

    @respx.mock
    def test_ocr_with_pages(self, client, base_url, mock_ocr_response):
        """Test OCR with specific pages."""
        mock_route = respx.post(f"{base_url.rstrip('/')}/ocr").mock(
            return_value=Response(200, json=mock_ocr_response)
        )

        result = client.ocr(
            document="https://example.com/doc.pdf", pages=[0, 1, 2], model="doctr"
        )

        # Verify request body
        request_body = mock_route.calls.last.request.content.decode()
        assert "[0,1,2]" in request_body or "[0, 1, 2]" in request_body
        assert "doctr" in request_body

        assert isinstance(result, OCRResponse)

    @respx.mock
    def test_ocr_beta(self, client, base_url, temp_file):
        """Test simple OCR beta method."""
        mock_response = {
            "object": "list",
            "data": [{"content": "Extracted text from OCR beta", "page": 0}],
        }

        respx.post(f"{base_url.rstrip('/')}/ocr-beta").mock(
            return_value=Response(200, json=mock_response)
        )

        result = client.ocr_beta(file_path=temp_file, model="gpt-4o-mini", dpi=200)

        assert isinstance(result, ParsedDocument)
        assert len(result.data) == 1
        assert result.data[0].content == "Extracted text from OCR beta"


class TestParsing:
    """Test document parsing method."""

    @pytest.fixture
    def mock_parsed_document(self):
        """Mock parsed document data."""
        return {
            "object": "list",
            "data": [
                {
                    "content": "# Page 1\n\nThis is the first page.",
                    "metadata": {"document_name": "test.txt", "page": 0},
                },
                {
                    "content": "# Page 2\n\nThis is the second page.",
                    "metadata": {"document_name": "test.txt", "page": 1},
                },
            ],
        }

    @respx.mock
    def test_parse_default_markdown(
        self, client, base_url, temp_file, mock_parsed_document
    ):
        """Test parsing document to markdown."""
        respx.post(f"{base_url.rstrip('/')}/parse-beta").mock(
            return_value=Response(200, json=mock_parsed_document)
        )

        result = client.parse(file_path=temp_file)

        assert isinstance(result, ParsedDocument)
        assert len(result.data) == 2
        assert result.data[0].content.startswith("# Page 1")

    @respx.mock
    def test_parse_with_options(
        self, client, base_url, temp_file, mock_parsed_document
    ):
        """Test parsing with custom options."""
        mock_route = respx.post(f"{base_url.rstrip('/')}/parse-beta").mock(
            return_value=Response(200, json=mock_parsed_document)
        )

        result = client.parse(
            file_path=temp_file,
            force_ocr=True,
            page_range="0-5",
        )

        # Verify form data
        request = mock_route.calls.last.request
        assert b"True" in request.content or b"true" in request.content
        assert b"0-5" in request.content

        assert isinstance(result, ParsedDocument)


class TestFileUpload:
    """Test file upload method."""

    @respx.mock
    def test_upload_file(self, client, base_url, temp_file):
        """Test uploading a file."""
        mock_response = {"id": 123}

        respx.post(f"{base_url.rstrip('/')}/files").mock(
            return_value=Response(200, json=mock_response)
        )

        result = client.upload_file(file_path=temp_file, purpose="analysis")

        assert isinstance(result, FileResponse)
        assert result.id == 123

    @respx.mock
    def test_upload_file_without_purpose(self, client, base_url, temp_file):
        """Test uploading a file without purpose."""
        mock_response = {"id": 789}

        respx.post(f"{base_url.rstrip('/')}/files").mock(
            return_value=Response(200, json=mock_response)
        )

        result = client.upload_file(file_path=temp_file)

        assert isinstance(result, FileResponse)
        assert result.id == 789


class TestHealthMonitoring:
    """Test health and monitoring methods."""

    @respx.mock
    def test_health_check(self, client, base_url):
        """Test API health check."""
        mock_health = {
            "status": "ok",
            "version": "1.0.0",
            "timestamp": 1234567890,
        }

        respx.get(f"{base_url.rstrip('/')}/health").mock(
            return_value=Response(200, json=mock_health)
        )

        result = client.health_check()

        assert isinstance(result, dict)
        assert result["status"] == "ok"
        assert result["version"] == "1.0.0"

    @respx.mock
    def test_get_metrics(self, client, base_url):
        """Test getting API metrics."""
        mock_metrics = {
            "requests_total": 10000,
            "requests_per_second": 50.5,
            "average_latency_ms": 120.3,
            "error_rate": 0.01,
            "uptime_seconds": 86400,
        }

        respx.get(f"{base_url.rstrip('/')}/metrics").mock(
            return_value=Response(200, json=mock_metrics)
        )

        result = client.get_metrics()

        assert isinstance(result, dict)
        assert result["requests_total"] == 10000
        assert result["requests_per_second"] == 50.5
