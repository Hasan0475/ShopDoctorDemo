// Typed API client. Base URL is proxied by Vite in dev (see vite.config.ts);
// set VITE_API_URL for other environments.
import type {
  ChatResult,
  Health,
  MarketingResult,
  Report,
  Shop,
  ShopCreate,
  SimulatorResult,
  TwinGroups,
} from "../types";

const BASE = (import.meta.env.VITE_API_URL as string | undefined) ?? "/api";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`${res.status} ${res.statusText}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => req<Health>("/health"),
  listShops: () => req<Shop[]>("/shops"),
  createShop: (payload: ShopCreate) =>
    req<Shop>("/shops", { method: "POST", body: JSON.stringify(payload) }),
  getReport: (shopId: number) => req<Report>(`/shops/${shopId}/report`),
  getTwins: (shopId: number) => req<TwinGroups>(`/shops/${shopId}/twins`),
  simulate: (payload: {
    dish: string;
    base_price: number;
    base_cost: number;
    base_units: number;
    price: number;
  }) => req<SimulatorResult>("/simulator", { method: "POST", body: JSON.stringify(payload) }),
  chat: (payload: { message: string; lang: "en" | "zh"; shop_id?: number }) =>
    req<ChatResult>("/chat", { method: "POST", body: JSON.stringify(payload) }),
  marketing: (shopId: number, limit = 4) =>
    req<MarketingResult>(`/shops/${shopId}/marketing?limit=${limit}`),
};
