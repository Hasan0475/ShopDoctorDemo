import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { useShop } from "../components/ShopContext";
import { ErrorBox, Loader, money } from "../components/ui";
import type { Dish, SimulatorResult } from "../types";

export default function Simulator() {
  const { report, loading } = useShop();
  const dishes: Dish[] = report?.dishes ?? [];
  const [dish, setDish] = useState<Dish | null>(null);
  const [price, setPrice] = useState(0);
  const [result, setResult] = useState<SimulatorResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (dishes.length && !dish) {
      const d = dishes[0];
      setDish(d);
      setPrice(d.price);
    }
  }, [dishes, dish]);

  const bounds = useMemo(() => {
    if (!dish) return { min: 5, max: 100 };
    return { min: Math.max(5, Math.round(dish.price * 0.5)), max: Math.round(dish.price * 2) };
  }, [dish]);

  useEffect(() => {
    if (!dish) return;
    let alive = true;
    setBusy(true);
    api
      .simulate({
        dish: dish.name,
        base_price: dish.price,
        base_cost: dish.cost,
        base_units: dish.units_per_month || 1000,
        price,
      })
      .then((r) => alive && setResult(r))
      .catch((e) => alive && setError(e instanceof Error ? e.message : "Simulator error"))
      .finally(() => alive && setBusy(false));
    return () => {
      alive = false;
    };
  }, [dish, price]);

  if (loading && !report) return <Loader />;
  if (!dishes.length) return <ErrorBox message="No dishes yet — run a check-up first." />;

  function pickDish(id: number) {
    const d = dishes.find((x) => x.id === id) ?? null;
    setDish(d);
    if (d) {
      setPrice(d.price);
      setResult(null);
    }
  }

  const delta = result?.profit_delta ?? 0;
  const dir = result?.direction ?? "flat";
  const barWidth = result ? Math.max(3, Math.min(100, 50 + (delta / (result.before_profit || 1)) * 100)) : 50;

  return (
    <>
      <h2 className="sec">Price Simulator</h2>
      <p className="sub">
        Slide a dish price and see the effect on monthly profit. Uses a demand elasticity of −1.4
        estimated from twin-shop data.
      </p>

      {error && <div className="error" style={{ marginBottom: 16 }}>{error}</div>}

      <div className="sim">
        <div className="card">
          <div className="pad">
            <div className="field">
              <label>Dish to simulate</label>
              <select value={dish?.id ?? ""} onChange={(e) => pickDish(Number(e.target.value))}>
                {dishes.map((d) => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Price (HK$)</label>
              <div className="slider-row">
                <input type="range" min={bounds.min} max={bounds.max} step={1} value={price}
                  onChange={(e) => setPrice(Number(e.target.value))} />
                <output>HK${price}</output>
              </div>
            </div>
            <div className="grid2" style={{ marginTop: 8 }}>
              <div className="metric">
                <div className="k">Units / month (est.)</div>
                <div className="v">{busy ? "…" : (result?.new_units ?? 0).toLocaleString()}</div>
              </div>
              <div className="metric">
                <div className="k">New dish margin</div>
                <div className={`v ${(result?.new_margin_pct ?? 0) >= 35 ? "tone-good" : "tone-bad"}`}>
                  {busy ? "…" : `${result?.new_margin_pct ?? 0}%`}
                </div>
              </div>
            </div>
            <p className="note">
              Baseline: {dish?.units_per_month.toLocaleString()} units at HK${dish?.price}, cost HK${dish?.cost}.
            </p>
          </div>
        </div>

        <div className="card">
          <div className="pad simout">
            <div className="k muted" style={{ fontSize: 13 }}>Change in monthly profit</div>
            <div className={`big ${dir === "up" ? "up" : dir === "down" ? "down" : ""}`}>
              {busy ? "…" : `${delta >= 0 ? "+" : "−"}${money(Math.abs(delta))}`}
            </div>
            <div className="bar" style={{ height: 12 }}><i style={{ width: `${barWidth}%` }} /></div>
            <div className="grid2">
              <div className="metric"><div className="k">Before</div><div className="v">{result ? money(result.before_profit) : "—"}</div></div>
              <div className="metric"><div className="k">After</div><div className="v">{result ? money(result.after_profit) : "—"}</div></div>
            </div>
            <div className="prob" style={{ margin: 0 }}>
              <div className="ic">💡</div>
              <div>
                <h4>{result?.advice_title ?? "Recommendation"}</h4>
                <p>{result?.advice ?? "Move the slider to explore."}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
