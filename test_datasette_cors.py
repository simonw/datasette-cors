import pytest
from unittest.mock import ANY
from datasette.app import Datasette


@pytest.mark.asyncio
async def test_datasette_cors_plugin_installed():
    ds = Datasette([], memory=True)
    response = await ds.client.get("/-/plugins.json")
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

    ds = Datasette(
        [],
        memory=True,
        config={"plugins": {"datasette-cors": {"hosts": ["http://example.com"]}}},
    )
    response = await ds.client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == expected_cors_header


@pytest.mark.asyncio
async def test_asgi_cors_headers():
    ds = Datasette(
        [],
        memory=True,
        config={
            "plugins": {
                "datasette-cors": {
                    "allow_all": True,
                    "headers": ["Authorization", "Content-Type"],
                }
            }
        },
    )
    response = await ds.client.get("/")
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert (
        response.headers["access-control-allow-headers"]
        == "Authorization, Content-Type"
    )


@pytest.mark.asyncio
async def test_asgi_cors_methods():
    ds = Datasette(
        [],
        memory=True,
        config={
            "plugins": {
                "datasette-cors": {
                    "allow_all": True,
                    "methods": ["GET", "POST", "OPTIONS"],
                }
            }
        },
    )
    response = await ds.client.get("/")
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert response.headers["access-control-allow-methods"] == "GET, POST, OPTIONS"


@pytest.mark.asyncio
async def test_asgi_cors_max_age():
    ds = Datasette(
        [],
        memory=True,
        config={"plugins": {"datasette-cors": {"allow_all": True, "max_age": 3600}}},
    )
    response = await ds.client.get("/")
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert response.headers["access-control-max-age"] == "3600"
