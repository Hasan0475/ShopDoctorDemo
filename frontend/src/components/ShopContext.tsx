import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { Report, Shop } from "../types";
import { api } from "../api/client";

interface ShopCtx {
  shops: Shop[];
  activeShop: Shop | null;
  setActiveShopId: (id: number) => void;
  report: Report | null;
  reloadReport: () => Promise<void>;
  loading: boolean;
  error: string | null;
  backendOnline: boolean;
}

const Ctx = createContext<ShopCtx | null>(null);

export function ShopProvider({ children }: { children: ReactNode }) {
  const [shops, setShops] = useState<Shop[]>([]);
  const [activeShopId, setActiveShopId] = useState<number | null>(null);
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [backendOnline, setBackendOnline] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        await api.health();
        setBackendOnline(true);
        const list = await api.listShops();
        setShops(list);
        if (list.length) setActiveShopId((prev) => prev ?? list[0].id);
      } catch (e) {
        setBackendOnline(false);
        setError(e instanceof Error ? e.message : "Backend unreachable");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const reloadReport = async () => {
    if (!activeShopId) return;
    setLoading(true);
    try {
      setReport(await api.getReport(activeShopId));
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load report");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeShopId) void reloadReport();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeShopId]);

  const activeShop = shops.find((s) => s.id === activeShopId) ?? null;

  return (
    <Ctx.Provider
      value={{
        shops,
        activeShop,
        setActiveShopId,
        report,
        reloadReport,
        loading,
        error,
        backendOnline,
      }}
    >
      {children}
    </Ctx.Provider>
  );
}

export function useShop(): ShopCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useShop must be used within ShopProvider");
  return ctx;
}
