// Types mirroring the FastAPI Pydantic schemas.

export interface Dish {
  id: number;
  name: string;
  price: number;
  cost: number;
  units_per_month: number;
  share_pct: number;
  margin: number;
  margin_pct: number;
  status: "healthy" | "thin" | "losing";
}

export interface Metric {
  label: string;
  value: string;
  tone: "neutral" | "good" | "warn" | "bad";
}

export interface Problem {
  icon: string;
  title: string;
  detail: string;
  severity: "good" | "warn" | "bad";
}

export interface Twin {
  name: string;
  trait: string;
}

export interface TwinGroups {
  survivors: Twin[];
  closed: Twin[];
  survivors_count: number;
  closed_count: number;
}

export interface Report {
  shop_id: number;
  shop_name: string;
  health_score: number;
  score_band: "healthy" | "watch" | "at-risk";
  summary: string;
  metrics: Metric[];
  dishes: Dish[];
  problems: Problem[];
  twins: TwinGroups;
  diagnosis: string;
}

export interface Shop {
  id: number;
  name: string;
  shop_type: string;
  district: string;
  years_open: number;
  monthly_revenue: number;
  created_at: string;
}

export interface SimulatorResult {
  dish: string;
  base_price: number;
  new_price: number;
  elasticity: number;
  base_units: number;
  new_units: number;
  base_margin_pct: number;
  new_margin_pct: number;
  before_profit: number;
  after_profit: number;
  profit_delta: number;
  direction: "up" | "down" | "flat";
  advice_title: string;
  advice: string;
}

export interface ChatResult {
  reply: string;
  lang: "en" | "zh";
  intent: string;
}

export interface MarketingPost {
  emoji: string;
  title: string;
  rationale: string;
  caption: string;
}

export interface MarketingResult {
  shop_id: number | null;
  posts: MarketingPost[];
}

export interface Health {
  status: string;
  version: string;
  llm_provider: string;
}

export interface DishInput {
  name: string;
  price: number;
  cost: number;
  units_per_month: number;
  share_pct: number;
}

export interface ShopCreate {
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
  google_maps_url?: string;
  dishes: DishInput[];
}
