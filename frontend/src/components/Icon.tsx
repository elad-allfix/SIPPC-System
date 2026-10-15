/** Line icons the stage views pick by meaning (the server allows exactly these names). */
const PATHS: Record<string, string> = {
  money: "M2 7h20v11H2zM2 11h20M16 15h2",
  click: "M9 9l10.5 3.5-4.5 1.5-1.5 4.5zM5 3v2M3 5h2M7.5 7.5L6 6",
  call: "M5 3h4l2 5-2.5 1.5a11 11 0 005 5L15 12l5 2v4a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z",
  eye_off: "M3 3l18 18M10.6 5.1A9.8 9.8 0 0112 5c6 0 10 7 10 7a17 17 0 01-3 3.6M6.6 6.6C3.8 8.4 2 12 2 12s4 7 10 7a9.6 9.6 0 004.4-1",
  page: "M2 5a2 2 0 012-2h16a2 2 0 012 2v14a2 2 0 01-2 2H4a2 2 0 01-2-2zM2 9h20M6 6h.01M9 6h.01",
  filter: "M3 5h18M7 12h10M10 19h4",
  search: "M11 4a7 7 0 100 14 7 7 0 000-14zM20 20l-4-4",
  ad: "M3 11l15-6v14L3 13zM7 13v5h3",
  mobile: "M8 2h8a2 2 0 012 2v16a2 2 0 01-2 2H8a2 2 0 01-2-2V4a2 2 0 012-2zM11 18h2",
  grid: "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z",
  calendar: "M4 5h16v16H4zM4 10h16M8 3v4M16 3v4",
  clock: "M12 3a9 9 0 100 18 9 9 0 000-18zM12 7v5l3 2",
  pin: "M12 21s-7-6.2-7-12a7 7 0 0114 0c0 5.8-7 12-7 12zM12 7a2 2 0 100 4 2 2 0 000-4z",
  users: "M9 11a4 4 0 100-8 4 4 0 000 8zM2 21v-1a6 6 0 0112 0v1M16 3.5a4 4 0 010 7.5M22 21v-1a6 6 0 00-4-5.6",
  trophy: "M8 21h8M12 17v4M7 4h10v5a5 5 0 01-10 0zM7 6H4a3 3 0 003 4M17 6h3a3 3 0 01-3 4",
  trend_up: "M3 17l6-6 4 4 8-8M15 7h6v6",
  trend_down: "M3 7l6 6 4-4 8 8M15 17h6v-6",
  target: "M12 3a9 9 0 100 18 9 9 0 000-18zM12 8a4 4 0 100 8 4 4 0 000-8zM12 12h.01",
  alert: "M12 3l10 18H2zM12 10v5M12 18h.01",
  question: "M12 3a9 9 0 100 18 9 9 0 000-18zM9.5 9.5a2.5 2.5 0 015 .5c0 1.7-2.5 2-2.5 4M12 17h.01",
  check: "M12 3a9 9 0 100 18 9 9 0 000-18zM8 12l3 3 5-6",
  bulb: "M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9V16h7v-2.1A6 6 0 0012 3z",
  flask: "M9 3h6M10 3v6L4.5 19a1.5 1.5 0 001.3 2h12.4a1.5 1.5 0 001.3-2L14 9V3M7 15h10",
  chart: "M4 20V10M10 20V4M16 20v-7M22 20H2",
  store: "M3 9l2-5h14l2 5M3 9h18v2a3 3 0 01-6 0 3 3 0 01-6 0 3 3 0 01-6 0zM5 13v8h14v-8M10 21v-5h4v5",
  globe: "M12 3a9 9 0 100 18 9 9 0 000-18zM3 12h18M12 3c2.5 2.5 3.5 5.5 3.5 9s-1 6.5-3.5 9c-2.5-2.5-3.5-5.5-3.5-9s1-6.5 3.5-9z",
  link: "M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1",
  star: "M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4l-5.5 2.9 1-6.2L3 9.7l6.2-.9z",
  bolt: "M13 2L4 14h7l-1 8 9-12h-7z",
  tag: "M3 3h8l10 10-8 8L3 11zM7.5 7.5h.01",
  pause: "M9 5v14M15 5v14",
  scale: "M12 3v18M7 21h10M4 7h16M4 7l-2 6a3 3 0 006 0zM20 7l-2 6a3 3 0 006 0z",
};

export default function Icon({ name, className = "h-4 w-4", stroke = 2 }: { name: string; className?: string; stroke?: number }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={stroke}
      strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={PATHS[name] ?? PATHS.chart} />
    </svg>
  );
}

/** Each stage's own symbol, used in its header. */
export const STAGE_ICON: Record<number, string> = { 1: "link", 2: "store", 3: "globe", 4: "page", 5: "trend_up", 6: "bulb", 7: "target" };
