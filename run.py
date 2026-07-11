"""Entry point — two modes:

  1. BATCH (submission mode, used by scoring harness):
       python run.py --input /data/tasks.jsonl --output /data/out/results.jsonl
     Reads {id, task} lines, writes {id, answer, source, remote_tokens} lines.

  2. DASHBOARD mode (dev / demo):
       python run.py [tasks_file]          # default: eval/tasks.sample.jsonl
     Prints a token report and writes dashboard/data.js for dashboard/index.html.

Environment:
  MOCK=0   — real local + remote models (default in Dockerfile)
  MOCK=1   — canned inference; verifies pipeline logic with zero deps
"""
import argparse
import json
import os
import sys

from cache import SemanticCache
from policy import OnlinePolicy

REPO = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Task loading — preserves 'id' field (required by scoring harness)
# ---------------------------------------------------------------------------

def load_tasks(path):
    """Return list of dicts with at least {id, task}. Supports both
    {id, task} format (submission) and bare {task} format (legacy dev tasks)."""
    rows = []
    for i, line in enumerate(open(path, encoding="utf-8")):
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        # Normalise field name: 'task' or 'prompt'
        text = obj.get("task") or obj.get("prompt") or ""
        task_id = obj.get("id", str(i))
        rows.append({"id": task_id, "task": text, "_raw": obj})
    return rows


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def _build_runner(cache, policy):
    """Return (engine_name, run_fn) — LangGraph if available, else fallback."""
    try:
        from graph import build_graph
        app = build_graph(cache, policy)

        def run(item):
            state = {
                "id": item["id"],
                "task": item["task"],
                "done": False,
                "remote_tokens": 0,
                "tokens_saved": 0,
            }
            return app.invoke(state)

        return "langgraph", run
    except Exception:
        import engine as eng

        def run(item):
            return eng.run_task(item["id"], item["task"], cache, policy)

        return "fallback-engine", run


def run_all(tasks, cache=None, policy=None):
    cache = cache or SemanticCache()
    policy = policy or OnlinePolicy()
    engine, run_fn = _build_runner(cache, policy)

    recs = []
    for item in tasks:
        r = run_fn(item)
        recs.append({
            "id": item["id"],
            "task": item["task"],
            "answer": r.get("answer", ""),
            "category": r.get("category"),
            "source": r.get("source"),
            "route_p": r.get("route_p"),
            "confidence": r.get("confidence"),
            "remote_tokens": r.get("remote_tokens", 0),
            "tokens_saved": r.get("tokens_saved", 0),
        })
    return engine, recs


# ---------------------------------------------------------------------------
# Aggregation (dashboard / reporting)
# ---------------------------------------------------------------------------

def aggregate(recs):
    mix, cat = {}, {}
    n = len(recs)
    total_remote = sum(x["remote_tokens"] for x in recs)
    total_saved = sum(x["tokens_saved"] for x in recs)
    free = sum(1 for x in recs if x["remote_tokens"] == 0)
    for x in recs:
        s = x["source"] or "?"
        mix[s] = mix.get(s, 0) + 1
        c = x["category"] or "?"
        cat.setdefault(c, {"local": 0, "remote": 0, "cache": 0, "other": 0})
        key = ("local" if s in ("local", "triage_local")
               else "remote" if s == "remote"
               else "cache" if s == "cache" else "other")
        cat[c][key] += 1
    return {
        "n": n, "remote_tokens": total_remote, "tokens_saved": total_saved,
        "free_pct": round(100 * free / n, 1) if n else 0,
        "escalate_pct": round(100 * mix.get("remote", 0) / n, 1) if n else 0,
        "cache_hits": mix.get("cache", 0), "mix": mix, "by_category": cat,
    }


# ---------------------------------------------------------------------------
# Output modes
# ---------------------------------------------------------------------------

def write_results_jsonl(recs, out_path):
    """Submission output — {id, answer, source, remote_tokens} per line."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps({
                "id": r["id"],
                "answer": r.get("answer", ""),
                "source": r.get("source", ""),
                "remote_tokens": r.get("remote_tokens", 0),
            }) + "\n")


def write_dashboard(engine, recs, agg):
    d = os.path.join(REPO, "dashboard")
    os.makedirs(d, exist_ok=True)
    payload = {"engine": engine, "records": recs, "agg": agg}
    with open(os.path.join(d, "data.js"), "w", encoding="utf-8") as f:
        f.write("window.DATA = " + json.dumps(payload, indent=2) + ";\n")


def print_report(engine, recs, agg):
    print(f"# FrugalRoute | engine={engine}\n")
    for x in recs:
        print(f"[{str(x['source']):12}] remote={x['remote_tokens']:4} "
              f"route_p={str(x['route_p']):4} conf={str(x['confidence']):4} "
              f"id={x['id']} {str(x['task'])[:40]}")
    print(f"\nremote_tokens={agg['remote_tokens']}  tokens_saved={agg['tokens_saved']}  "
          f"free%={agg['free_pct']}  escalate%={agg['escalate_pct']}  "
          f"cache_hits={agg['cache_hits']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="FrugalRoute — token-efficient LLM router")
    parser.add_argument("--input", "-i",
                        help="Input tasks JSONL (submission mode). "
                             "If omitted, runs eval/tasks.sample.jsonl in dashboard mode.")
    parser.add_argument("--output", "-o",
                        help="Output results JSONL path (submission mode). "
                             "Required when --input is given.")
    # Legacy positional: python run.py tasks.jsonl
    parser.add_argument("tasks_file", nargs="?", default=None,
                        help="(dev) Task file positional arg for dashboard mode.")
    args = parser.parse_args()

    # --- BATCH / SUBMISSION MODE ---
    if args.input:
        if not args.output:
            parser.error("--output is required when --input is specified")
        tasks = load_tasks(args.input)
        engine, recs = run_all(tasks)
        write_results_jsonl(recs, args.output)
        agg = aggregate(recs)
        print_report(engine, recs, agg)
        print(f"\nresults -> {args.output}  ({len(recs)} tasks, "
              f"remote_tokens={agg['remote_tokens']})")
        return

    # --- DASHBOARD / DEV MODE ---
    path = args.tasks_file or os.path.join(REPO, "eval", "tasks.sample.jsonl")
    tasks = load_tasks(path)
    engine, recs = run_all(tasks)
    agg = aggregate(recs)
    write_dashboard(engine, recs, agg)
    print_report(engine, recs, agg)
    print("dashboard -> open dashboard/index.html  (data.js written)")


if __name__ == "__main__":
    main()
