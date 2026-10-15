import { useEffect, useRef, useState } from "react";

const KEY = "allfix.chatWidth";
const DEFAULT = 0.42; // share of the row the conversation takes
const MIN_LEFT = 360; // px
const MIN_RIGHT = 300; // px

function saved() {
  try { const v = Number(localStorage.getItem(KEY)); return v > 0 && v < 1 ? v : DEFAULT; } catch { return DEFAULT; }
}
function save(v: number) { try { localStorage.setItem(KEY, String(v)); } catch { /* storage unavailable */ } }

/** Two panes side by side with a divider the user drags to any width. The width is kept per
 * device; double-click the divider to reset it. On narrow screens the panes stack. */
export default function Split({ left, right }: { left: React.ReactNode; right: React.ReactNode }) {
  const row = useRef<HTMLDivElement>(null);
  const [share, setShare] = useState(saved);
  const [dragging, setDragging] = useState(false);

  const clamp = (x: number, w: number) => {
    const lo = Math.min(MIN_LEFT, w / 2), hi = Math.max(w - MIN_RIGHT, w / 2);
    return Math.min(Math.max(x, lo), hi) / w;
  };
  const moveTo = (clientX: number) => {
    const r = row.current?.getBoundingClientRect();
    if (r && r.width) setShare(clamp(clientX - r.left, r.width));
  };

  useEffect(() => {
    if (!dragging) return;
    const move = (e: PointerEvent) => moveTo(e.clientX);
    const up = () => setDragging(false);
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
    return () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    };
  }, [dragging]);

  useEffect(() => { if (!dragging) save(share); }, [dragging, share]);

  const nudge = (dir: number) => {
    const w = row.current?.getBoundingClientRect().width;
    if (w) setShare((s) => clamp(s * w + dir * 40, w));
  };

  return (
    <div ref={row} className="flex min-h-0 min-w-0 flex-1 max-md:flex-col max-md:gap-3" data-testid="split">
      <div className="flex min-h-0 min-w-0 shrink-0 max-md:!w-full" style={{ width: `calc(${share * 100}% - 7px)` }}>{left}</div>
      <div role="separator" aria-orientation="vertical" aria-label="Drag to resize the conversation" tabIndex={0}
        title="Drag to resize · double-click to reset"
        onPointerDown={(e) => { e.preventDefault(); setDragging(true); }}
        onDoubleClick={() => setShare(DEFAULT)}
        onKeyDown={(e) => { if (e.key === "ArrowLeft") nudge(-1); else if (e.key === "ArrowRight") nudge(1); }}
        className="group relative z-10 flex w-[14px] shrink-0 cursor-col-resize touch-none items-center justify-center max-md:hidden"
        data-testid="split-handle">
        <span className={`h-full w-px rounded-full transition-colors ${dragging ? "bg-accent" : "bg-white/10 group-hover:bg-accent/70"}`} />
        <span className={`absolute h-10 w-[5px] rounded-full transition-all ${dragging ? "bg-accent step-glow" : "bg-white/25 group-hover:bg-accent"}`} />
      </div>
      <div className="flex min-h-0 min-w-0 flex-1">{right}</div>
    </div>
  );
}
