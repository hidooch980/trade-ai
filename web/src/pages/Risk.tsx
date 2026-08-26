import { useCallback, useEffect, useState, type FormEvent } from "react";
import { accounts as accountsApi, risk as riskApi } from "../api/client";
import type {
  RiskAssessment,
  RiskPolicy,
  RiskRule,
  TradingAccount,
} from "../api/types";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { IconArrow, IconLock, IconRefresh, IconShield, IconTarget } from "../components/Icons";
import { Panel } from "../components/Panel";

const POLICY_FIELDS = [
  { key: "max_daily_loss_percent", unit: "%", step: "0.1" },
  { key: "max_total_loss_percent", unit: "%", step: "0.1" },
  { key: "max_risk_per_trade_percent", unit: "%", step: "0.05" },
  { key: "max_open_positions", unit: "", step: "1" },
  { key: "max_total_exposure_ratio", unit: "×", step: "0.5" },
  { key: "max_symbol_exposure_percent", unit: "%", step: "1" },
  { key: "max_correlated_positions", unit: "", step: "1" },
  { key: "warn_at_percent", unit: "%", step: "1" },
] as const;

function num(value: string | number | null | undefined): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function trim(value: string, digits = 2): string {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return value;
  return String(Number(parsed.toFixed(digits)));
}

function message(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

/* ------------------------------------------------------------- headroom bar */

function RuleBar({ rule }: { rule: RiskRule }) {
  const { t, n } = useApp();
  const used = Math.min(100, Math.max(0, num(rule.utilisation_percent)));
  const tone = rule.status === "BREACH" ? "breach" : rule.status === "WARN" ? "warn" : "ok";

  return (
    <div className={`gauge gauge--${tone}`}>
      <div className="gauge__head">
        <span className="gauge__name">{t(`risk.rule.${rule.rule}`)}</span>
        <span className="gauge__value" dir="ltr">
          {n(trim(rule.used))}
          {rule.unit === "percent" ? "%" : rule.unit === "ratio" ? "×" : ""} /{" "}
          {n(trim(rule.limit))}
          {rule.unit === "percent" ? "%" : rule.unit === "ratio" ? "×" : ""}
        </span>
      </div>
      <div className="gauge__track">
        <span className="gauge__fill" style={{ width: `${used}%` }} />
      </div>
      <div className="gauge__foot">
        <span className={`tag tag--${tone === "ok" ? "active" : tone === "warn" ? "expired" : "revoked"}`}>
          {t(`risk.status.${rule.status}`)}
        </span>
        <span className="tiny">
          {t("risk.headroom")}: <b dir="ltr">{n(trim(rule.headroom))}</b>
          {rule.detail && rule.detail !== "NOT_APPLICABLE" ? ` · ${rule.detail}` : ""}
        </span>
      </div>
    </div>
  );
}

/* --------------------------------------------------------------- what-if */

const EMPTY_TRADE = {
  symbol: "EURUSD",
  side: "BUY",
  volume: "0.10",
  entry_price: "1.1000",
  stop_loss: "1.0950",
};

function WhatIf({
  accountId,
  onResult,
}: {
  accountId: string;
  onResult: (a: RiskAssessment) => void;
}) {
  const { t } = useApp();
  const [trade, setTrade] = useState(EMPTY_TRADE);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      onResult(
        await riskApi.assess(accountId, {
          trade: {
            symbol: trade.symbol.trim().toUpperCase(),
            side: trade.side,
            volume: trade.volume,
            entry_price: trade.entry_price,
            stop_loss: trade.stop_loss || null,
          },
        }),
      );
    } catch (err: unknown) {
      setError(message(err));
    } finally {
      setBusy(false);
    }
  };

  const field = (key: keyof typeof EMPTY_TRADE) => ({
    value: trade[key],
    onChange: (e: { target: { value: string } }) =>
      setTrade((current) => ({ ...current, [key]: e.target.value })),
  });

  return (
    <form className="whatif" onSubmit={submit}>
      {error && <div className="alert alert--error">{error}</div>}

      <div className="whatif__grid">
        <div className="field">
          <label htmlFor="wi-symbol">{t("risk.symbol")}</label>
          <input id="wi-symbol" className="input" dir="ltr" required {...field("symbol")} />
        </div>
        <div className="field">
          <label htmlFor="wi-side">{t("risk.side")}</label>
          <select
            id="wi-side"
            className="select"
            value={trade.side}
            onChange={(e) => setTrade((c) => ({ ...c, side: e.target.value }))}
          >
            <option value="BUY">{t("risk.buy")}</option>
            <option value="SELL">{t("risk.sell")}</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="wi-volume">{t("risk.volume")}</label>
          <input
            id="wi-volume"
            className="input"
            dir="ltr"
            type="number"
            step="0.01"
            min="0.01"
            required
            {...field("volume")}
          />
        </div>
        <div className="field">
          <label htmlFor="wi-entry">{t("risk.entry")}</label>
          <input
            id="wi-entry"
            className="input"
            dir="ltr"
            type="number"
            step="any"
            required
            {...field("entry_price")}
          />
        </div>
        <div className="field">
          <label htmlFor="wi-sl">{t("risk.stop")}</label>
          <input
            id="wi-sl"
            className="input"
            dir="ltr"
            type="number"
            step="any"
            {...field("stop_loss")}
          />
        </div>
      </div>

      <p className="tiny">{t("risk.stopNote")}</p>

      <button className="btn btn--primary" type="submit" disabled={busy}>
        {busy ? <span className="spinner" /> : <IconTarget width={16} height={16} />}
        {busy ? "" : t("risk.check")}
      </button>
    </form>
  );
}

/* ---------------------------------------------------------------- policy */

function PolicyForm({
  policy,
  onSaved,
}: {
  policy: RiskPolicy;
  onSaved: (p: RiskPolicy) => void;
}) {
  const { t } = useApp();
  const [draft, setDraft] = useState<Record<string, string>>(() =>
    Object.fromEntries(
      POLICY_FIELDS.map((f) => [f.key, String(policy[f.key as keyof RiskPolicy] ?? "")]),
    ),
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    setSaved(false);
    try {
      onSaved(await riskApi.savePolicy(policy.account_id, draft));
      setSaved(true);
    } catch (err: unknown) {
      setError(message(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="policy" onSubmit={submit}>
      {error && <div className="alert alert--error">{error}</div>}
      {saved && <div className="alert alert--ok">{t("risk.saved")}</div>}

      <div className="policy__grid">
        {POLICY_FIELDS.map((f) => (
          <div className="field" key={f.key}>
            <label htmlFor={`p-${f.key}`}>
              {t(`risk.policy.${f.key}`)}
              {f.unit && <span className="policy__unit"> ({f.unit})</span>}
            </label>
            <input
              id={`p-${f.key}`}
              className="input"
              dir="ltr"
              type="number"
              step={f.step}
              min="0"
              value={draft[f.key]}
              onChange={(e) =>
                setDraft((current) => ({ ...current, [f.key]: e.target.value }))
              }
            />
          </div>
        ))}
      </div>

      <button className="btn btn--primary" type="submit" disabled={busy}>
        {busy ? <span className="spinner" /> : t("risk.save")}
      </button>
    </form>
  );
}

/* -------------------------------------------------------------------- page */

export function RiskPage() {
  const { t, n, user } = useApp();
  const [list, setList] = useState<TradingAccount[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [policy, setPolicy] = useState<RiskPolicy | null>(null);
  const [assessment, setAssessment] = useState<RiskAssessment | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    accountsApi
      .list()
      .then((data) => {
        setList(data.items);
        const preferred = data.items.find((a) => a.is_default) ?? data.items[0];
        if (preferred) setSelected(preferred.id);
      })
      .catch((e: unknown) => setError(message(e)));
  }, [user]);

  const load = useCallback(() => {
    if (!selected) return;
    setBusy(true);
    setError(null);
    Promise.all([riskApi.state(selected), riskApi.policy(selected)])
      .then(([state, stored]) => {
        setAssessment(state);
        setPolicy(stored);
      })
      .catch((e: unknown) => setError(message(e)))
      .finally(() => setBusy(false));
  }, [selected]);

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
            {t("risk.signedOutBody")}
          </p>
          <Link to="/login" className="btn btn--primary btn--block" style={{ marginTop: 22 }}>
            {t("nav.login")}
            <IconArrow />
          </Link>
        </div>
      </div>
    );
  }

  if (list.length === 0) {
    return (
      <div className="container section">
        <div className="card form-card" style={{ marginInline: "auto", textAlign: "center" }}>
          <div className="card__icon" style={{ marginInline: "auto" }}>
            <IconShield />
          </div>
          <h1 className="h3">{t("risk.noAccounts")}</h1>
          <p className="muted" style={{ marginTop: 10 }}>
            {t("risk.noAccountsBody")}
          </p>
          <Link to="/accounts" className="btn btn--primary btn--block" style={{ marginTop: 22 }}>
            {t("mt5.addTitle")}
            <IconArrow />
          </Link>
        </div>
      </div>
    );
  }

  const decision = assessment?.decision ?? "ALLOW";

  return (
    <div className="container section">
      <header className="page-head">
        <div>
          <span className="eyebrow">
            <IconShield width={14} height={14} /> {t("risk.eyebrow")}
          </span>
          <h1 className="h2">{t("risk.title")}</h1>
          <p className="lead">{t("risk.sub")}</p>
        </div>
        <div className="risk-head-actions">
          <select
            className="select"
            value={selected}
            aria-label={t("risk.account")}
            onChange={(e) => setSelected(e.target.value)}
          >
            {list.map((a) => (
              <option key={a.id} value={a.id}>
                {a.name} · {a.login}
              </option>
            ))}
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
      </header>

      {error && <div className="alert alert--error">{error}</div>}

      {assessment && (
        <div className={`verdict verdict--${decision.toLowerCase()}`}>
          <div className="verdict__badge">{t(`risk.decision.${decision}`)}</div>
          <div className="verdict__body">
            <p className="verdict__text">{t(`risk.decisionBody.${decision}`)}</p>
            {assessment.reasons.length > 0 && (
              <p className="tiny">
                {t("risk.reasons")}:{" "}
                {assessment.reasons.map((r) => t(`risk.rule.${r}`)).join(" · ")}
              </p>
            )}
          </div>
          <dl className="verdict__stats">
            <div>
              <dt>{t("mt5.equity")}</dt>
              <dd dir="ltr">{n(trim(assessment.equity))}</dd>
            </div>
            <div>
              <dt>{t("risk.dayStart")}</dt>
              <dd dir="ltr">{n(trim(assessment.day_start_equity))}</dd>
            </div>
            <div>
              <dt>{t("risk.peak")}</dt>
              <dd dir="ltr">{n(trim(assessment.peak_equity))}</dd>
            </div>
            <div>
              <dt>{t("risk.exposure")}</dt>
              <dd dir="ltr">{n(trim(assessment.exposure))}</dd>
            </div>
          </dl>
        </div>
      )}

      <div className="risk-layout">
        <Panel
          title={t("risk.headroomTitle")}
          action={
            <button
              className="btn btn--quiet btn--sm"
              disabled={!selected || busy}
              onClick={() => {
                void riskApi.resetDay(selected).then((p) => {
                  setPolicy(p);
                  load();
                });
              }}
            >
              {t("risk.resetDay")}
            </button>
          }
        >
          {assessment ? (
            <div className="gauges">
              {assessment.rules.map((r) => (
                <RuleBar rule={r} key={r.rule} />
              ))}
            </div>
          ) : (
            <p className="empty">{t("state.loading")}</p>
          )}
        </Panel>

        <div className="risk-side">
          <Panel title={t("risk.whatIf")}>
            {selected && <WhatIf accountId={selected} onResult={setAssessment} />}
          </Panel>

          <Panel title={t("risk.limits")}>
            {policy ? (
              <PolicyForm
                policy={policy}
                onSaved={(saved) => {
                  setPolicy(saved);
                  load();
                }}
              />
            ) : (
              <p className="empty">{t("state.loading")}</p>
            )}
          </Panel>
        </div>
      </div>
    </div>
  );
}
