"""Production wiring with LangGraph (requires `pip install langgraph`).

The agentic decision graph (Edge-Cloud Pareto-Router):

  ingest -> triage --(block/local-answer)--> account -> END
               +---> cache --(hit)----------> account -> END
                       +---> route -> local -> gate --(confident)--> account -> END
                                                  +--(unsure)------> remote -> account -> END

run.py falls back to engine.py automatically if langgraph isn't installed.
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END
import nodes


class S(TypedDict, total=False):
    id: str           # task identifier — passed through to results.jsonl
    task: str
    augmented_task: str
    category: str
    candidate: str
    answer: str
    source: str
    confidence: float
    confident: bool
    route_p: float
    remote_tokens: int
    tokens_saved: int
    done: bool
    skip_local: bool
    force_local: bool
    gold: str         # gold label (eval harness only — not present at scoring time)


def build_graph(cache, policy):
    g = StateGraph(S)
    g.add_node("ingest", nodes.ingest)
    g.add_node("triage", nodes.triage_node)
    g.add_node("cache", lambda s: nodes.cache_lookup(s, cache))
    g.add_node("route", nodes.route)
    g.add_node("local", lambda s: nodes.local(s, policy))
    g.add_node("gate", nodes.gate)
    g.add_node("remote", nodes.remote)
    g.add_node("account", lambda s: nodes.account(s, cache, policy))

    g.set_entry_point("ingest")
    g.add_edge("ingest", "triage")
    g.add_conditional_edges("triage", lambda s: "account" if s.get("done") else "cache")
    g.add_conditional_edges("cache", lambda s: "account" if s.get("done") else "route")
    g.add_edge("route", "local")
    g.add_edge("local", "gate")
    g.add_conditional_edges("gate", lambda s: "account" if s.get("done") else "remote")
    g.add_edge("remote", "account")
    g.add_edge("account", END)
    return g.compile()
