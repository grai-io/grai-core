from django.urls import reverse


def test_index(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200, f"verb `get` failed on index with status {response.status_code}"
