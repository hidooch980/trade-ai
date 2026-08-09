import { useState, type FormEvent } from "react";
import { ApiError, auth, tokenStore } from "../api/client";
import { useApp } from "../app/AppContext";
import { Link, navigate } from "../app/router";

function errorText(e: unknown, fallback: string): string {
  if (e instanceof ApiError) return e.message;
  if (e instanceof Error && e.message) return e.message;
  return fallback;
}

/* ------------------------------------------------------------------ login */

export function LoginPage() {
  const { t, lang, setUser } = useApp();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [device, setDevice] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const res = await auth.login({
        username,
        password,
        language: lang,
        device_name: device || null,
      });
      tokenStore.save(res);
      setUser(res.user);
      navigate("/dashboard");
    } catch (err) {
      setError(errorText(err, t("state.error")));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container auth-wrap">
      <form className="card form-card" onSubmit={submit}>
        <h1 className="h3">{t("auth.loginTitle")}</h1>
        <p className="muted" style={{ marginTop: 8, marginBottom: 24, fontSize: 15 }}>
          {t("auth.loginSub")}
        </p>

        {error && <div className="alert alert--error">{error}</div>}

        <div className="field">
          <label htmlFor="u">{t("auth.username")}</label>
          <input
            id="u"
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </div>

        <div className="field">
          <label htmlFor="p">{t("auth.password")}</label>
          <input
            id="p"
            type="password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </div>

        <div className="field">
          <label htmlFor="d">{t("auth.deviceName")}</label>
          <input
            id="d"
            className="input"
            value={device}
            onChange={(e) => setDevice(e.target.value)}
            placeholder="Chrome · Windows"
          />
        </div>

        <button className="btn btn--primary btn--block" disabled={busy} type="submit">
          {busy ? <span className="spinner" /> : t("auth.submitLogin")}
        </button>

        <div className="form-row">
          <span className="muted">
            {t("auth.noAccount")}{" "}
            <Link to="/register" className="link">
              {t("nav.register")}
            </Link>
          </span>
          <Link to="/forgot-password" className="link">
            {t("auth.forgot")}
          </Link>
        </div>
      </form>
    </div>
  );
}

/* --------------------------------------------------------------- register */

export function RegisterPage() {
  const { t, lang } = useApp();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await auth.register({ email, username, password, language: lang });
      setDone(true);
    } catch (err) {
      setError(errorText(err, t("state.error")));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container auth-wrap">
      <form className="card form-card" onSubmit={submit}>
        <h1 className="h3">{t("auth.registerTitle")}</h1>
        <p className="muted" style={{ marginTop: 8, marginBottom: 24, fontSize: 15 }}>
          {t("auth.registerSub")}
        </p>

        {error && <div className="alert alert--error">{error}</div>}
        {done && <div className="alert alert--ok">{t("auth.registered")}</div>}

        <div className="field">
          <label htmlFor="re">{t("auth.email")}</label>
          <input
            id="re"
            type="email"
            className="input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            required
          />
        </div>

        <div className="field">
          <label htmlFor="ru">{t("auth.username")}</label>
          <input
            id="ru"
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            minLength={3}
            maxLength={100}
            autoComplete="username"
            required
          />
        </div>

        <div className="field">
          <label htmlFor="rp">{t("auth.password")}</label>
          <input
            id="rp"
            type="password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={8}
            maxLength={128}
            autoComplete="new-password"
            required
          />
          <p className="tiny" style={{ marginTop: 6 }}>
            {t("auth.passwordHint")}
          </p>
        </div>

        <button className="btn btn--primary btn--block" disabled={busy} type="submit">
          {busy ? <span className="spinner" /> : t("auth.submitRegister")}
        </button>

        <div className="form-row">
          <span className="muted">
            {t("auth.haveAccount")}{" "}
            <Link to="/login" className="link">
              {t("nav.login")}
            </Link>
          </span>
        </div>
      </form>
    </div>
  );
}

/* -------------------------------------------------------- forgot password */

export function ForgotPasswordPage() {
  const { t } = useApp();
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await auth.forgotPassword(email);
      setSent(true);
    } catch (err) {
      setError(errorText(err, t("state.error")));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container auth-wrap">
      <form className="card form-card" onSubmit={submit}>
        <h1 className="h3">{t("auth.forgotTitle")}</h1>
        <p className="muted" style={{ marginTop: 8, marginBottom: 24, fontSize: 15 }}>
          {t("auth.forgotSub")}
        </p>

        {error && <div className="alert alert--error">{error}</div>}
        {sent && <div className="alert alert--ok">{t("auth.resetSent")}</div>}

        <div className="field">
          <label htmlFor="fe">{t("auth.email")}</label>
          <input
            id="fe"
            type="email"
            className="input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <button className="btn btn--primary btn--block" disabled={busy} type="submit">
          {busy ? <span className="spinner" /> : t("auth.sendReset")}
        </button>

        <div className="form-row">
          <Link to="/login" className="link">
            {t("common.back")}
          </Link>
        </div>
      </form>
    </div>
  );
}
