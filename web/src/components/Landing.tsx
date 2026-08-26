import { useEffect, useRef, useState } from "react";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import {
  FIRST_PAYOUT_DAYS,
  HEADLINE_STATS,
  PAYOUT_WALL,
  TRUST,
  COMPARE_ROWS,
} from "../data/landing";
import { MODEL_IDS, money, pct, planFor, FEATURED_SIZE, type ModelId } from "../data/plans";
import {
  IconArrow,
  IconBolt,
  IconCard,
  IconChat,
  IconCheck,
  IconClock,
  IconEye,
  IconGlobe,
  IconHeadset,
  IconLock,
  IconPulse,
  IconRocket,
  IconSend,
  IconShield,
  IconStar,
  IconTarget,
  IconTerminal,
  IconUsers,
  IconWallet,
  IconX,
} from "./Icons";
import { Reveal } from "./Reveal";
import { SectionHead } from "./Sections";

/* ================================================================ promo bar */

const PROMO_KEY = "tradeai.promo.v1";
const PROMO_CODE = "TRADEAI25";

function msUntilMidnight(): number {
  const now = new Date();
  const end = new Date(now);
  end.setHours(24, 0, 0, 0);
  return end.getTime() - now.getTime();
}

function two(value: number): string {
  return String(Math.max(0, value)).padStart(2, "0");
}

/** Dismissible offer strip above the navbar, with a countdown to midnight. */
export function PromoBar() {
  const { t, n } = useApp();
  const [shown, setShown] = useState(() => localStorage.getItem(PROMO_KEY) !== "off");
  const [left, setLeft] = useState(msUntilMidnight);

  useEffect(() => {
    if (!shown) return;
    const id = setInterval(() => setLeft(msUntilMidnight()), 1000);
    return () => clearInterval(id);
  }, [shown]);

  useEffect(() => {
    document.documentElement.style.setProperty("--topbar-h", shown ? "40px" : "0px");
  }, [shown]);

  if (!shown) return null;

  const total = Math.floor(left / 1000);
  const clock = `${two(Math.floor(total / 3600))}:${two(Math.floor((total % 3600) / 60))}:${two(total % 60)}`;

  return (
    <div className="promo">
      <div className="container promo__inner">
        <span className="promo__spark" aria-hidden="true">
          <IconBolt width={14} height={14} />
        </span>
        <span className="promo__text">
          <span className="promo__long">{t("promo.text")}</span>
          <span className="promo__short">{t("promo.short")}</span>
        </span>
        {/* outside promo__text so the code survives the ellipsis on phones */}
        <b className="promo__code">{PROMO_CODE}</b>
        <span className="promo__timer">
          {t("promo.ends")} <b dir="ltr">{n(clock)}</b>
        </span>
        <button
          type="button"
          className="promo__close"
          aria-label={t("promo.close")}
          onClick={() => {
            localStorage.setItem(PROMO_KEY, "off");
            setShown(false);
          }}
        >
          <IconX width={12} height={12} />
        </button>
      </div>
    </div>
  );
}

/* ================================================================ trust row */

/** Rating + volume proof, sat directly under the hero buttons. */
export function TrustRow() {
  const { t, n } = useApp();
  const full = Math.round(TRUST.rating);

  return (
    <div className="trust">
      <div className="trust__item">
        <span className="trust__stars" aria-hidden="true">
          {Array.from({ length: 5 }, (_, i) => (
            <IconStar key={i} className={i < full ? "" : "is-off"} />
          ))}
        </span>
        <span className="trust__text">
          <b>{n(TRUST.rating.toFixed(1))}</b>
          <span className="muted"> / {n(5)} · {n(TRUST.reviews.toLocaleString("en-US"))} {t("trust.reviews")}</span>
        </span>
      </div>

      <span className="trust__sep" aria-hidden="true" />

      <div className="trust__item">
        <IconUsers width={16} height={16} />
        <span className="trust__text">
          <b>{n(TRUST.traders.toLocaleString("en-US"))}</b>
          <span className="muted"> {t("trust.traders")}</span>
        </span>
      </div>

      <span className="trust__sep" aria-hidden="true" />

      <div className="trust__item">
        <IconClock width={16} height={16} />
        <span className="trust__text">
          <b>{n(21)}h</b>
          <span className="muted"> {t("trust.payout")}</span>
        </span>
      </div>
    </div>
  );
}

/* ============================================================ benefit trio */

const BENEFITS = [
  { icon: IconWallet, key: "b1" },
  { icon: IconTarget, key: "b2" },
  { icon: IconHeadset, key: "b3" },
];

/** The three promises FundedNext-style landing pages lead with. */
export function BenefitTrio() {
  const { t } = useApp();
  return (
    <section className="section section--tight">
      <div className="container">
        <div className="grid grid-3">
          {BENEFITS.map(({ icon: Icon, key }, i) => (
            <Reveal key={key} delay={i * 80}>
              <article className="benefit">
                <span className="benefit__tag">{t(`bene.${key}.tag`)}</span>
                <div className="benefit__icon">
                  <Icon width={22} height={22} />
                </div>
                <h3 className="benefit__title">{t(`bene.${key}.t`)}</h3>
                <p className="benefit__body">{t(`bene.${key}.d`)}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ============================================================== payout wall */

function PayoutChip({ row }: { row: (typeof PAYOUT_WALL)[number] }) {
  const { t, n } = useApp();
  return (
    <div className="wall__chip">
      <span className="wall__flag" aria-hidden="true">
        {row.flag}
      </span>
      <span className="wall__who">
        <b>{row.name}</b>
        <span className="wall__meta">
          {row.country} · {n(row.hours)}h {t("wall.paidIn")}
        </span>
      </span>
      <span className="wall__amount">{n(money(row.amount))}</span>
    </div>
  );
}

/** Two counter-scrolling marquees of recent payouts. */
export function PayoutWall() {
  const { t } = useApp();
  const half = Math.ceil(PAYOUT_WALL.length / 2);
  const rows = [PAYOUT_WALL.slice(0, half), PAYOUT_WALL.slice(half)];

  return (
    <section className="section section--tight" id="wall">
      <div className="container">
        <SectionHead
          eyebrow={
            <>
              <span className="dot" /> {t("wall.live")}
            </>
          }
          title={t("wall.title")}
          sub={t("wall.sub")}
        />
      </div>

      <div className="wall">
        {rows.map((group, idx) => (
          <div className={`wall__track ${idx === 1 ? "wall__track--rev" : ""}`} key={idx}>
            {/* duplicated once so the loop has no visible seam */}
            {[...group, ...group].map((row, i) => (
              <PayoutChip row={row} key={`${row.name}-${i}`} />
            ))}
          </div>
        ))}
      </div>
    </section>
  );
}

/* ================================================================ count-up */

/** Animates 0 → value the first time the element is scrolled into view. */
function useCountUp(target: number, decimals: number) {
  const ref = useRef<HTMLDivElement>(null);
  const [value, setValue] = useState(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const reduced = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    if (reduced || !("IntersectionObserver" in window)) {
      setValue(target);
      return;
    }

    let raf = 0;
    const io = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        io.disconnect();
        const start = performance.now();
        const tick = (now: number) => {
          const p = Math.min(1, (now - start) / 1400);
          // ease-out cubic — fast first, settles on the number
          setValue(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) raf = requestAnimationFrame(tick);
        };
        raf = requestAnimationFrame(tick);
      },
      { threshold: 0.4 },
    );
    io.observe(el);
    return () => {
      io.disconnect();
      cancelAnimationFrame(raf);
    };
  }, [target]);

  return { ref, text: value.toFixed(decimals) };
}

function HeadlineStat({ stat }: { stat: (typeof HEADLINE_STATS)[number] }) {
  const { t, n } = useApp();
  const { ref, text } = useCountUp(stat.value, stat.decimals ?? 0);
  const pretty = stat.decimals ? text : Number(text).toLocaleString("en-US");

  return (
    <div className="stat" ref={ref}>
      <div className="stat__value" dir="ltr">
        {stat.prefix ?? ""}
        {n(pretty)}
        {stat.suffix ?? ""}
      </div>
      <div className="stat__label">{t(stat.labelKey)}</div>
    </div>
  );
}

export function HeadlineStats() {
  return (
    <div className="stats">
      {HEADLINE_STATS.map((s) => (
        <HeadlineStat stat={s} key={s.labelKey} />
      ))}
    </div>
  );
}

/* =========================================================== compare table */

function compareCell(
  model: ModelId,
  row: string,
  n: (v: string | number) => string,
): string {
  const plan = planFor(model, FEATURED_SIZE);
  switch (row) {
    case "fee":
      return n(money(plan.fee));
    case "profitTarget":
      return plan.targets.length === 0
        ? "—"
        : plan.targets.map((x) => n(pct(x))).join(" → ");
    case "dailyLoss":
      return n(pct(plan.dailyLoss));
    case "maxLoss":
      return n(pct(plan.maxLoss));
    case "split":
      return n(pct(plan.split));
    default:
      return "";
  }
}

/** Side-by-side model table — the numbers all read from data/plans.ts. */
export function CompareSection() {
  const { t, n } = useApp();

  return (
    <section className="section" id="compare">
      <div className="container">
        <SectionHead
          eyebrow={t("compare.eyebrow")}
          title={t("compare.title")}
          sub={t("compare.sub", { size: n(money(FEATURED_SIZE)) })}
        />

        <Reveal>
          <div className="compare">
            <table className="compare__table">
              <thead>
                <tr>
                  <th scope="col">{t("compare.feature")}</th>
                  {MODEL_IDS.map((m) => (
                    <th scope="col" key={m} className={m === "express" ? "is-best" : ""}>
                      {t(`models.${m}`)}
                      {m === "express" && <span className="compare__flag">{t("compare.best")}</span>}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {COMPARE_ROWS.map((row) => (
                  <tr key={row}>
                    <th scope="row">{t(`models.${row}`)}</th>
                    {MODEL_IDS.map((m) => (
                      <td key={m} className={m === "express" ? "is-best" : ""}>
                        {row === "timeLimit" ? (
                          <span className="up">{t("models.unlimited")}</span>
                        ) : row === "firstPayout" ? (
                          <>
                            {n(FIRST_PAYOUT_DAYS[m])} {t("compare.days")}
                          </>
                        ) : row === "split" ? (
                          <span className="up">{compareCell(m, row, n)}</span>
                        ) : (
                          compareCell(m, row, n)
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Reveal>

        <p className="tiny compare__note">{t("compare.note", { size: n(money(FEATURED_SIZE)) })}</p>
      </div>
    </section>
  );
}

/* ========================================================== integrations */

const INTEGRATIONS = [
  { icon: IconTerminal, key: "platform", value: "MetaTrader 5" },
  { icon: IconRocket, key: "charts", value: "TradingView" },
  { icon: IconCard, key: "cards", value: "Visa · Mastercard" },
  { icon: IconWallet, key: "crypto", value: "USDT · BTC" },
  { icon: IconSend, key: "transfers", value: "Wise · SEPA" },
  { icon: IconLock, key: "security", value: "TLS 1.3 · 2FA" },
];

/** Quiet credibility strip: what you trade on, and how money moves. */
export function IntegrationsStrip() {
  const { t } = useApp();
  return (
    <section className="section section--tight">
      <div className="container">
        <p className="integ__head">{t("integ.title")}</p>
        <div className="integ">
          {INTEGRATIONS.map(({ icon: Icon, key, value }) => (
            <div className="integ__item" key={key}>
              <Icon width={18} height={18} />
              <span>
                <b>{value}</b>
                <span className="integ__label">{t(`integ.${key}`)}</span>
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ================================================================ support */

const SUPPORT_STATS = [
  { v: "24/7", k: "support.s1" },
  { v: `<${TRUST.replySeconds}s`, k: "support.s2" },
  { v: `${TRUST.languages}`, k: "support.s3" },
  { v: `${TRUST.supportAgents}+`, k: "support.s4" },
];

export function SupportSection() {
  const { t, n } = useApp();
  return (
    <section className="section" id="support">
      <div className="container">
        <div className="support">
          <div className="support__copy">
            <span className="eyebrow">
              <IconHeadset width={14} height={14} /> {t("support.eyebrow")}
            </span>
            <h2 className="h2">{t("support.title")}</h2>
            <p className="lead">{t("support.sub")}</p>

            <div className="support__actions">
              <Link to="/contact" className="btn btn--primary">
                {t("support.contact")}
                <IconArrow />
              </Link>
              <Link to="/faq" className="btn btn--ghost">
                <IconChat width={16} height={16} />
                {t("support.faq")}
              </Link>
            </div>
          </div>

          <div className="support__stats">
            {SUPPORT_STATS.map((s) => (
              <div className="support__stat" key={s.k}>
                <div className="support__value" dir="ltr">
                  {n(s.v)}
                </div>
                <div className="support__label">{t(s.k)}</div>
              </div>
            ))}
            <div className="support__langs">
              <IconGlobe width={16} height={16} />
              <span>{t("support.langList")}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ============================================================= mobile cta */

/** Sticky buy bar that appears on phones once the hero is off screen. */
export function MobileCta() {
  const { t, n } = useApp();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 700);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div className={`mobile-cta ${visible ? "is-in" : ""}`}>
      <span className="mobile-cta__price">
        <span className="mobile-cta__from">{t("mobile.from")}</span>
        <b>{n(money(planFor("evaluation", 5000).fee))}</b>
      </span>
      <Link to="/register" className="btn btn--primary btn--sm">
        {t("hero.cta")}
        <IconArrow width={15} height={15} />
      </Link>
    </div>
  );
}

/* ============================================================ guarantee ribbon */

const GUARANTEES = [
  { icon: IconCheck, key: "g1" },
  { icon: IconCheck, key: "g2" },
  { icon: IconCheck, key: "g3" },
  { icon: IconCheck, key: "g4" },
];

export function GuaranteeRibbon() {
  const { t } = useApp();
  return (
    <div className="ribbon">
      {GUARANTEES.map(({ icon: Icon, key }) => (
        <span className="ribbon__item" key={key}>
          <span className="tick">
            <Icon />
          </span>
          {t(`guarantee.${key}`)}
        </span>
      ))}
    </div>
  );
}

/* ============================================================= trading bot */

const BOT_FLOW = [
  { icon: IconPulse, key: "f1" },
  { icon: IconTarget, key: "f2" },
  { icon: IconBolt, key: "f3" },
  { icon: IconShield, key: "f4" },
  { icon: IconEye, key: "f5" },
  { icon: IconCheck, key: "f6" },
];

const BOT_DOES = ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10"];
const BOT_WHO = ["w1", "w2", "w3", "w4"];

/** What the automated trader is, what it does, and who it suits. */
export function BotSection() {
  const { t } = useApp();

  return (
    <section className="section" id="bot">
      <div className="container">
        <SectionHead
          eyebrow={
            <>
              <IconRocket width={14} height={14} /> {t("bot.eyebrow")}
            </>
          }
          title={t("bot.title")}
          sub={t("bot.sub")}
        />

        <Reveal>
          <div className="bot-flow">
            {BOT_FLOW.map(({ icon: Icon, key }, i) => (
              <div className="bot-flow__step" key={key}>
                <span className="bot-flow__icon">
                  <Icon width={18} height={18} />
                </span>
                <span className="bot-flow__label">{t(`bot.${key}`)}</span>
                {i < BOT_FLOW.length - 1 && (
                  <span className="bot-flow__arrow" aria-hidden="true" />
                )}
              </div>
            ))}
          </div>
        </Reveal>

        <div className="bot-grid">
          <Reveal>
            <article className="card bot-card">
              <h3 className="card__title">{t("bot.does.title")}</h3>
              <ul className="bot-list">
                {BOT_DOES.map((key) => (
                  <li key={key}>
                    <span className="tick">
                      <IconCheck />
                    </span>
                    {t(`bot.${key}`)}
                  </li>
                ))}
              </ul>
            </article>
          </Reveal>

          <Reveal delay={90}>
            <div className="bot-side">
              <article className="card">
                <h3 className="card__title">{t("bot.why.title")}</h3>
                <p className="card__body">{t("bot.why.body1")}</p>
                <p className="card__body" style={{ marginTop: 12 }}>
                  {t("bot.why.body2")}
                </p>
              </article>

              <article className="card">
                <h3 className="card__title">{t("bot.who.title")}</h3>
                <ul className="bot-list bot-list--who">
                  {BOT_WHO.map((key) => (
                    <li key={key}>
                      <span className="tick">
                        <IconUsers width={12} height={12} />
                      </span>
                      {t(`bot.${key}`)}
                    </li>
                  ))}
                </ul>
              </article>
            </div>
          </Reveal>
        </div>

        <p className="tiny bot-note">{t("bot.note")}</p>
      </div>
    </section>
  );
}
