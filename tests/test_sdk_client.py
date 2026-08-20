from mcplane.sdk.client import McplaneClient


def test_client_init():
    c = McplaneClient("http://127.0.0.1:8090/", token="abc")
    assert c.base_url == "http://127.0.0.1:8090"
    assert c.token == "abc"


def test_client_strips_slash():
    c = McplaneClient("http://x///")
    assert c.base_url == "http://x"
