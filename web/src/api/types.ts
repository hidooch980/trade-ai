// Response shapes mirrored from backend/app (FastAPI).
// Where a route returns an unmodelled dict we keep it permissive rather than lie about the shape.

export interface UserResponse {
  id: string;
  email: string;
  username: string;
  language: string;
  role: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: UserResponse;
}

export interface SessionResponse {
  id: string;
  device_name: string | null;
  ip_address: string | null;
  user_agent: string | null;
  expires_at: string;
  last_used_at: string | null;
  revoked_at: string | null;
  created_at: string;
}

export interface AdminUser {
  id: string;
  email: string;
  username: string;
  language: string;
  role: string;
  failed_login_attempts: number;
  locked_until: string | null;
  is_locked: boolean;
  email_verified_at: string | null;
  active_sessions: number;
  created_at: string;
  updated_at: string;
}

export interface AdminUserList {
  items: AdminUser[];
  total: number;
  limit: number;
  offset: number;
}

export interface AdminUserQuery {
  search?: string;
  role?: string;
  locked?: boolean;
  limit?: number;
  offset?: number;
}

export type AccountKind = "DEMO" | "REAL";
export type AccountStatus = "PENDING" | "CONNECTED" | "DISCONNECTED" | "ERROR";

export interface TradingAccount {
  id: string;
  name: string;
  platform: string;
  broker: string | null;
  server: string | null;
  login: string | null;
  account_kind: AccountKind;
  status: AccountStatus;
  is_default: boolean;
  currency: string;
  balance: string;
  equity: string;
  leverage: number | null;
  /** Whether the server still holds a terminal password for this account. */
  has_credentials: boolean;
  last_connected_at: string | null;
  last_error: string | null;
  created_at: string;
  updated_at: string;
}

export interface TradingAccountList {
  items: TradingAccount[];
  total: number;
  /** SIMULATION while the MT5 adapter runs on the in-process bridge. */
  mode: string;
}

export interface AccountConnection {
  account: TradingAccount;
  connected: boolean;
  status: string;
  mode: string;
  detail: string | null;
}

export interface AccountRegisterPayload {
  name: string;
  server: string;
  login: string;
  password: string;
  account_kind: AccountKind;
  broker?: string | null;
  currency?: string;
  make_default?: boolean;
}

export interface RegisterPayload {
  email: string;
  username: string;
  password: string;
  language?: string;
}

export interface LoginPayload {
  username: string;
  password: string;
  language?: string;
  device_name?: string | null;
}

export interface DashboardStatus {
  market: unknown;
  strategy: unknown;
  journal_count: number;
  feedback: unknown;
  system: string;
}

export interface GuardianSummary {
  status: string | null;
  services: Record<string, unknown> | null;
  risk: Record<string, unknown> | null;
  open_positions: unknown;
  execution: Record<string, unknown> | null;
}

export interface Position {
  ticket?: string | number;
  symbol?: string;
  side?: string;
  type?: string;
  volume?: number;
  lot?: number;
  entry?: number;
  entry_price?: number;
  price?: number;
  sl?: number;
  tp?: number;
  pnl?: number;
  profit?: number;
  opened_at?: string;
  [key: string]: unknown;
}

export interface LanguagesResponse {
  languages?: string[];
  supported?: string[];
  [key: string]: unknown;
}

export type Json = Record<string, unknown>;
