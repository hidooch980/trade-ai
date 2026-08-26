import { useCallback, useEffect, useRef, useState } from "react";
import { useApp } from "../app/AppContext";
import { Link, navigate, useRoute } from "../app/router";
import { LANGS, type Lang } from "../i18n";
import { IconClose, IconMenu } from "./Icons";
import { ThemeToggle } from "./ThemeToggle";

/**
 * The site is a single landing page, so the nav points at sections rather than
 * routes. The standalone pages still exist and stay reachable from the footer.
 */
const SECTIONS = [
  { id: "models", key: "nav.challenges" },
  { id: "how", key: "nav.how" },
  { id: "platform", key: "nav.platform" },
  { id: "bot", key: "nav.bot" },
  { id: "payouts", key: "nav.payouts" },
  { id: "faq", key: "nav.faq" },
];

const IDS = SECTIONS.map((s) => s.id);

function scrollToSection(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function Navbar() {
  const { t, lang, setLang, user, logout } = useApp();
  const [route] = useRoute();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const [active, setActive] = useState<string | null>(null);
  const headerRef = useRef<HTMLElement>(null);

  const onLanding = route === "/";

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Highlight whichever section currently owns the top of the viewport.
  useEffect(() => {
    if (!onLanding || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver(
      (entries) => {
        const hit = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        if (hit) setActive(hit.target.id);
      },
      { rootMargin: "-45% 0px -50% 0px" },
    );
    IDS.forEach((id) => {
      const el = document.getElementById(id);
      if (el) io.observe(el);
    });
    return () => io.disconnect();
  }, [onLanding, route]);

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
    // The header sits below the promo bar until that scrolls away, so the sheet
    // has to start at wherever the header actually ends right now.
    if (open && headerRef.current) {
      const bottom = headerRef.current.getBoundingClientRect().bottom;
      document.documentElement.style.setProperty("--nav-bottom", `${Math.round(bottom)}px`);
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  const goto = useCallback(
    (id: string) => {
      setOpen(false);
      if (onLanding) {
        scrollToSection(id);
        return;
      }
      // Land on the page first, then jump once the section exists in the DOM.
      navigate("/");
      requestAnimationFrame(() => requestAnimationFrame(() => scrollToSection(id)));
    },
    [onLanding],
  );

  const current = LANGS.find((l) => l.code === lang) ?? LANGS[0];

  const langSwitch = (
    <div className="lang-menu nav__util">
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

  const sectionLinks = (onClose?: () => void) =>
    SECTIONS.map((s) => (
      <button
        key={s.id}
        type="button"
        className={`nav__link ${onLanding && active === s.id ? "nav__link--active" : ""}`}
        onClick={() => {
          onClose?.();
          goto(s.id);
        }}
      >
        {t(s.key)}
      </button>
    ));

  return (
    <>
      <header ref={headerRef} className={`nav ${scrolled ? "nav--scrolled" : ""}`}>
        <div className="container nav__inner">
          <Link to="/" className="brand">
            <span className="brand__mark" aria-hidden="true">
              T
            </span>
            <span>{t("brand.name")}</span>
          </Link>

          <nav className="nav__links">{sectionLinks()}</nav>

          <div className="nav__actions">
            <ThemeToggle className="nav__util" />
            {langSwitch}
            {user ? (
              <>
                {user.role === "ADMIN" && (
                  <Link to="/admin/users" className="btn btn--quiet btn--sm nav__util">
                    {t("nav.admin")}
                  </Link>
                )}
                <Link to="/intelligence" className="btn btn--quiet btn--sm nav__util">
                  {t("nav.intel")}
                </Link>
                <Link to="/account" className="btn btn--ghost btn--sm">
                  {t("nav.account")}
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
              aria-label={t("nav.menu")}
              aria-expanded={open}
            >
              {open ? <IconClose /> : <IconMenu />}
            </button>
          </div>
        </div>
      </header>

      {open && (
        <div className="nav__mobile">
          {/* On phones the header only has room for the brand and the CTA, so
              the theme and language controls move in here. */}
          <div className="nav__mobile-utils">
            <ThemeToggle />
            <div className="lang-menu">
              <button
                type="button"
                className="lang-menu__trigger"
                aria-haspopup="listbox"
                aria-expanded={langOpen}
                onClick={() => setLangOpen((o) => !o)}
              >
                <span aria-hidden="true">🌐</span>
                {current.name}
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
          </div>
          {sectionLinks(() => setOpen(false))}
          <button
            type="button"
            className="nav__link"
            onClick={() => {
              setOpen(false);
              goto("support");
            }}
          >
            {t("nav.support")}
          </button>
          <Link to="/contact" className="nav__link" onClick={() => setOpen(false)}>
            {t("nav.contact")}
          </Link>
          <div className="nav__mobile-actions">
            {user ? (
              <>
                <Link to="/account" className="btn btn--ghost btn--block">
                  {t("nav.account")}
                </Link>
                <Link to="/accounts" className="btn btn--ghost btn--block">
                  {t("nav.mt5")}
                </Link>
                <Link to="/risk" className="btn btn--ghost btn--block">
                  {t("nav.risk")}
                </Link>
                <Link to="/intelligence" className="btn btn--ghost btn--block">
                  {t("nav.intel")}
                </Link>
                <Link to="/dashboard" className="btn btn--ghost btn--block">
                  {t("nav.dashboard")}
                </Link>
                {user.role === "ADMIN" && (
                  <Link to="/admin/users" className="btn btn--ghost btn--block">
                    {t("nav.admin")}
                  </Link>
                )}
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
