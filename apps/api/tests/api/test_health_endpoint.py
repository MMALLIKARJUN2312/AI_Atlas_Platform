from .conftest import create_test_client

client = create_test_client()


def test_health_endpoint():

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "service": "AI Atlas Platform",
    }