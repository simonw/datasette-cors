import json

import pytest
from asgiref.testing import ApplicationCommunicator
from datasette.app import Datasette


@pytest.mark.asyncio
async def test_datasette_cors_plugin_installed():
    instance = ApplicationCommunicator(
        Datasette([], memory=True).app(),
        {
            "type": "http",
            "http_version": "1.0",
            "method": "GET",
            "path": "/-/plugins.json",
        },
    )
    await instance.send_input({"type": "http.request"})
    response_start = await instance.receive_output(1)
    assert "http.response.start" == response_start["type"]
    assert 200 == response_start["status"]
    body = await instance.receive_output(1)
    assert [
        {
            "name": "datasette_cors",
            "static": False,
            "templates": False,
            "version": "0.1",
        }
    ] == json.loads(body["body"].decode("utf8"))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_origin,expected_cors_header",
    [
        (None, None),
        (b"http://example.com", b"http://example.com"),
        (b"http://foo.com", None),
    ],
)
async def test_asgi_cors_two_hosts_and_a_wildcard(request_origin, expected_cors_header):
    instance = ApplicationCommunicator(
        Datasette(
            [],
            memory=True,
            metadata={"plugins": {"datasette-cors": {"hosts": ["http://example.com"]}}},
        ).app(),
        {
            "type": "http",
            "http_version": "1.0",
            "method": "GET",
            "path": "/",
            "headers": [[b"origin", request_origin]],
        },
    )
    await instance.send_input({"type": "http.request"})
    event = await instance.receive_output(1)
    assert 200 == event["status"]
    assert expected_cors_header == dict(event.get("headers") or []).get(
        b"access-control-allow-origin"
    )
