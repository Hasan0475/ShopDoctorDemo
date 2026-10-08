import { NavLink, Route, Routes } from "react-router-dom";
import { ShopProvider, useShop } from "./components/ShopContext";
import Home from "./pages/Home";
import CheckUp from "./pages/CheckUp";
import HealthReport from "./pages/HealthReport";
import Simulator from "./pages/Simulator";
import Chat from "./pages/Chat";
import Marketing from "./pages/Marketing";
import Business from "./pages/Business";

const LINKS = [
  { to: "/", label: "Home", end: true },
  { to: "/checkup", label: "Check-Up" },
  { to: "/report", label: "Health Report" },
  { to: "/simulator", label: "Price Simulator" },
  { to: "/chat", label: "Ask Shop Doctor" },
  { to: "/marketing", label: "Marketing Kit" },
  { to: "/business", label: "Business" },
];

function Banner() {
  const { backendOnline } = useShop();
  if (backendOnline) return null;
  return (
    <div className="wrap" style={{ paddingTop: 16 }}>
      <div className="error">
        <b>Backend not reachable.</b> Start the API with{" "}
        <code>uvicorn app.main:app --reload</code> in <code>backend/</code>, then refresh.
      </div>
    </div>
  );
}

function Shell() {
  return (
    <>
      <header className="top">
        <div className="wrap nav">
          <div className="logo">
            <span className="dot">✚</span> ShopDoctor{" "}
            <span className="badge">HACK4SDG · SDG 8</span>
          </div>
          <nav className="links">
            {LINKS.map((l) => (
              <NavLink key={l.to} to={l.to} end={l.end} className={({ isActive }) => (isActive ? "active" : "")}>
                {l.label}
              </NavLink>
            ))}
          </nav>
          <NavLink to="/checkup" className="btn btn-primary btn-sm">
            Start free check-up
          </NavLink>
        </div>
      </header>
      <Banner />
      <main className="wrap page">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/checkup" element={<CheckUp />} />
          <Route path="/report" element={<HealthReport />} />
          <Route path="/simulator" element={<Simulator />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/marketing" element={<Marketing />} />
          <Route path="/business" element={<Business />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
      <footer>
        <div className="wrap">
          ShopDoctor · demo prototype for HACK4SDG (Track 4: Future Work &amp; Enterprises) ·
          SDG 8: Decent Work &amp; Economic Growth. All figures illustrative.
        </div>
      </footer>
    </>
  );
}

export default function App() {
  return (
    <ShopProvider>
      <Shell />
    </ShopProvider>
  );
}
