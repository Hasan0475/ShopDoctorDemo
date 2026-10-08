import { Link } from "react-router-dom";
import { useShop } from "../components/ShopContext";
import { Gauge, Loader } from "../components/ui";

const FIVE_STEPS = [
  { n: "1", t: "The Check-Up", p: "Menu, storefront & Google Maps photos, opening hours, revenue + costs." },
  { n: "2", t: "Twin Shops", p: "Finds similar nearby shops, split into Survivors and Closed." },
  { n: "3", t: "Diagnosis", p: "Compares the two groups: what did survivors do differently?" },
  { n: "4", t: "Prescription", p: "Health score, predicted revenue, and concrete suggestions." },
  { n: "5", t: "Follow-Up", p: "After a month, new data adjusts the plan. (Pro)" },
];

const TOOLS = [
  { to: "/report", ic: "📋", t: "Health Report", p: "Score, dish profit margins, top problems." },
  { to: "/simulator", ic: "🎚️", t: "Price Simulator", p: "Slide a price, see monthly profit change." },
  { to: "/chat", ic: "💬", t: "Ask Shop Doctor", p: "Follow-up chat in Cantonese or English." },
  { to: "/marketing", ic: "📣", t: "Marketing Kit", p: "Outlines for Insta posts, captions, photos." },
];

export default function Home() {
  const { report, loading } = useShop();
  return (
    <>
      <div className="hero">
        <div>
          <span className="pill">Track 4 · Future Work &amp; Enterprises</span>
          <h1>
            A 20-minute AI check-up that shows your shop's <span className="grad">health</span>.
          </h1>
          <p className="lede">
            Shop Doctor reads a restaurant's numbers, finds what is losing money, and gives
            data-backed suggestions — like a family doctor for Hong Kong's small shops.
          </p>
          <div className="cta">
            <Link to="/checkup" className="btn btn-primary">Start free check-up →</Link>
            <Link to="/report" className="btn btn-ghost">See a sample report</Link>
          </div>
          <p className="note">
            Full-stack demo (FastAPI + React) with illustrative data · Free check-up, Pro
            follow-up care.
          </p>
        </div>
        <div className="card">
          <div className="pad">
            {loading || !report ? (
              <Loader label="Loading sample shop…" />
            ) : (
              <>
                <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
                  <div>
                    <div style={{ fontWeight: 800, fontSize: 16 }}>{report.shop_name}</div>
                    <div className="pill" style={{ marginTop: 6 }}>Sham Shui Po · Café</div>
                  </div>
                  <span className={`tag ${report.score_band === "at-risk" ? "losing" : report.score_band === "watch" ? "thin" : "healthy"}`}>
                    {report.score_band === "at-risk" ? "At risk" : report.score_band === "watch" ? "Watch" : "Healthy"}
                  </span>
                </div>
                <div className="score-wrap" style={{ marginTop: 18 }}>
                  <Gauge score={report.health_score} band={report.score_band} />
                  <div style={{ flex: 1, minWidth: 170 }}>
                    {report.metrics.slice(1, 3).map((m) => (
                      <div className="metric" key={m.label} style={{ marginBottom: 10 }}>
                        <div className="k">{m.label}</div>
                        <div className={`v tone-${m.tone}`}>{m.value}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      <h2 className="sec" style={{ marginTop: 44 }}>Five steps, like a visit to a doctor</h2>
      <p className="sub">How it works — from check-up to follow-up.</p>
      <div className="steps">
        {FIVE_STEPS.map((s) => (
          <div className="step" key={s.n}>
            <div className="n">{s.n}</div>
            <h4>{s.t}</h4>
            <p>{s.p}</p>
          </div>
        ))}
      </div>

      <h2 className="sec" style={{ marginTop: 44 }}>What owners receive</h2>
      <p className="sub">Four tools, one dashboard.</p>
      <div className="steps four">
        {TOOLS.map((t) => (
          <Link to={t.to} className="step clickable" key={t.t}>
            <div className="n">{t.ic}</div>
            <h4>{t.t}</h4>
            <p>{t.p}</p>
          </Link>
        ))}
      </div>
    </>
  );
}
