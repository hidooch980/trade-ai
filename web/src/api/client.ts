/**
 * Typed client for the Trade-AI FastAPI backend.
 *
 * Every route registered in backend/app/api/main.py is covered here:
 *   root/health, /dashboard/status, /backtest/run, /market/tick, /market/run,
 *   /market/status, /signal, /ws/market, /api/trading/*, /auth/*, /i18n/*,
 *   /guardian/*  — plus /api/ai/performance (see note on aiPerformance below).
 *
 * Base URL: VITE_API_BASE if set, otherwise the dev proxy at /api-proxy
 * (see vite.config.ts), which forwards to http://localhost:8000.
 */

import type {
  AdminUser,
  AdminUserList,
  AdminUserQuery,
  DashboardStatus,
  GuardianSummary,
  Json,
  LanguagesResponse,
  LoginPayload,
  Position,
  RegisterPayload,
  SessionResponse,
  TokenResponse,
} from "./types";

const ENV_BASE = (import.meta.env.VITE_API_BASE as string | undefined)?.replace(/\/$/, "");
export const API_BASE = ENV_BASE || "/api-proxy";

const ACCESS_KEY = "tradeai.access_token";
const REFRESH_KEY = "tradeai.refresh_token";
const USER_KEY = "tradeai.user";

export const tokenStore = {
  access: () => localStorage.getItem(ACCESS_KEY),
  refresh: () => localStorage.getItem(REFRESH_KEY),
  user: () => {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as TokenResponse["user"];
    } catch {
      return null;
    }
  },
  save: (t: TokenResponse) => {
    localStorage.setItem(ACCESS_KEY, t.access_token);
    localStorage.setItem(REFRESH_KEY, t.refresh_token);
    localStorage.setItem(USER_KEY, JSON.stringify(t.user));
  },
  clear: () => {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
  },
};

export class ApiError extends Error {
  status: number;
  body: unknown;
  constructor(status: number, message: string, body: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

interface RequestOptions {
  method?: string;
  body?: unknown;
  auth?: boolean;
  language?: string;
  signal?: AbortSignal;
  /** Internal: prevents infinite refresh recursion. */
  _retried?: boolean;
}

async function request<T>(path: string, opts: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, auth = false, language, signal } = opts;

  const headers: Record<string, string> = { Accept: "application/json" };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  // Backend resolves language via app/i18n/dependencies.get_request_language.
  if (language) headers["Accept-Language"] = language;
  if (auth) {
    const token = tokenStore.access();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
    signal,
  });

  // Access token expired: refresh once, then replay the original request.
  if (res.status === 401 && auth && !opts._retried && tokenStore.refresh()) {
    try {
      const refreshed = await auth_.refresh();
      tokenStore.save(refreshed);
      return request<T>(path, { ...opts, _retried: true });
    } catch {
      tokenStore.clear();
    }
  }

  const text = await res.text();
  let parsed: unknown = null;
  if (text) {
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = text;
    }
  }

  if (!res.ok) {
    const detail =
      (parsed && typeof parsed === "object" && "detail" in parsed
        ? String((parsed as Json).detail)
        : null) || res.statusText || `HTTP ${res.status}`;
    throw new ApiError(res.status, detail, parsed);
  }

  return parsed as T;
}

/* ------------------------------------------------------------------ system */

export const system = {
  /** GET / */
  root: () => request<{ status: string; system: string }>("/"),
  /** GET /health */
  health: () => request<{ status: string }>("/health"),
};

/* -------------------------------------------------------------------- auth */

const auth_ = {
  /** POST /auth/register */
  register: (payload: RegisterPayload) =>
    request<Json>("/auth/register", {
      method: "POST",
      body: { language: "en", ...payload },
    }),

  /** POST /auth/login */
  login: (payload: LoginPayload) =>
    request<TokenResponse>("/auth/login", {
      method: "POST",
      body: { language: "en", ...payload },
    }),

  /** POST /auth/refresh */
  refresh: () => {
    const refresh_token = tokenStore.refresh();
    if (!refresh_token) throw new ApiError(401, "No refresh token", null);
    return request<TokenResponse>("/auth/refresh", {
      method: "POST",
      body: { refresh_token },
    });
  },

  /** POST /auth/logout */
  logout: () => {
    const refresh_token = tokenStore.refresh();
    if (!refresh_token) return Promise.resolve({} as Json);
    return request<Json>("/auth/logout", {
      method: "POST",
      body: { refresh_token },
      auth: true,
    });
  },

  /** POST /auth/logout-all */
  logoutAll: () => request<Json>("/auth/logout-all", { method: "POST", auth: true }),

  /** GET /auth/me */
  me: () => request<TokenResponse["user"]>("/auth/me", { auth: true }),

  /** GET /auth/sessions */
  sessions: () => request<SessionResponse[]>("/auth/sessions", { auth: true }),

  /** POST /auth/forgot-password */
  forgotPassword: (email: string) =>
    request<Json>("/auth/forgot-password", { method: "POST", body: { email } }),

  /** POST /auth/reset-password */
  resetPassword: (token: string, new_password: string) =>
    request<Json>("/auth/reset-password", {
      method: "POST",
      body: { token, new_password },
    }),
};

export const auth = auth_;

/* ------------------------------------------------------------------- admin */

function queryString(params: Record<string, string | number | boolean | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === "") continue;
    search.set(key, String(value));
  }
  const out = search.toString();
  return out ? `?${out}` : "";
}

export const admin = {
  /** GET /admin/users */
  users: (query: AdminUserQuery = {}, signal?: AbortSignal) =>
    request<AdminUserList>(`/admin/users${queryString({ ...query })}`, {
      auth: true,
      signal,
    }),

  /** GET /admin/users/{id} */
  user: (id: string, signal?: AbortSignal) =>
    request<AdminUser>(`/admin/users/${encodeURIComponent(id)}`, { auth: true, signal }),

  /** GET /admin/users/{id}/sessions */
  userSessions: (id: string, signal?: AbortSignal) =>
    request<SessionResponse[]>(`/admin/users/${encodeURIComponent(id)}/sessions`, {
      auth: true,
      signal,
    }),

  /** PATCH /admin/users/{id}/role */
  setRole: (id: string, role: string) =>
    request<AdminUser>(`/admin/users/${encodeURIComponent(id)}/role`, {
      method: "PATCH",
      body: { role },
      auth: true,
    }),

  /** POST /admin/users/{id}/lock */
  lock: (id: string, minutes?: number) =>
    request<AdminUser>(`/admin/users/${encodeURIComponent(id)}/lock`, {
      method: "POST",
      body: minutes ? { minutes } : {},
      auth: true,
    }),

  /** POST /admin/users/{id}/unlock */
  unlock: (id: string) =>
    request<AdminUser>(`/admin/users/${encodeURIComponent(id)}/unlock`, {
      method: "POST",
      auth: true,
    }),

  /** POST /admin/users/{id}/revoke-sessions */
  revokeSessions: (id: string) =>
    request<AdminUser>(`/admin/users/${encodeURIComponent(id)}/revoke-sessions`, {
      method: "POST",
      auth: true,
    }),
};

/* --------------------------------------------------------------- dashboard */

export const dashboard = {
  /** GET /dashboard/status */
  status: (signal?: AbortSignal) =>
    request<DashboardStatus>("/dashboard/status", { signal }),
};

/* ------------------------------------------------------------------ market */

export const market = {
  /** GET /market/status */
  status: (signal?: AbortSignal) => request<Json>("/market/status", { signal }),
  /** POST /market/tick */
  tick: (payload: Json) => request<Json>("/market/tick", { method: "POST", body: payload }),
  /** POST /market/run */
  run: () => request<Json>("/market/run", { method: "POST" }),
  /** POST /signal */
  signal: (payload: Json) => request<Json>("/signal", { method: "POST", body: payload }),
};

/* ---------------------------------------------------------------- backtest */

export const backtest = {
  /** POST /backtest/run */
  run: (payload: Json) => request<Json>("/backtest/run", { method: "POST", body: payload }),
};

/* ----------------------------------------------------------------- trading */

export const trading = {
  /** GET /api/trading/positions */
  positions: (signal?: AbortSignal) =>
    request<Position[] | Json>("/api/trading/positions", { auth: true, signal }),
  /** GET /api/trading/history */
  history: (signal?: AbortSignal) =>
    request<Position[] | Json>("/api/trading/history", { auth: true, signal }),
  /** GET /api/trading/journal */
  journal: (signal?: AbortSignal) =>
    request<Json[] | Json>("/api/trading/journal", { auth: true, signal }),
  /** POST /api/trading/close/{ticket} */
  close: (ticket: string) =>
    request<Json>(`/api/trading/close/${encodeURIComponent(ticket)}`, {
      method: "POST",
      auth: true,
    }),
  /** POST /api/trading/monitor */
  monitor: (payload: Json) =>
    request<Json>("/api/trading/monitor", { method: "POST", body: payload, auth: true }),
  /** POST /api/trading/tick */
  tick: (payload: Json) =>
    request<Json>("/api/trading/tick", { method: "POST", body: payload, auth: true }),
  /** POST /api/trading/execute */
  execute: (payload: Json) =>
    request<Json>("/api/trading/execute", { method: "POST", body: payload, auth: true }),
};

/* ---------------------------------------------------------------- guardian */

export const guardian = {
  /** GET /guardian/status */
  status: (signal?: AbortSignal) => request<Json>("/guardian/status", { signal }),
  /** GET /guardian/summary */
  summary: (signal?: AbortSignal) =>
    request<GuardianSummary>("/guardian/summary", { signal }),
};

/* -------------------------------------------------------------------- i18n */

export const i18n = {
  /** GET /i18n/languages */
  languages: () => request<LanguagesResponse>("/i18n/languages"),
  /** GET /i18n/current */
  current: (language?: string) => request<Json>("/i18n/current", { language }),
};

/* ----------------------------------------------------------------------- ai
 * NOTE: backend/app/api/routes/ai_performance.py defines these routes but the
 * module is NOT included in app/api/main.py, so they 404 until a
 * `app.include_router(ai_performance.router)` line is added there.
 */
export const ai = {
  /** GET /api/ai/performance */
  performance: (signal?: AbortSignal) =>
    request<Json>("/api/ai/performance", { signal }),
  /** GET /api/ai/performance/{symbol}/{timeframe} */
  performanceFor: (symbol: string, timeframe: string, signal?: AbortSignal) =>
    request<Json>(
      `/api/ai/performance/${encodeURIComponent(symbol)}/${encodeURIComponent(timeframe)}`,
      { signal },
    ),
};

/* --------------------------------------------------------------- websocket */

/** Opens /ws/market. Returns a closer function. */
export function connectMarketSocket(
  onMessage: (data: unknown) => void,
  onStateChange?: (state: "connecting" | "open" | "closed") => void,
): () => void {
  let socket: WebSocket | null = null;
  let retry: ReturnType<typeof setTimeout> | null = null;
  let disposed = false;
  let attempt = 0;

  const url = () => {
    const base = API_BASE.startsWith("http")
      ? API_BASE
      : `${location.origin}${API_BASE}`;
    return `${base.replace(/^http/, "ws")}/ws/market`;
  };

  const open = () => {
    if (disposed) return;
    onStateChange?.("connecting");
    try {
      socket = new WebSocket(url());
    } catch {
      schedule();
      return;
    }
    socket.onopen = () => {
      attempt = 0;
      onStateChange?.("open");
    };
    socket.onmessage = (ev) => {
      try {
        onMessage(JSON.parse(ev.data));
      } catch {
        onMessage(ev.data);
      }
    };
    socket.onclose = () => {
      onStateChange?.("closed");
      schedule();
    };
    socket.onerror = () => socket?.close();
  };

  const schedule = () => {
    if (disposed) return;
    attempt = Math.min(attempt + 1, 6);
    retry = setTimeout(open, 1000 * 2 ** (attempt - 1));
  };

  open();

  return () => {
    disposed = true;
    if (retry) clearTimeout(retry);
    socket?.close();
  };
}

export const api = {
  system,
  auth,
  admin,
  dashboard,
  market,
  backtest,
  trading,
  guardian,
  i18n,
  ai,
  connectMarketSocket,
};

export default api;
