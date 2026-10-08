import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import { useShop } from "../components/ShopContext";
import { ErrorBox, Loader } from "../components/ui";
import type { MarketingPost } from "../types";

export default function Marketing() {
  const { activeShop, loading } = useShop();
  const [posts, setPosts] = useState<MarketingPost[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState<number | null>(null);

  const load = useCallback(async () => {
    if (!activeShop) return;
    setBusy(true);
    setError(null);
    try {
      const res = await api.marketing(activeShop.id, 4);
      setPosts(res.posts);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load marketing kit");
    } finally {
      setBusy(false);
    }
  }, [activeShop]);

  useEffect(() => {
    void load();
  }, [load]);

  async function copy(i: number, text: string) {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(i);
      setTimeout(() => setCopied(null), 1200);
    } catch {
      /* clipboard unavailable */
    }
  }

  if (loading && !activeShop) return <Loader />;
  if (!activeShop) return <ErrorBox message="No shop selected — run a check-up first." />;

  return (
    <>
      <h2 className="sec">Marketing Kit</h2>
      <p className="sub">
        Instagram post ideas, captions and photo briefs — generated from your highest-margin dishes.
      </p>
      <div style={{ marginBottom: 16 }}>
        <button className="btn btn-ghost btn-sm" onClick={load} disabled={busy}>
          {busy ? "Generating…" : "↻ Regenerate ideas"}
        </button>
        <span className="badge" style={{ marginLeft: 8 }}>Pro feature</span>
      </div>

      {error && <div className="error" style={{ marginBottom: 16 }}>{error}</div>}

      <div className="mk">
        {posts.map((p, i) => (
          <div className="post" key={i}>
            <div className="img">{p.emoji}</div>
            <div className="body">
              <h4>{p.title}</h4>
              <p>{p.rationale}</p>
              <div className="caption">"{p.caption}"</div>
              <button className="copy" onClick={() => copy(i, p.caption)}>
                {copied === i ? "Copied ✓" : "Copy caption"}
              </button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
