"""Report / diagnosis tests."""


def _demo_shop_id(client):
    shops = client.get("/api/shops").json()
    assert shops, "seed should create a demo shop"
    return shops[0]["id"]


def test_report_structure(client):
    sid = _demo_shop_id(client)
    r = client.get(f"/api/shops/{sid}/report")
    assert r.status_code == 200
    body = r.json()
    assert 0 <= body["health_score"] <= 100
    assert body["score_band"] in {"healthy", "watch", "at-risk"}
    assert len(body["dishes"]) >= 1
    assert body["metrics"] and body["problems"]
    assert body["twins"]["survivors_count"] > 0
    assert body["twins"]["closed_count"] > 0


def test_dish_margins_computed(client):
    sid = _demo_shop_id(client)
    body = client.get(f"/api/shops/{sid}/report").json()
    by_name = {d["name"]: d for d in body["dishes"]}
    # Signature milk tea: (26-8)/26 = 69%
    assert by_name["Signature milk tea"]["margin_pct"] == 69
    assert by_name["Signature milk tea"]["status"] == "healthy"
    # Club sandwich: (42-39)/42 = 7% -> losing
    assert by_name["Club sandwich"]["status"] == "losing"


def test_report_404(client):
    assert client.get("/api/shops/999999/report").status_code == 404


def test_create_shop_and_report(client):
    payload = {
        "name": "Test Noodle House",
        "shop_type": "Cha chaan teng",
        "district": "Mong Kok",
        "years_open": 2,
        "monthly_revenue": 200000,
        "monthly_rent": 40000,
        "monthly_staff_cost": 50000,
        "ingredient_pct": 25,
        "waste_pct": 4,
        "menu_size": 8,
        "dishes": [
            {"name": "Wonton noodles", "price": 45, "cost": 15, "units_per_month": 2000, "share_pct": 60},
            {"name": "Soy milk", "price": 15, "cost": 4, "units_per_month": 1500, "share_pct": 40},
        ],
    }
    r = client.post("/api/shops", json=payload)
    assert r.status_code == 201
    sid = r.json()["id"]

    report = client.get(f"/api/shops/{sid}/report").json()
    # High margins, low rent/waste -> should score well
    assert report["health_score"] >= 70
    assert report["score_band"] in {"healthy", "watch"}
