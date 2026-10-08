"""Marketing kit tests."""


def _demo_shop_id(client):
    return client.get("/api/shops").json()[0]["id"]


def test_marketing_endpoint(client):
    sid = _demo_shop_id(client)
    r = client.get(f"/api/shops/{sid}/marketing")
    assert r.status_code == 200
    body = r.json()
    assert body["shop_id"] == sid
    assert len(body["posts"]) >= 4
    first = body["posts"][0]
    assert first["emoji"] and first["title"] and first["caption"]
    # The bundle idea should be present
    titles = " ".join(p["title"].lower() for p in body["posts"])
    assert "set" in titles


def test_marketing_prioritises_high_margin(client):
    sid = _demo_shop_id(client)
    body = client.get(f"/api/shops/{sid}/marketing").json()
    # Highest-margin dishes should be heroed first (lemon tea / milk tea ~69-73%)
    assert any("lemon tea" in p["title"].lower() or "milk tea" in p["title"].lower()
               for p in body["posts"])


def test_marketing_404(client):
    assert client.get("/api/shops/999999/marketing").status_code == 404
