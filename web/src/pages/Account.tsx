import { useCallback, useState } from "react";
import { auth } from "../api/client";
import type { SessionResponse, UserResponse } from "../api/types";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { IconArrow, IconLock } from "../components/Icons";
import { Panel, useEndpoint } from "../components/Panel";

/** "3 hours ago" / "in 12 days", in whichever language is active. */
export function relativeTime(iso: string | null, lang: string): string {
  if (!iso) return "—";

  const delta = new Date(iso).getTime() - Date.now();
  if (Number.isNaN(delta)) return "—";

  const units: [Intl.RelativeTimeFormatUnit, number][] = [
    ["year", 365 * 24 * 3600e3],
    ["month", 30 * 24 * 3600e3],
    ["day", 24 * 3600e3],
    ["hour", 3600e3],
    ["minute", 60e3],
  ];

  const rtf = new Intl.RelativeTimeFormat(lang, { numeric: "auto" });

  for (const [unit, ms] of units) {
    if (Math.abs(delta) >= ms) return rtf.format(Math.round(delta / ms), unit);
  }
  return rtf.format(Math.round(delta / 1000), "second");
}

export function absoluteTime(iso: string | null, lang: string): string {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleString(lang, { dateStyle: "medium", timeStyle: "short" });
}

/** Chrome 121 on Windows → "Chrome · Windows"; anything unparsed stays raw. */
export function describeAgent(agent: string | null): string {
  if (!agent) return "—";

  const browser =
    /Edg\//.test(agent) ? "Edge"
    : /OPR\//.test(agent) ? "Opera"
    : /Chrome\//.test(agent) ? "Chrome"
    : /Safari\//.test(agent) && !/Chrome/.test(agent) ? "Safari"
    : /Firefox\//.test(agent) ? "Firefox"
    : null;

  const os =
    /Windows/.test(agent) ? "Windows"
    : /Android/.test(agent) ? "Android"
    : /(iPhone|iPad|iOS)/.test(agent) ? "iOS"
    : /Mac OS X/.test(agent) ? "macOS"
    : /Linux/.test(agent) ? "Linux"
    : null;

  if (!browser && !os) return agent.slice(0, 40);
  return [browser, os].filter(Boolean).join(" · ");
}

export type SessionState = "active" | "revoked" | "expired";

export function sessionState(session: SessionResponse): SessionState {
  if (session.revoked_at) return "revoked";
  if (new Date(session.expires_at).getTime() <= Date.now()) return "expired";
  return "active";
}

export function SessionsTable({ rows }: { rows: SessionResponse[] }) {
  const { t, n, lang } = useApp();

  if (rows.length === 0) return <p className="empty">{t("account.noSessions")}</p>;

  return (
    <table className="data">
      <thead>
        <tr>
          <th scope="col">{t("account.device")}</th>
          <th scope="col">{t("account.browser")}</th>
          <th scope="col">{t("account.ip")}</th>
          <th scope="col">{t("account.lastUsed")}</th>
          <th scope="col">{t("account.expires")}</th>
          <th scope="col">{t("account.state")}</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((s) => {
          const state = sessionState(s);
          return (
            <tr key={s.id}>
              <td>{s.device_name || t("account.unnamedDevice")}</td>
              <td>{describeAgent(s.user_agent)}</td>
              <td dir="ltr">{s.ip_address || "—"}</td>
              <td title={absoluteTime(s.last_used_at ?? s.created_at, lang)}>
                {n(relativeTime(s.last_used_at ?? s.created_at, lang))}
              </td>
              <td title={absoluteTime(s.expires_at, lang)}>
                {n(relativeTime(s.expires_at, lang))}
              </td>
              <td>
                <span className={`tag tag--${state}`}>{t(`account.state.${state}`)}</span>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

/* ------------------------------------------------------------------ page */

function ProfileRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="kv__row">
      <span className="kv__k">{label}</span>
      <span className="kv__v">{value}</span>
    </div>
  );
}

export function AccountPage() {
  const { t, n, user, setUser, logout } = useApp();
  const [signingOut, setSigningOut] = useState(false);

  const me = useEndpoint<UserResponse>(
    useCallback(() => auth.me(), []),
    Boolean(user),
  );

  const sessions = useEndpoint<SessionResponse[]>(
    useCallback(() => auth.sessions(), []),
    Boolean(user),
  );

  if (!user) {
    return (
      <div className="container section">
        <div className="card form-card" style={{ marginInline: "auto", textAlign: "center" }}>
          <div className="card__icon" style={{ marginInline: "auto" }}>
            <IconLock />
          </div>
          <h1 className="h3">{t("account.signedOutTitle")}</h1>
          <p className="muted" style={{ marginTop: 10 }}>
            {t("account.signedOutBody")}
          </p>
          <Link to="/login" className="btn btn--primary btn--block" style={{ marginTop: 22 }}>
            {t("nav.login")}
            <IconArrow />
          </Link>
        </div>
      </div>
    );
  }

  const profile = me.data ?? user;
  const rows = sessions.data ?? [];
  const live = rows.filter((s) => sessionState(s) === "active").length;

  const signOutEverywhere = async () => {
    setSigningOut(true);
    try {
      await auth.logoutAll();
      // logout-all kills this device's session too, so follow it locally.
      await logout();
      setUser(null);
    } finally {
      setSigningOut(false);
    }
  };

  return (
    <div className="container section">
      <header className="page-head">
        <div>
          <span className="eyebrow">{t("account.eyebrow")}</span>
          <h1 className="h2">{t("account.title")}</h1>
          <p className="lead">{t("account.sub")}</p>
        </div>
        <span className="avatar avatar--lg" aria-hidden="true">
          {profile.username.slice(0, 1).toUpperCase()}
        </span>
      </header>

      <div className="dash-grid" style={{ marginTop: 32 }}>
        <Panel title={t("account.profile")} onRefresh={me.reload} busy={me.busy}>
          {me.error && <p className="empty">{me.error}</p>}
          <div className="kv">
            <ProfileRow label={t("auth.username")} value={profile.username} />
            <ProfileRow label={t("auth.email")} value={profile.email} />
            <ProfileRow label={t("account.role")} value={t(`role.${profile.role}`)} />
            <ProfileRow label={t("account.language")} value={profile.language.toUpperCase()} />
            <ProfileRow label={t("account.activeSessions")} value={n(live)} />
          </div>
        </Panel>

        <Panel
          title={t("account.security")}
          action={
            <button
              className="btn btn--danger btn--sm"
              onClick={() => void signOutEverywhere()}
              disabled={signingOut || live === 0}
            >
              {signingOut ? <span className="spinner" /> : t("account.signOutAll")}
            </button>
          }
        >
          <p className="muted" style={{ fontSize: 14 }}>
            {t("account.securityBody")}
          </p>
          <ul className="rule-list" style={{ marginTop: 14 }}>
            <li>{t("account.tip1")}</li>
            <li>{t("account.tip2")}</li>
            <li>{t("account.tip3")}</li>
          </ul>
        </Panel>
      </div>

      <div style={{ marginTop: 20 }}>
        <Panel
          title={t("account.sessions")}
          onRefresh={sessions.reload}
          busy={sessions.busy}
        >
          {sessions.error && <p className="empty">{sessions.error}</p>}
          <SessionsTable rows={rows} />
        </Panel>
      </div>
    </div>
  );
}
