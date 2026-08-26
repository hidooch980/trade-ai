import { useCallback, useEffect, useState, type ReactNode } from "react";
import { useApp } from "../app/AppContext";
import { IconRefresh } from "./Icons";

export function Panel({
  title,
  children,
  onRefresh,
  busy,
  action,
}: {
  title: string;
  children: ReactNode;
  onRefresh?: () => void;
  busy?: boolean;
  action?: ReactNode;
}) {
  const { t } = useApp();

  return (
    <section className="panel">
      <header className="panel__head">
        <h2 className="panel__title">{title}</h2>
        <div className="panel__tools">
          {action}
          {onRefresh && (
            <button
              className="btn btn--ghost btn--sm"
              onClick={onRefresh}
              disabled={busy}
              aria-label={t("dash.refresh")}
            >
              {busy ? <span className="spinner" /> : <IconRefresh />}
            </button>
          )}
        </div>
      </header>
      <div className="panel__body">{children}</div>
    </section>
  );
}

/** Generic "fetch on mount + manual refresh" hook. */
export function useEndpoint<T>(fn: (signal?: AbortSignal) => Promise<T>, enabled = true) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const load = useCallback(() => {
    if (!enabled) return;
    setBusy(true);
    setError(null);
    fn()
      .then((d) => setData(d))
      .catch((e: unknown) => setError(e instanceof Error ? e.message : String(e)))
      .finally(() => setBusy(false));
  }, [fn, enabled]);

  useEffect(() => {
    load();
  }, [load]);

  return { data, error, busy, reload: load };
}
