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
