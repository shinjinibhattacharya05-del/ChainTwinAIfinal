import os
from backend.services.geo import label

def ask_llm(question, docs, hazards_text, ranking, alts, key=None):
    """Returns (answer, source) on success or (None, error_message). No offline fallback."""
    key = key or os.getenv("ANTHROPIC_API_KEY")
    if not key: return None, "No API key set. Paste your Anthropic API key in the sidebar to enable AI answers."
    ev = "\n".join(f"[{i+1}] {d[0]} ({d[1]}): {d[2]}" for i, (_, d) in enumerate(docs))
    facts = (f"Hazards: {hazards_text}\nSupplier ranking: " + ", ".join(f"{k}:{v['score']}" for k, v in ranking)
             + "\nRoutes: " + " | ".join(f"{a['name']}: {label(a['path'])}, {a['hrs']}h, ₹{a['cost_L']}L, risk {a['level']}, blocked={a['blocked']}" for a in alts))
    try:
        import anthropic
        model = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
        r = anthropic.Anthropic(api_key=key).messages.create(model=model, max_tokens=800, messages=[{"role": "user", "content":
            "You are a supply-chain decision assistant. Use ONLY the facts and evidence below and cite evidence as [n]. "
            "Structure the answer as: WHAT happened, WHAT happens if we do nothing, WHAT to consider and WHY.\n"
            f"FACTS:\n{facts}\nEVIDENCE:\n{ev}\nQUESTION: {question}"}])
        return r.content[0].text, f"Claude ({model})"
    except Exception as e:
        return None, f"LLM call failed: {str(e)[:200]}"
