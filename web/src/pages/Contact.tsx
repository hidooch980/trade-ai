import { useState, type FormEvent } from "react";
import { useApp } from "../app/AppContext";
import { SectionHead } from "../components/Sections";

export function ContactPage() {
  const { t } = useApp();
  const [sent, setSent] = useState(false);

  const submit = (e: FormEvent) => {
    e.preventDefault();
    // No contact endpoint exists on the backend yet — wire this to one when it lands.
    setSent(true);
  };

  return (
    <section className="section">
      <div className="container">
        <SectionHead eyebrow={t("nav.contact")} title={t("contact.title")} sub={t("contact.sub")} />

        <div className="grid grid-2" style={{ alignItems: "start" }}>
          <form className="card" onSubmit={submit}>
            {sent && <div className="alert alert--ok">{t("contact.sent")}</div>}

            <div className="field">
              <label htmlFor="cn">{t("contact.name")}</label>
              <input id="cn" className="input" required />
            </div>
            <div className="field">
              <label htmlFor="ce">{t("auth.email")}</label>
              <input id="ce" type="email" className="input" required />
            </div>
            <div className="field">
              <label htmlFor="cm">{t("contact.message")}</label>
              <textarea id="cm" className="textarea" required />
            </div>
            <button className="btn btn--primary btn--block" type="submit">
              {t("contact.send")}
            </button>
          </form>

          <div className="card">
            <h3 className="card__title">{t("contact.channels")}</h3>
            <div className="kv" style={{ marginTop: 16 }}>
              <div className="kv__row">
                <span className="kv__k">Email</span>
                <span className="kv__v">support@trade-ai.example</span>
              </div>
              <div className="kv__row">
                <span className="kv__k">Telegram</span>
                <span className="kv__v">@tradeai_support</span>
              </div>
              <div className="kv__row">
                <span className="kv__k">Discord</span>
                <span className="kv__v">discord.gg/tradeai</span>
              </div>
              <div className="kv__row">
                <span className="kv__k">SLA</span>
                <span className="kv__v">&lt; 4h</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
