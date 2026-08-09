import { useState } from "react";
import { useApp } from "../app/AppContext";
import { Link } from "../app/router";
import {
  FEATURED_SIZE,
  MODEL_IDS,
  money,
  pct,
  planFor,
  SIZES,
  type ModelId,
} from "../data/plans";
import { IconArrow } from "./Icons";
import { Reveal } from "./Reveal";

/** Model tabs + size chips + the three comparison cards. */
export function PlanPicker({ compact = false }: { compact?: boolean }) {
  const { t, n } = useApp();
  const [size, setSize] = useState<number>(FEATURED_SIZE);
  const [model, setModel] = useState<ModelId>("evaluation");

  return (
    <>
      <div style={{ textAlign: "center" }}>
        <div className="tabs" role="tablist" aria-label={t("models.title")}>
          {MODEL_IDS.map((m) => (
            <button
              key={m}
              role="tab"
              aria-selected={model === m}
              onClick={() => setModel(m)}
            >
              {t(`models.${m}`)}
            </button>
          ))}
        </div>

        <div className="sizes">
          {SIZES.map((s) => (
            <button
              key={s}
              className="chip"
              aria-pressed={size === s}
              onClick={() => setSize(s)}
            >
              {n(money(s))}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-3">
        {MODEL_IDS.map((m, i) => {
          const plan = planFor(m, size);
          const featured = m === model;
          return (
            <Reveal key={m} delay={i * 80}>
              <article className={`card plan ${featured ? "plan--featured" : ""}`}>
                {featured && <span className="plan__badge">{t("models.popular")}</span>}

                <h3 className="plan__name">{t(`models.${m}`)}</h3>
                <p className="plan__desc">{t(`models.${m}Desc`)}</p>

                <div className="plan__price">
                  <span className="plan__amount">{n(money(plan.fee))}</span>
                  <span className="plan__per">{t("common.perMonth")}</span>
                </div>

                <div className="plan__rows">
                  <div className="plan__row">
                    <span>{t("models.accountSize")}</span>
                    <span>{n(money(plan.size))}</span>
                  </div>

                  {plan.targets.length === 0 ? (
                    <div className="plan__row">
                      <span>{t("models.profitTarget")}</span>
                      <span>—</span>
                    </div>
                  ) : (
                    plan.targets.map((target, idx) => (
                      <div className="plan__row" key={idx}>
                        <span>
                          {t("models.profitTarget")}
                          {plan.targets.length > 1 ? ` · ${t(`models.phase${idx + 1}`)}` : ""}
                        </span>
                        <span>
                          {n(pct(target))} · {n(money(plan.size * target))}
                        </span>
                      </div>
                    ))
                  )}

                  <div className="plan__row">
                    <span>{t("models.dailyLoss")}</span>
                    <span>
                      {n(pct(plan.dailyLoss))} · {n(money(plan.size * plan.dailyLoss))}
                    </span>
                  </div>
                  <div className="plan__row">
                    <span>{t("models.maxLoss")}</span>
                    <span>
                      {n(pct(plan.maxLoss))} · {n(money(plan.size * plan.maxLoss))}
                    </span>
                  </div>
                  <div className="plan__row">
                    <span>{t("models.split")}</span>
                    <span className="up">{n(pct(plan.split))}</span>
                  </div>
                  <div className="plan__row">
                    <span>{t("models.timeLimit")}</span>
                    <span>{t("models.unlimited")}</span>
                  </div>
                </div>

                <div className="plan__foot">
                  <Link
                    to="/register"
                    className={`btn btn--block ${featured ? "btn--primary" : "btn--ghost"}`}
                  >
                    {t("models.select")} {n(money(plan.size))}
                    <IconArrow />
                  </Link>
                  <p className="plan__refund">{t("models.refund")}</p>
                </div>
              </article>
            </Reveal>
          );
        })}
      </div>

      {!compact && (
        <p className="tiny" style={{ textAlign: "center", marginTop: 28 }}>
          {t("footer.disclaimer")}
        </p>
      )}
    </>
  );
}
