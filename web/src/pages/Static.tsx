import { useApp } from "../app/AppContext";
import { PlanPicker } from "../components/PlanPicker";
import { Reveal } from "../components/Reveal";
import {
  CtaSection,
  FaqSection,
  PayoutSection,
  PlatformSection,
  RulesSection,
  SectionHead,
  StatsBar,
  StepsSection,
  TestimonialSection,
} from "../components/Sections";

function PageHead({ eyebrow, title, sub }: { eyebrow: string; title: string; sub?: string }) {
  return (
    <section className="section section--tight" style={{ paddingBottom: 0 }}>
      <div className="container">
        <SectionHead eyebrow={eyebrow} title={title} sub={sub} />
      </div>
    </section>
  );
}

export function ChallengesPage() {
  const { t } = useApp();
  return (
    <>
      <PageHead eyebrow={t("nav.challenges")} title={t("models.title")} sub={t("models.sub")} />
      <section className="section" style={{ paddingTop: 24 }}>
        <div className="container">
          <PlanPicker />
        </div>
      </section>
      <RulesSection />
      <FaqSection limit={6} />
      <CtaSection />
    </>
  );
}

export function HowItWorksPage() {
  const { t } = useApp();
  return (
    <>
      <PageHead eyebrow={t("nav.how")} title={t("how.title")} sub={t("how.sub")} />
      <StepsSection />
      <section className="section section--tight">
        <div className="container">
          <Reveal>
            <StatsBar />
          </Reveal>
        </div>
      </section>
      <RulesSection />
      <TestimonialSection />
      <CtaSection />
    </>
  );
}

export function PlatformPage() {
  const { t } = useApp();
  return (
    <>
      <PageHead
        eyebrow={t("nav.platform")}
        title={t("platform.title")}
        sub={t("platform.sub")}
      />
      <PlatformSection />
      <CtaSection />
    </>
  );
}

export function PayoutsPage() {
  const { t } = useApp();
  return (
    <>
      <PageHead eyebrow={t("nav.payouts")} title={t("payout.title")} sub={t("payout.sub")} />
      <PayoutSection />
      <TestimonialSection />
      <CtaSection />
    </>
  );
}

export function FaqPage() {
  return (
    <>
      <FaqSection limit={6} />
      <CtaSection />
    </>
  );
}

export function AboutPage() {
  const { t } = useApp();
  return (
    <>
      <PageHead eyebrow={t("nav.about")} title={t("about.title")} sub={t("about.sub")} />
      <section className="section" style={{ paddingTop: 32 }}>
        <div className="container">
          <div style={{ maxWidth: "70ch", display: "grid", gap: 20 }}>
            <p className="muted">{t("about.body1")}</p>
            <p className="muted">{t("about.body2")}</p>
            <p className="muted">{t("about.body3")}</p>
          </div>

          <div className="grid grid-3" style={{ marginTop: 56 }}>
            {[1, 2, 3].map((i) => (
              <Reveal key={i} delay={i * 70}>
                <article className="card" style={{ height: "100%" }}>
                  <h3 className="card__title">{t(`about.v${i}.t`)}</h3>
                  <p className="card__body">{t(`about.v${i}.d`)}</p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </section>
      <section className="section section--tight">
        <div className="container">
          <StatsBar />
        </div>
      </section>
      <CtaSection />
    </>
  );
}

/** Placeholder legal pages so the footer never links into a 404. */
export function LegalPage({ which }: { which: string }) {
  const { t } = useApp();
  const titles: Record<string, string> = {
    terms: t("footer.terms"),
    privacy: t("footer.privacy"),
    risk: t("footer.risk"),
    refund: t("footer.refund"),
  };
  return (
    <section className="section">
      <div className="container">
        <SectionHead
          eyebrow={t("footer.legal")}
          title={titles[which] ?? t("footer.legal")}
          center={false}
        />
        <p className="muted" style={{ maxWidth: "70ch" }}>
          {t("footer.disclaimer")}
        </p>
      </div>
    </section>
  );
}

export function NotFoundPage() {
  const { t } = useApp();
  return (
    <section className="section" style={{ minHeight: "56vh", display: "grid", placeItems: "center" }}>
      <div className="container" style={{ textAlign: "center" }}>
        <h1 className="h1">404</h1>
        <p className="lead">{t("dash.empty")}</p>
        <a href="#/" className="btn btn--primary" style={{ marginTop: 24 }}>
          {t("common.back")}
        </a>
      </div>
    </section>
  );
}
