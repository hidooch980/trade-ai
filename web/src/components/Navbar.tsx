import { useEffect, useState } from "react";
import { useApp } from "../app/AppContext";
import { Link, useRoute } from "../app/router";
import { LANGS, type Lang } from "../i18n";
import { IconClose, IconMenu } from "./Icons";

const LINKS = [
  { to: "/challenges", key: "nav.challenges" },
  { to: "/how-it-works", key: "nav.how" },
  { to: "/platform", key: "nav.platform" },
  { to: "/payouts", key: "nav.payouts" },
  { to: "/faq", key: "nav.faq" },
  { to: "/about", key: "nav.about" },
];

export function Navbar() {
  const { t, lang, setLang, user, logout } = useApp();
  const [route] = useRoute();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Close the mobile sheet whenever the route changes.
  useEffect(() => setOpen(false), [route]);

  // Dismiss the language menu on any outside click.
  useEffect(() => {
    if (!langOpen) return;
    const close = (e: MouseEvent) => {
      if (!(e.target as HTMLElement).closest(".lang-menu")) setLangOpen(false);
    };
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, [langOpen]);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  const current = LANGS.find((l) => l.code === lang) ?? LANGS[0];

  const langSwitch = (
    <div className="lang-menu">
      <button
        type="button"
        className="lang-menu__trigger"
        aria-haspopup="listbox"
        aria-expanded={langOpen}
        onClick={() => setLangOpen((o) => !o)}
      >
        <span aria-hidden="true">🌐</span>
        {current.label}
      </button>
      {langOpen && (
        <ul className="lang-menu__list" role="listbox">
          {LANGS.map((l) => (
            <li key={l.code}>
              <button
                type="button"
                role="option"
                aria-selected={lang === l.code}
                className={lang === l.code ? "is-active" : ""}
                onClick={() => {
                  setLang(l.code as Lang);
                  setLangOpen(false);
                }}
              >
                <span>{l.name}</span>
                <span className="lang-menu__code">{l.label}</span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  return (
    <>
      <header className={`nav ${scrolled ? "nav--scrolled" : ""}`}>
        <div className="container nav__inner">
          <Link to="/" className="brand">
            <span className="brand__mark" aria-hidden="true">
              T
            </span>
            <span>{t("brand.name")}</span>
          </Link>

          <nav className="nav__links">
            {LINKS.map((l) => (
              <Link
                key={l.to}
                to={l.to}
                className={`nav__link ${route === l.to ? "nav__link--active" : ""}`}
              >
                {t(l.key)}
              </Link>
            ))}
          </nav>

          <div className="nav__actions">
            {langSwitch}
            {user ? (
              <>
                <Link to="/dashboard" className="btn btn--ghost btn--sm">
                  {t("nav.dashboard")}
                </Link>
                <button className="btn btn--quiet btn--sm" onClick={() => void logout()}>
                  {t("nav.logout")}
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn btn--ghost btn--sm">
                  {t("nav.login")}
                </Link>
                <Link to="/register" className="btn btn--primary btn--sm">
                  {t("nav.register")}
                </Link>
              </>
            )}
            <button
              className="nav__burger"
              onClick={() => setOpen((o) => !o)}
              aria-label="Menu"
              aria-expanded={open}
            >
              {open ? <IconClose /> : <IconMenu />}
            </button>
          </div>
        </div>
      </header>

      {open && (
        <div className="nav__mobile">
          {LINKS.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              className={`nav__link ${route === l.to ? "nav__link--active" : ""}`}
              onClick={() => setOpen(false)}
            >
              {t(l.key)}
            </Link>
          ))}
          <Link to="/contact" className="nav__link" onClick={() => setOpen(false)}>
            {t("nav.contact")}
          </Link>
          <div className="nav__mobile-actions">
            {user ? (
              <>
                <Link to="/dashboard" className="btn btn--ghost btn--block">
                  {t("nav.dashboard")}
                </Link>
                <button className="btn btn--danger btn--block" onClick={() => void logout()}>
                  {t("nav.logout")}
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn btn--ghost btn--block">
                  {t("nav.login")}
                </Link>
                <Link to="/register" className="btn btn--primary btn--block">
                  {t("nav.register")}
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}
