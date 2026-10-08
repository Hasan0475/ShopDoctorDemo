import { useShop } from "../components/ShopContext";
import { ErrorBox, Gauge, Loader, MarginBar } from "../components/ui";

export default function HealthReport() {
  const { report, loading, error } = useShop();

  if (loading && !report) return <Loader />;
  if (error && !report) return <ErrorBox message={error} />;
  if (!report) return <ErrorBox message="No report available. Is the backend running?" />;

  return (
    <>
      <h2 className="sec">Health Report</h2>
      <p className="sub">{report.shop_name} · last 3 months</p>

      <div className="card">
        <div className="pad">
          <div className="score-wrap">
            <Gauge score={report.health_score} band={report.score_band} />
            <div className="metrics">
              {report.metrics.map((m) => (
                <div className="metric" key={m.label}>
                  <div className="k">{m.label}</div>
                  <div className={`v tone-${m.tone}`}>{m.value}</div>
                </div>
              ))}
            </div>
          </div>
          <p className="note">{report.diagnosis}</p>
        </div>
      </div>

      <h2 className="sec" style={{ marginTop: 30, fontSize: 20 }}>Dish profit margins</h2>
      <p className="sub">What is actually making — and losing — money.</p>
      <div className="card">
        <div className="pad" style={{ padding: "6px 20px" }}>
          <table>
            <thead>
              <tr>
                <th>Dish</th>
                <th>Price</th>
                <th>Cost</th>
                <th>Margin</th>
                <th>Share</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {report.dishes.map((d) => (
                <tr key={d.id}>
                  <td style={{ fontWeight: 600 }}>{d.name}</td>
                  <td>HK${d.price}</td>
                  <td>HK${d.cost}</td>
                  <td style={{ minWidth: 140 }}><MarginBar pct={d.margin_pct} /></td>
                  <td>{d.share_pct}%</td>
                  <td>
                    <span className={`tag ${d.status}`}>
                      {d.status === "healthy" ? "Healthy" : d.status === "thin" ? "Thin" : "Losing"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <h2 className="sec" style={{ marginTop: 30, fontSize: 20 }}>Top problems</h2>
      <p className="sub">Ranked by impact on profit.</p>
      {report.problems.map((p, i) => (
        <div className={`prob sev-${p.severity}`} key={i}>
          <div className="ic">{p.icon}</div>
          <div>
            <h4>{p.title}</h4>
            <p>{p.detail}</p>
          </div>
        </div>
      ))}

      <h2 className="sec" style={{ marginTop: 30, fontSize: 20 }}>
        Twin Shops — Survivors vs Closed
      </h2>
      <p className="sub">
        Similar {report.shop_name ? "cha chaan tengs" : "shops"} in the area, split by who was
        still open after 2 years ({report.twins.survivors_count} survived · {report.twins.closed_count} closed).
      </p>
      <div className="twins">
        <div className="card twin">
          <div className="pad">
            <h3><span className="dotg" /> Survivors (still open)</h3>
            <div className="list">
              {report.twins.survivors.map((t) => (
                <div className="item" key={t.name}>
                  <span>{t.name}</span>
                  <span className="muted" style={{ fontSize: 13, textAlign: "right" }}>{t.trait}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="card twin">
          <div className="pad">
            <h3><span className="dotb" /> Closed (shut down)</h3>
            <div className="list">
              {report.twins.closed.map((t) => (
                <div className="item" key={t.name}>
                  <span>{t.name}</span>
                  <span className="muted" style={{ fontSize: 13, textAlign: "right" }}>{t.trait}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
