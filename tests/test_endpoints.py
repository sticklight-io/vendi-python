def test_endpoints(vendi_client):
    res = vendi_client.endpoints.list()
    assert isinstance(res, list)

