import pytest


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_datasette_cors():
    assert False, "Tests not yet written - need to ship Datasette 0.29 first"
