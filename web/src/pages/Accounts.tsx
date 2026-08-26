import { useCallback, useEffect, useState, type FormEvent } from "react";
import { ApiError, accounts as accountsApi } from "../api/client";
import type { AccountKind, TradingAccount, TradingAccountList } from "../api/types";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { IconArrow, IconBolt, IconCheck, IconLock, IconRefresh, IconX } from "../components/Icons";
import { Panel } from "../components/Panel";
import { absoluteTime, relativeTime } from "./Account";

const KINDS: AccountKind[] = ["DEMO", "REAL"];

const EMPTY_FORM = {
  name: "",
  server: "",
  login: "",
  password: "",
  broker: "",
  account_kind: "DEMO" as AccountKind,
};

function money(value: string, currency: string, lang: string): string {
  const amount = Number(value);
  if (Number.isNaN(amount)) return `${value} ${currency}`;
  return amount.toLocaleString(lang, {
    style: "currency",
    currency: /^[A-Z]{3}$/.test(currency) ? currency : "USD",
    maximumFractionDigits: 2,
  });
}

function message(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return error instanceof Error ? error.message : String(error);
}

/* ------------------------------------------------------------- add account */

function AddAccountForm({ onAdded }: { onAdded: () => void }) {
  const { t } = useApp();
  const [form, setForm] = useState(EMPTY_FORM);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const field = (key: keyof typeof EMPTY_FORM) => ({
    value: form[key],
    onChange: (e: { target: { value: string } }) =>
      setForm((f) => ({ ...f, [key]: e.target.value })),
  });

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await accountsApi.register({
        name: form.name.trim(),
        server: form.server.trim(),
        login: form.login.trim(),
        password: form.password,
        account_kind: form.account_kind,
        broker: form.broker.trim() || null,
      });
      onAdded();
      setForm(EMPTY_FORM);
    } catch (err: unknown) {
      setError(message(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="mt5-form" onSubmit={submit}>
      {error && <div className="alert alert--error">{error}</div>}

      <div className="mt5-form__grid">
        <div className="field">
          <label htmlFor="acc-name">{t("mt5.nickname")}</label>
          <input
            id="acc-name"
            className="input"
            required
            maxLength={100}
            placeholder={t("mt5.nicknameHint")}
            {...field("name")}
          />
        </div>

        <div className="field">
          <label htmlFor="acc-broker">{t("mt5.broker")}</label>
          <input
            id="acc-broker"
            className="input"
            maxLength={100}
            placeholder={t("mt5.brokerHint")}
            {...field("broker")}
          />
        </div>

        <div className="field">
          <label htmlFor="acc-server">{t("mt5.server")}</label>
          <input
            id="acc-server"
            className="input"
            required
            maxLength={120}
            dir="ltr"
            placeholder="ICMarketsSC-Demo"
            {...field("server")}
          />
        </div>

        <div className="field">
          <label htmlFor="acc-login">{t("mt5.login")}</label>
          <input
            id="acc-login"
            className="input"
            required
            maxLength={64}
            dir="ltr"
            inputMode="numeric"
            placeholder="51234567"
            {...field("login")}
          />
        </div>

        <div className="field">
          <label htmlFor="acc-password">{t("mt5.password")}</label>
          <input
            id="acc-password"
            className="input"
            type="password"
            required
            autoComplete="new-password"
            {...field("password")}
          />
        </div>

        <div className="field">
          <label htmlFor="acc-kind">{t("mt5.kind")}</label>
          <select
            id="acc-kind"
            className="select"
            value={form.account_kind}
            onChange={(e) =>
              setForm((f) => ({ ...f, account_kind: e.target.value as AccountKind }))
            }
          >
            {KINDS.map((k) => (
              <option key={k} value={k}>
                {t(`mt5.kind.${k}`)}
              </option>
            ))}
          </select>
        </div>
      </div>

      <p className="tiny mt5-form__note">{t("mt5.passwordNote")}</p>

      <button className="btn btn--primary" type="submit" disabled={busy}>
        {busy ? <span className="spinner" /> : t("mt5.add")}
        {!busy && <IconArrow />}
      </button>
    </form>
  );
}

/* ---------------------------------------------------------------- one card */

function AccountCard({
  account,
  onChanged,
  onRemoved,
  onError,
}: {
  account: TradingAccount;
  onChanged: (a: TradingAccount) => void;
  onRemoved: (id: string) => void;
  onError: (msg: string) => void;
}) {
  const { t, n, lang } = useApp();
  const [busy, setBusy] = useState<string | null>(null);
  const [password, setPassword] = useState("");
  const [asking, setAsking] = useState(false);

  const run = async (label: string, fn: () => Promise<TradingAccount>) => {
    setBusy(label);
    try {
      onChanged(await fn());
    } catch (err: unknown) {
      onError(message(err));
    } finally {
      setBusy(null);
    }
  };

  const remove = async () => {
    setBusy("delete");
    try {
      await accountsApi.remove(account.id);
      onRemoved(account.id);
    } catch (err: unknown) {
      onError(message(err));
    } finally {
      setBusy(null);
    }
  };

  const state = account.status.toLowerCase();

  return (
    <article className={`mt5-card mt5-card--${state}`}>
      <header className="mt5-card__head">
        <div>
          <h3 className="mt5-card__name">
            {account.name}
            {account.is_default && (
              <span className="mt5-card__default">{t("mt5.default")}</span>
            )}
          </h3>
          <p className="mt5-card__meta" dir="ltr">
            {account.platform} · {account.server} · {account.login}
          </p>
        </div>
        <span className={`tag tag--${state === "connected" ? "active" : state === "error" ? "revoked" : "expired"}`}>
          {t(`mt5.status.${account.status}`)}
        </span>
      </header>

      <div className="mt5-card__rows">
        <div className="mt5-card__row">
          <span>{t("mt5.kind")}</span>
          <span>{t(`mt5.kind.${account.account_kind}`)}</span>
        </div>
        <div className="mt5-card__row">
          <span>{t("mt5.balance")}</span>
          <span dir="ltr">{n(money(account.balance, account.currency, lang))}</span>
        </div>
        <div className="mt5-card__row">
          <span>{t("mt5.equity")}</span>
          <span dir="ltr">{n(money(account.equity, account.currency, lang))}</span>
        </div>
        <div className="mt5-card__row">
          <span>{t("mt5.lastConnected")}</span>
          <span title={absoluteTime(account.last_connected_at, lang)}>
            {account.last_connected_at
              ? n(relativeTime(account.last_connected_at, lang))
              : "—"}
          </span>
        </div>
        {account.broker && (
          <div className="mt5-card__row">
            <span>{t("mt5.broker")}</span>
            <span>{account.broker}</span>
          </div>
        )}
      </div>

      {!account.has_credentials && (
        <div className="alert alert--error mt5-card__alert">
          <span>{t("mt5.needsPassword")}</span>
          {asking ? (
            <div className="mt5-card__relogin">
              <input
                className="input"
                type="password"
                autoComplete="new-password"
                aria-label={t("mt5.password")}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button
                className="btn btn--primary btn--sm"
                disabled={!password || busy === "password"}
                onClick={() =>
                  void run("password", async () => {
                    const updated = await accountsApi.setPassword(account.id, password);
                    setPassword("");
                    setAsking(false);
                    return updated;
                  })
                }
              >
                {busy === "password" ? <span className="spinner" /> : <IconCheck />}
              </button>
              <button className="btn btn--quiet btn--sm" onClick={() => setAsking(false)}>
                <IconX />
              </button>
            </div>
          ) : (
            <button className="btn btn--ghost btn--sm" onClick={() => setAsking(true)}>
              {t("mt5.resupply")}
            </button>
          )}
        </div>
      )}

      {account.last_error && account.has_credentials && (
        <p className="tiny mt5-card__error">
          {t("mt5.lastError")}: <code dir="ltr">{account.last_error}</code>
        </p>
      )}

      <footer className="mt5-card__actions">
        {account.status === "CONNECTED" ? (
          <button
            className="btn btn--ghost btn--sm"
            disabled={busy !== null}
            onClick={() =>
              void run("disconnect", async () => {
                const r = await accountsApi.disconnect(account.id);
                return r.account;
              })
            }
          >
            {busy === "disconnect" ? <span className="spinner" /> : t("mt5.disconnect")}
          </button>
        ) : (
          <button
            className="btn btn--primary btn--sm"
            disabled={busy !== null || !account.has_credentials}
            onClick={() =>
              void run("connect", async () => {
                const r = await accountsApi.connect(account.id);
                return r.account;
              })
            }
          >
            {busy === "connect" ? <span className="spinner" /> : <IconBolt width={15} height={15} />}
            {busy === "connect" ? "" : t("mt5.connect")}
          </button>
        )}

        {!account.is_default && (
          <button
            className="btn btn--quiet btn--sm"
            disabled={busy !== null}
            onClick={() =>
              void run("default", () =>
                accountsApi.update(account.id, { make_default: true }),
              )
            }
          >
            {t("mt5.makeDefault")}
          </button>
        )}

        <button
          className="btn btn--danger btn--sm mt5-card__remove"
          disabled={busy !== null}
          onClick={() => void remove()}
        >
          {busy === "delete" ? <span className="spinner" /> : t("mt5.remove")}
        </button>
      </footer>
    </article>
  );
}

/* -------------------------------------------------------------------- page */

export function AccountsPage() {
  const { t, n, user } = useApp();
  const [data, setData] = useState<TradingAccountList | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    if (!user) return;
    setBusy(true);
    setError(null);
    accountsApi
      .list()
      .then(setData)
      .catch((e: unknown) => setError(message(e)))
      .finally(() => setBusy(false));
  }, [user]);

  useEffect(() => {
    load();
  }, [load]);

  if (!user) {
    return (
      <div className="container section">
        <div className="card form-card" style={{ marginInline: "auto", textAlign: "center" }}>
          <div className="card__icon" style={{ marginInline: "auto" }}>
            <IconLock />
          </div>
          <h1 className="h3">{t("account.signedOutTitle")}</h1>
          <p className="muted" style={{ marginTop: 10 }}>
            {t("mt5.signedOutBody")}
          </p>
          <Link to="/login" className="btn btn--primary btn--block" style={{ marginTop: 22 }}>
            {t("nav.login")}
            <IconArrow />
          </Link>
        </div>
      </div>
    );
  }

  const items = data?.items ?? [];

  const replace = (updated: TradingAccount) =>
    setData((current) =>
      current
        ? {
            ...current,
            // A new default clears the flag on every other row server-side,
            // so re-read rather than patching one item in place.
            items: updated.is_default
              ? current.items.map((a) =>
                  a.id === updated.id ? updated : { ...a, is_default: false },
                )
              : current.items.map((a) => (a.id === updated.id ? updated : a)),
          }
        : current,
    );

  return (
    <div className="container section">
      <header className="page-head">
        <div>
          <span className="eyebrow">{t("mt5.eyebrow")}</span>
          <h1 className="h2">{t("mt5.title")}</h1>
          <p className="lead">{t("mt5.sub")}</p>
        </div>
        <button
          className="btn btn--ghost btn--sm"
          onClick={load}
          disabled={busy}
          aria-label={t("dash.refresh")}
        >
          {busy ? <span className="spinner" /> : <IconRefresh />}
        </button>
      </header>

      {data && (
        <div className="mt5-mode">
          <b>{t("mt5.modeLabel")}: {data.mode}</b>
          <span>{t("mt5.modeNote")}</span>
        </div>
      )}

      {error && <div className="alert alert--error">{error}</div>}

      <div className="mt5-layout">
        <Panel title={t("mt5.addTitle")}>
          {/* Re-read rather than splicing: the server orders default-first,
              then newest, and a local insert would not match. */}
          <AddAccountForm onAdded={load} />
        </Panel>

        <Panel
          title={t("mt5.yourAccounts")}
          action={<span className="tiny">{n(items.length)}</span>}
        >
          {items.length === 0 ? (
            <p className="empty">{t("mt5.none")}</p>
          ) : (
            <div className="mt5-list">
              {items.map((a) => (
                <AccountCard
                  key={a.id}
                  account={a}
                  onChanged={replace}
                  onRemoved={(id) =>
                    setData((current) =>
                      current
                        ? {
                            ...current,
                            total: current.total - 1,
                            items: current.items.filter((x) => x.id !== id),
                          }
                        : current,
                    )
                  }
                  onError={setError}
                />
              ))}
            </div>
          )}
        </Panel>
      </div>
    </div>
  );
}
