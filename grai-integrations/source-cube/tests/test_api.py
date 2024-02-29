def test_api_ready_endpoint(api):
    assert api.ready().status_code == 200


def test_api_meta_endpoint(api):
    result = api.meta()
