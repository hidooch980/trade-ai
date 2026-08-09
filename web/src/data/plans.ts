export type ModelId = "evaluation" | "express" | "instant";

export interface PlanRow {
  size: number;
  fee: number;
  /** Profit target as a fraction of account size, per phase. */
  targets: number[];
  dailyLoss: number;
  maxLoss: number;
  split: number;
}

/**
 * Programme terms. Editing these numbers is the only thing needed to
 * re-price the site — every card, table and comparison reads from here.
 */
export const PLANS: Record<ModelId, PlanRow[]> = {
  evaluation: [
    { size: 5000, fee: 32, targets: [0.08, 0.05], dailyLoss: 0.05, maxLoss: 0.1, split: 0.8 },
    { size: 10000, fee: 58, targets: [0.08, 0.05], dailyLoss: 0.05, maxLoss: 0.1, split: 0.8 },
    { size: 25000, fee: 129, targets: [0.08, 0.05], dailyLoss: 0.05, maxLoss: 0.1, split: 0.8 },
    { size: 50000, fee: 239, targets: [0.08, 0.05], dailyLoss: 0.05, maxLoss: 0.1, split: 0.8 },
    { size: 100000, fee: 419, targets: [0.08, 0.05], dailyLoss: 0.05, maxLoss: 0.1, split: 0.8 },
    { size: 200000, fee: 799, targets: [0.08, 0.05], dailyLoss: 0.05, maxLoss: 0.1, split: 0.8 },
  ],
  express: [
    { size: 5000, fee: 45, targets: [0.09], dailyLoss: 0.04, maxLoss: 0.08, split: 0.8 },
    { size: 10000, fee: 79, targets: [0.09], dailyLoss: 0.04, maxLoss: 0.08, split: 0.8 },
    { size: 25000, fee: 169, targets: [0.09], dailyLoss: 0.04, maxLoss: 0.08, split: 0.8 },
    { size: 50000, fee: 299, targets: [0.09], dailyLoss: 0.04, maxLoss: 0.08, split: 0.8 },
    { size: 100000, fee: 529, targets: [0.09], dailyLoss: 0.04, maxLoss: 0.08, split: 0.8 },
    { size: 200000, fee: 989, targets: [0.09], dailyLoss: 0.04, maxLoss: 0.08, split: 0.8 },
  ],
  instant: [
    { size: 5000, fee: 119, targets: [], dailyLoss: 0.03, maxLoss: 0.06, split: 0.85 },
    { size: 10000, fee: 219, targets: [], dailyLoss: 0.03, maxLoss: 0.06, split: 0.85 },
    { size: 25000, fee: 479, targets: [], dailyLoss: 0.03, maxLoss: 0.06, split: 0.85 },
    { size: 50000, fee: 899, targets: [], dailyLoss: 0.03, maxLoss: 0.06, split: 0.85 },
    { size: 100000, fee: 1599, targets: [], dailyLoss: 0.03, maxLoss: 0.06, split: 0.85 },
    { size: 200000, fee: 2999, targets: [], dailyLoss: 0.03, maxLoss: 0.06, split: 0.85 },
  ],
};

export const MODEL_IDS: ModelId[] = ["evaluation", "express", "instant"];
export const SIZES = PLANS.evaluation.map((p) => p.size);
export const FEATURED_SIZE = 100000;

export function planFor(model: ModelId, size: number): PlanRow {
  return PLANS[model].find((p) => p.size === size) ?? PLANS[model][0];
}

export function money(value: number, fractionDigits = 0): string {
  return `$${value.toLocaleString("en-US", {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  })}`;
}

export function pct(value: number): string {
  return `${(value * 100).toLocaleString("en-US", { maximumFractionDigits: 1 })}%`;
}
