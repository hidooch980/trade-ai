import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { IconArrow, IconBolt } from "../components/Icons";
import {
  BenefitTrio,
  BotSection,
  CompareSection,
  GuaranteeRibbon,
  HeadlineStats,
  IntegrationsStrip,
  MobileCta,
  PayoutWall,
  SupportSection,
  TrustRow,
} from "../components/Landing";
import { LiveHud } from "../components/LiveHud";
import { PlanPicker } from "../components/PlanPicker";
import { Reveal } from "../components/Reveal";
import {
  CtaSection,
  FaqSection,
  PayoutSection,
  PlatformSection,
  RulesSection,
  SectionHead,
  StepsSection,
  TestimonialSection,
} from "../components/Sections";

export function Home() {
  const { t } = useApp();

  return (
    <>
      <section className="hero">
        <div className="container">
          <span className="pill">
            <span className="dot" />
            {t("hero.badge")}
          </span>

          <h1 className="h1 hero__title">
            {t("hero.title")}
            <span className="hero__accent">{t("hero.titleAccent")}</span>
          </h1>

          <p className="lead hero__sub">{t("hero.sub")}</p>

          <div className="hero__cta">
            <Link to="/register" className="btn btn--primary btn--lg">
              {t("hero.cta")}
              <IconArrow />
            </Link>
            <a
              href="#how"
              className="btn btn--ghost btn--lg"
              onClick={(e) => {
                e.preventDefault();
                document.getElementById("how")?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              <IconBolt width={16} height={16} />
              {t("hero.cta2")}
            </a>
          </div>

          <GuaranteeRibbon />
          <TrustRow />
          <LiveHud />
        </div>
      </section>

      <IntegrationsStrip />

      <section className="section section--tight">
        <div className="container">
          <Reveal>
            <HeadlineStats />
          </Reveal>
        </div>
      </section>

      <BenefitTrio />

      <section className="section" id="models">
        <div className="container">
          <SectionHead
            eyebrow={t("nav.challenges")}
            title={t("models.title")}
            sub={t("models.sub")}
          />
          <PlanPicker compact />
        </div>
      </section>

      <CompareSection />
      <StepsSection />
      <BotSection />
      <PlatformSection />
      <PayoutSection />
      <PayoutWall />
      <RulesSection />
      <TestimonialSection />
      <SupportSection />
      <FaqSection limit={6} />
      <CtaSection />
      <MobileCta />
    </>
  );
}
