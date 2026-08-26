/**
 * Copy-free landing data. Everything user-visible that is *not* a proper noun
 * lives in i18n; the numbers below are the placeholder marketing figures and
 * are the only place they are defined.
 */

export interface PayoutRow {
  name: string;
  flag: string;
  country: string;
  amount: number;
  hours: number;
}

/** Feeds the scrolling payout wall. Names are illustrative. */
export const PAYOUT_WALL: PayoutRow[] = [
  { name: "A. Kowalski", flag: "🇵🇱", country: "PL", amount: 18240, hours: 19 },
  { name: "M. Haddad", flag: "🇦🇪", country: "AE", amount: 9110, hours: 14 },
  { name: "S. Yilmaz", flag: "🇹🇷", country: "TR", amount: 31780, hours: 22 },
  { name: "R. Mehta", flag: "🇮🇳", country: "IN", amount: 7420, hours: 11 },
  { name: "L. Fernandes", flag: "🇵🇹", country: "PT", amount: 12960, hours: 26 },
  { name: "K. Nowak", flag: "🇵🇱", country: "PL", amount: 5380, hours: 9 },
  { name: "D. Schneider", flag: "🇩🇪", country: "DE", amount: 24150, hours: 17 },
  { name: "N. Okafor", flag: "🇳🇬", country: "NG", amount: 8890, hours: 21 },
  { name: "J. Dupont", flag: "🇫🇷", country: "FR", amount: 15630, hours: 13 },
  { name: "H. Tanaka", flag: "🇯🇵", country: "JP", amount: 41200, hours: 28 },
  { name: "P. Sanchez", flag: "🇪🇸", country: "ES", amount: 6740, hours: 8 },
  { name: "V. Petrov", flag: "🇧🇬", country: "BG", amount: 19870, hours: 24 },
];

export interface HeadlineStat {
  /** Numeric part, animated from zero when the strip scrolls into view. */
  value: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  labelKey: string;
}

export const HEADLINE_STATS: HeadlineStat[] = [
  { value: 41.6, prefix: "$", suffix: "M", decimals: 1, labelKey: "stats.paid" },
  { value: 12480, suffix: "+", labelKey: "stats.traders" },
  { value: 137, labelKey: "stats.countries" },
  { value: 21, suffix: "h", labelKey: "stats.payoutTime" },
];

/** Rows of the model comparison table, in display order. */
export const COMPARE_ROWS = [
  "fee",
  "profitTarget",
  "dailyLoss",
  "maxLoss",
  "split",
  "timeLimit",
  "firstPayout",
] as const;

export type CompareRow = (typeof COMPARE_ROWS)[number];

/** Days until the first payout unlocks, per model. */
export const FIRST_PAYOUT_DAYS: Record<string, number> = {
  evaluation: 14,
  express: 14,
  instant: 7,
};

export const TRUST = {
  rating: 4.8,
  reviews: 3120,
  traders: 12480,
  languages: 6,
  supportAgents: 40,
  replySeconds: 25,
};
