import { useEffect, useState } from "react";

/** Animated circular health-score gauge. */
export function Gauge({ score, band }: { score: number; band: string }) {
  const [shown, setShown] = useState(0);
  useEffect(() => {
    let v = 0;
    const step = Math.max(1, Math.round(score / 40));
    const t = setInterval(() => {
      v += step;
      if (v >= score) {
        v = score;
        clearInterval(t);
      }
      setShown(v);
    }, 18);
    return () => clearInterval(t);
  }, [score]);

  const color =
    band === "healthy" ? "var(--good)" : band === "watch" ? "var(--warn)" : "var(--bad)";
  return (
    <div
      className="gauge"
      style={{ background: `conic-gradient(${color} ${shown * 3.6}deg, #1d2c47 0)` }}
    >
      <div className="val">
        <b>{shown}</b>
        <span>Health Score</span>
      </div>
    </div>
  );
}

export function MarginBar({ pct }: { pct: number }) {
  return (
    <div className="margin-cell">
      <span style={{ minWidth: 40 }}>{pct}%</span>
      <span className="bar" style={{ flex: 1 }}>
        <i style={{ width: `${Math.max(4, Math.min(100, pct))}%` }} />
      </span>
    </div>
  );
}

export function Loader({ label = "Consulting Shop Doctor…" }: { label?: string }) {
  return <div className="loader">{label}</div>;
}

export function ErrorBox({ message }: { message: string }) {
  return <div className="error">{message}</div>;
}

export function money(n: number): string {
  return "HK$" + Math.round(n).toLocaleString();
}
