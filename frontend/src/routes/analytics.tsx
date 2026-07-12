import { createFileRoute } from "@tanstack/react-router";
import { Area, AreaChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Zap, Cloud, Brain } from "lucide-react";

export const Route = createFileRoute("/analytics")({
  component: Analytics,
  head: () => ({ meta: [{ title: "Analytics — FrugalRoute" }, { name: "description", content: "Deep routing metrics, cost savings and query breakdown." }] }),
});

const days = Array.from({ length: 30 }, (_, i) => {
  const cloudOnly = 120 + Math.sin(i / 3) * 30 + i * 4;
  const frugal = cloudOnly * (0.28 + Math.random() * 0.08);
  return { day: `D${i + 1}`, cloudOnly: Math.round(cloudOnly), frugal: Math.round(frugal) };
});

const routing = [
  { name: "Local", value: 52, color: "var(--amd)" },
  { name: "Remote", value: 43, color: "var(--electric)" },
  { name: "Cache", value: 5, color: "oklch(0.78 0.15 160)" },
];

const queries = [
  { t: "14:22:08", p: "Extract total from invoice PDF text…", cat: "Extraction", src: "local", ms: 11 },
  { t: "14:21:41", p: "Draft board memo on Q3 pipeline risk…", cat: "Long-form", src: "remote", ms: 512 },
  { t: "14:21:12", p: "What is 18% of 4,320?", cat: "Math", src: "local", ms: 7 },
  { t: "14:20:55", p: "Classify support ticket sentiment…", cat: "Classification", src: "local", ms: 9 },
  { t: "14:20:31", p: "Summarize this 40-page contract…", cat: "Summarization", src: "remote", ms: 890 },
  { t: "14:20:02", p: "Extract total from invoice PDF text…", cat: "Extraction", src: "cache", ms: 3 },
  { t: "14:19:44", p: "Translate paragraph to German", cat: "Translation", src: "local", ms: 14 },
  { t: "14:19:20", p: "Explain quantum entanglement to a 10yo…", cat: "Reasoning", src: "remote", ms: 610 },
] as const;

function Analytics() {
  return (
    <div className="w-full px-4 py-8 md:px-6">
      <header className="mb-8">
        <div className="font-mono-tech text-[11px] uppercase tracking-widest text-muted-foreground">System</div>
        <h1 className="text-3xl font-bold md:text-4xl">Analytics</h1>
        <p className="mt-1 text-muted-foreground">Where routing is winning, and where the leaks are.</p>
      </header>

      <div className="grid gap-5 lg:grid-cols-3">
        {[
          { k: "30D SAVINGS", v: "$4,281", sub: "vs 100% cloud", accent: "text-primary text-glow-red" },
          { k: "REQUESTS", v: "182,431", sub: "42 rps peak", accent: "" },
          { k: "AVG COST / REQ", v: "$0.00021", sub: "-73% MoM", accent: "text-accent text-glow-blue" },
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
              <p className="text-xs text-muted-foreground">Cloud-only baseline vs FrugalRoute (USD, daily)</p>
            </div>
            <div className="flex gap-3 font-mono-tech text-[10px] uppercase tracking-widest">
              <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-accent" /> Cloud only</span>
              <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-primary" /> FrugalRoute</span>
            </div>
          </div>
          <div className="h-72">
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
                <Area type="monotone" dataKey="cloudOnly" stroke="var(--electric)" strokeWidth={2} fill="url(#cloud)" />
                <Area type="monotone" dataKey="frugal" stroke="var(--amd)" strokeWidth={2} fill="url(#frugal)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Donut */}
        <div className="glass rounded-2xl p-6">
          <h2 className="text-lg font-semibold">Routing Distribution</h2>
          <p className="text-xs text-muted-foreground">Last 24 hours</p>
          <div className="relative mt-2 h-56">
            <ResponsiveContainer>
              <PieChart>
                <Pie data={routing} dataKey="value" innerRadius={60} outerRadius={90} paddingAngle={3} stroke="none">
                  {routing.map((r) => <Cell key={r.name} fill={r.color} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "rgba(20,20,28,0.9)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="pointer-events-none absolute inset-0 grid place-items-center">
              <div className="text-center">
                <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">TOTAL</div>
                <div className="font-mono-tech text-2xl font-bold">100%</div>
              </div>
            </div>
          </div>
          <div className="mt-2 space-y-2">
            {routing.map((r) => (
              <div key={r.name} className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full" style={{ background: r.color }} />
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
          <span className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">Live · streaming</span>
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
              {queries.map((q, i) => (
                <tr key={i} className="hover:bg-white/[0.02]">
                  <td className="px-6 py-3 font-mono-tech text-xs text-muted-foreground">{q.t}</td>
                  <td className="px-6 py-3">{q.p}</td>
                  <td className="px-6 py-3"><span className="rounded-md bg-white/5 px-2 py-0.5 text-xs">{q.cat}</span></td>
                  <td className="px-6 py-3"><SourceTag src={q.src} /></td>
                  <td className="px-6 py-3 text-right font-mono-tech text-xs">{q.ms}ms</td>
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
  const s = map[src];
  return (
    <span className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 font-mono-tech text-[10px] uppercase tracking-widest ${s.cls}`}>
      {s.icon}{s.label}
    </span>
  );
}
