/**
 * Best-effort CLIENT-SIDE hardware detection for recommending which local
 * FrugalRoute model to `ollama pull`.
 *
 * IMPORTANT LIMITATION: browsers do not expose real CPU/GPU model names or
 * VRAM size for privacy reasons. We can only get approximate signals:
 *   - navigator.deviceMemory   -> rounded-down RAM estimate in GB (Chrome/Edge
 *                                 only; undefined on Firefox/Safari)
 *   - navigator.hardwareConcurrency -> logical CPU core count (widely supported)
 *   - WebGL UNMASKED_RENDERER_WEBGL -> a GPU renderer string, when the browser
 *     doesn't block it for fingerprinting protection. On many Windows laptops
 *     this reports the INTEGRATED gpu (e.g. "ANGLE (Intel, Intel(R) UHD
 *     Graphics ...)") even when a much stronger discrete GPU is installed,
 *     because WebGL context creation defaults to the power-saving adapter
 *     unless the browser/OS is explicitly set to prefer the discrete GPU.
 *     We treat this kind of string as AMBIGUOUS, not as "this machine is
 *     weak" — see guessGpuTier below.
 *
 * This is a real, honest heuristic — not a substitute for actually reading
 * VRAM (which only server-side tools like nvidia-smi/rocm-smi can do; see
 * hwselect.py for that half of the story, used when Ollama runs on a server
 * you control). Here we're recommending a model for the visitor's OWN
 * machine, so we work with what a browser can actually tell us — and because
 * that's inherently unreliable, the UI also lets the user override the
 * recommendation manually (see HardwareRecommendation.tsx).
 */

export type ModelTier = "low" | "mid" | "high" | "flagship";
type GpuTierGuess = ModelTier | "unknown";

export interface ModelRec {
  tag: string;
  label: string;
  approxVramGb: number;
  tier: ModelTier;
  note?: string;
}

// Real models this project has actually pulled and benchmarked (eval/benchmark.json).
// approxVramGb = measured `ollama list` disk size, a solid proxy for resident VRAM at Q4.
// Ordered ascending within each tier so the override dropdown reads sensibly.
export const MODEL_CATALOG: ModelRec[] = [
  { tag: "qwen3:4b", label: "Qwen3 4B", approxVramGb: 2.5, tier: "low" },
  { tag: "gemma4:e2b", label: "Gemma4 E2B", approxVramGb: 7.2, tier: "low" },
  { tag: "qwen3:8b", label: "Qwen3 8B", approxVramGb: 5.2, tier: "mid" },
  { tag: "gemma4:e4b", label: "Gemma4 E4B", approxVramGb: 9.6, tier: "mid" },
  {
    tag: "gemma4:12b",
    label: "Gemma4 12B",
    approxVramGb: 7.6,
    tier: "mid",
    note: "Best measured accuracy-per-GB in our benchmark sweep — recommended default.",
  },
  { tag: "qwen3:14b", label: "Qwen3 14B", approxVramGb: 9.3, tier: "high" },
  { tag: "gemma4:26b", label: "Gemma4 26B", approxVramGb: 17, tier: "high" },
  { tag: "qwen3:30b-a3b", label: "Qwen3 30B-A3B (MoE)", approxVramGb: 18, tier: "flagship" },
  { tag: "gemma4:31b", label: "Gemma4 31B", approxVramGb: 19, tier: "flagship" },
  { tag: "qwen3:32b", label: "Qwen3 32B", approxVramGb: 20, tier: "flagship" },
];

export interface DetectedHardware {
  ramGbEstimate: number | null; // null = browser wouldn't say (Firefox/Safari)
  cpuCores: number | null;
  gpuRenderer: string | null;
  gpuTierGuess: GpuTierGuess;
  supported: boolean; // false if we got basically nothing useful
}

function detectGpuRenderer(): string | null {
  try {
    const canvas = document.createElement("canvas");
    const gl = (canvas.getContext("webgl") ||
      canvas.getContext("experimental-webgl")) as WebGLRenderingContext | null;
    if (!gl) return null;
    const ext = gl.getExtension("WEBGL_debug_renderer_info");
    if (!ext) return null;
    const renderer = gl.getParameter(ext.UNMASKED_RENDERER_WEBGL);
    return typeof renderer === "string" ? renderer : null;
  } catch {
    return null;
  }
}

// Keyword-based GPU tier guess from the renderer string. Returns "unknown"
// (rather than guessing "low") for ambiguous/integrated-looking strings,
// since those are frequently reported even on machines with a much stronger
// discrete GPU that WebGL simply isn't hitting. Only returns a confident
// tier when the string names a specific, unambiguous discrete part.
function guessGpuTier(renderer: string | null): GpuTierGuess {
  if (!renderer) return "unknown";
  const r = renderer.toLowerCase();

  const flagship = ["rtx 40", "rtx 50", "rx 7900", "rx 7800", "instinct", "a100", "h100"];
  const high = ["rtx 30", "rtx 20", "rx 6800", "rx 6900", "radeon rx 6", "radeon rx 7"];
  const mid = ["gtx 16", "gtx 10", "rx 5", "rx 500", "radeon rx"];
  // Integrated/mobile parts — genuinely weak, safe to call "low".
  const low = ["uhd graphics", "iris", "vega 8", "vega 3", "mali", "adreno", "apple m1"];

  if (flagship.some((k) => r.includes(k))) return "flagship";
  if (high.some((k) => r.includes(k))) return "high";
  if (mid.some((k) => r.includes(k))) return "mid";
  if (low.some((k) => r.includes(k))) return "low";

  // Generic "ANGLE (...)" strings with no specific model named (common on
  // Windows Chrome when WebGL isn't running on the discrete GPU) — ambiguous.
  return "unknown";
}

export function detectHardware(): DetectedHardware {
  const nav = navigator as Navigator & { deviceMemory?: number };
  const ramGbEstimate = typeof nav.deviceMemory === "number" ? nav.deviceMemory : null;
  const cpuCores = typeof navigator.hardwareConcurrency === "number"
    ? navigator.hardwareConcurrency
    : null;
  const gpuRenderer = detectGpuRenderer();
  const gpuTierGuess = guessGpuTier(gpuRenderer);
  const supported = ramGbEstimate !== null || cpuCores !== null || gpuRenderer !== null;
  return { ramGbEstimate, cpuCores, gpuRenderer, gpuTierGuess, supported };
}

/**
 * Recommend a model tag given what we could detect. Deliberately conservative
 * and CPU-core-aware: when the GPU string is ambiguous (very common), we lean
 * on logical CPU core count as the tiebreaker instead of silently downgrading
 * to "low" — a 16+ core machine reporting a vague ANGLE string is far more
 * likely to be a capable desktop than a weak laptop.
 */
export function recommendModel(hw: DetectedHardware): ModelRec {
  const ram = hw.ramGbEstimate;
  const cores = hw.cpuCores;

  let tier: ModelTier;

  if (hw.gpuTierGuess !== "unknown") {
    // Confident, specific GPU match — trust it, but let a huge RAM/core count
    // bump one tier up (e.g. a flagship GPU we under-classified as "high").
    tier = hw.gpuTierGuess;
    if (tier !== "flagship" && ((ram ?? 0) >= 32 || (cores ?? 0) >= 24)) {
      const order: ModelTier[] = ["low", "mid", "high", "flagship"];
      tier = order[Math.min(order.indexOf(tier) + 1, order.length - 1)];
    }
  } else {
    // No usable GPU signal — fall back to CPU cores (a much more reliable
    // browser API) as a proxy for overall machine class, with RAM as a
    // secondary nudge when Chrome actually reports it.
    if ((cores ?? 0) >= 24) tier = "flagship";
    else if ((cores ?? 0) >= 16) tier = "high";
    else if ((cores ?? 0) >= 8) tier = "mid";
    else if (cores !== null) tier = "low";
    else tier = "mid"; // nothing usable at all — safest proven default

    if (ram !== null) {
      if (ram >= 32 && tier !== "flagship") {
        const order: ModelTier[] = ["low", "mid", "high", "flagship"];
        tier = order[Math.min(order.indexOf(tier) + 1, order.length - 1)];
      } else if (ram <= 4 && tier !== "low") {
        tier = "low";
      }
    }
  }

  const candidates = MODEL_CATALOG.filter((m) => m.tier === tier);
  return (
    candidates.find((m) => m.note) ??
    candidates[0] ??
    MODEL_CATALOG.find((m) => m.tag === "gemma4:12b")!
  );
}
