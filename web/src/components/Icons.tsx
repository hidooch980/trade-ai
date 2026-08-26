import type { SVGProps } from "react";

type P = SVGProps<SVGSVGElement>;

const base = (props: P) => ({
  width: 20,
  height: 20,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.9,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  ...props,
});

export const IconShield = (p: P) => (
  <svg {...base(p)}>
    <path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3Z" />
    <path d="m9 12 2 2 4-4" />
  </svg>
);

export const IconPulse = (p: P) => (
  <svg {...base(p)}>
    <path d="M3 12h4l2.5-7 5 14L17 12h4" />
  </svg>
);

export const IconJournal = (p: P) => (
  <svg {...base(p)}>
    <path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v18H6.5A1.5 1.5 0 0 1 5 19.5v-15Z" />
    <path d="M9 8h6M9 12h6M9 16h3" />
  </svg>
);

export const IconChart = (p: P) => (
  <svg {...base(p)}>
    <path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />
  </svg>
);

export const IconTerminal = (p: P) => (
  <svg {...base(p)}>
    <rect x="2.5" y="4" width="19" height="16" rx="2.5" />
    <path d="m7 9 3 3-3 3M13 15h4" />
  </svg>
);

export const IconEye = (p: P) => (
  <svg {...base(p)}>
    <path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
);

export const IconWallet = (p: P) => (
  <svg {...base(p)}>
    <path d="M3 7.5A2.5 2.5 0 0 1 5.5 5H18v3" />
    <rect x="3" y="7.5" width="18" height="12" rx="2.5" />
    <circle cx="16.5" cy="13.5" r="1.2" fill="currentColor" stroke="none" />
  </svg>
);

export const IconClock = (p: P) => (
  <svg {...base(p)}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 7v5l3.5 2" />
  </svg>
);

export const IconBolt = (p: P) => (
  <svg {...base(p)}>
    <path d="M13 2 4.5 13.5H11L10 22l8.5-11.5H12L13 2Z" />
  </svg>
);

export const IconRefresh = (p: P) => (
  <svg {...base(p)}>
    <path d="M20 11a8 8 0 1 0-.6 4" />
    <path d="M20 5v6h-6" />
  </svg>
);

export const IconCheck = (p: P) => (
  <svg {...base({ width: 13, height: 13, strokeWidth: 3, ...p })}>
    <path d="m4 12.5 5 5L20 6.5" />
  </svg>
);

export const IconX = (p: P) => (
  <svg {...base({ width: 12, height: 12, strokeWidth: 3, ...p })}>
    <path d="M6 6l12 12M18 6 6 18" />
  </svg>
);

export const IconPlus = (p: P) => (
  <svg {...base({ width: 14, height: 14, strokeWidth: 2.4, ...p })}>
    <path d="M12 5v14M5 12h14" />
  </svg>
);

export const IconArrow = (p: P) => (
  <svg {...base({ width: 17, height: 17, ...p })}>
    <path d="M5 12h13M13 6l6 6-6 6" />
  </svg>
);

export const IconMenu = (p: P) => (
  <svg {...base(p)}>
    <path d="M4 7h16M4 12h16M4 17h16" />
  </svg>
);

export const IconClose = (p: P) => (
  <svg {...base(p)}>
    <path d="M6 6l12 12M18 6 6 18" />
  </svg>
);

export const IconSun = (p: P) => (
  <svg {...base(p)}>
    <circle cx="12" cy="12" r="4.2" />
    <path d="M12 2.5v2.2M12 19.3v2.2M4.2 4.2l1.6 1.6M18.2 18.2l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.2 19.8l1.6-1.6M18.2 5.8l1.6-1.6" />
  </svg>
);

export const IconMoon = (p: P) => (
  <svg {...base(p)}>
    <path d="M20 14.4A8.5 8.5 0 0 1 9.6 4a8.5 8.5 0 1 0 10.4 10.4Z" />
  </svg>
);

export const IconStar = (p: P) => (
  <svg {...base({ width: 15, height: 15, strokeWidth: 0, fill: "currentColor", ...p })}>
    <path d="m12 3.2 2.6 5.3 5.9.85-4.25 4.15 1 5.85L12 16.6l-5.25 2.75 1-5.85L3.5 9.35l5.9-.85L12 3.2Z" />
  </svg>
);

export const IconGlobe = (p: P) => (
  <svg {...base(p)}>
    <circle cx="12" cy="12" r="9" />
    <path d="M3 12h18M12 3c2.4 2.5 3.6 5.5 3.6 9S14.4 18.5 12 21c-2.4-2.5-3.6-5.5-3.6-9S9.6 5.5 12 3Z" />
  </svg>
);

export const IconHeadset = (p: P) => (
  <svg {...base(p)}>
    <path d="M4 13v-1a8 8 0 0 1 16 0v1" />
    <rect x="2.5" y="13" width="4.5" height="6.5" rx="2" />
    <rect x="17" y="13" width="4.5" height="6.5" rx="2" />
    <path d="M20 19.5v.5a2.5 2.5 0 0 1-2.5 2.5H13" />
  </svg>
);

export const IconLock = (p: P) => (
  <svg {...base(p)}>
    <rect x="4" y="10.5" width="16" height="10.5" rx="2.5" />
    <path d="M8 10.5V7.5a4 4 0 0 1 8 0v3" />
  </svg>
);

export const IconCard = (p: P) => (
  <svg {...base(p)}>
    <rect x="2.5" y="5" width="19" height="14" rx="2.5" />
    <path d="M2.5 10h19" />
  </svg>
);

export const IconUsers = (p: P) => (
  <svg {...base(p)}>
    <circle cx="9" cy="8" r="3.4" />
    <path d="M2.8 20a6.2 6.2 0 0 1 12.4 0" />
    <path d="M16 5.2a3.4 3.4 0 0 1 0 5.6M17.6 14.4A6.2 6.2 0 0 1 21.2 20" />
  </svg>
);

export const IconTarget = (p: P) => (
  <svg {...base(p)}>
    <circle cx="12" cy="12" r="8.5" />
    <circle cx="12" cy="12" r="4.6" />
    <circle cx="12" cy="12" r="1.1" fill="currentColor" stroke="none" />
  </svg>
);

export const IconRocket = (p: P) => (
  <svg {...base(p)}>
    <path d="M13.5 4.2c3.4-1.5 6.3-1.2 6.3-1.2s.3 2.9-1.2 6.3c-1.3 3-3.6 5.2-6 6.6l-4-4c1.4-2.4 3.6-4.7 6.6-6" />
    <path d="M9.4 15.9 8.1 20l-4.2-4.2 4.1-1.3M6.7 17.3c-1.2 1.2-1.5 3.7-1.5 3.7s2.5-.3 3.7-1.5" />
    <circle cx="15.2" cy="8.8" r="1.5" />
  </svg>
);

export const IconChat = (p: P) => (
  <svg {...base(p)}>
    <path d="M20.5 12.4c0 4-3.8 7.2-8.5 7.2-1 0-2-.15-2.9-.42L4 21l1.5-3.7C4.05 16 3.5 14.3 3.5 12.4c0-4 3.8-7.2 8.5-7.2s8.5 3.2 8.5 7.2Z" />
  </svg>
);

export const IconSend = (p: P) => (
  <svg {...base(p)}>
    <path d="M21 3 10.5 13.5M21 3l-6.8 18-3.7-7.5L3 9.8 21 3Z" />
  </svg>
);
