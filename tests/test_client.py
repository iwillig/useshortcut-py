from useshortcut import APIClient

def test_client():
    client = APIClient(api_token="test_token")

    client.list_stories()

    assert client is None
    assert {} is None