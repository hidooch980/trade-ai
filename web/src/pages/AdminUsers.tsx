import { useCallback, useEffect, useState } from "react";
import { admin } from "../api/client";
import type { AdminUser, AdminUserList, SessionResponse } from "../api/types";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { IconArrow, IconClose, IconLock, IconRefresh } from "../components/Icons";
import { Panel } from "../components/Panel";
import { SessionsTable, absoluteTime, relativeTime } from "./Account";

const ROLES = ["ADMIN", "TRADER", "VIEWER", "CUSTOMER"] as const;
const PAGE_SIZE = 20;

type LockedFilter = "all" | "locked" | "active";

export function AdminUsersPage() {
  const { t, n, lang, user } = useApp();

  const [search, setSearch] = useState("");
  const [debounced, setDebounced] = useState("");
  const [role, setRole] = useState("");
  const [locked, setLocked] = useState<LockedFilter>("all");
  const [offset, setOffset] = useState(0);

  const [page, setPage] = useState<AdminUserList | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [sessions, setSessions] = useState<SessionResponse[]>([]);

  // Typing a name should not fire a request per keystroke.
  useEffect(() => {
    const id = setTimeout(() => {
      setDebounced(search);
      setOffset(0);
    }, 300);
    return () => clearTimeout(id);
  }, [search]);

  const load = useCallback(() => {
    setBusy(true);
    setError(null);
    admin
      .users({
        search: debounced || undefined,
        role: role || undefined,
        locked: locked === "all" ? undefined : locked === "locked",
        limit: PAGE_SIZE,
        offset,
      })
      .then(setPage)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : String(e)))
      .finally(() => setBusy(false));
  }, [debounced, role, locked, offset]);

  useEffect(() => {
    load();
  }, [load]);

  const isAdmin = user?.role === "ADMIN";

  if (!user || !isAdmin) {
    return (
      <div className="container section">
        <div className="card form-card" style={{ marginInline: "auto", textAlign: "center" }}>
          <div className="card__icon" style={{ marginInline: "auto" }}>
            <IconLock />
          </div>
          <h1 className="h3">{t(user ? "admin.forbidden" : "account.signedOutTitle")}</h1>
          <p className="muted" style={{ marginTop: 10 }}>
            {t(user ? "admin.forbiddenBody" : "account.signedOutBody")}
          </p>
          <Link
            to={user ? "/dashboard" : "/login"}
            className="btn btn--primary btn--block"
            style={{ marginTop: 22 }}
          >
            {t(user ? "nav.dashboard" : "nav.login")}
            <IconArrow />
          </Link>
        </div>
      </div>
    );
  }

  /** Runs one moderation call and splices the fresh row back into the page. */
  const act = async (id: string, fn: () => Promise<AdminUser>) => {
    setPending(id);
    setError(null);
    try {
      const updated = await fn();
      setPage((current) =>
        current
          ? {
              ...current,
              items: current.items.map((u) => (u.id === updated.id ? updated : u)),
            }
          : current,
      );
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setPending(null);
    }
  };

  const toggleSessions = async (id: string) => {
    if (expanded === id) {
      setExpanded(null);
      return;
    }
    setExpanded(id);
    setSessions([]);
    try {
      setSessions(await admin.userSessions(id));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    }
  };

  const total = page?.total ?? 0;
  const items = page?.items ?? [];
  const from = total === 0 ? 0 : offset + 1;
  const to = Math.min(offset + PAGE_SIZE, total);

  return (
    <div className="container section">
      <header className="page-head">
        <div>
          <span className="eyebrow">{t("admin.eyebrow")}</span>
          <h1 className="h2">{t("admin.title")}</h1>
          <p className="lead">{t("admin.sub")}</p>
        </div>
      </header>

      <div className="admin-filters">
        <input
          className="input"
          type="search"
          value={search}
          placeholder={t("admin.searchPlaceholder")}
          aria-label={t("admin.search")}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          className="select"
          value={role}
          aria-label={t("account.role")}
          onChange={(e) => {
            setRole(e.target.value);
            setOffset(0);
          }}
        >
          <option value="">{t("admin.allRoles")}</option>
          {ROLES.map((r) => (
            <option key={r} value={r}>
              {t(`role.${r}`)}
            </option>
          ))}
        </select>

        <select
          className="select"
          value={locked}
          aria-label={t("account.state")}
          onChange={(e) => {
            setLocked(e.target.value as LockedFilter);
            setOffset(0);
          }}
        >
          <option value="all">{t("admin.allStates")}</option>
          <option value="active">{t("account.state.active")}</option>
          <option value="locked">{t("admin.locked")}</option>
        </select>

        <button
          className="btn btn--ghost btn--sm"
          onClick={load}
          disabled={busy}
          aria-label={t("dash.refresh")}
        >
          {busy ? <span className="spinner" /> : <IconRefresh />}
        </button>
      </div>

      {error && <div className="alert alert--error">{error}</div>}

      <Panel
        title={t("admin.users")}
        action={
          <span className="tiny">
            {t("admin.showing", { from: n(from), to: n(to), total: n(total) })}
          </span>
        }
      >
        {items.length === 0 && !busy ? (
          <p className="empty">{t("admin.noResults")}</p>
        ) : (
          <table className="data data--wide">
            <thead>
              <tr>
                <th scope="col">{t("admin.user")}</th>
                <th scope="col">{t("account.role")}</th>
                <th scope="col">{t("account.state")}</th>
                <th scope="col">{t("admin.failed")}</th>
                <th scope="col">{t("account.activeSessions")}</th>
                <th scope="col">{t("admin.joined")}</th>
                <th scope="col">{t("admin.actions")}</th>
              </tr>
            </thead>
            <tbody>
              {items.map((u) => {
                const self = u.id === user.id;
                const working = pending === u.id;
                return (
                  <tr key={u.id} className={expanded === u.id ? "is-open" : ""}>
                    <td>
                      <span className="admin-user">
                        <b>{u.username}</b>
                        <span className="admin-user__mail" dir="ltr">
                          {u.email}
                        </span>
                      </span>
                    </td>

                    <td>
                      <select
                        className="select select--sm"
                        value={u.role}
                        disabled={self || working}
                        title={self ? t("admin.selfRole") : undefined}
                        aria-label={t("account.role")}
                        onChange={(e) =>
                          void act(u.id, () => admin.setRole(u.id, e.target.value))
                        }
                      >
                        {ROLES.map((r) => (
                          <option key={r} value={r}>
                            {t(`role.${r}`)}
                          </option>
                        ))}
                      </select>
                    </td>

                    <td>
                      <span className={`tag tag--${u.is_locked ? "revoked" : "active"}`}>
                        {u.is_locked ? t("admin.locked") : t("account.state.active")}
                      </span>
                      {u.is_locked && u.locked_until && (
                        <span
                          className="tiny"
                          style={{ display: "block", marginTop: 4 }}
                          title={absoluteTime(u.locked_until, lang)}
                        >
                          {n(relativeTime(u.locked_until, lang))}
                        </span>
                      )}
                    </td>

                    <td>{n(u.failed_login_attempts)}</td>

                    <td>
                      <button
                        className="linkish"
                        onClick={() => void toggleSessions(u.id)}
                        aria-expanded={expanded === u.id}
                      >
                        {n(u.active_sessions)}
                      </button>
                    </td>

                    <td title={absoluteTime(u.created_at, lang)}>
                      {n(relativeTime(u.created_at, lang))}
                    </td>

                    <td>
                      <div className="admin-actions">
                        {u.is_locked ? (
                          <button
                            className="btn btn--ghost btn--sm"
                            disabled={working}
                            onClick={() => void act(u.id, () => admin.unlock(u.id))}
                          >
                            {t("admin.unlock")}
                          </button>
                        ) : (
                          <button
                            className="btn btn--danger btn--sm"
                            disabled={self || working}
                            title={self ? t("admin.selfLock") : undefined}
                            onClick={() => void act(u.id, () => admin.lock(u.id))}
                          >
                            {t("admin.lock")}
                          </button>
                        )}
                        <button
                          className="btn btn--quiet btn--sm"
                          disabled={working || u.active_sessions === 0}
                          onClick={() => void act(u.id, () => admin.revokeSessions(u.id))}
                        >
                          {t("admin.revoke")}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}

        {expanded && (
          <div className="admin-sessions">
            <header className="admin-sessions__head">
              <h3 className="panel__title">{t("admin.sessionsOf")}</h3>
              <button
                className="btn btn--quiet btn--sm"
                onClick={() => setExpanded(null)}
                aria-label={t("dash.close")}
              >
                <IconClose width={14} height={14} />
              </button>
            </header>
            <SessionsTable rows={sessions} />
          </div>
        )}

        <div className="pager">
          <button
            className="btn btn--ghost btn--sm"
            disabled={offset === 0 || busy}
            onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}
          >
            {t("admin.prev")}
          </button>
          <span className="tiny">
            {t("admin.showing", { from: n(from), to: n(to), total: n(total) })}
          </span>
          <button
            className="btn btn--ghost btn--sm"
            disabled={to >= total || busy}
            onClick={() => setOffset(offset + PAGE_SIZE)}
          >
            {t("admin.next")}
          </button>
        </div>
      </Panel>
    </div>
  );
}
