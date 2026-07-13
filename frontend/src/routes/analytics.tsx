import { useEffect, useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Area, AreaChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Zap, Cloud, Brain } from "lucide-react";
import { api } from "@/lib/api";

export const Route = createFileRoute("/analytics")({
  component: Analytics,
  head: () => ({ meta: [{ title: "Analytics — FrugalRoute" }, { name: "description", content: "Deep routing metrics, cost savings and query breakdown." }] }),
});

// All data on this page comes from GET /api/analytics, which aggregates the
// backend's real query log (server.py's _log_query / QUERY_LOG_PATH) — every
// number here reflects requests FrugalRoute has actually processed, not
// simulated or placeholder data.

type DailyPoint = { day: string; requests: number; actual_cost: number; cloud_only_cost: number };
type RoutingSlice = { name: string; value: number };
type RecentQuery = { ts: number; task_preview: string; category: string | null; source: string | null; latency_ms: number | null };

type AnalyticsData = {
  total_requests: number;
  avg_cost_per_request: number;
  total_savings: number;
  routing: RoutingSlice[];
  daily: DailyPoint[];
  recent_queries: RecentQuery[];
};

const ROUTING_COLOR: Record<string, string> = {
  Local: "var(--amd)",
  Remote: "var(--electric)",
  Cache: "oklch(0.78 0.15 160)",
};

function Analytics() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch(api("/api/analytics"))
      .then((r) => r.json())
      .then((d) => { if (!cancelled) setData(d); })
      .catch(() => { if (!cancelled) setError("Could not reach the backend for analytics data."); });
    return () => { cancelled = true; };
  }, []);

  if (error) {
    return (
      <div className="w-full px-4 py-8 md:px-6">
        <div className="glass rounded-2xl p-6 text-sm text-red-400">{error}</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="w-full px-4 py-8 md:px-6">
        <div className="glass rounded-2xl p-6 text-sm text-muted-foreground">Loading real analytics…</div>
      </div>
    );
  }

  if (data.total_requests === 0) {
    return (
      <div className="w-full px-4 py-8 md:px-6">
        <header className="mb-8">
          <div className="font-mono-tech text-[11px] uppercase tracking-widest text-muted-foreground">System</div>
          <h1 className="text-3xl font-bold md:text-4xl">Analytics</h1>
          <p className="mt-1 text-muted-foreground">Where routing is winning, and where the leaks are.</p>
        </header>
        <div className="glass rounded-2xl p-6 text-sm text-muted-foreground">
          No requests logged yet — this page fills in with real data as soon as FrugalRoute starts
          handling queries. Try asking something in Neural Chat, then come back here.
        </div>
      </div>
    );
  }

  const routing: RoutingSlice[] = data.routing.filter((r) => r.value > 0);
  const days = data.daily;

  return (
    <div className="w-full px-4 py-8 md:px-6">
      <header className="mb-8">
        <div className="font-mono-tech text-[11px] uppercase tracking-widest text-muted-foreground">System</div>
        <h1 className="text-3xl font-bold md:text-4xl">Analytics</h1>
        <p className="mt-1 text-muted-foreground">Where routing is winning, and where the leaks are.</p>
      </header>

      <div className="grid gap-5 lg:grid-cols-3">
        {[
          {
            k: "SAVINGS", v: `$${data.total_savings.toFixed(4)}`,
            sub: "vs 100% cloud (estimated)", accent: "text-primary text-glow-red",
          },
          { k: "REQUESTS", v: data.total_requests.toLocaleString(), sub: "all-time logged", accent: "" },
          {
            k: "AVG COST / REQ", v: `$${data.avg_cost_per_request.toFixed(6)}`,
            sub: "actual, not projected", accent: "text-accent text-glow-blue",
          },
        ].map((s) => (
          <div key={s.k} className="glass rounded-2xl p-6">
            <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">{s.k}</div>
            <div className={`mt-2 font-mono-tech text-3xl font-bold ${s.accent}`}>{s.v}</div>
            <div className="text-xs text-muted-foreground">{s.sub}</div>
          </div>
        ))}
      </div>

      {/* Cost chart */}
      <div className="mt-6 grid gap-5 lg:grid-cols-3">
        <div className="glass rounded-2xl p-6 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">API Cost Savings Over Time</h2>
              <p className="text-xs text-muted-foreground">
                Cloud-only estimate vs FrugalRoute actual (USD, daily — only days with real traffic appear)
              </p>
            </div>
            <div className="flex gap-3 font-mono-tech text-[10px] uppercase tracking-widest">
              <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-accent" /> Cloud only</span>
              <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-primary" /> FrugalRoute</span>
            </div>
          </div>
          <div className="h-72">
            {days.length === 0 ? (
              <div className="grid h-full place-items-center text-sm text-muted-foreground">
                Not enough daily data yet.
              </div>
            ) : (
              <ResponsiveContainer>
                <AreaChart data={days} margin={{ left: -20, right: 5, top: 5, bottom: 0 }}>
                  <defs>
                    <linearGradient id="cloud" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stopColor="var(--electric)" stopOpacity={0.4} />
                      <stop offset="100%" stopColor="var(--electric)" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="frugal" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stopColor="var(--amd)" stopOpacity={0.5} />
                      <stop offset="100%" stopColor="var(--amd)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="day" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: "rgba(20,20,28,0.9)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 }} />
                  <Area type="monotone" dataKey="cloud_only_cost" name="Cloud only" stroke="var(--electric)" strokeWidth={2} fill="url(#cloud)" />
                  <Area type="monotone" dataKey="actual_cost" name="FrugalRoute" stroke="var(--amd)" strokeWidth={2} fill="url(#frugal)" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Donut */}
        <div className="glass rounded-2xl p-6">
          <h2 className="text-lg font-semibold">Routing Distribution</h2>
          <p className="text-xs text-muted-foreground">All logged requests</p>
          <div className="relative mt-2 h-56">
            <ResponsiveContainer>
              <PieChart>
                <Pie data={routing} dataKey="value" innerRadius={60} outerRadius={90} paddingAngle={3} stroke="none">
                  {routing.map((r) => <Cell key={r.name} fill={ROUTING_COLOR[r.name] ?? "var(--amd)"} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "rgba(20,20,28,0.9)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="pointer-events-none absolute inset-0 grid place-items-center">
              <div className="text-center">
                <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">TOTAL</div>
                <div className="font-mono-tech text-2xl font-bold">{data.total_requests}</div>
              </div>
            </div>
          </div>
          <div className="mt-2 space-y-2">
            {routing.map((r) => (
              <div key={r.name} className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full" style={{ background: ROUTING_COLOR[r.name] ?? "var(--amd)" }} />
                  {r.name}
                </span>
                <span className="font-mono-tech">{r.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="mt-6 glass rounded-2xl">
        <div className="flex items-center justify-between border-b border-border/60 px-6 py-4">
          <h2 className="text-lg font-semibold">Recent Queries</h2>
          <span className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">Real · logged</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
                <th className="px-6 py-3">Timestamp</th>
                <th className="px-6 py-3">Prompt</th>
                <th className="px-6 py-3">Category</th>
                <th className="px-6 py-3">Source</th>
                <th className="px-6 py-3 text-right">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {data.recent_queries.map((q, i) => (
                <tr key={i} className="hover:bg-white/[0.02]">
                  <td className="px-6 py-3 font-mono-tech text-xs text-muted-foreground">
                    {new Date(q.ts * 1000).toLocaleTimeString()}
                  </td>
                  <td className="px-6 py-3">{q.task_preview}</td>
                  <td className="px-6 py-3"><span className="rounded-md bg-white/5 px-2 py-0.5 text-xs">{q.category ?? "—"}</span></td>
                  <td className="px-6 py-3"><SourceTag src={(q.source as "local" | "remote" | "cache") ?? "local"} /></td>
                  <td className="px-6 py-3 text-right font-mono-tech text-xs">{q.latency_ms ?? "—"}ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function SourceTag({ src }: { src: "local" | "remote" | "cache" }) {
  const map = {
    local: { icon: <Zap className="h-3 w-3" />, label: "Local", cls: "text-primary border-primary/40 bg-primary/10" },
    remote: { icon: <Cloud className="h-3 w-3" />, label: "Remote", cls: "text-accent border-accent/40 bg-accent/10" },
    cache: { icon: <Brain className="h-3 w-3" />, label: "Cache", cls: "text-emerald-300 border-emerald-400/40 bg-emerald-400/10" },
  } as const;
  const s = map[src] ?? map.local;
  return (
    <span className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 font-mono-tech text-[10px] uppercase tracking-widest ${s.cls}`}>
      {s.icon}{s.label}
    </span>
  );
}
