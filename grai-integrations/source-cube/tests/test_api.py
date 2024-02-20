def test_api_is_ready(api, run_live):
    assert api.ready().status_code == 200
