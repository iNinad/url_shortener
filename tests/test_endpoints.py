from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# Get the base url of the application
BASE_URL = client.base_url

# Define a global variable to hold the short_url value
short_url_value = None


def test_shorten_url():
    """
    Test case for the shorten url endpoint.
    The tests include a valid URL, a duplicate original URL for dynamic expiration case, and an invalid URL scenario.
    """
    global short_url_value  # Access the global variable
    data = {"original_url": "https://gmail.com"}
    response = client.post("/shorten/", json=data)
    assert response.status_code == 200
    assert "short_url" in response.json()

    # Store the short_url value as it will be used in other tests
    short_url_value = response.json()["short_url"]

    # Test case where the same valid original URL is used.
    # The same short url should be created for the same original url only the expiration time will be updated
    data = {"original_url": "https://gmail.com"}
    response = client.post("/shorten/", json=data)
    assert response.status_code == 200
    assert response.json()["short_url"] == short_url_value

    # Test case where invalid original URL is used.
    data = {"original_url": "invalid_url"}
    response = client.post("/shorten/", json=data)
    assert response.status_code == 422


def test_fetch_original_url():
    """
    Test case for fetching the original url from the short url.
    The tests include an existing short URL and a non-existing short URL scenario.
    """
    global short_url_value
    response = client.get(f"/shorten/?short_url={short_url_value}")
    assert response.status_code == 200
    assert "original_url" in response.json()

    # Test case where a non-existing short URL is used.
    short_url = f"{BASE_URL}/non_existing_short_url"
    response = client.get(f"/shorten/?short_url={short_url}")
    assert response.status_code == 404


def test_delete_short_url():
    """
    Test case for deleting a short url.
    The tests cover a scenario of successful deletion and scenario where the short URL does not exist.
    """
    global short_url_value
    data = {"short_url": short_url_value}
    response = client.request("DELETE", "/shorten/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Short URL deleted successfully"}

    # Test case where a non-existing short URL is attempted for deletion.
    data = {"short_url": f"{BASE_URL}/non_existing_short_url"}
    response = client.request("DELETE", "/shorten/", json=data)
    assert response.status_code == 404
