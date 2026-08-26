import { useApp } from "../app/AppContext";
import { IconMoon, IconSun } from "./Icons";

/** Two-state switch: whichever half is lit is the theme you are looking at. */
export function ThemeToggle({ className = "" }: { className?: string }) {
  const { theme, setTheme, t } = useApp();

  return (
    <div
      className={`theme-toggle ${className}`.trim()}
      role="group"
      aria-label={t("theme.label")}
    >
      <button
        type="button"
        aria-pressed={theme === "light"}
        aria-label={t("theme.light")}
        title={t("theme.light")}
        onClick={() => setTheme("light")}
      >
        <IconSun width={15} height={15} />
      </button>
      <button
        type="button"
        aria-pressed={theme === "dark"}
        aria-label={t("theme.dark")}
        title={t("theme.dark")}
        onClick={() => setTheme("dark")}
      >
        <IconMoon width={15} height={15} />
      </button>
    </div>
  );
}
