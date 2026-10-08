"""Price simulator math + endpoint tests."""
from app.agents.pricing_agent import simulate_price


def test_price_increase_with_elasticity():
    # Raising price reduces units; profit direction depends on margin/elasticity.
    res = simulate_price("milk tea", base_price=26, base_cost=8, base_units=1850, new_price=30)
    assert res.new_units < res.base_units
    assert res.new_margin_pct > res.base_margin_pct
    assert res.direction in {"up", "down", "flat"}


def test_break_even_is_flat():
    res = simulate_price("x", base_price=40, base_cost=20, base_units=1000, new_price=40)
    assert res.profit_delta == 0
    assert res.direction == "flat"


def test_extreme_price_hike_loses_volume():
    res = simulate_price("x", base_price=20, base_cost=5, base_units=1000, new_price=60)
    assert res.new_units < 400  # elasticity -1.4 => big volume drop


def test_simulator_endpoint(client):
    r = client.post(
        "/api/simulator",
        json={
            "dish": "Signature milk tea",
            "base_price": 26,
            "base_cost": 8,
            "base_units": 1850,
            "price": 30,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["elasticity"] == -1.4
    assert body["new_units"] < body["base_units"]
    assert body["advice"]
