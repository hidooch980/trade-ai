import { useEffect, useMemo, useRef, useState } from "react";
import { connectMarketSocket, dashboard, guardian, market, system } from "../api/client";
import { useApp } from "../app/AppContext";

type Conn = "connecting" | "open" | "closed";

interface Quote {
  symbol: string;
  price: number;
  prev: number;
}

const SYMBOLS = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD"];

/** Digs a symbol→price map out of whatever shape the backend hands back. */
function extractPrices(payload: unknown, into: Map<string, number>): void {
  if (!payload || typeof payload !== "object") return;
  const obj = payload as Record<string, unknown>;

  // { symbol: "XAUUSD", price/bid/last: 2345.1 }
  const sym = typeof obj.symbol === "string" ? obj.symbol : null;
  const direct = obj.price ?? obj.bid ?? obj.last ?? obj.close;
  if (sym && typeof direct === "number") {
    into.set(sym, direct);
    return;
  }

  // { XAUUSD: 2345.1 } or { XAUUSD: { price: 2345.1 } } — and nested wrappers.
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === "number" && SYMBOLS.includes(key)) {
      into.set(key, value);
    } else if (value && typeof value === "object") {
      const inner = value as Record<string, unknown>;
      const p = inner.price ?? inner.bid ?? inner.last ?? inner.close;
      if (SYMBOLS.includes(key) && typeof p === "number") into.set(key, p);
      else extractPrices(value, into);
    }
  }
}

function decimals(symbol: string): number {
  if (symbol === "BTCUSD") return 1;
  if (symbol === "XAUUSD") return 2;
  return 5;
}

export function LiveHud() {
  const { t, n } = useApp();
  const [conn, setConn] = useState<Conn>("connecting");
  const [quotes, setQuotes] = useState<Record<string, Quote>>({});
  const [sysOnline, setSysOnline] = useState<boolean | null>(null);
  const [journalCount, setJournalCount] = useState<number | null>(null);
  const [guardianStatus, setGuardianStatus] = useState<string | null>(null);
  const quotesRef = useRef<Record<string, Quote>>({});

  // Health + dashboard + guardian, polled gently.
  useEffect(() => {
    const ac = new AbortController();

    const poll = () => {
      system
        .health()
        .then((r) => setSysOnline(r.status === "HEALTHY"))
        .catch(() => setSysOnline(false));

      dashboard
        .status(ac.signal)
        .then((d) => {
          if (typeof d.journal_count === "number") setJournalCount(d.journal_count);
          const map = new Map<string, number>();
          extractPrices(d.market, map);
          applyPrices(map);
        })
        .catch(() => undefined);

      guardian
        .summary(ac.signal)
        .then((g) => setGuardianStatus(g.status ?? null))
        .catch(() => undefined);

      market
        .status(ac.signal)
        .then((m) => {
          const map = new Map<string, number>();
          extractPrices(m, map);
          applyPrices(map);
        })
        .catch(() => undefined);
    };

    const applyPrices = (map: Map<string, number>) => {
      if (map.size === 0) return;
      setQuotes(() => {
        const next = { ...quotesRef.current };
        for (const [sym, price] of map) {
          const prev = next[sym]?.price ?? price;
          next[sym] = { symbol: sym, price, prev };
        }
        quotesRef.current = next;
        return next;
      });
    };

    poll();
    const id = setInterval(poll, 8000);
    return () => {
      ac.abort();
      clearInterval(id);
    };
  }, []);

  // Live ticks over /ws/market.
  useEffect(() => {
    return connectMarketSocket(
      (data) => {
        const map = new Map<string, number>();
        extractPrices(data, map);
        if (map.size === 0) return;
        setQuotes(() => {
          const next = { ...quotesRef.current };
          for (const [sym, price] of map) {
            const prev = next[sym]?.price ?? price;
            next[sym] = { symbol: sym, price, prev };
          }
          quotesRef.current = next;
          return next;
        });
      },
      (state) => setConn(state),
    );
  }, []);

  const cells = useMemo(
    () =>
      SYMBOLS.map((sym) => {
        const q = quotes[sym];
        const delta = q ? q.price - q.prev : 0;
        const pctDelta = q && q.prev ? (delta / q.prev) * 100 : 0;
        return { sym, q, delta, pctDelta };
      }),
    [quotes],
  );

  const connLabel =
    conn === "open"
      ? t("state.online")
      : conn === "connecting"
        ? t("state.connecting")
        : t("state.offline");

  return (
    <div className="hud">
      <div className="hud__bar">
        <span className="hud__dots" aria-hidden="true">
          <i />
          <i />
          <i />
        </span>
        <span className={`dot ${conn === "open" ? "" : conn === "connecting" ? "dot--amber" : "dot--red"}`} />
        <span>
          /ws/market · {connLabel}
        </span>
        <span style={{ marginInlineStart: "auto" }}>
          {t("dash.system")}:{" "}
          {sysOnline === null ? "—" : sysOnline ? t("state.online") : t("state.offline")}
        </span>
      </div>

      <div className="hud__grid">
        {cells.map(({ sym, q, delta, pctDelta }) => (
          <div className="hud__cell" key={sym}>
            <div className="hud__label">{sym}</div>
            <div className="hud__value">
              {q ? n(q.price.toFixed(decimals(sym))) : "—"}
            </div>
            <div className={`hud__delta ${delta >= 0 ? "up" : "down"}`}>
              {q ? `${delta >= 0 ? "+" : ""}${n(pctDelta.toFixed(2))}%` : " "}
            </div>
          </div>
        ))}
      </div>

      <div className="hud__foot">
        <span className="status-pill">
          <span
            className={`dot ${guardianStatus && guardianStatus !== "NO_STATE" ? "" : "dot--amber"}`}
          />
          {t("dash.guardian")}: {guardianStatus ?? "—"}
        </span>
        <span className="status-pill">
          {t("dash.journalCount")}: {journalCount === null ? "—" : n(journalCount)}
        </span>
      </div>
    </div>
  );
}
