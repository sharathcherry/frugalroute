import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Send,
  Paperclip,
  Zap,
  Cloud,
  Brain,
  Copy,
  RefreshCw,
  ThumbsUp,
  ThumbsDown,
  Sparkles,
  Cpu,
  Activity,
  DollarSign,
  Gauge,
  Command,
  ArrowUpRight,
  PanelRight,
  X,
} from "lucide-react";
import { type Msg, type Source, type ChatSession, loadSessions, saveSession } from "../lib/sessions";
import { api } from "../lib/api";

export const Route = createFileRoute("/chat")({
  validateSearch: (search: Record<string, unknown>) => ({
    session: typeof search.session === "string" ? search.session : undefined,
  }),
  component: ChatPage,
  head: () => ({
    meta: [
      { title: "Neural Chat — FrugalRoute" },
      { name: "description", content: "Chat with hybrid AI routing across local and cloud models." },
    ],
  }),
});

const SRC_META = {
  local: {
    icon: Zap,
    label: "Local",
    tone: "text-primary",
    ring: "ring-primary/40",
    bg: "bg-primary/10",
    border: "border-primary/40",
    glow: "glow-red",
  },
  remote: {
    icon: Cloud,
    label: "Remote",
    tone: "text-accent",
    ring: "ring-accent/40",
    bg: "bg-accent/10",
    border: "border-accent/40",
    glow: "glow-blue",
  },
  cache: {
    icon: Brain,
    label: "Cache",
    tone: "text-emerald-300",
    ring: "ring-emerald-400/40",
    bg: "bg-emerald-400/10",
    border: "border-emerald-400/40",
    glow: "",
  },
} as const;

const SOURCE_MAP: Record<string, Source> = {
  local: "local",
  remote: "remote",
  cache: "cache",
  triage_local: "local",
  triage_block: "local",
  semantic_cache: "cache",
  ollama: "local",
  fireworks: "remote",
};

function normalizeSource(raw: string): Source {
  return SOURCE_MAP[raw] ?? (raw.includes("remote") ? "remote" : raw.includes("cache") ? "cache" : "local");
}

function modelLabel(source: Source): string {
  return source === "cache" ? "Semantic Cache" : source === "remote" ? "Fireworks" : "Local Model";
}

function routeReason(source: Source, routeP?: number, confidence?: number): string {
  if (source === "cache") return "Semantic cache hit · embedding similarity match, zero token cost.";
  if (source === "remote")
    return `Escalated to cloud · local confidence below the 0.55 threshold${
      typeof routeP === "number" ? ` · P(remote)=${routeP}` : ""
    }.`;
  return `Kept on the local node · ${
    typeof confidence === "number"
      ? `confidence ${Math.round(confidence * 100)}% cleared the threshold`
      : "handled below the complexity threshold"
  }, no cloud tokens spent.`;
}

export default function ChatPage() {
  const { session: sessionParam } = Route.useSearch();

  const [sessionId] = useState(() => sessionParam ?? crypto.randomUUID());
  const [messages, setMessages] = useState<Msg[]>(() => {
    if (sessionParam) {
      const found = loadSessions().find((s) => s.id === sessionParam);
      if (found) return found.messages;
    }
    return [];
  });
  const [input, setInput] = useState("");
  const [thinking, setThinking] = useState<Source | null>(null);
  const [stats, setStats] = useState({ dollars: 0, tokens: 0, queries: 0 });
  const [inspectorOpen, setInspectorOpen] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);
  const taRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, thinking]);

  // Persist session so the sidebar "Recent" dropdown can reload it
  useEffect(() => {
    if (messages.length === 0) return;
    const firstUser = messages.find((m) => m.role === "user");
    saveSession({
      id: sessionId,
      title: firstUser ? firstUser.text.slice(0, 40) + (firstUser.text.length > 40 ? "…" : "") : "New Chat",
      ts: Date.now(),
      messages,
    } as ChatSession);
  }, [messages, sessionId]);

  async function send(text?: string) {
    const q = (text ?? input).trim();
    if (!q || thinking) return;
    setInput("");
    setMessages((m) => [...m, { id: crypto.randomUUID(), role: "user", text: q }]);
    setThinking("local"); // optimistic; corrected once the router responds

    try {
      const res = await fetch(api("/api/route"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: q }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();

      const source = normalizeSource(String(data.source ?? "local"));
      const remoteTokens = data.remote_tokens ?? 0;
      const tokensSaved = data.tokens_saved ?? 0;

      setThinking(source);
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: data.answer || "(no answer returned)",
          source,
          model: modelLabel(source),
          ms: data.latency_ms ?? 0,
          tokens: remoteTokens,
          cost: remoteTokens * 0.0000015,
          saved: tokensSaved * 0.000002,
          reason: routeReason(source, data.route_p, data.confidence),
          confidence: typeof data.confidence === "number" ? data.confidence : undefined,
        },
      ]);
      setStats((s) => ({
        dollars: +(s.dollars + tokensSaved * 0.000002).toFixed(4),
        tokens: s.tokens + remoteTokens,
        queries: s.queries + 1,
      }));
    } catch (err) {
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: `Could not reach the FrugalRoute backend. Make sure the server is running on port 8000.\n\n\`${String(err)}\``,
          source: "local",
          model: "Error",
          ms: 0,
        },
      ]);
    } finally {
      setThinking(null);
    }
  }

  const lastAssistant = useMemo(
    () => [...messages].reverse().find((m) => m.role === "assistant"),
    [messages],
  );

  return (
    <div className="relative flex h-screen flex-col overflow-hidden">
      {/* Ambient grid backdrop */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.35]"
        style={{
          backgroundImage:
            "linear-gradient(to right, oklch(1 0 0 / 0.04) 1px, transparent 1px), linear-gradient(to bottom, oklch(1 0 0 / 0.04) 1px, transparent 1px)",
          backgroundSize: "56px 56px",
          maskImage: "radial-gradient(ellipse at top, black 40%, transparent 90%)",
        }}
      />
      <div
        aria-hidden
        className="pointer-events-none absolute -top-40 left-1/2 h-96 w-[80%] -translate-x-1/2 rounded-full blur-3xl"
        style={{ background: "radial-gradient(closest-side, oklch(0.62 0.24 27 / 0.25), transparent)" }}
      />

      {/* Header */}
      <header className="glass-strong sticky top-0 z-20 flex items-center justify-between border-b border-border/60 px-6 py-4">
        <div className="flex items-center gap-4">
          <div className="relative grid h-10 w-10 place-items-center rounded-xl bg-white/5 ring-1 ring-white/10">
            <Cpu className="h-5 w-5 text-primary" />
            <span className="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full bg-emerald-400 ring-2 ring-background" />
          </div>
          <h1 className="truncate text-lg font-semibold tracking-tight">Neural Chat</h1>
        </div>
        <div className="flex items-center gap-2">
          {stats.queries > 0 && (
            <div className="hidden items-center gap-2 md:flex">
              <MetricChip icon={DollarSign} label="Saved" value={`$${stats.dollars.toFixed(2)}`} tone="primary" />
              <MetricChip icon={Activity} label="Paid tok" value={stats.tokens.toLocaleString()} tone="accent" />
              <MetricChip icon={Gauge} label="Queries" value={String(stats.queries)} tone="emerald" />
            </div>
          )}
          <button
            onClick={() => setInspectorOpen((v) => !v)}
            title={inspectorOpen ? "Hide info" : "Show info"}
            className={`grid h-10 w-10 shrink-0 place-items-center rounded-xl transition-colors ${
              inspectorOpen
                ? "bg-primary/15 text-primary ring-1 ring-primary/40"
                : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
            }`}
          >
            <PanelRight className="h-4 w-4" />
          </button>
        </div>
      </header>

      {/* Body */}
      <div className="relative z-10 flex flex-1 min-h-0">
        {/* Messages column */}
        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto flex max-w-3xl flex-col gap-6 px-4 py-8 md:px-8">
            {messages.length === 0 && !thinking && <EmptyState onPick={(p) => send(p)} />}
            {messages.map((m) =>
              m.role === "user" ? <UserBubble key={m.id} text={m.text} /> : <AssistantBubble key={m.id} msg={m} />,
            )}
            {thinking && <RoutingIndicator source={thinking} />}
            <div ref={endRef} />
          </div>
        </div>

        {/* Info panel — hidden by default, toggled from the header */}
        {inspectorOpen && (
          <aside className="w-80 shrink-0 overflow-y-auto border-l border-border/60 p-4">
            <RouteInspector last={lastAssistant} onClose={() => setInspectorOpen(false)} />
          </aside>
        )}
      </div>

      {/* Composer — reserve the Route Inspector width on xl so it centers on the same column as the messages */}
      <div className={`relative z-10 border-t border-border/60 bg-background/60 p-4 backdrop-blur-xl md:p-6 ${inspectorOpen ? "xl:pr-80" : ""}`}>
        <div className="mx-auto max-w-3xl">
          <div className="glass-strong group relative flex items-end gap-2 rounded-2xl p-2 ring-1 ring-transparent transition-all focus-within:ring-primary/40 focus-within:glow-red">
            <button className="grid h-10 w-10 shrink-0 place-items-center rounded-xl text-muted-foreground transition-colors hover:bg-white/5 hover:text-foreground">
              <Paperclip className="h-4 w-4" />
            </button>
            <textarea
              ref={taRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  send();
                }
              }}
              rows={1}
              disabled={!!thinking}
              placeholder="Ask anything — FrugalRoute picks the cheapest capable model…"
              className="min-h-[40px] max-h-40 flex-1 resize-none bg-transparent px-2 py-2.5 text-sm outline-none placeholder:text-muted-foreground disabled:opacity-50"
            />
            <div className="flex items-center gap-1">
              <span className="hidden items-center gap-1 rounded-md border border-border/60 bg-white/5 px-2 py-1 font-mono-tech text-[10px] text-muted-foreground md:inline-flex">
                <Command className="h-3 w-3" /> ⏎
              </span>
              <button
                onClick={() => send()}
                disabled={!input.trim() || !!thinking}
                className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-primary text-primary-foreground glow-red transition-transform hover:scale-105 disabled:opacity-40 disabled:hover:scale-100"
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
          </div>
          <div className="mt-2 flex items-center justify-between px-1">
            <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
              Local-first · threshold 0.55
            </div>
            <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
              Enter to send · Shift+Enter newline
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ---------- pieces ---------- */

function MetricChip({
  icon: Icon,
  label,
  value,
  tone,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: string;
  tone: "primary" | "accent" | "emerald";
}) {
  const toneMap = {
    primary: "text-primary",
    accent: "text-accent",
    emerald: "text-emerald-300",
  } as const;
  return (
    <div className="glass flex items-center gap-2.5 rounded-xl px-3 py-2">
      <Icon className={`h-3.5 w-3.5 ${toneMap[tone]}`} />
      <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">{label}</div>
      <div className={`font-mono-tech text-xs font-bold ${toneMap[tone]}`}>{value}</div>
    </div>
  );
}

// Client-side fallback pool — instant, varied on each load even if the
// backend suggestion endpoint is slow or unavailable.
const FALLBACK_POOL = [
  "What is the current price of AMD stock?",
  "Translate 'Good morning, how are you?' to French.",
  "What is 47 times 89?",
  "Summarize what photosynthesis is in one sentence.",
  "Who wrote the novel 1984?",
  "What is the capital of Australia?",
  "Extract the total from: 'Total due: $1,240.55'",
  "What's the weather in Tokyo right now?",
  "Explain in one line why the sky is blue.",
  "What is the square root of 2025?",
  "Translate 'thank you very much' to Spanish.",
  "Who painted the Mona Lisa?",
];

const SUGGEST_ICONS = [Zap, Sparkles, Brain, Cloud] as const;

function sample<T>(arr: T[], n: number): T[] {
  return [...arr].sort(() => Math.random() - 0.5).slice(0, n);
}

function EmptyState({ onPick }: { onPick: (p: string) => void }) {
  const [suggestions, setSuggestions] = useState<string[]>(() => sample(FALLBACK_POOL, 4));
  const [loading, setLoading] = useState(false);

  const generate = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(api("/api/suggestions?n=4"));
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data.suggestions) && data.suggestions.length) {
          setSuggestions(data.suggestions.slice(0, 4));
          return;
        }
      }
      setSuggestions(sample(FALLBACK_POOL, 4));
    } catch {
      setSuggestions(sample(FALLBACK_POOL, 4));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    generate();
  }, [generate]);

  return (
    <div className="flex flex-col items-center gap-8 py-12 text-center">
      <div className="grid h-14 w-14 place-items-center rounded-2xl bg-white/5 ring-1 ring-white/10">
        <Sparkles className="h-6 w-6 text-primary" />
      </div>
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">Ask anything</h2>
        <p className="max-w-md text-sm text-muted-foreground">
          Routed to your local model or the cloud — whichever is cheaper and capable.
        </p>
      </div>

      <div className="w-full">
        <div className="mb-2 flex items-center justify-between px-1">
          <span className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
            Suggested {loading && "· generating…"}
          </span>
          <button
            onClick={generate}
            disabled={loading}
            className="inline-flex items-center gap-1.5 rounded-lg px-2 py-1 font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground hover:text-foreground disabled:opacity-50"
          >
            <RefreshCw className={`h-3 w-3 ${loading ? "animate-spin" : ""}`} />
            Shuffle
          </button>
        </div>
        <div className="grid w-full grid-cols-1 gap-2.5 sm:grid-cols-2">
          {suggestions.map((prompt, i) => {
            const Icon = SUGGEST_ICONS[i % SUGGEST_ICONS.length];
            return (
              <button
                key={`${i}-${prompt}`}
                onClick={() => onPick(prompt)}
                className="glass group flex items-center gap-3 rounded-xl p-4 text-left transition-colors hover:bg-white/[0.04]"
              >
                <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-white/5 text-muted-foreground transition-colors group-hover:text-primary">
                  <Icon className="h-4 w-4" />
                </div>
                <span className="line-clamp-2 min-w-0 flex-1 text-sm text-muted-foreground transition-colors group-hover:text-foreground">
                  {prompt}
                </span>
                <ArrowUpRight className="h-3.5 w-3.5 shrink-0 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function UserBubble({ text }: { text: string }) {
  return (
    <div className="flex items-start justify-end gap-3">
      <div className="max-w-[80%] rounded-2xl rounded-br-md border border-primary/40 bg-primary/[0.08] px-4 py-3 text-sm leading-relaxed shadow-[0_0_24px_-8px_oklch(0.62_0.24_27_/_0.5)]">
        {text}
      </div>
      <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-white/5 font-mono-tech text-xs font-bold ring-1 ring-white/10">
        YOU
      </div>
    </div>
  );
}

function AssistantBubble({ msg }: { msg: Msg }) {
  const meta = SRC_META[(msg.source ?? "local") as Source];
  const Icon = meta.icon;
  return (
    <div className="group flex items-start gap-3">
      <div className={`grid h-8 w-8 shrink-0 place-items-center rounded-lg ${meta.bg} ${meta.tone} ring-1 ${meta.ring}`}>
        <Icon className="h-4 w-4" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="mb-1.5 flex items-center gap-2">
          <span className={`font-mono-tech text-[10px] uppercase tracking-widest ${meta.tone}`}>
            {meta.label} · {msg.model}
          </span>
          <span className="h-1 w-1 rounded-full bg-muted-foreground/50" />
          <span className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
            {msg.ms}ms
          </span>
          {typeof msg.tokens === "number" && msg.tokens > 0 && (
            <>
              <span className="h-1 w-1 rounded-full bg-muted-foreground/50" />
              <span className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
                {msg.tokens} tok
              </span>
            </>
          )}
        </div>
        <div className={`glass rounded-2xl rounded-tl-md border ${meta.border} px-4 py-3 text-sm leading-relaxed`}>
          <div className="whitespace-pre-wrap">{msg.text}</div>
        </div>
        <div className="mt-2 flex items-center gap-1 opacity-60 transition-opacity group-hover:opacity-100">
          <IconBtn title="Copy" onClick={() => navigator.clipboard?.writeText(msg.text)}>
            <Copy className="h-3 w-3" />
          </IconBtn>
          <IconBtn title="Regenerate"><RefreshCw className="h-3 w-3" /></IconBtn>
          <IconBtn title="Good"><ThumbsUp className="h-3 w-3" /></IconBtn>
          <IconBtn title="Bad"><ThumbsDown className="h-3 w-3" /></IconBtn>
        </div>
      </div>
    </div>
  );
}

function IconBtn({ children, title, onClick }: { children: React.ReactNode; title: string; onClick?: () => void }) {
  return (
    <button
      title={title}
      onClick={onClick}
      className="grid h-7 w-7 place-items-center rounded-md text-muted-foreground transition-colors hover:bg-white/5 hover:text-foreground"
    >
      {children}
    </button>
  );
}

function RoutingIndicator({ source }: { source: Source }) {
  const meta = SRC_META[source];
  const Icon = meta.icon;
  return (
    <div className="flex items-start gap-3">
      <div className={`grid h-8 w-8 shrink-0 place-items-center rounded-lg ${meta.bg} ${meta.tone} ring-1 ${meta.ring}`}>
        <Icon className="h-4 w-4" />
      </div>
      <div className={`glass rounded-2xl rounded-tl-md border ${meta.border} px-4 py-3`}>
        <div className="flex items-center gap-3">
          <div className="flex gap-1">
            <span className={`h-1.5 w-1.5 rounded-full ${meta.bg} animate-pulse-dot`} style={{ animationDelay: "0ms" }} />
            <span className={`h-1.5 w-1.5 rounded-full ${meta.bg} animate-pulse-dot`} style={{ animationDelay: "200ms" }} />
            <span className={`h-1.5 w-1.5 rounded-full ${meta.bg} animate-pulse-dot`} style={{ animationDelay: "400ms" }} />
          </div>
          <span className={`font-mono-tech text-[11px] uppercase tracking-widest ${meta.tone}`}>
            Routing…
          </span>
        </div>
      </div>
    </div>
  );
}

function RouteInspector({ last, onClose }: { last?: Msg; onClose?: () => void }) {
  return (
    <div className="sticky top-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="font-mono-tech text-[10px] uppercase tracking-[0.25em] text-muted-foreground">Info</div>
        {onClose && (
          <button
            onClick={onClose}
            title="Hide"
            className="grid h-6 w-6 place-items-center rounded-md text-muted-foreground transition-colors hover:bg-white/5 hover:text-foreground"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      {!last ? (
        <div className="glass rounded-2xl p-5 text-center">
          <div className="mx-auto mb-3 grid h-10 w-10 place-items-center rounded-xl bg-white/5">
            <Activity className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="text-sm font-medium">No routing yet</div>
          <div className="mt-1 text-xs text-muted-foreground">
            Send a message to see the router's decision breakdown.
          </div>
        </div>
      ) : (
        <>
          <DecisionCard msg={last} />
          <StatCard label="Latency" value={`${last.ms}ms`} bar={Math.min(100, ((last.ms ?? 0) / 8000) * 100)} tone="accent" />
          <StatCard
            label="Paid Tokens"
            value={String(last.tokens ?? 0)}
            bar={Math.min(100, ((last.tokens ?? 0) / 800) * 100)}
            tone="primary"
          />
          <StatCard
            label="Confidence"
            value={typeof last.confidence === "number" ? `${Math.round(last.confidence * 100)}%` : "n/a"}
            bar={(last.confidence ?? 0) * 100}
            tone="emerald"
          />
          <div className="glass rounded-2xl p-4">
            <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
              Why this route?
            </div>
            <div className="mt-2 text-xs leading-relaxed">{last.reason}</div>
          </div>
        </>
      )}
    </div>
  );
}

function DecisionCard({ msg }: { msg: Msg }) {
  const meta = SRC_META[(msg.source ?? "local") as Source];
  const Icon = meta.icon;
  return (
    <div className={`glass relative overflow-hidden rounded-2xl border ${meta.border} p-4`}>
      <div
        aria-hidden
        className="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full blur-2xl"
        style={{
          background:
            msg.source === "local"
              ? "oklch(0.62 0.24 27 / 0.35)"
              : msg.source === "remote"
              ? "oklch(0.68 0.16 232 / 0.35)"
              : "oklch(0.75 0.14 160 / 0.3)",
        }}
      />
      <div className="relative flex items-center gap-3">
        <div className={`grid h-11 w-11 place-items-center rounded-xl ${meta.bg} ${meta.tone} ring-1 ${meta.ring}`}>
          <Icon className="h-5 w-5" />
        </div>
        <div className="min-w-0">
          <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
            Routed to
          </div>
          <div className={`text-sm font-bold ${meta.tone}`}>{meta.label.toUpperCase()}</div>
          <div className="truncate text-[11px] text-muted-foreground">{msg.model}</div>
        </div>
      </div>
      {msg.source !== "remote" && (
        <div className="relative mt-3 flex items-center justify-between border-t border-border/60 pt-3">
          <span className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">Cloud cost</span>
          <span className="font-mono-tech text-sm font-bold text-emerald-300">$0.00 · free</span>
        </div>
      )}
    </div>
  );
}

function StatCard({
  label,
  value,
  bar,
  tone,
}: {
  label: string;
  value: string;
  bar: number;
  tone: "primary" | "accent" | "emerald";
}) {
  const toneMap = {
    primary: { text: "text-primary", bg: "bg-primary" },
    accent: { text: "text-accent", bg: "bg-accent" },
    emerald: { text: "text-emerald-300", bg: "bg-emerald-400" },
  } as const;
  const t = toneMap[tone];
  return (
    <div className="glass rounded-2xl p-4">
      <div className="flex items-center justify-between">
        <span className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">{label}</span>
        <span className={`font-mono-tech text-sm font-bold ${t.text}`}>{value}</span>
      </div>
      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-white/5">
        <div className={`h-full ${t.bg} transition-all duration-500`} style={{ width: `${bar}%` }} />
      </div>
    </div>
  );
}
