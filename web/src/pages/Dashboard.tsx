import { useCallback, useState } from "react";
import {
  ai,
  backtest,
  dashboard as dashboardApi,
  guardian,
  market,
  trading,
} from "../api/client";
import type { Json, Position, SessionResponse } from "../api/types";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { auth } from "../api/client";
import { LiveHud } from "../components/LiveHud";
import { Panel, useEndpoint } from "../components/Panel";

/* ------------------------------------------------------------- primitives */

function JsonBlock({ value }: { value: unknown }) {
  const { t } = useApp();
  if (value === null || value === undefined) return <p className="empty">{t("dash.empty")}</p>;
  return <pre className="json">{JSON.stringify(value, null, 2)}</pre>;
}

function asArray(value: unknown): Record<string, unknown>[] {
  if (Array.isArray(value)) return value as Record<string, unknown>[];
  if (value && typeof value === "object") {
    for (const key of ["positions", "history", "journal", "items", "data", "result"]) {
      const inner = (value as Record<string, unknown>)[key];
      if (Array.isArray(inner)) return inner as Record<string, unknown>[];
    }
  }
  return [];
}

/* -------------------------------------------------------------- positions */

function PositionsPanel() {
  const { t, n } = useApp();
  const { data, error, busy, reload } = useEndpoint<Position[] | Json>(
    useCallback((s?: AbortSignal) => trading.positions(s), []),
  );
  const [closing, setClosing] = useState<string | null>(null);

  const rows = asArray(data) as Position[];

  const close = async (ticket: string) => {
    setClosing(ticket);
    try {
      await trading.close(ticket);
      reload();
    } catch {
      // The error surfaces on the next reload; nothing useful to add here.
    } finally {
      setClosing(null);
    }
  };

  return (
    <Panel title={t("dash.positions")} onRefresh={reload} busy={busy}>
      {error && <p className="empty">{error}</p>}
      {!error && rows.length === 0 && <p className="empty">{t("dash.empty")}</p>}
      {rows.length > 0 && (
        <table className="data">
          <thead>
            <tr>
              <th>#</th>
              <th>{t("dash.symbol")}</th>
              <th>Side</th>
              <th>Lot</th>
              <th>Entry</th>
              <th>PnL</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {rows.map((p, i) => {
              const ticket = String(p.ticket ?? i);
              const pnl = Number(p.pnl ?? p.profit ?? 0);
              return (
                <tr key={ticket}>
                  <td>{n(ticket)}</td>
                  <td>{String(p.symbol ?? "—")}</td>
                  <td>{String(p.side ?? p.type ?? "—").toUpperCase()}</td>
                  <td>{n(String(p.volume ?? p.lot ?? "—"))}</td>
                  <td>{n(String(p.entry ?? p.entry_price ?? p.price ?? "—"))}</td>
                  <td className={pnl >= 0 ? "up" : "down"}>{n(pnl.toFixed(2))}</td>
                  <td>
                    <button
                      className="btn btn--danger btn--sm"
                      disabled={closing === ticket}
                      onClick={() => void close(ticket)}
                    >
                      {closing === ticket ? <span className="spinner" /> : t("dash.close")}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </Panel>
  );
}

/* ---------------------------------------------------------------- generic */

function HistoryPanel() {
  const { t } = useApp();
  const { data, error, busy, reload } = useEndpoint(
    useCallback((s?: AbortSignal) => trading.history(s), []),
  );
  return (
    <Panel title={t("dash.history")} onRefresh={reload} busy={busy}>
      {error ? <p className="empty">{error}</p> : <JsonBlock value={data} />}
    </Panel>
  );
}

function JournalPanel() {
  const { t } = useApp();
  const { data, error, busy, reload } = useEndpoint(
    useCallback((s?: AbortSignal) => trading.journal(s), []),
  );
  return (
    <Panel title={t("dash.journal")} onRefresh={reload} busy={busy}>
      {error ? <p className="empty">{error}</p> : <JsonBlock value={data} />}
    </Panel>
  );
}

function GuardianPanel() {
  const { t } = useApp();
  const { data, error, busy, reload } = useEndpoint(
    useCallback((s?: AbortSignal) => guardian.status(s), []),
  );
  return (
    <Panel title={t("dash.guardian")} onRefresh={reload} busy={busy}>
      {error ? <p className="empty">{error}</p> : <JsonBlock value={data} />}
    </Panel>
  );
}

function SystemPanel() {
  const { t, n } = useApp();
  const { data, error, busy, reload } = useEndpoint(
    useCallback((s?: AbortSignal) => dashboardApi.status(s), []),
  );
  return (
    <Panel title={t("dash.system")} onRefresh={reload} busy={busy}>
      {error && <p className="empty">{error}</p>}
      {data && (
        <div className="kv">
          <div className="kv__row">
            <span className="kv__k">system</span>
            <span className="kv__v">{String(data.system)}</span>
          </div>
          <div className="kv__row">
            <span className="kv__k">{t("dash.journalCount")}</span>
            <span className="kv__v">{n(data.journal_count ?? 0)}</span>
          </div>
          <div className="kv__row">
            <span className="kv__k">strategy</span>
            <span className="kv__v">{JSON.stringify(data.strategy)}</span>
          </div>
          <div className="kv__row">
            <span className="kv__k">feedback</span>
            <span className="kv__v">{JSON.stringify(data.feedback)}</span>
          </div>
        </div>
      )}
    </Panel>
  );
}

function SessionsPanel() {
  const { t, n } = useApp();
  const { data, error, busy, reload } = useEndpoint<SessionResponse[]>(
    useCallback(() => auth.sessions(), []),
  );
  const rows = Array.isArray(data) ? data : [];
  return (
    <Panel
      title={t("dash.sessions")}
      onRefresh={reload}
      busy={busy}
      action={
        <button className="btn btn--danger btn--sm" onClick={() => void auth.logoutAll().then(reload)}>
          logout-all
        </button>
      }
    >
      {error && <p className="empty">{error}</p>}
      {!error && rows.length === 0 && <p className="empty">{t("dash.empty")}</p>}
      {rows.length > 0 && (
        <table className="data">
          <thead>
            <tr>
              <th>Device</th>
              <th>IP</th>
              <th>Last used</th>
              <th>Expires</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((s) => (
              <tr key={s.id}>
                <td>{s.device_name ?? "—"}</td>
                <td>{s.ip_address ?? "—"}</td>
                <td>{n(s.last_used_at?.slice(0, 16).replace("T", " ") ?? "—")}</td>
                <td>{n(s.expires_at?.slice(0, 16).replace("T", " ") ?? "—")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Panel>
  );
}

function AiPanel() {
  const { t } = useApp();
  const { data, error, busy, reload } = useEndpoint(
    useCallback((s?: AbortSignal) => ai.performance(s), []),
  );
  return (
    <Panel title={t("dash.performance")} onRefresh={reload} busy={busy}>
      {error ? (
        <p className="empty">
          {error} — <code>/api/ai/performance</code> is defined in
          <code> app/api/routes/ai_performance.py</code> but not registered in
          <code> app/api/main.py</code>.
        </p>
      ) : (
        <JsonBlock value={data} />
      )}
    </Panel>
  );
}

/* ------------------------------------------------------------ engine tools */

function ToolsPanel() {
  const { t } = useApp();
  const [symbol, setSymbol] = useState("XAUUSD");
  const [timeframe, setTimeframe] = useState("M1");
  const [result, setResult] = useState<unknown>(null);
  const [busy, setBusy] = useState<string | null>(null);

  const run = async (name: string, fn: () => Promise<unknown>) => {
    setBusy(name);
    try {
      setResult(await fn());
    } catch (e) {
      setResult({ error: e instanceof Error ? e.message : String(e) });
    } finally {
      setBusy(null);
    }
  };

  return (
    <Panel title={t("dash.tools")}>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 16 }}>
        <div className="field" style={{ margin: 0, flex: "1 1 140px" }}>
          <label htmlFor="sym">{t("dash.symbol")}</label>
          <input
            id="sym"
            className="input"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          />
        </div>
        <div className="field" style={{ margin: 0, flex: "1 1 120px" }}>
          <label htmlFor="tf">{t("dash.timeframe")}</label>
          <select
            id="tf"
            className="select"
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
          >
            {["M1", "M5", "M15", "H1", "H4", "D1"].map((tf) => (
              <option key={tf} value={tf}>
                {tf}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 16 }}>
        <button
          className="btn btn--ghost btn--sm"
          disabled={busy !== null}
          onClick={() => void run("signal", () => market.signal({ symbol, timeframe }))}
        >
          {busy === "signal" ? <span className="spinner" /> : t("dash.runSignal")}
        </button>
        <button
          className="btn btn--ghost btn--sm"
          disabled={busy !== null}
          onClick={() => void run("market", () => market.run())}
        >
          {busy === "market" ? <span className="spinner" /> : t("dash.runMarket")}
        </button>
        <button
          className="btn btn--ghost btn--sm"
          disabled={busy !== null}
          onClick={() => void run("backtest", () => backtest.run({ symbol, timeframe }))}
        >
          {busy === "backtest" ? <span className="spinner" /> : t("dash.runBacktest")}
        </button>
        <button
          className="btn btn--ghost btn--sm"
          disabled={busy !== null}
          onClick={() => void run("perf", () => ai.performanceFor(symbol, timeframe))}
        >
          {busy === "perf" ? <span className="spinner" /> : t("dash.performance")}
        </button>
      </div>

      <JsonBlock value={result} />
    </Panel>
  );
}

/* -------------------------------------------------------------------- page */

export function DashboardPage() {
  const { t, user } = useApp();

  if (!user) {
    return (
      <div className="container auth-wrap">
        <div className="card form-card" style={{ textAlign: "center" }}>
          <h1 className="h3">{t("dash.loginRequired")}</h1>
          <Link to="/login" className="btn btn--primary btn--block" style={{ marginTop: 20 }}>
            {t("nav.login")}
          </Link>
        </div>
      </div>
    );
  }

  return (
    <section className="section section--tight">
      <div className="container">
        <div className="section-head" style={{ marginBottom: 32 }}>
          <span className="eyebrow">{user.username}</span>
          <h1 className="h2">{t("dash.title")}</h1>
          <p className="lead">{t("dash.sub")}</p>
        </div>

        <LiveHud />

        <div className="dash-grid" style={{ marginTop: 24 }}>
          <SystemPanel />
          <GuardianPanel />
          <PositionsPanel />
          <SessionsPanel />
          <ToolsPanel />
          <AiPanel />
          <HistoryPanel />
          <JournalPanel />
        </div>
      </div>
    </section>
  );
}
