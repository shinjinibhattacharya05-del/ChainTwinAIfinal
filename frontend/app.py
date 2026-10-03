
import sys, os, time, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd, plotly.graph_objects as go, streamlit as st
from frontend import api, theme
from frontend.map_view import build_map

st.set_page_config("ChainTwin AI", "⛓️", layout="wide"); theme.apply(); ss = st.session_state
try: META = api.get("/api/meta"); S = api.get("/api/state")
except api.ApiError:
    st.error("Backend not reachable. Start it first:  `uvicorn backend.main:app --reload --port 8000`"); st.stop()
CITY = META["cities"]; lab = lambda p: " → ".join(CITY[c]["name"] for c in p); KEY = lambda: ss.get("api_key") or None
ss.setdefault("chat", [])

@st.fragment(run_every=2)
def tracker(key):
    d = api.get("/api/ships"); rows = []
    for s in d["ships"]:
        st_ = "✅ Delivered" if s["delivered"] else "🔴 Held" if s["hold"] else "🔵 Rerouted" if ("Re" in s["note"] or "Better" in s["note"]) else "🟢 In transit"
        rows.append({"Shipment": s["id"], "Supplier": s["supplier"], "Status": st_, "Route": lab(s["route"]), "Progress %": s["progress"], "Remaining km": s["remaining_km"], "ETA (sim h)": s["eta_h"], "Delay vs plan (h)": s["delay_h"], "Last change": s["note"]})
    a, b = st.columns([1, 1.25]); a.plotly_chart(build_map(META, d["hazards"], d["statuses"], ships=d["ships"], h=360), width="stretch", key=f"tm_{key}")
    b.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", column_config={"Progress %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d%%")})
    b.markdown("**Live change log**"); b.code("\n".join(d["log"][:7]) or "No changes yet – run a scan, change priorities or click Re-optimize.")

def evidence(ev, expanded=True):
    with st.expander("How did AI reach this decision? (retrieved evidence)", expanded=expanded):
        for i, e in enumerate(ev): st.markdown(f"**[{i+1}] {e['title']}** · {e['date']} · relevance `{e['score']:.0%}`  \n> {e['text']}")

def copilot(key):
    qs = ["Find the best alternate supplier", "What is the optimal route now?", "What happens if we wait?", "Why not Supplier C?"]; cols = st.columns(4); ask = None
    for i, q in enumerate(qs):
        if cols[i].button(q, key=f"{key}q{i}", width="stretch"): ask = q
    with st.form(f"form{key}", clear_on_submit=True):
        t = st.text_input("Ask ChainTwin AI (RAG over company documents)", placeholder="e.g. Which supplier can deliver 50,000 units in 5 days?")
        if st.form_submit_button("Ask") and t: ask = t
    if ask:
        with st.spinner("Retrieving evidence and asking the LLM…"): r = api.post("/api/copilot", {"question": ask}, key=KEY())
        st.error(r["error"]) if r["error"] else ss.chat.append(dict(q=ask, **r))
    if ss.chat:
        m = ss.chat[-1]; st.markdown(f"**Q:** {m['q']}"); st.markdown(m["answer"]); st.caption(f"Answered by: {m['source']}"); evidence(m["evidence"])
        if st.button("✅ Apply optimal routes to all shipments", key=f"{key}apply"): st.toast(f"{api.post('/api/respond')['changes']} shipment change(s) applied"); st.rerun()

def scan_and_respond(sel):
    with st.status("🛰 Satellite scan in progress…", expanded=True) as s:
        st.write("Fetching latest vs baseline imagery for 5 monitored zones…"); time.sleep(.5); r = api.post("/api/scan", {"events": sel})
        for z in r["zones"]: st.write(f"🔴 {z['zone']}: **{z['det']['type']}** detected ({z['det']['conf']:.0%}, {z['det']['area']}% area changed)" if z["det"] else f"⚪ {z['zone']}: no change"); time.sleep(.3)
        for t in ["Propagating impact through supply-chain graph…", "Retrieving evidence & ranking suppliers…", "Optimising routes (hazard-aware)…"]: st.write(t); time.sleep(.4)
        s.update(label=f"Scan complete – {len(r['hazards'])} hazard(s), {r['changes']} shipment change(s)", state="complete")
    st.rerun()

PAGES = ["Dashboard", "Satellite Detection", "AI Copilot (RAG)", "Route Optimizer", "Supplier Tracker", "Supplier Intelligence", "Simulations", "Rewind Engine", "Reports", "Settings"]
with st.sidebar:
    st.markdown("## ⛓️ CHAIN TWIN AI"); st.caption("From physical-world signal to traceable business decision.")
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.text_input("🔑 Anthropic API key", type="password", key="api_key", placeholder="sk-ant-...", help="Sent to the backend per request; never stored.")
    st.caption("🟢 Key set" if ss.get("api_key") else "🔴 Add an API key to enable AI answers")
    auto = st.toggle("Auto-reroute on detection", S["auto"])
    with st.expander("⚙️ Routing priorities", expanded=True):
        w = [st.slider("Speed", 0.0, 2.0, S["w"][0], .1), st.slider("Cost", 0.0, 2.0, S["w"][1], .1), st.slider("Safety", 0.0, 2.0, S["w"][2], .1)]
    if w != S["w"] or auto != S["auto"]:
        n = api.post("/api/priorities", {"w": w, "auto": auto})["changes"]; st.toast(f"{n} route(s) updated live") if n else None; S = api.get("/api/state")
    st.error("● Active disruption") if S["hazards"] else st.success("● All systems operational")
    if st.button("🔄 Reset everything", width="stretch"): api.post("/api/reset"); ss.chat = []; st.rerun()

if page == "Dashboard":
    st.title("Supply Chain Command Center"); st.caption("Real-time intelligence for disruption, risk and operational decisions.")
    c = st.columns([3, 1.2, 1]); sel = c[0].multiselect("Physical events to simulate (detected from satellite imagery)", META["events"], META["events"][:2])
    c[1].write(""); go_ = c[1].button("🛰 Scan & Respond", type="primary", width="stretch"); c[2].write("")
    if c[2].button("Clear hazards", width="stretch"): api.post("/api/hazards/clear"); st.rerun()
    if go_: scan_and_respond(sel)
    K, hz = S["kpis"], S["hazards"]; HS = META["hazard_styles"]
    if hz: st.markdown('<div class="banner"><b class="red">SUPPLY CHAIN DISRUPTION DETECTED</b><br>' + " · ".join(f"{HS[h['type']]['ic']} {h['type'].replace('_',' ').title()} – {h['name']} ({h['conf']:.0%})" for h in hz) + '<br><span class="lbl">Source: Satellite change detection · Severity HIGH</span></div>', unsafe_allow_html=True)
    k = st.columns(4); g = lambda x: "grn" if x["good"] else "red"
    theme.kpi(k[0], "Production risk", K["risk"]["v"], "Supplier A → Factory X", g(K["risk"])); theme.kpi(k[1], "Inventory remaining", K["inventory"]["v"], "Critical threshold: 7 days", "grn" if K["inventory"]["good"] else "org")
    theme.kpi(k[2], "Expected delay", K["delay"]["v"], "After actions" if K["mitigated"] else "If no action", g(K["delay"])); theme.kpi(k[3], "Financial exposure", K["exposure"]["v"], "Reduced from ₹50L" if K["mitigated"] else "Projected loss", g(K["exposure"]))
    if K["mitigated"]: st.markdown('<div class="ok"><b class="grn">Disruption contained.</b> Estimated loss reduced from ₹50L to ₹5L. Recovery time reduced from 10 days to 3 days.</div>', unsafe_allow_html=True)
    m, r = st.columns([2.2, 1])
    with m:
        o = st.columns(3); net, hzl, sat = o[0].toggle("Supply layer", True), o[1].toggle("Disaster layer", True), o[2].toggle("Satellite basemap", False)
        st.plotly_chart(build_map(META, hz, S["statuses"], routes=S["routes"] if hz else (), chosen=S["best"]["path"], sat=sat, show_net=net, show_hz=hzl), width="stretch")
        st.caption("🔴 Disrupted  🟠 At risk  🟢 Healthy  🔵 Alternate supplier · cyan = optimal Pune→Bangalore route")
    with r:
        top = S["ranking"][0]; st.markdown("**🎯 AI recommended action**")
        st.markdown(f'<div class="card"><div class="lbl">Switch to</div><div class="big cyn">{META["suppliers"][top["id"]]["name"]}</div><div class="lbl">Suitability {top["score"]}/100 · {top["hrs"]} h away</div></div>', unsafe_allow_html=True)
        st.write(""); st.markdown("**Route options (Pune → Bangalore)**"); st.dataframe(pd.DataFrame([{"Route": a["name"], "h": a["hrs"], "₹L": a["cost_L"], "Risk": a["level"]} for a in S["routes"]]), hide_index=True, width="stretch"); st.caption("Best: " + lab(S["best"]["path"]))
        if st.button("✅ Apply plan to shipments", width="stretch"): st.toast(f"{api.post('/api/respond')['changes']} change(s) applied"); st.rerun()
    t1, t2, t3 = st.tabs(["📡 Live supplier tracker", "🤖 AI Copilot (LLM + RAG)", "🛰 Latest detections"])
    with t1: tracker("dash")
    with t2: copilot("dash")
    with t3:
        for z in S["zones"]: st.write(f"**{z['zone']}** – " + (f"{z['det']['type']} {z['det']['conf']:.0%}" if z["det"] else "no change"))
        if not S["zones"]: st.info("Run 'Scan & Respond' to analyse satellite imagery.")
    st.markdown("**How the decision was made:** " + "  →  ".join(f"`{i+1} {p}`" for i, p in enumerate(META["pipeline"])))

elif page == "Satellite Detection":
    st.title("Satellite Disaster Detection"); st.caption("Before/after change detection → spectral classification → geolocated hazard. Demo tiles are synthetic; upload real imagery below.")
    sel = st.multiselect("Inject events into demo imagery", META["events"], META["events"][:2])
    if st.button("🛰 Run satellite scan", type="primary"): scan_and_respond(sel)
    for z in api.get("/api/scan/images") if S["zones"] else []:
        a = st.columns([1, 1, 1, 1.3]); a[0].image(base64.b64decode(z["before"]), caption=f"{z['zone']} – baseline"); a[1].image(base64.b64decode(z["after"]), caption="Latest pass"); a[2].image(base64.b64decode(z["mask"]), caption="Change mask")
        a[3].markdown(f"### {'🔴 ' + z['det']['type'].replace('_',' ').upper() if z['det'] else '⚪ No change'}" + (f"\nConfidence **{z['det']['conf']:.0%}** · area changed **{z['det']['area']}%**  \nLat/Lon `{z['lat']:.2f}, {z['lon']:.2f}`" if z["det"] else ""))
    st.divider(); st.subheader("Bring your own imagery"); u = st.columns(3); f1, f2 = u[0].file_uploader("Before image", ["png", "jpg"]), u[1].file_uploader("After image", ["png", "jpg"])
    city = u[2].selectbox("Location", list(CITY), format_func=lambda c: CITY[c]["name"]); rad = u[2].number_input("Impact radius (km)", 5, 100, 25)
    if f1 and f2:
        b = lambda f: base64.b64encode(f.getvalue()).decode(); det = api.post("/api/scan/upload", {"before": b(f1), "after": b(f2), "city": city, "radius": rad})["detection"]
        if det:
            st.success(f"Detected {det['type']} ({det['conf']:.0%})")
            if st.button("Add to hazard layer"): api.post("/api/scan/upload", {"before": b(f1), "after": b(f2), "city": city, "radius": rad, "apply": True}); st.rerun()
        else: st.info("No significant change detected.")

elif page == "AI Copilot (RAG)":
    st.title("AI Copilot"); st.caption("Retrieval over company documents + LLM reasoning for alternate suppliers and routes."); copilot("page")
    with st.expander("Knowledge base"): st.dataframe(pd.DataFrame(META["docs"], columns=["Title", "Date", "Content"]), hide_index=True, width="stretch")

elif page == "Route Optimizer":
    st.title("Route Optimizer"); c = st.columns(3); keys = list(CITY); fmt = lambda k: CITY[k]["name"]
    o = c[0].selectbox("Origin", keys, keys.index("PUN"), format_func=fmt); d = c[1].selectbox("Destination", keys, keys.index("BLR"), format_func=fmt); c[2].selectbox("Cargo", ["Semiconductor X"])
    R = api.get("/api/routes", origin=o, dest=d)
    if not R["routes"]: st.error("No viable route under current hazards.")
    else:
        b = R["best"]; st.success(f"Optimal for your priorities: {lab(b['path'])} · {b['hrs']} h · ₹{b['cost_L']}L · risk {b['level']}")
        st.dataframe(pd.DataFrame([{"Route": a["name"], "Path": lab(a["path"]), "km": a["km"], "Hours": a["hrs"], "Cost ₹L": a["cost_L"], "Risk": f"{a['level']} ({a['risk']})"} for a in R["routes"]]), hide_index=True, width="stretch")
        pick = st.selectbox("Assign route to shipment", ["SH-B", "SH-C", "SH-A"])
        if st.button("Assign optimal route to shipment"): api.post(f"/api/ships/{pick}/assign", {"path": b["path"]}); st.toast("Route assigned – see Supplier Tracker")
        st.plotly_chart(build_map(META, S["hazards"], S["statuses"], routes=R["routes"], chosen=b["path"]), width="stretch")

elif page == "Supplier Tracker":
    st.title("Live Supplier Tracker"); st.caption("Updates every 2s (1 s = 3 simulated minutes). Hazard or priority changes reroute shipments in real time."); c = st.columns(3)
    if c[0].button("🔁 Re-optimize all routes"): st.toast(f"{api.post('/api/respond')['changes']} route(s) changed")
    if c[1].button("⏩ Fast-forward 6 h"): api.post("/api/fast-forward"); st.rerun()
    tracker("page")

elif page == "Supplier Intelligence":
    st.title("AI Supplier Intelligence"); c = st.columns(5); c[0].text_input("Component", "Semiconductor X"); c[1].text_input("Quantity", "50,000 units"); c[2].text_input("Delivery", "Within 5 days"); c[3].text_input("Budget", "₹15,00,000"); c[4].text_input("Destination", "Factory X – Bangalore")
    with st.expander("Criteria weights"):
        cc = st.columns(6); wts = {k: cc[i].slider(k, 0, 10, 5) for i, k in enumerate(["Cost", "Delivery", "Capacity", "Reliability", "Risk", "Quality"])}
    if st.button("Find Optimal Supplier", type="primary"):
        with st.spinner("Analyzing supplier documents, performance, capacity, pricing, logistics risk and disruption status…"): rk = api.post("/api/suppliers/rank", {"weights": wts})
        st.dataframe(pd.DataFrame([{"Supplier": v["name"], "City": v["city"], "Status": v["status"], "Suitability": v["score"], "Hours to Bangalore": v["hrs"], "Route": lab(v["path"])} for v in rk]), hide_index=True, width="stretch")
        fig = go.Figure([go.Bar(name=v["name"], x=list(v["f"]), y=list(v["f"].values())) for v in rk if v["f"]]); fig.update_layout(barmode="group", paper_bgcolor="#070d1c", plot_bgcolor="#0e1a35", font_color="#dbe6ff", height=320); st.plotly_chart(fig, width="stretch")
        r = api.post("/api/copilot", {"question": f"Why is {rk[0]['name']} the most suitable supplier?", "retrieval_query": f"{rk[0]['name']} capacity delivery quality contract", "k": 5}, key=KEY())
        st.markdown(f"#### WHY {rk[0]['name'].upper()}?"); st.markdown(r["answer"]) if r["answer"] else st.error(r["error"])
        if r["answer"]: st.caption(r["source"]); evidence(r["evidence"], False)

elif page == "Simulations":
    st.title("What-If Simulation"); dl = st.slider("Loss per delay-day (₹L)", 1.0, 10.0, 5.0, .5); c = st.columns(3)
    sc = [("Wait for Supplier A", c[0].number_input("Wait delay (days)", 1, 30, 10), 1.0, 0.0), ("Switch to Supplier B", c[1].number_input("Switch delay", 1, 30, 5), .4, 2.0), ("Switch B + Reroute", c[2].number_input("Reroute delay", 1, 30, 3), .2, 2.0)]
    df = pd.DataFrame([{"Scenario": n, "Delay (days)": d, "Extra cost (₹L)": e, "Loss (₹L)": round(d*dl*m+e, 1)} for n, d, m, e in sc]); st.dataframe(df, hide_index=True, width="stretch")
    fig = go.Figure([go.Bar(x=df.Scenario, y=df["Loss (₹L)"], name="Loss ₹L", marker_color="#ff5a5f"), go.Bar(x=df.Scenario, y=df["Delay (days)"], name="Delay days", marker_color="#4cc9f0")]); fig.update_layout(barmode="group", paper_bgcolor="#070d1c", plot_bgcolor="#0e1a35", font_color="#dbe6ff"); st.plotly_chart(fig, width="stretch")

elif page == "Rewind Engine":
    st.title("REWIND ENGINE"); st.caption("What if we had acted earlier? · Counterfactual Simulation"); d = st.slider("Act this many days earlier", 0, 3, 3); loss, rec = [50, 35, 18, 5][d], [10, 6, 4, 1][d]; c = st.columns(3)
    c[0].metric("Recovery", f"{rec} days", f"{rec-10} days" if d else None, delta_color="inverse"); c[1].metric("Projected loss", f"₹{loss}L", f"-₹{50-loss}L" if d else None, delta_color="inverse"); c[2].metric("Inventory", ["Critical", "Low", "Adequate", "Stable"][d])

elif page == "Reports":
    st.title("Executive Report"); top = S["ranking"][0]
    df = pd.DataFrame({"Section": ["Disruption summary", "Statuses", "Recommended supplier", "Recommended route", "Financial exposure", "Shipment changes"],
        "Detail": ["; ".join(f"{h['type']} near {h['name']}" for h in S["hazards"]) or "none", str(S["statuses"]), f"{META['suppliers'][top['id']]['name']} ({top['score']}/100)", lab(S["best"]["path"]), S["kpis"]["exposure"]["v"], "; ".join(S["log"][:3]) or "none"]})
    st.dataframe(df, hide_index=True, width="stretch"); c = st.columns(2); c[0].download_button("Export CSV", df.to_csv(index=False), "chaintwin_report.csv"); c[1].download_button("Export TXT", df.to_string(index=False), "chaintwin_report.txt")

elif page == "Settings":
    st.title("Settings"); st.info("API key is entered in the sidebar and forwarded to the backend per request."); st.text_input("Backend URL", api.BASE, disabled=True, help="Set CHAINTWIN_API to change"); st.text_input("LLM model", "claude-sonnet-5-5 (backend LLM_MODEL env var)", disabled=True)
    st.selectbox("Graph store", ["In-memory", "Neo4j (stub)"]); st.selectbox("Optimizer", ["Hazard-aware Dijkstra", "OR-Tools (stub)"]); st.selectbox("Imagery source", ["Synthetic demo / uploads", "Sentinel-2 (stub)"])