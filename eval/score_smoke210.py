"""
Scores out/smoke210.jsonl against eval/tasks_smoke200.jsonl's gold labels,
using the EXACT same correctness function as eval/score.py (kept identical on
purpose so these numbers are apples-to-apples with the earlier gemma4/qwen3
benchmark numbers already in the README).
"""
import json
import os
import re

REPO = "/root/frugalroute"


def normalize(s):
    s = str(s).lower().replace(",", "")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def correct(gold, answer):
    g, a = normalize(gold), normalize(answer)
    if not g:
        return None
    return g == a or g in a or a in g


def main():
    tasks = [json.loads(l) for l in open(os.path.join(REPO, "eval", "tasks_smoke200.jsonl")) if l.strip()]
    recs = [json.loads(l) for l in open(os.path.join(REPO, "out", "smoke210.jsonl")) if l.strip()]
    recs_by_id = {r["id"]: r for r in recs}

    n = len(tasks)
    n_correct = 0
    local_hits = 0
    remote_tokens = 0
    cat_stats = {}
    wrong_examples = []

    for i, t in enumerate(tasks):
        r = recs_by_id.get(str(i), {})
        ans = r.get("answer", "")
        src = r.get("source", "")
        rt = r.get("remote_tokens", 0) or 0
        remote_tokens += rt
        if src in ("local", "triage_local", "cache"):
            local_hits += 1
        ok = correct(t["gold"], ans)
        cat = t.get("category", "?")
        cs = cat_stats.setdefault(cat, [0, 0])
        cs[1] += 1
        if ok:
            n_correct += 1
            cs[0] += 1
        else:
            wrong_examples.append({
                "task": t["task"], "gold": t["gold"], "answer": ans[:120],
                "source": src, "category": cat,
            })

    result = {
        "tag": "smoke210_gemma4_12b",
        "n": n,
        "accuracy": round(n_correct / n, 4) if n else 0,
        "local_hit_rate_pct": round(100 * local_hits / n, 1) if n else 0,
        "remote_tokens": remote_tokens,
        "per_category": {
            c: {"correct": v[0], "total": v[1], "acc": round(v[0] / v[1], 3)}
            for c, v in sorted(cat_stats.items())
        },
    }
    print(json.dumps(result, indent=2))
    with open(os.path.join(REPO, "out", "smoke210.score.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n=== {len(wrong_examples)} WRONG ANSWERS (for honest review) ===")
    for w in wrong_examples:
        print(f"[{w['category']:>14}] [{w['source']:>6}] Q: {w['task'][:70]}")
        print(f"{'':22}gold={w['gold']!r}  got={w['answer']!r}")


if __name__ == "__main__":
    main()
