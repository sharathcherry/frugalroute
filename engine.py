"""Dependency-free runner that mirrors the LangGraph graph. Lets you test the
full pipeline (triage -> cache -> route -> local -> gate -> remote) with stdlib
only, before installing langgraph or wiring real models. run.py uses the real
graph when langgraph is installed and falls back to this otherwise.
"""
import nodes


def run_task(task_id, task, cache, policy):
    """Run the full pipeline for one task. Returns the final state dict."""
    state = {
        "id": task_id,
        "task": task,
        "done": False,
        "remote_tokens": 0,
        "tokens_saved": 0,
    }
    nodes.ingest(state)
    nodes.triage_node(state)                      # Phase 1
    if state.get("done"):
        return nodes.account(state, cache, policy)
    nodes.cache_lookup(state, cache)
    if state.get("done"):
        return nodes.account(state, cache, policy)
    nodes.route(state)                            # Phase 2 (predictive)
    nodes.local(state, policy)
    nodes.gate(state)                             # Phase 2 (cascade + calibration)
    if not state.get("done"):
        nodes.remote(state)                       # Phase 3 (compress + paid call)
    return nodes.account(state, cache, policy)
