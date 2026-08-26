import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { auth as authApi, tokenStore } from "../api/client";
import type { UserResponse } from "../api/types";
import { dirFor, localizeDigits, translate, LANGS, type Lang } from "../i18n";

export type Theme = "light" | "dark";

interface AppValue {
  lang: Lang;
  dir: "ltr" | "rtl";
  setLang: (l: Lang) => void;
  theme: Theme;
  setTheme: (t: Theme) => void;
  toggleTheme: () => void;
  t: (key: string, vars?: Record<string, string | number>) => string;
  /** Translate + localize digits inside the result. */
  n: (value: string | number) => string;
  user: UserResponse | null;
  setUser: (u: UserResponse | null) => void;
  logout: () => Promise<void>;
}

const AppContext = createContext<AppValue | null>(null);

const LANG_KEY = "tradeai.lang";
const THEME_KEY = "tradeai.theme";

const CODES = LANGS.map((l) => l.code);

function initialLang(): Lang {
  const stored = localStorage.getItem(LANG_KEY) as Lang | null;
  if (stored && CODES.includes(stored)) return stored;
  const browser = navigator.language.toLowerCase().slice(0, 2) as Lang;
  return CODES.includes(browser) ? browser : "en";
}

/** A stored choice wins; otherwise follow whatever the OS is set to. */
function initialTheme(): Theme {
  const stored = localStorage.getItem(THEME_KEY);
  if (stored === "light" || stored === "dark") return stored;
  return window.matchMedia?.("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

/** Keeps the browser chrome (mobile address bar) in step with the theme. */
function paintBrowserChrome(theme: Theme) {
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", theme === "light" ? "#f4f7fd" : "#05070f");
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(initialLang);
  const [theme, setThemeState] = useState<Theme>(initialTheme);
  const [user, setUser] = useState<UserResponse | null>(() => tokenStore.user());

  const dir = dirFor(lang);

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = dir;
    document.documentElement.dataset.lang = lang;
    localStorage.setItem(LANG_KEY, lang);
  }, [lang, dir]);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(THEME_KEY, theme);
    paintBrowserChrome(theme);
  }, [theme]);

  // A stored token may be stale; confirm it against /auth/me on boot.
  useEffect(() => {
    if (!tokenStore.access()) return;
    let alive = true;
    authApi
      .me()
      .then((u) => alive && setUser(u))
      .catch(() => {
        tokenStore.clear();
        if (alive) setUser(null);
      });
    return () => {
      alive = false;
    };
  }, []);

  const setLang = useCallback((l: Lang) => setLangState(l), []);
  const setTheme = useCallback((t: Theme) => setThemeState(t), []);
  const toggleTheme = useCallback(
    () => setThemeState((t) => (t === "dark" ? "light" : "dark")),
    [],
  );

  const t = useCallback(
    (key: string, vars?: Record<string, string | number>) => translate(lang, key, vars),
    [lang],
  );
  const n = useCallback(
    (value: string | number) => localizeDigits(String(value), lang),
    [lang],
  );

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } catch {
      // Logging out locally matters more than the server round-trip succeeding.
    }
    tokenStore.clear();
    setUser(null);
  }, []);

  const value = useMemo<AppValue>(
    () => ({ lang, dir, setLang, theme, setTheme, toggleTheme, t, n, user, setUser, logout }),
    [lang, dir, setLang, theme, setTheme, toggleTheme, t, n, user, logout],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp(): AppValue {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used inside <AppProvider>");
  return ctx;
}
