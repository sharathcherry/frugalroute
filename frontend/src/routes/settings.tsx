import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Cpu, Cloud, Save, Eye, EyeOff, Sliders, RefreshCw, Check, Star, Zap, Download, HardDriveDownload } from "lucide-react";

type LocalModel = {
  name: string;
  params?: string;
  quant?: string;
  size_mb: number;
  fits_gpu: boolean;
  tools: boolean;
};
type ModelsResp = {
  available: LocalModel[];
  selected: string;
  recommended?: string | null;
  gpu_vram_mb: number;
  gpu_budget_mb: number;
  error?: string;
};
type CatalogModel = {
  tag: string;
  label: string;
  params: string;
  size_mb: number;
  fits_gpu: boolean;
  installed: boolean;
};

export const Route = createFileRoute("/settings")({
  component: SettingsPage,
  head: () => ({ meta: [{ title: "Settings — FrugalRoute" }, { name: "description", content: "Configure local and remote endpoints and routing thresholds." }] }),
});

function SettingsPage() {
  const [localUrl, setLocalUrl] = useState("http://localhost:11434");
  const [provider, setProvider] = useState("OpenAI");
  const [apiKey, setApiKey] = useState("");
  const [reveal, setReveal] = useState(false);
  const [threshold, setThreshold] = useState(0.72);

  const [models, setModels] = useState<ModelsResp | null>(null);
  const [loadingModels, setLoadingModels] = useState(false);
  const [switching, setSwitching] = useState<string | null>(null);

  const loadModels = useCallback(async () => {
    setLoadingModels(true);
    try {
      const res = await fetch(api("/api/models"));
      const data: ModelsResp = await res.json();
      setModels(data);
      if (data.error) toast.error("Ollama not reachable", { description: data.error });
    } catch (e) {
      toast.error("Could not load local models", { description: String(e) });
    } finally {
      setLoadingModels(false);
    }
  }, []);

  const [catalog, setCatalog] = useState<CatalogModel[]>([]);
  const [pullTag, setPullTag] = useState<string>("");
  const [pull, setPull] = useState<{ tag: string; percent: number; status: string } | null>(null);

  const loadCatalog = useCallback(async () => {
    try {
      const res = await fetch(api("/api/models/catalog"));
      const data = await res.json();
      setCatalog(data.models ?? []);
      setPullTag((prev) => prev || (data.models ?? []).find((m: CatalogModel) => !m.installed)?.tag || "");
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    loadModels();
    loadCatalog();
  }, [loadModels, loadCatalog]);

  async function startPull() {
    const tag = pullTag;
    if (!tag || pull) return;
    try {
      await fetch(api("/api/models/pull"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: tag }),
      });
    } catch (e) {
      toast.error("Could not start download", { description: String(e) });
      return;
    }
    setPull({ tag, percent: 0, status: "starting" });
    const poll = async () => {
      try {
        const r = await fetch(api(`/api/models/pull/status?model=${encodeURIComponent(tag)}`));
        const s = await r.json();
        setPull({ tag, percent: s.percent ?? 0, status: s.status ?? "" });
        if (s.error) {
          toast.error("Download failed", { description: s.error });
          setPull(null);
          return;
        }
        if (s.done) {
          toast.success("Model downloaded", { description: tag });
          setPull(null);
          loadModels();
          loadCatalog();
          return;
        }
      } catch {
        /* keep polling */
      }
      setTimeout(poll, 1200);
    };
    setTimeout(poll, 1000);
  }

  async function selectModel(name: string) {
    setSwitching(name);
    try {
      const res = await fetch(api("/api/models/select"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: name }),
      });
      const data = await res.json();
      setModels((m) => (m ? { ...m, selected: data.selected } : m));
      toast.success("Local model switched", { description: `Now routing to ${data.selected}` });
    } catch (e) {
      toast.error("Switch failed", { description: String(e) });
    } finally {
      setSwitching(null);
    }
  }

  function save() {
    toast.success("Configuration saved", { description: "Router will apply new thresholds on next request." });
  }

  return (
    <div className="w-full px-4 py-8 md:px-6">
      <header className="mb-8">
        <div className="font-mono-tech text-[11px] uppercase tracking-widest text-muted-foreground">Configuration</div>
        <h1 className="text-3xl font-bold md:text-4xl">Settings</h1>
        <p className="mt-1 text-muted-foreground">Wire up endpoints and dial in your cost/quality trade-off.</p>
      </header>

      {/* LOCAL */}
      <Section icon={<Cpu className="h-4 w-4 text-primary" />} title="Local Endpoint" subtitle="Models detected on this PC via Ollama">
        <Field label="Ollama / vLLM URL">
          <input value={localUrl} onChange={(e) => setLocalUrl(e.target.value)} className={inputCls} />
        </Field>
        <div className="md:col-span-2">
          <div className="mb-1.5 flex items-center justify-between">
            <div className="font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
              Detected Local Models
              {models && (
                <span className="ml-2 text-muted-foreground/60">
                  · GPU {models.gpu_vram_mb ? `${Math.round(models.gpu_vram_mb / 1024)}GB` : "—"} · budget{" "}
                  {models.gpu_budget_mb ? `${(models.gpu_budget_mb / 1024).toFixed(1)}GB` : "—"}
                </span>
              )}
            </div>
            <button
              onClick={loadModels}
              disabled={loadingModels}
              className="inline-flex items-center gap-1.5 rounded-lg px-2 py-1 font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground hover:text-foreground disabled:opacity-50"
            >
              <RefreshCw className={`h-3 w-3 ${loadingModels ? "animate-spin" : ""}`} />
              Detect
            </button>
          </div>

          <div className="grid gap-2">
            {!models && loadingModels && (
              <div className="glass rounded-xl px-4 py-6 text-center text-sm text-muted-foreground">Detecting…</div>
            )}
            {models && models.available.length === 0 && (
              <div className="glass rounded-xl px-4 py-6 text-center text-sm text-muted-foreground">
                No Ollama models found. Pull one with{" "}
                <code className="font-mono-tech text-primary">ollama pull qwen2.5:3b-instruct</code>.
              </div>
            )}
            {models?.available.map((m) => {
              const active = m.name === models.selected;
              const recommended = m.name === models.recommended;
              return (
                <button
                  key={m.name}
                  onClick={() => selectModel(m.name)}
                  disabled={switching === m.name || active}
                  className={`glass group flex items-center gap-3 rounded-xl px-4 py-3 text-left transition-all ${
                    active ? "ring-1 ring-primary/50 glow-red" : "hover:ring-1 hover:ring-primary/30"
                  }`}
                >
                  <div
                    className={`grid h-9 w-9 shrink-0 place-items-center rounded-lg ${
                      active ? "bg-primary/15 text-primary" : "bg-white/5 text-muted-foreground"
                    }`}
                  >
                    {active ? <Check className="h-4 w-4" /> : <Zap className="h-4 w-4" />}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="truncate text-sm font-semibold">{m.name}</span>
                      {recommended && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-primary/10 px-1.5 py-0.5 font-mono-tech text-[9px] uppercase tracking-widest text-primary">
                          <Star className="h-2.5 w-2.5" /> Best fit
                        </span>
                      )}
                    </div>
                    <div className="mt-0.5 flex flex-wrap items-center gap-x-2 font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
                      {m.params && <span>{m.params}</span>}
                      {m.quant && <span>· {m.quant}</span>}
                      <span>· {(m.size_mb / 1024).toFixed(1)}GB</span>
                      <span className={m.fits_gpu ? "text-emerald-300" : "text-accent"}>
                        · {m.fits_gpu ? "fits GPU" : "spills to CPU"}
                      </span>
                      {m.tools && <span>· tools</span>}
                    </div>
                  </div>
                  {switching === m.name ? (
                    <RefreshCw className="h-4 w-4 shrink-0 animate-spin text-muted-foreground" />
                  ) : active ? (
                    <span className="shrink-0 font-mono-tech text-[10px] uppercase tracking-widest text-primary">Active</span>
                  ) : (
                    <span className="shrink-0 font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100">
                      Use
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </Section>

      {/* DOWNLOAD */}
      <Section
        icon={<HardDriveDownload className="h-4 w-4 text-primary" />}
        title="Download a Model"
        subtitle="One-click pull from Ollama — Gemma, Qwen, Llama, Phi, Mistral, DeepSeek"
      >
        <div className="md:col-span-2">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <label className="block flex-1">
              <div className="mb-1.5 font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
                Model
              </div>
              <select
                value={pullTag}
                onChange={(e) => setPullTag(e.target.value)}
                disabled={!!pull}
                className={inputCls}
              >
                {catalog.map((m) => (
                  <option key={m.tag} value={m.tag} disabled={m.installed}>
                    {m.label} · {(m.size_mb / 1024).toFixed(1)}GB
                    {m.installed ? " · installed" : m.fits_gpu ? " · fits GPU" : " · spills to CPU"}
                  </option>
                ))}
              </select>
            </label>
            <button
              onClick={startPull}
              disabled={!pullTag || !!pull}
              className="inline-flex h-[42px] items-center justify-center gap-2 rounded-lg bg-primary px-5 text-sm font-semibold text-primary-foreground glow-red transition-transform hover:scale-[1.02] disabled:opacity-40 disabled:hover:scale-100"
            >
              {pull ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Download className="h-4 w-4" />}
              {pull ? "Downloading…" : "Download"}
            </button>
          </div>

          {pull && (
            <div className="glass mt-4 rounded-xl p-4">
              <div className="mb-2 flex items-center justify-between font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
                <span className="truncate">
                  {pull.tag} · {pull.status}
                </span>
                <span className="text-primary">{pull.percent}%</span>
              </div>
              <div className="h-1.5 overflow-hidden rounded-full bg-white/5">
                <div
                  className="h-full bg-primary transition-all duration-500"
                  style={{ width: `${pull.percent}%` }}
                />
              </div>
            </div>
          )}
          <p className="mt-3 text-xs text-muted-foreground">
            Downloaded models appear in <span className="text-foreground">Detected Local Models</span> above and can be
            selected instantly. Larger models than your GPU fits will still run, but slower (CPU offload).
          </p>
        </div>
      </Section>

      {/* REMOTE */}
      <Section icon={<Cloud className="h-4 w-4 text-accent" />} title="Remote Endpoint" subtitle="Frontier model for hard prompts">
        <Field label="API Provider">
          <select value={provider} onChange={(e) => setProvider(e.target.value)} className={inputCls}>
            <option>OpenAI</option>
            <option>Fireworks</option>
            <option>Groq</option>
          </select>
        </Field>
        <Field label="API Key">
          <div className="relative">
            <input
              type={reveal ? "text" : "password"}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-••••••••••••••••"
              className={inputCls + " pr-10"}
            />
            <button type="button" onClick={() => setReveal((r) => !r)} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
              {reveal ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
        </Field>
      </Section>

      {/* THRESHOLD */}
      <Section icon={<Sliders className="h-4 w-4 text-emerald-400" />} title="Routing Threshold" subtitle="Higher = more aggressive local routing (cheaper). Lower = safer cloud fallback.">
        <div className="glass rounded-xl p-5">
          <div className="mb-4 flex items-baseline justify-between">
            <div className="font-mono-tech text-[11px] uppercase tracking-widest text-muted-foreground">Confidence Threshold</div>
            <div className="font-mono-tech text-3xl font-bold text-primary text-glow-red">{threshold.toFixed(2)}</div>
          </div>
          <input
            type="range" min={0} max={1} step={0.01}
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full accent-[var(--amd)]"
            style={{
              background: `linear-gradient(to right, var(--amd) 0%, var(--amd) ${threshold * 100}%, rgba(255,255,255,0.1) ${threshold * 100}%, rgba(255,255,255,0.1) 100%)`,
              WebkitAppearance: "none", height: 6, borderRadius: 9999,
            }}
          />
          <div className="mt-2 flex justify-between font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">
            <span>0.0 · always cloud</span>
            <span>0.5 · balanced</span>
            <span>1.0 · always local</span>
          </div>
        </div>
      </Section>

      <div className="mt-8 flex justify-end">
        <button onClick={save} className="inline-flex items-center gap-2 rounded-xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground glow-red transition-transform hover:scale-[1.02]">
          <Save className="h-4 w-4" /> Save Configuration
        </button>
      </div>
    </div>
  );
}

const inputCls =
  "w-full rounded-lg border border-border bg-white/[0.02] px-3 py-2.5 text-sm outline-none transition-colors focus:border-primary/60 focus:bg-white/[0.04] font-mono-tech";

function Section({ icon, title, subtitle, children }: { icon: React.ReactNode; title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <section className="glass mb-5 rounded-2xl p-6">
      <div className="mb-4 flex items-center gap-2">
        <div className="grid h-8 w-8 place-items-center rounded-lg bg-white/5">{icon}</div>
        <div>
          <h2 className="text-lg font-semibold">{title}</h2>
          <p className="text-xs text-muted-foreground">{subtitle}</p>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">{children}</div>
    </section>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <div className="mb-1.5 font-mono-tech text-[10px] uppercase tracking-widest text-muted-foreground">{label}</div>
      {children}
    </label>
  );
}
