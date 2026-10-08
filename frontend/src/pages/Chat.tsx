import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import { useShop } from "../components/ShopContext";

type Lang = "en" | "zh";
interface Msg { who: "bot" | "me"; text: string; }

const GREET: Record<Lang, string> = {
  en: "Hi! I'm your Shop Doctor 🩺 I've read your shop's report. Ask me about margins, pricing, waste, or marketing — in English or 廣東話.",
  zh: "你好！我係你嘅 Shop Doctor 🩺 我睇咗你店舖嘅報告。可以問我利潤、定價、浪費或者推廣 — 廣東話或英文都得。",
};

const QUICK: Record<Lang, string[]> = {
  en: ["Which dishes lose money?", "Should I raise prices?", "How do I cut waste?", "Marketing ideas?"],
  zh: ["邊啲菜蝕錢？", "應該加價嗎？", "點樣減少浪費？", "推廣建議？"],
};

export default function Chat() {
  const { activeShop } = useShop();
  const [lang, setLang] = useState<Lang>("en");
  const [msgs, setMsgs] = useState<Msg[]>([{ who: "bot", text: GREET.en }]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const logRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMsgs([{ who: "bot", text: GREET[lang] }]);
  }, [lang]);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: "smooth" });
  }, [msgs]);

  async function send(text: string) {
    const message = text.trim();
    if (!message || busy) return;
    setMsgs((m) => [...m, { who: "me", text: message }]);
    setInput("");
    setBusy(true);
    try {
      const res = await api.chat({
        message,
        lang,
        shop_id: activeShop?.id,
      });
      setMsgs((m) => [...m, { who: "bot", text: res.reply }]);
    } catch {
      setMsgs((m) => [...m, { who: "bot", text: "Sorry — I couldn't reach Shop Doctor. Is the backend running?" }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <h2 className="sec">Ask Shop Doctor</h2>
      <p className="sub">Follow-up chat in Cantonese or English, grounded in your report.</p>
      <div className="card chat">
        <div className="log" ref={logRef}>
          {msgs.map((m, i) => (
            <div className={`msg ${m.who}`} key={i}>{m.text}</div>
          ))}
          {busy && <div className="msg bot">…</div>}
        </div>
        <div className="quick">
          {QUICK[lang].map((q) => (
            <button key={q} onClick={() => send(q)} disabled={busy}>{q}</button>
          ))}
        </div>
        <div className="input">
          <div className="lang">
            <button className={lang === "en" ? "active" : ""} onClick={() => setLang("en")}>EN</button>
            <button className={lang === "zh" ? "active" : ""} onClick={() => setLang("zh")}>廣東話</button>
          </div>
          <input
            value={input}
            placeholder={lang === "zh" ? "問吓你嘅店舖…" : "Ask about your shop…"}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send(input)}
          />
          <button className="btn btn-primary btn-sm" onClick={() => send(input)} disabled={busy}>Send</button>
        </div>
      </div>
    </>
  );
}
