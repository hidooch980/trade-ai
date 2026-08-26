import { useCallback, useEffect, useState, type FormEvent } from "react";
import { intelligence as intelligenceApi } from "../api/client";
import type {
  IntelligenceMeta,
  MarketView,
  SignalKind,
  SourceWeight,
} from "../api/types";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { IconArrow, IconLock, IconPulse, IconTarget } from "../components/Icons";
import { Panel } from "../components/Panel";

const KINDS: SignalKind[] = [
  "TECHNICAL",
  "FLOW",
  "LIQUIDITY",
  "MACRO",
  "SENTIMENT",
  "NEWS",
];

const SYMBOLS = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD", "US500"];

type Draft = Record<SignalKind, { value: number; confidence: number; on: boolean }>;

const START: Draft = {
  TECHNICAL: { value: 72, confidence: 80, on: true },
  FLOW: { value: 66, confidence: 70, on: true },
  LIQUIDITY: { value: 55, confidence: 60, on: false },
  MACRO: { value: 58, confidence: 55, on: true },
  SENTIMENT: { value: 62, confidence: 45, on: false },
  NEWS: { value: 50, confidence: 40, on: false },
};

function num(v: string | number): number {
  const n = Number(v);
  return Number.isFinite(n) ? n : 0;
}

function round(v: string | number, digits = 1): string {
  return String(Number(num(v).toFixed(digits)));
}

function message(e: unknown): string {
  return e instanceof Error ? e.message : String(e);
}

/** Bullish, bearish or neither — the tone every mark on the page keys off. */
function tone(bias: string): "up" | "down" | "flat" {
  if (bias.includes("BULLISH")) return "up";
  if (bias.includes("BEARISH")) return "down";
  return "flat";
}

/* ------------------------------------------------------------- score meter */

/**
 * A diverging meter: 50 is the neutral midpoint, bullish runs one way and
 * bearish the other. The needle carries the number and the bias word as well
 * as the hue, so a reader who cannot separate the two poles still gets the
 * answer — the two are only ~9 ΔE apart under deuteranopia.
 */
function ScoreMeter({ view }: { view: MarketView }) {
  const { t, n } = useApp();
  const score = num(view.score);
  const t0 = tone(view.bias);

  return (
    <figure className={`meter meter--${t0}`}>
      <figcaption className="meter__caption">
        <span className="meter__symbol" dir="ltr">
          {view.symbol}
        </span>
        <span className={`tag tag--${t0 === "up" ? "active" : t0 === "down" ? "revoked" : "expired"}`}>
          {t(`intel.bias.${view.bias}`)}
        </span>
      </figcaption>

      <div className="meter__value" dir="ltr">
        {n(round(view.score))}
        <span className="meter__of">/ {n(100)}</span>
      </div>

      <div className="meter__track" role="img" aria-label={`${t("intel.score")} ${round(view.score)}`}>
        <span className="meter__mid" aria-hidden="true" />
        <span className="meter__needle" style={{ insetInlineStart: `${score}%` }} />
      </div>

      <div className="meter__scale" aria-hidden="true">
        <span>{t("intel.bearishEnd")}</span>
        <span>{t("intel.neutralEnd")}</span>
        <span>{t("intel.bullishEnd")}</span>
      </div>
    </figure>
  );
}

/* --------------------------------------------------------- contribution bars */

/**
 * Magnitude across named sources: one measure, one hue, category on the axis
 * label rather than in the colour. Each bar is directly labelled, so no
 * legend is needed and no value is hidden behind a hover.
 */
function Contributions({ sources }: { sources: SourceWeight[] }) {
  const { t, n } = useApp();
  const ranked = [...sources].sort((a, b) => num(b.contribution) - num(a.contribution));
  const top = Math.max(...ranked.map((s) => num(s.contribution)), 1);

  if (ranked.length === 0) return <p className="empty">{t("intel.noSignals")}</p>;

  return (
    <ul className="contrib">
      {ranked.map((s) => {
        const pct = num(s.contribution);
        return (
          <li className="contrib__row" key={s.kind}>
            <span className="contrib__label">
              {t(`intel.kind.${s.kind}`)}
              {s.source && <span className="contrib__source">{s.source}</span>}
            </span>
            <span
              className="contrib__track"
              title={`${t("intel.reads")} ${round(s.value)} · ${t("intel.sureness")} ${round(s.confidence)}%`}
            >
              <span className="contrib__fill" style={{ width: `${(pct / top) * 100}%` }} />
            </span>
            <span className="contrib__value" dir="ltr">
              {n(round(pct))}%
            </span>
          </li>
        );
      })}
    </ul>
  );
}

/* ------------------------------------------------------------------- page */

export function IntelligencePage() {
  const { t, n, user } = useApp();
  const [symbol, setSymbol] = useState(SYMBOLS[0]);
  const [draft, setDraft] = useState<Draft>(START);
  const [blackout, setBlackout] = useState(false);
  const [view, setView] = useState<MarketView | null>(null);
  const [meta, setMeta] = useState<IntelligenceMeta | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    intelligenceApi.meta().then(setMeta).catch(() => undefined);
  }, [user]);

  const run = useCallback(
    async (e?: FormEvent) => {
      e?.preventDefault();
      setBusy(true);
      setError(null);
      try {
        setView(
          await intelligenceApi.view({
            symbol,
            signals: KINDS.filter((k) => draft[k].on).map((k) => ({
              kind: k,
              value: String(draft[k].value),
              confidence: String(draft[k].confidence),
              source: "",
            })),
            blockers: blackout ? ["NEWS_BLACKOUT"] : [],
          }),
        );
      } catch (err: unknown) {
        setError(message(err));
      } finally {
        setBusy(false);
      }
    },
    [symbol, draft, blackout],
  );

  useEffect(() => {
    if (user) void run();
    // Only on first load; after that the button drives it.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  if (!user) {
    return (
      <div className="container section">
        <div className="card form-card" style={{ marginInline: "auto", textAlign: "center" }}>
          <div className="card__icon" style={{ marginInline: "auto" }}>
            <IconLock />
          </div>
          <h1 className="h3">{t("account.signedOutTitle")}</h1>
          <p className="muted" style={{ marginTop: 10 }}>
            {t("intel.signedOutBody")}
          </p>
          <Link to="/login" className="btn btn--primary btn--block" style={{ marginTop: 22 }}>
            {t("nav.login")}
            <IconArrow />
          </Link>
        </div>
      </div>
    );
  }

  const weightOf = (kind: SignalKind) =>
    meta?.kinds.find((k) => k.kind === kind)?.default_weight ?? "";

  return (
    <div className="container section">
      <header className="page-head">
        <div>
          <span className="eyebrow">
            <IconPulse width={14} height={14} /> {t("intel.eyebrow")}
          </span>
          <h1 className="h2">{t("intel.title")}</h1>
          <p className="lead">{t("intel.sub")}</p>
        </div>
      </header>

      <div className="mt5-mode">
        <b>{t("intel.inputsLabel")}</b>
        <span>{t("intel.inputsNote")}</span>
      </div>

      {error && <div className="alert alert--error">{error}</div>}

      <div className="risk-layout">
        <Panel title={t("intel.viewTitle")}>
          {view ? (
            <>
              <ScoreMeter view={view} />

              <dl className="verdict__stats intel-stats">
                <div>
                  <dt>{t("intel.decision")}</dt>
                  <dd>{t(`intel.decision.${view.decision}`)}</dd>
                </div>
                <div>
                  <dt>{t("intel.agreement")}</dt>
                  <dd dir="ltr">{n(round(view.agreement))}%</dd>
                </div>
                <div>
                  <dt>{t("intel.confidence")}</dt>
                  <dd dir="ltr">{n(round(view.confidence))}%</dd>
                </div>
              </dl>

              {view.notes.length > 0 && (
                <ul className="intel-notes">
                  {view.notes.map((note) => (
                    <li key={note}>{t(`intel.note.${note}`)}</li>
                  ))}
                </ul>
              )}

              {view.blockers.length > 0 && (
                <div className="alert alert--error" style={{ marginTop: 14 }}>
                  {t("intel.blockedBy")}:{" "}
                  {view.blockers.map((b) => t(`intel.blocker.${b}`)).join(" · ")}
                </div>
              )}

              <h3 className="intel-subhead">{t("intel.whoDrove")}</h3>
              <Contributions sources={view.sources} />
            </>
          ) : (
            <p className="empty">{t("state.loading")}</p>
          )}
        </Panel>

        <Panel title={t("intel.signalsTitle")}>
          <form onSubmit={run}>
            <div className="field">
              <label htmlFor="intel-symbol">{t("risk.symbol")}</label>
              <select
                id="intel-symbol"
                className="select"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
              >
                {SYMBOLS.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            <div className="signals">
              {KINDS.map((kind) => {
                const row = draft[kind];
                return (
                  <div className={`signal ${row.on ? "" : "is-off"}`} key={kind}>
                    <label className="signal__head">
                      <input
                        type="checkbox"
                        checked={row.on}
                        onChange={(e) =>
                          setDraft((d) => ({ ...d, [kind]: { ...d[kind], on: e.target.checked } }))
                        }
                      />
                      <span className="signal__name">{t(`intel.kind.${kind}`)}</span>
                      <span className="signal__weight" dir="ltr">
                        ×{n(weightOf(kind))}
                      </span>
                    </label>

                    <div className="signal__slider">
                      <span className="signal__legend">{t("intel.reads")}</span>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={row.value}
                        disabled={!row.on}
                        aria-label={`${t(`intel.kind.${kind}`)} ${t("intel.reads")}`}
                        onChange={(e) =>
                          setDraft((d) => ({
                            ...d,
                            [kind]: { ...d[kind], value: Number(e.target.value) },
                          }))
                        }
                      />
                      <output dir="ltr">{n(row.value)}</output>
                    </div>

                    <div className="signal__slider">
                      <span className="signal__legend">{t("intel.sureness")}</span>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={row.confidence}
                        disabled={!row.on}
                        aria-label={`${t(`intel.kind.${kind}`)} ${t("intel.sureness")}`}
                        onChange={(e) =>
                          setDraft((d) => ({
                            ...d,
                            [kind]: { ...d[kind], confidence: Number(e.target.value) },
                          }))
                        }
                      />
                      <output dir="ltr">{n(row.confidence)}%</output>
                    </div>
                  </div>
                );
              })}
            </div>

            <label className="signal__blackout">
              <input
                type="checkbox"
                checked={blackout}
                onChange={(e) => setBlackout(e.target.checked)}
              />
              <span>{t("intel.blackout")}</span>
            </label>
            <p className="tiny">{t("intel.blackoutNote")}</p>

            <button className="btn btn--primary" type="submit" disabled={busy}>
              {busy ? <span className="spinner" /> : <IconTarget width={16} height={16} />}
              {busy ? "" : t("intel.recompute")}
            </button>
          </form>
        </Panel>
      </div>
    </div>
  );
}
