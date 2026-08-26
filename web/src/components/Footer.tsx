import { useApp } from "../app/AppContext";
import { Link } from "../app/router";

export function Footer() {
  const { t, n } = useApp();
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer__grid">
          <div className="footer__col">
            <Link to="/" className="brand">
              <span className="brand__mark" aria-hidden="true">
                T
              </span>
              <span>{t("brand.name")}</span>
            </Link>
            <p className="muted" style={{ marginTop: 14, maxWidth: "38ch", fontSize: 15 }}>
              {t("brand.tagline")}
            </p>
          </div>

          <div className="footer__col">
            <h4>{t("footer.product")}</h4>
            <ul>
              <li>
                <Link to="/challenges">{t("nav.challenges")}</Link>
              </li>
              <li>
                <Link to="/how-it-works">{t("nav.how")}</Link>
              </li>
              <li>
                <Link to="/platform">{t("nav.platform")}</Link>
              </li>
              <li>
                <Link to="/payouts">{t("nav.payouts")}</Link>
              </li>
              <li>
                <Link to="/dashboard">{t("nav.dashboard")}</Link>
              </li>
              <li>
                <Link to="/account">{t("nav.account")}</Link>
              </li>
            </ul>
          </div>

          <div className="footer__col">
            <h4>{t("footer.company")}</h4>
            <ul>
              <li>
                <Link to="/about">{t("nav.about")}</Link>
              </li>
              <li>
                <Link to="/contact">{t("nav.contact")}</Link>
              </li>
              <li>
                <Link to="/faq">{t("nav.faq")}</Link>
              </li>
              <li>
                <Link to="/contact">{t("footer.affiliate")}</Link>
              </li>
              <li>
                <Link to="/contact">{t("footer.support")}</Link>
              </li>
            </ul>
          </div>

          <div className="footer__col">
            <h4>{t("footer.legal")}</h4>
            <ul>
              <li>
                <Link to="/legal/terms">{t("footer.terms")}</Link>
              </li>
              <li>
                <Link to="/legal/privacy">{t("footer.privacy")}</Link>
              </li>
              <li>
                <Link to="/legal/risk">{t("footer.risk")}</Link>
              </li>
              <li>
                <Link to="/legal/refund">{t("footer.refund")}</Link>
              </li>
            </ul>
          </div>
        </div>

        <p className="disclaimer">{t("footer.disclaimer")}</p>

        <div className="footer__bottom">
          <span>
            © {n(year)} {t("brand.name")}. {t("footer.rights")}
          </span>
          <span>v1.0.0</span>
        </div>
      </div>
    </footer>
  );
}
