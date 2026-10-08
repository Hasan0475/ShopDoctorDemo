import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import type { DishInput } from "../types";

interface FormState {
  name: string;
  shop_type: string;
  district: string;
  years_open: number;
  open_time: string;
  close_time: string;
  days_per_week: number;
  peak_period: string;
  monthly_revenue: number;
  monthly_rent: number;
  monthly_staff_cost: number;
  ingredient_pct: number;
  waste_pct: number;
  menu_size: number;
  google_maps_url: string;
}

const INITIAL: FormState = {
  name: "",
  shop_type: "Cha chaan teng",
  district: "Sham Shui Po",
  years_open: 3,
  open_time: "07:00",
  close_time: "18:00",
  days_per_week: 6,
  peak_period: "Lunch",
  monthly_revenue: 180000,
  monthly_rent: 55000,
  monthly_staff_cost: 68000,
  ingredient_pct: 26,
  waste_pct: 9,
  menu_size: 12,
  google_maps_url: "",
};

const DEFAULT_DISHES: DishInput[] = [
  { name: "Signature milk tea", price: 26, cost: 8, units_per_month: 1800, share_pct: 26 },
  { name: "Beef brisket noodles", price: 52, cost: 34, units_per_month: 600, share_pct: 18 },
  { name: "Baked pork chop rice", price: 58, cost: 29, units_per_month: 550, share_pct: 18 },
];

const STEPS = ["Shop basics", "Photos & listing", "Opening hours", "Revenue & costs", "Menu & twins"];

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="field">
      <label>{label}</label>
      {children}
    </div>
  );
}

export default function CheckUp() {
  const nav = useNavigate();
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<FormState>(INITIAL);
  const [dishes, setDishes] = useState<DishInput[]>(DEFAULT_DISHES);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof FormState>(k: K, v: FormState[K]) =>
    setForm((f) => ({ ...f, [k]: v }));

  const num = (k: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement>) =>
    set(k, (Number(e.target.value) as never));

  const updateDish = (i: number, patch: Partial<DishInput>) =>
    setDishes((d) => d.map((x, idx) => (idx === i ? { ...x, ...patch } : x)));

  const last = step === STEPS.length - 1;

  async function finish() {
    setSubmitting(true);
    setError(null);
    try {
      const created = await api.createShop({ ...form, dishes });
      localStorage.setItem("shopdoctor.lastShopId", String(created.id));
      nav("/report");
      window.location.reload();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create shop");
      setSubmitting(false);
    }
  }

  return (
    <>
      <h2 className="sec">The Check-Up</h2>
      <p className="sub">
        Answer a few questions — takes about 20 minutes. Your diagnosis is generated from this data.
      </p>
      <div className="wizard">
        <div className="steps-nav">
          {STEPS.map((s, i) => (
            <div
              key={s}
              className={`s ${i === step ? "active" : ""} ${i < step ? "done" : ""}`}
              onClick={() => setStep(i)}
            >
              <span className="c">{i < step ? "✓" : i + 1}</span>
              {s}
            </div>
          ))}
        </div>

        <div className="card">
          <div className="pad">
            <h3 style={{ marginTop: 0 }}>{step + 1}. {STEPS[step]}</h3>

            {step === 0 && (
              <div className="grid2">
                <Field label="Shop name">
                  <input value={form.name} placeholder="e.g. Ming Kee Cha Chaan Teng"
                    onChange={(e) => set("name", e.target.value)} />
                </Field>
                <Field label="Type">
                  <select value={form.shop_type} onChange={(e) => set("shop_type", e.target.value)}>
                    <option>Cha chaan teng</option><option>Café</option>
                    <option>Noodle shop</option><option>Bakery</option>
                  </select>
                </Field>
                <Field label="District">
                  <select value={form.district} onChange={(e) => set("district", e.target.value)}>
                    <option>Sham Shui Po</option><option>Mong Kok</option>
                    <option>Causeway Bay</option><option>Kwun Tong</option>
                  </select>
                </Field>
                <Field label="Years open">
                  <input type="number" value={form.years_open} onChange={num("years_open")} />
                </Field>
              </div>
            )}

            {step === 1 && (
              <>
                <Field label="Menu (photo)">
                  <div className="drop">📷 Drop your <b>menu photo</b> here — we read dish names &amp; prices with OCR.</div>
                </Field>
                <Field label="Shop front (photo)">
                  <div className="drop">🏪 Drop a <b>storefront photo</b> — signage &amp; foot-traffic cues.</div>
                </Field>
                <Field label="Google Maps page">
                  <input placeholder="https://maps.google.com/…" value={form.google_maps_url}
                    onChange={(e) => set("google_maps_url", e.target.value)} />
                </Field>
                <p className="note">Uploads are stubbed in this demo — dish data is entered in step 5.</p>
              </>
            )}

            {step === 2 && (
              <div className="grid2">
                <Field label="Open"><input type="time" value={form.open_time} onChange={(e) => set("open_time", e.target.value)} /></Field>
                <Field label="Close"><input type="time" value={form.close_time} onChange={(e) => set("close_time", e.target.value)} /></Field>
                <Field label="Days per week"><input type="number" min={0} max={7} value={form.days_per_week} onChange={num("days_per_week")} /></Field>
                <Field label="Peak period">
                  <select value={form.peak_period} onChange={(e) => set("peak_period", e.target.value)}>
                    <option>Breakfast</option><option>Lunch</option><option>Dinner</option><option>All day</option>
                  </select>
                </Field>
              </div>
            )}

            {step === 3 && (
              <div className="grid2">
                <Field label="Monthly revenue (HK$)"><input type="number" value={form.monthly_revenue} onChange={num("monthly_revenue")} /></Field>
                <Field label="Monthly rent (HK$)"><input type="number" value={form.monthly_rent} onChange={num("monthly_rent")} /></Field>
                <Field label="Staff cost / month (HK$)"><input type="number" value={form.monthly_staff_cost} onChange={num("monthly_staff_cost")} /></Field>
                <Field label="Ingredient cost % of sales"><input type="number" value={form.ingredient_pct} onChange={num("ingredient_pct")} /></Field>
                <Field label="Food waste % (weekday)"><input type="number" value={form.waste_pct} onChange={num("waste_pct")} /></Field>
                <Field label="Dishes on menu"><input type="number" value={form.menu_size} onChange={num("menu_size")} /></Field>
              </div>
            )}

            {step === 4 && (
              <>
                <p className="muted" style={{ marginTop: 0 }}>
                  Enter your top dishes — we compute each one's margin. Then Shop Doctor finds
                  similar nearby shops and splits them into <b>Survivors</b> and <b>Closed</b>.
                </p>
                {dishes.map((d, i) => (
                  <div className="grid2" key={i} style={{ gridTemplateColumns: "2fr 1fr 1fr 1fr", marginBottom: 10 }}>
                    <input placeholder="Dish name" value={d.name} onChange={(e) => updateDish(i, { name: e.target.value })} />
                    <input type="number" title="Price" value={d.price} onChange={(e) => updateDish(i, { price: Number(e.target.value) })} />
                    <input type="number" title="Cost" value={d.cost} onChange={(e) => updateDish(i, { cost: Number(e.target.value) })} />
                    <input type="number" title="Units/month" value={d.units_per_month} onChange={(e) => updateDish(i, { units_per_month: Number(e.target.value) })} />
                  </div>
                ))}
                <div style={{ display: "flex", gap: 10, marginTop: 6 }}>
                  <button className="btn btn-ghost btn-sm" onClick={() => setDishes((d) => [...d, { name: "", price: 30, cost: 12, units_per_month: 300, share_pct: 5 }])}>+ Add dish</button>
                  <button className="btn btn-ghost btn-sm" onClick={() => setDishes((d) => d.slice(0, -1))} disabled={dishes.length <= 1}>− Remove</button>
                </div>
                <div className="twins" style={{ marginTop: 16 }}>
                  <div className="metric"><div className="k">🟢 Survivors found</div><div className="v up">8</div><div className="note">still open after 2 years</div></div>
                  <div className="metric"><div className="k">🔴 Closed found</div><div className="v down">6</div><div className="note">shut down</div></div>
                </div>
              </>
            )}

            {error && <div className="error" style={{ marginTop: 14 }}>{error}</div>}

            <div className="cta">
              {step > 0 && <button className="btn btn-ghost" onClick={() => setStep(step - 1)}>← Back</button>}
              {!last ? (
                <button className="btn btn-primary" onClick={() => setStep(step + 1)}
                  disabled={step === 0 && !form.name.trim()}>
                  Continue →
                </button>
              ) : (
                <button className="btn btn-primary" onClick={finish} disabled={submitting || !form.name.trim()}>
                  {submitting ? "Diagnosing…" : "Get my diagnosis →"}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
