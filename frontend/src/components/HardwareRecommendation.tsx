import { useEffect, useRef, useState } from "react";
import { Cpu, Download, Check, Loader2 } from "lucide-react";
import { api } from "@/lib/api";

/**
 * Shown in the welcome modal's first slide.
 *
 * IMPORTANT: this reads REAL hardware from FrugalRoute's own backend
 * (/api/health + /api/models/catalog), which calls hwselect.py — real
 * nvidia-smi/rocm-smi + RAM detection, not a browser-side guess. There is no
 * reliable way for a website to read a REMOTE VISITOR's own PC hardware over
 * HTTP (browsers don't expose that, for good privacy reasons) — what CAN be
 * detected honestly is the hardware of the machine actually running Ollama,
 * which is exactly the machine that matters for "download this model now",
 * since that's where it will actually run.
 */

interface CatalogModel {
  tag: string;
  label: string;
  params: string;
  size_mb: number;
  accuracy: number;
  remote_tokens: number;
  note?: string;
  fits_gpu: boolean;
  installed: boolean;
}

interface HealthInfo {
  gpu_vram_mb: number;
  ram_gb: number;
  recommended_model: string | null;
  ollama_online: boolean;
  local_model: string;
}

type PullStatus = "idle" | "pulling" | "selecting" | "done" | "error";

export function HardwareRecommendation() {
  const [health, setHealth] = useState<HealthInfo | null>(null);
  const [models, setModels] = useState<CatalogModel[]>([]);
  const [selectedTag, setSelectedTag] = useState<string | null>(null);
  const [pullStatus, setPullStatus] = useState<PullStatus>("idle");
  const [pullPercent, setPullPercent] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      fetch(api("/api/health")).then((r) => r.json()),
      fetch(api("/api/models/catalog")).then((r) => r.json()),
    ])
      .then(([healthData, catalogData]) => {
        if (cancelled) return;
        setHealth(healthData);
        setModels(catalogData.models ?? []);
        setSelectedTag(healthData.recommended_model ?? null);
      })
      .catch(() => {
        if (!cancelled) setError("Could not reach FrugalRoute's backend to detect hardware.");
      });
    return () => {
      cancelled = true;
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  const selected = models.find((m) => m.tag === selectedTag);
  const recommended = models.find((m) => m.tag === health?.recommended_model);

  const startPull = async (tag: string) => {
    setPullStatus("pulling");
    setPullPercent(0);
    setError(null);
    try {
      await fetch(api("/api/models/pull"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: tag }),
      });
    } catch {
      setPullStatus("error");
      setError("Could not start the download — backend unreachable.");
      return;
    }

    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(api(`/api/models/pull/status?model=${encodeURIComponent(tag)}`));
        const s = await res.json();
        setPullPercent(s.percent ?? 0);
        if (s.error) {
          setPullStatus("error");
          setError(s.error);
          if (pollRef.current) clearInterval(pollRef.current);
        } else if (s.done) {
          if (pollRef.current) clearInterval(pollRef.current);
          setPullStatus("selecting");
          await fetch(api("/api/models/select"), {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ model: tag }),
          });
          setModels((prev) => prev.map((m) => (m.tag === tag ? { ...m, installed: true } : m)));
          setPullStatus("done");
        }
      } catch {
        // transient poll failure — keep trying until the interval is cleared
      }
    }, 1500);
  };

  if (error && !health) {
    return (
      <div className="glass mt-4 rounded-xl p-4 text-xs text-red-400">{error}</div>
    );
  }

  if (!health || !models.length) {
    return (
      <div className="glass mt-4 rounded-xl p-4 text-xs text-muted-foreground">
        Detecting hardware…
      </div>
    );
  }

  return (
    <div className="glass mt-4 rounded-xl p-4">
      <div className="flex items-center gap-2 font-mono-tech text-[10px] uppercase tracking-widest text-primary text-glow-red">
        <Cpu className="h-3 w-3" />
        Detected by FrugalRoute's backend
      </div>

      <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-muted-foreground">
        <div>
          <div className="text-foreground font-semibold">
            {(health.gpu_vram_mb / 1024).toFixed(1)} GB
          </div>
          GPU VRAM (real, via rocm-smi/nvidia-smi)
        </div>
        <div>
          <div className="text-foreground font-semibold">{health.ram_gb} GB</div>
          System RAM
        </div>
      </div>

      <div className="mt-1.5 text-[10px] leading-relaxed text-muted-foreground/70">
        This is the real hardware of the machine currently running Ollama for this deployment —
        not a browser guess. It's the machine that will actually run whatever model you pick below.
      </div>

      <div className="mt-3 border-t border-white/5 pt-3">
        <div className="text-sm">
          Recommended:{" "}
          <span className="text-foreground font-semibold">{recommended?.label ?? health.recommended_model}</span>
        </div>
        {recommended?.note && <div className="mt-1 text-xs text-muted-foreground">{recommended.note}</div>}

        <select
          value={selectedTag ?? ""}
          onChange={(e) => setSelectedTag(e.target.value)}
          className="mt-2 w-full rounded-lg border border-white/10 bg-black/30 px-2 py-1.5 text-xs text-foreground"
        >
          {models.map((m) => (
            <option key={m.tag} value={m.tag}>
              {m.label} — {(m.size_mb / 1024).toFixed(1)}GB — {(m.accuracy * 100).toFixed(1)}% accuracy
              {m.installed ? " — installed" : ""}
              {!m.fits_gpu ? " — may not fit this GPU" : ""}
            </option>
          ))}
        </select>

        {selected && (
          <div className="mt-3">
            {selected.installed && pullStatus === "idle" ? (
              <div className="inline-flex items-center gap-2 rounded-lg bg-emerald-400/10 px-3 py-1.5 text-xs text-emerald-400">
                <Check className="h-3 w-3" />
                Already installed
              </div>
            ) : pullStatus === "pulling" ? (
              <div className="inline-flex items-center gap-2 rounded-lg bg-white/5 px-3 py-1.5 text-xs text-foreground">
                <Loader2 className="h-3 w-3 animate-spin" />
                Downloading… {pullPercent}%
              </div>
            ) : pullStatus === "selecting" ? (
              <div className="inline-flex items-center gap-2 rounded-lg bg-white/5 px-3 py-1.5 text-xs text-foreground">
                <Loader2 className="h-3 w-3 animate-spin" />
                Setting as active model…
              </div>
            ) : pullStatus === "done" ? (
              <div className="inline-flex items-center gap-2 rounded-lg bg-emerald-400/10 px-3 py-1.5 text-xs text-emerald-400">
                <Check className="h-3 w-3" />
                Installed &amp; active
              </div>
            ) : (
              <button
                onClick={() => startPull(selected.tag)}
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-3 py-1.5 text-xs font-semibold text-primary-foreground glow-red hover:scale-[1.02] transition-transform"
              >
                <Download className="h-3 w-3" />
                Download now
              </button>
            )}
            {pullStatus === "error" && (
              <div className="mt-1.5 text-xs text-red-400">{error}</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
