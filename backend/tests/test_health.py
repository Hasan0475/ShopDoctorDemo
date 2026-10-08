"""Health/meta endpoint tests."""
def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["llm_provider"] == "mock"


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["app"] == "ShopDoctor API"
