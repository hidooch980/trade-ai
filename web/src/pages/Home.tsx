import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import { IconArrow } from "../components/Icons";
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
  StatsBar,
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
            <Link to="/register" className="btn btn--primary">
              {t("hero.cta")}
              <IconArrow />
            </Link>
            <Link to="/how-it-works" className="btn btn--ghost">
              {t("hero.cta2")}
            </Link>
          </div>

          <p className="hero__note">{t("hero.note")}</p>

          <LiveHud />
        </div>
      </section>

      <section className="section section--tight">
        <div className="container">
          <Reveal>
            <StatsBar />
          </Reveal>
        </div>
      </section>

      <section className="section" id="challenges">
        <div className="container">
          <SectionHead
            eyebrow={t("nav.challenges")}
            title={t("models.title")}
            sub={t("models.sub")}
          />
          <PlanPicker compact />
        </div>
      </section>

      <StepsSection />
      <PlatformSection />
      <PayoutSection />
      <RulesSection />
      <TestimonialSection />
      <FaqSection limit={4} />
      <CtaSection />
    </>
  );
}
