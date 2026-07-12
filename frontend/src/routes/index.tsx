import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import {
  ArrowRight,
  Cpu,
  Cloud,
  Database,
  Zap,
  Route as RouteIcon,
  Shield,
  Gauge,
  Sparkles,
  X,
} from "lucide-react";
export const Route = createFileRoute("/")({
  component: Overview,
});
type Slide = {
  kicker: string;
  title: string;
  subtitle: string;
  body?: React.ReactNode;
  items?: { icon: React.ReactNode; title: string; desc: string; accent: "red" | "blue" | "emerald" }[];
  cta: string;
};
const slides: Slide[] = [
  {
    kicker: "01 · WELCOME",
    title: "Welcome to FrugalRoute",
    subtitle: "Hybrid AI Routing on AMD Ryzen AI",
    body: (
      <div className="space-y-4 text-sm leading-relaxed text-muted-foreground">
        <p>
          FrugalRoute decides in <span className="text-foreground font-semibold">microseconds</span> whether a prompt
          runs on your <span className="text-primary font-semibold">local AMD node</span> or a{" "}
          <span className="text-accent font-semibold">frontier cloud model</span> — so you pay cents where you used
          to pay dollars.
        </p>
        <div className="glass rounded-xl p-4">
          <div className="font-mono-tech text-[10px] uppercase tracking-widest text-primary text-glow-red">
            THE AMD STORY
          </div>
          <p className="mt-2 text-sm text-muted-foreground">
            Local inference runs on a <span className="text-foreground font-semibold">single AMD Ryzen AI</span>{" "}
            NPU with Qwen 3B, hitting a{" "}
            <span className="text-foreground font-semibold">12ms median latency</span> across a live routing
            benchmark of 14.2M tokens.
          </p>
        </div>
      </div>
    ),
    cta: "Next",
  },
  {
    kicker: "02 · HOW IT WORKS",
    title: "How It Works",
    subtitle: "5 Signals, 1 Router",
    items: [
      {
        icon: <RouteIcon className="h-4 w-4" />,
        title: "Intent Classifier",
        desc: "Scores the prompt for reasoning depth, tool use, and creative range in under 3ms on-device.",
        accent: "red",
      },
      {
        icon: <Gauge className="h-4 w-4" />,
        title: "Confidence Threshold",
        desc: "A tunable dial (0.0 – 1.0) that decides how aggressively local models handle the load.",
        accent: "blue",
      },
      {
        icon: <Database className="h-4 w-4" />,
        title: "Semantic Cache",
        desc: "Vector-dedup hits repeat queries at a 34% rate, returning zero-cost cached completions.",
        accent: "emerald",
      },
      {
        icon: <Cpu className="h-4 w-4" />,
        title: "Local Path · Qwen 3B",
        desc: "AMD Ryzen AI executes drafts, classification, and short-form generation at 12ms median.",
        accent: "red",
      },
      {
        icon: <Cloud className="h-4 w-4" />,
        title: "Cloud Path · GPT-4o",
        desc: "Frontier providers are engaged only when the router demands maximum capability.",
        accent: "blue",
      },
    ],
    cta: "Next",
  },
  {
    kicker: "03 · GET STARTED",
    title: "Pick Your Entry Point",
    subtitle: "3 surfaces to explore FrugalRoute",
    items: [
      {
        icon: <Sparkles className="h-4 w-4" />,
        title: "Neural Chat",
        desc: "Run prompts through the live router and watch each response tagged LOCAL or CLOUD in real time.",
        accent: "red",
      },
      {
        icon: <Zap className="h-4 w-4" />,
        title: "Analytics",
        desc: "Inspect token flow, latency histograms, and monthly savings vs. an all-cloud baseline.",
        accent: "blue",
      },
      {
        icon: <Shield className="h-4 w-4" />,
        title: "Settings",
        desc: "Wire API providers, mask keys, and dial in the confidence threshold to match your budget.",
        accent: "emerald",
      },
    ],
    cta: "Launch FrugalRoute",
  },
];
function Overview() {
  const [open, setOpen] = useState(true);
  const [step, setStep] = useState(0);
  const slide = slides[step];
  const isLast = step === slides.length - 1;
  return (
    <div className="relative mx-auto min-h-[calc(100vh-4rem)] max-w-7xl px-6 py-10 md:px-10 md:py-16">
      {/* Blurred background context */}
      <div className={open ? "pointer-events-none select-none blur-md" : ""}>
        <BackgroundOverview />
      </div>
      {/* Modal */}
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 md:p-8">
          <div
            className="absolute inset-0 bg-background/70 backdrop-blur-xl"
            onClick={() => setOpen(false)}
          />
          <div className="relative w-full max-w-2xl">
            {/* glow ring */}
            <div className="absolute -inset-px rounded-3xl bg-gradient-to-br from-primary/40 via-accent/20 to-transparent blur-md" />
            <div className="glass-strong relative overflow-hidden rounded-3xl">
              {/* header stripe */}
              <div className="flex items-center justify-between border-b border-white/5 px-6 py-3">
                <div className="flex items-center gap-2 font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
                  <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-primary" />
                  {slide.kicker}
                </div>
                <button
                  onClick={() => setOpen(false)}
                  className="rounded-full p-1.5 text-muted-foreground transition-colors hover:bg-white/5 hover:text-foreground"
                  aria-label="Close intro"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
              <div className="px-6 py-7 md:px-8 md:py-8">
                {/* Title block */}
                <div className="flex items-start gap-4">
                  <div className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl bg-gradient-to-br from-primary to-primary/40 glow-red">
                    <RouteIcon className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-extrabold tracking-tight md:text-3xl">{slide.title}</h2>
                    <p className="mt-1 font-mono-tech text-[11px] uppercase tracking-widest text-accent">
                      {slide.subtitle}
                    </p>
                  </div>
                </div>
                {/* Body */}
                <div className="mt-6 max-h-[46vh] overflow-y-auto pr-1">
                  {slide.body}
                  {slide.items && (
                    <div className="space-y-3">
                      {slide.items.map((it) => (
                        <div
                          key={it.title}
                          className="glass group flex items-start gap-3 rounded-xl p-4 transition-colors hover:border-primary/40"
                        >
                          <div
                            className={`grid h-8 w-8 shrink-0 place-items-center rounded-lg ${
                              it.accent === "red"
                                ? "bg-primary/15 text-primary"
                                : it.accent === "blue"
                                  ? "bg-accent/15 text-accent"
                                  : "bg-emerald-400/15 text-emerald-400"
                            }`}
                          >
                            {it.icon}
                          </div>
                          <div>
                            <div className="text-sm font-semibold">{it.title}</div>
                            <div className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
                              {it.desc}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
              {/* Footer */}
              <div className="flex items-center justify-between border-t border-white/5 bg-black/20 px-6 py-4">
                <div className="flex items-center gap-1.5">
                  {slides.map((_, i) => (
                    <button
                      key={i}
                      onClick={() => setStep(i)}
                      className={`h-1.5 rounded-full transition-all ${
                        i === step ? "w-8 bg-primary glow-red" : "w-3 bg-white/15 hover:bg-white/30"
                      }`}
                      aria-label={`Go to step ${i + 1}`}
                    />
                  ))}
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setOpen(false)}
                    className="rounded-lg px-3 py-2 text-xs font-medium text-muted-foreground hover:text-foreground"
                  >
                    Skip
                  </button>
                  {isLast ? (
                    <Link
                      to="/chat"
                      onClick={() => setOpen(false)}
                      className="group inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-xs font-semibold text-primary-foreground glow-red transition-transform hover:scale-[1.02]"
                    >
                      {slide.cta}
                      <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
                    </Link>
                  ) : (
                    <button
                      onClick={() => setStep((s) => Math.min(s + 1, slides.length - 1))}
                      className="group inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-xs font-semibold text-primary-foreground glow-red transition-transform hover:scale-[1.02]"
                    >
                      {slide.cta}
                      <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      {/* Reopen chip when closed */}
      {!open && (
        <button
          onClick={() => {
            setStep(0);
            setOpen(true);
          }}
          className="fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-full glass px-4 py-2 font-mono-tech text-[11px] uppercase tracking-widest text-foreground hover:bg-white/5"
        >
          <Sparkles className="h-3.5 w-3.5 text-primary" />
          Replay intro
        </button>
      )}
    </div>
  );
}
function BackgroundOverview() {
  return (
    <div className="space-y-10">
      <div className="inline-flex items-center gap-2 rounded-full glass px-3 py-1 font-mono-tech text-[11px] uppercase tracking-widest text-muted-foreground">
        <span className="h-1.5 w-1.5 rounded-full bg-primary" />
        v0.4 · Obsidian build
      </div>
      <h1 className="text-5xl font-extrabold leading-[1.02] tracking-tight md:text-7xl">
        Intelligence <span className="text-primary text-glow-red">Routed.</span>
        <br />
        Costs <span className="text-accent text-glow-blue">Slashed.</span>
      </h1>
      <p className="max-w-xl text-lg text-muted-foreground">
        FrugalRoute decides in microseconds whether a prompt runs on your local AMD node or a frontier cloud model.
      </p>
      <div className="grid gap-5 md:grid-cols-3">
        {[
          { k: "TOKENS SAVED", v: "14.2M" },
          { k: "LOCAL LATENCY", v: "12ms" },
          { k: "CACHE HIT", v: "34%" },
        ].map((s) => (
          <div key={s.k} className="glass rounded-2xl p-6">
            <div className="font-mono-tech text-[11px] uppercase tracking-widest text-muted-foreground">{s.k}</div>
            <div className="mt-3 font-mono-tech text-4xl font-bold">{s.v}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
