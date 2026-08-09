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

interface AppValue {
  lang: Lang;
  dir: "ltr" | "rtl";
  setLang: (l: Lang) => void;
  t: (key: string) => string;
  /** Translate + localize digits inside the result. */
  n: (value: string | number) => string;
  user: UserResponse | null;
  setUser: (u: UserResponse | null) => void;
  logout: () => Promise<void>;
}

const AppContext = createContext<AppValue | null>(null);

const LANG_KEY = "tradeai.lang";

const CODES = LANGS.map((l) => l.code);

function initialLang(): Lang {
  const stored = localStorage.getItem(LANG_KEY) as Lang | null;
  if (stored && CODES.includes(stored)) return stored;
  const browser = navigator.language.toLowerCase().slice(0, 2) as Lang;
  return CODES.includes(browser) ? browser : "en";
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(initialLang);
  const [user, setUser] = useState<UserResponse | null>(() => tokenStore.user());

  const dir = dirFor(lang);

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = dir;
    document.documentElement.dataset.lang = lang;
    localStorage.setItem(LANG_KEY, lang);
  }, [lang, dir]);

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

  const t = useCallback((key: string) => translate(lang, key), [lang]);
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
    () => ({ lang, dir, setLang, t, n, user, setUser, logout }),
    [lang, dir, setLang, t, n, user, logout],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp(): AppValue {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used inside <AppProvider>");
  return ctx;
}
