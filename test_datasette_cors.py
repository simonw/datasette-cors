import httpx
import pytest
from unittest.mock import ANY
from datasette.app import Datasette


@pytest.mark.asyncio
async def test_datasette_cors_plugin_installed():
    async with httpx.AsyncClient(app=Datasette([], memory=True).app()) as client:
        response = await client.get("http://localhost/-/plugins.json")
        assert response.status_code == 200
        assert response.json() == [
            {
                "name": "datasette-cors",
                "static": False,
                "templates": False,
                "version": ANY,
                "hooks": ["asgi_wrapper"],
            }
        ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_origin,expected_cors_header",
    [
        (None, None),
        ("http://example.com", "http://example.com"),
        ("http://foo.com", None),
    ],
)
async def test_asgi_cors_hosts(request_origin, expected_cors_header):
    headers = {}
    if request_origin:
        headers["Origin"] = request_origin

    async with httpx.AsyncClient(
        app=Datasette(
            [],
            memory=True,
            metadata={"plugins": {"datasette-cors": {"hosts": ["http://example.com"]}}},
        ).app()
    ) as client:
        response = await client.get("http://localhost/", headers=headers)
        assert response.status_code == 200
        assert (
            response.headers.get("access-control-allow-origin") == expected_cors_header
        )
