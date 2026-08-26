import { useState, type ReactNode } from "react";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import {
  IconArrow,
  IconBolt,
  IconChart,
  IconCheck,
  IconClock,
  IconEye,
  IconJournal,
  IconPlus,
  IconPulse,
  IconShield,
  IconTerminal,
  IconWallet,
  IconX,
} from "./Icons";
import { Reveal } from "./Reveal";

export function SectionHead({
  eyebrow,
  title,
  sub,
  center = true,
}: {
  eyebrow?: ReactNode;
  title: string;
  sub?: string;
  center?: boolean;
}) {
  return (
    <div className={`section-head ${center ? "section-head--center" : ""}`}>
      {eyebrow && <span className="eyebrow">{eyebrow}</span>}
      <h2 className="h2">{title}</h2>
      {sub && <p className="lead">{sub}</p>}
    </div>
  );
}

/* ------------------------------------------------------------------ stats */

export function StatsBar() {
  const { t, n } = useApp();
  const items = [
    { v: "12,480+", k: "stats.traders" },
    { v: "$41.6M", k: "stats.paid" },
    { v: "137", k: "stats.countries" },
    { v: "99.98%", k: "stats.uptime" },
  ];
  return (
    <div className="stats">
      {items.map((s) => (
        <div className="stat" key={s.k}>
          <div className="stat__value">{n(s.v)}</div>
          <div className="stat__label">{t(s.k)}</div>
        </div>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ steps */

export function StepsSection() {
  const { t } = useApp();
  return (
    <section className="section" id="how">
      <div className="container">
        <SectionHead eyebrow={t("nav.how")} title={t("how.title")} sub={t("how.sub")} />
        <div className="steps">
          {[1, 2, 3, 4].map((i) => (
            <Reveal key={i} delay={i * 70}>
              <div className="step">
                <h3 className="step__title">{t(`how.s${i}.t`)}</h3>
                <p className="step__body">{t(`how.s${i}.d`)}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

/* --------------------------------------------------------------- platform */

const PLATFORM_ICONS = [IconShield, IconPulse, IconJournal, IconChart, IconTerminal, IconEye];

export function PlatformSection() {
  const { t } = useApp();
  return (
    <section className="section" id="platform">
      <div className="container">
        <SectionHead
          eyebrow={t("nav.platform")}
          title={t("platform.title")}
          sub={t("platform.sub")}
        />
        <div className="grid grid-3">
          {PLATFORM_ICONS.map((Icon, i) => (
            <Reveal key={i} delay={i * 60}>
              <article className="card card--hover" style={{ height: "100%" }}>
                <div className="card__icon">
                  <Icon />
                </div>
                <h3 className="card__title">{t(`platform.f${i + 1}.t`)}</h3>
                <p className="card__body">{t(`platform.f${i + 1}.d`)}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- payouts */

const PAYOUT_ICONS = [IconClock, IconWallet, IconBolt, IconCheck];

export function PayoutSection() {
  const { t } = useApp();
  return (
    <section className="section" id="payouts">
      <div className="container">
        <SectionHead
          eyebrow={t("nav.payouts")}
          title={t("payout.title")}
          sub={t("payout.sub")}
        />
        <div className="grid grid-4">
          {PAYOUT_ICONS.map((Icon, i) => (
            <Reveal key={i} delay={i * 60}>
              <article className="card card--hover" style={{ height: "100%" }}>
                <div className="card__icon">
                  <Icon />
                </div>
                <h3 className="card__title">{t(`payout.p${i + 1}.t`)}</h3>
                <p className="card__body">{t(`payout.p${i + 1}.d`)}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ rules */

export function RulesSection() {
  const { t } = useApp();
  return (
    <section className="section">
      <div className="container">
        <SectionHead title={t("rules.title")} sub={t("rules.sub")} />
        <div className="rules">
          <Reveal>
            <div className="card" style={{ height: "100%" }}>
              <h3 className="card__title" style={{ color: "var(--pos)" }}>
                {t("rules.allowed")}
              </h3>
              <ul className="rule-list">
                {[1, 2, 3, 4].map((i) => (
                  <li key={i}>
                    <span className="tick">
                      <IconCheck />
                    </span>
                    {t(`rules.a${i}`)}
                  </li>
                ))}
              </ul>
            </div>
          </Reveal>
          <Reveal delay={90}>
            <div className="card" style={{ height: "100%" }}>
              <h3 className="card__title" style={{ color: "var(--red)" }}>
                {t("rules.forbidden")}
              </h3>
              <ul className="rule-list">
                {[1, 2, 3, 4].map((i) => (
                  <li key={i}>
                    <span className="cross">
                      <IconX />
                    </span>
                    {t(`rules.f${i}`)}
                  </li>
                ))}
              </ul>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}

/* ----------------------------------------------------------- testimonials */

const TESTIMONIALS = [
  { name: "A. Kowalski", meta: "$100K · Evaluation", payout: "$18,240", initial: "A" },
  { name: "M. Haddad", meta: "$50K · Express", payout: "$9,110", initial: "M" },
  { name: "S. Yilmaz", meta: "$200K · Instant", payout: "$31,780", initial: "S" },
];

const QUOTES: Record<string, string[]> = {
  en: [
    "The drawdown counter in the dashboard is the reason I passed. I could see the exact buffer left instead of guessing at 2am.",
    "Payout hit my account 19 hours after I requested it. No extra verification round, no email chain.",
    "I run an EA and expected the usual argument about it. There was none — the rule page said allowed, and it was allowed.",
  ],
  fa: [
    "شمارنده‌ی دراودان در داشبورد دلیل قبولی من بود. دقیقاً می‌دیدم چقدر فضا مانده، به‌جای حدس‌زدن ساعت دو نصف‌شب.",
    "تسویه ۱۹ ساعت بعد از درخواست به حسابم رسید. نه راند اضافه‌ی احراز هویت، نه زنجیره‌ی ایمیل.",
    "اکسپرت اجرا می‌کنم و انتظار بحث همیشگی را داشتم. خبری نبود — صفحه‌ی قوانین گفته بود مجاز، و مجاز بود.",
  ],
  tr: [
    "Panodaki drawdown sayacı geçmemin sebebi. Gece ikide tahmin yürütmek yerine kalan payı tam olarak görüyordum.",
    "Ödeme, talebimden 19 saat sonra hesabıma geçti. Ek doğrulama turu yok, e-posta zinciri yok.",
    "Bir EA çalıştırıyorum ve her zamanki tartışmayı bekliyordum. Olmadı — kural sayfası izinli diyordu, izinliydi.",
  ],
  ar: [
    "عدّاد الانخفاض في لوحة التحكم هو سبب اجتيازي. كنت أرى الهامش المتبقي بدقة بدل التخمين في الثانية فجرًا.",
    "وصلت الأرباح إلى حسابي بعد 19 ساعة من الطلب. بلا جولة تحقق إضافية ولا سلسلة رسائل.",
    "أشغّل روبوت تداول وتوقّعت الجدال المعتاد. لم يحدث — صفحة القواعد قالت مسموح، وكان مسموحًا.",
  ],
  de: [
    "Der Drawdown-Zähler im Dashboard ist der Grund, warum ich bestanden habe. Ich sah den exakten Puffer, statt um zwei Uhr nachts zu raten.",
    "Die Auszahlung war 19 Stunden nach meinem Antrag auf dem Konto. Keine zusätzliche Prüfrunde, keine E-Mail-Kette.",
    "Ich nutze einen EA und rechnete mit der üblichen Diskussion. Es gab keine — die Regelseite sagte erlaubt, und es war erlaubt.",
  ],
  fr: [
    "Le compteur de drawdown du tableau de bord explique ma réussite. Je voyais la marge exacte au lieu de deviner à deux heures du matin.",
    "Le paiement est arrivé 19 heures après ma demande. Aucune vérification supplémentaire, aucune chaîne d'e-mails.",
    "J'utilise un EA et je m'attendais au débat habituel. Il n'y en a pas eu — la page des règles disait autorisé, et c'était autorisé.",
  ],
};

export function TestimonialSection() {
  const { t, n, lang } = useApp();
  const quotes = QUOTES[lang] ?? QUOTES.en;
  return (
    <section className="section">
      <div className="container">
        <SectionHead title={t("testi.title")} sub={t("testi.sub")} />
        <div className="grid grid-3">
          {TESTIMONIALS.map((p, i) => (
            <Reveal key={p.name} delay={i * 70}>
              <article className="card quote" style={{ height: "100%" }}>
                <p className="quote__text">“{quotes[i]}”</p>
                <div className="quote__who">
                  <span className="avatar" aria-hidden="true">
                    {p.initial}
                  </span>
                  <span>
                    <span className="quote__name">{p.name}</span>
                    <span className="quote__meta" style={{ display: "block" }}>
                      {n(p.meta)}
                    </span>
                  </span>
                  <span className="badge-payout">{n(p.payout)}</span>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------- faq */

export function FaqSection({ limit }: { limit?: number }) {
  const { t } = useApp();
  const [open, setOpen] = useState<number | null>(0);
  const count = limit ?? 6;

  return (
    <section className="section" id="faq">
      <div className="container">
        <SectionHead eyebrow={t("nav.faq")} title={t("faq.title")} />
        <div className="faq">
          {Array.from({ length: count }, (_, i) => i + 1).map((i) => {
            const expanded = open === i - 1;
            return (
              <div className="faq__item" key={i}>
                <button
                  className="faq__q"
                  aria-expanded={expanded}
                  onClick={() => setOpen(expanded ? null : i - 1)}
                >
                  {t(`faq.q${i}`)}
                  <span className="faq__icon" aria-hidden="true">
                    <IconPlus />
                  </span>
                </button>
                {expanded && <p className="faq__a">{t(`faq.a${i}`)}</p>}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------- cta */

export function CtaSection() {
  const { t } = useApp();
  return (
    <section className="section section--tight">
      <div className="container">
        <div className="cta-box">
          <h2 className="h2">{t("cta.title")}</h2>
          <p className="lead" style={{ maxWidth: 520, margin: "16px auto 0" }}>
            {t("cta.sub")}
          </p>
          <div style={{ marginTop: 30 }}>
            <Link to="/register" className="btn btn--primary">
              {t("cta.button")}
              <IconArrow />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
