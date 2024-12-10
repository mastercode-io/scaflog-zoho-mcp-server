# tests/test_server.py
import pytest
from pydantic import AnyUrl
import mcp.types as types
from mcp import ClientSession

@pytest.mark.asyncio
async def test_server_resources(client_session: ClientSession):
    """Test server resources functionality."""
    # List available resources
    resources = await client_session.list_resources()
    assert len(resources) > 0
    assert any(str(r.uri) == "zoho://forms" for r in resources)
    assert any(str(r.uri) == "zoho://forms/test_form" for r in resources)

    # Read a resource
    resource = await client_session.read_resource("zoho://forms/test_form")
    assert resource.mimeType == "application/json"
    assert "form" in resource.text
    assert "records" in resource.text

@pytest.mark.asyncio
async def test_server_tools(client_session: ClientSession):
    """Test server tools functionality."""
    # List available tools
    tools = await client_session.list_tools()
    assert any(tool.name == "create-record" for tool in tools)

    # Call a tool
    result = await client_session.call_tool(
        "create-record",
        arguments={
            "form_name": "test_form",
            "data": {"test_field": "test_value"}
        }
    )
    assert len(result) == 1
    assert result[0].type == "text"
    assert "created successfully" in result[0].text