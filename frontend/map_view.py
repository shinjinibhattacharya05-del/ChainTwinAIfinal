
import math, numpy as np, plotly.graph_objects as go
def build_map(meta, hz, statuses, routes=(), chosen=None, ships=(), sat=False, h=520, show_net=True, show_hz=True):
    C, S, N, HS, COL = meta["cities"], meta["suppliers"], meta["nodes"], meta["hazard_styles"], meta["colors"]
    f = go.Figure()
    pos = lambda k: (C[S[k]["city"]]["lat"], C[S[k]["city"]]["lon"]) if k in S else (C[N[k]["city"]]["lat"] + N[k]["offset"], C[N[k]["city"]]["lon"] + N[k]["offset"])
    if show_net:
        for a, b in [("A","X"),("X","Y"),("Y","Z")] + ([("B","X"),("C","X")] if hz else []):
            (la1, lo1), (la2, lo2) = pos(a), pos(b); f.add_trace(go.Scattermap(lat=[la1, la2], lon=[lo1, lo2], mode="lines", hoverinfo="skip", line=dict(width=2, color="#4cc9f0" if a in "BC" else "#5b7bbf")))
    pal = ["#8ecae6", "#ffb703", "#c77dff", "#90be6d"]
    for i, r in enumerate(routes):
        f.add_trace(go.Scattermap(lat=[C[c]["lat"] for c in r["path"]], lon=[C[c]["lon"] for c in r["path"]], mode="lines", name=r["name"], line=dict(width=3, color=pal[i % 4])))
    if chosen: f.add_trace(go.Scattermap(lat=[C[c]["lat"] for c in chosen], lon=[C[c]["lon"] for c in chosen], mode="lines", line=dict(width=7, color="#00e5ff"), name="Selected"))
    if show_hz:
        for x in hz:
            t = np.linspace(0, 6.3, 50); f.add_trace(go.Scattermap(lat=list(x["lat"] + x["r"]/111*np.sin(t)), lon=list(x["lon"] + x["r"]/111*np.cos(t)), mode="lines", fill="toself", fillcolor="rgba(255,90,95,.2)", line=dict(color=HS[x["type"]]["c"], width=2), hoverinfo="skip"))
            f.add_trace(go.Scattermap(lat=[x["lat"]], lon=[x["lon"]], mode="markers+text", text=[HS[x["type"]]["ic"]], textfont=dict(size=22), marker=dict(size=10, color=HS[x["type"]]["c"]), hovertext=f"{x['type'].upper()} · {x['name']} · {x['conf']:.0%}", hoverinfo="text"))
    for k, name in [(k, v["name"]) for k, v in S.items()] + [(k, v["name"]) for k, v in N.items()]:
        st_ = statuses[k]; col = COL["alt"] if (hz and k in "BCD" and st_ == "healthy") else COL[st_]; la, lo = pos(k)
        f.add_trace(go.Scattermap(lat=[la], lon=[lo], mode="markers+text", text=[name], textposition="top right", textfont=dict(color="#fff", size=11), marker=dict(size=19 if st_ == "disrupted" else 14, color=col), hovertext=f"<b>{name}</b><br>{st_.upper()}", hoverinfo="text"))
    for s in ships:
        f.add_trace(go.Scattermap(lat=[p[0] for p in s["line"]], lon=[p[1] for p in s["line"]], mode="lines", line=dict(width=2, color="#fff"), opacity=.5, hoverinfo="skip"))
        f.add_trace(go.Scattermap(lat=[s["lat"]], lon=[s["lon"]], mode="markers+text", text=[s["id"]], textposition="bottom right", textfont=dict(color="#00e5ff", size=11), marker=dict(size=12, color="#fff"), hovertext=f"{s['id']} · {s['note']}", hoverinfo="text"))
    lay = [dict(below="traces", sourcetype="raster", source=["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"])] if sat else []
    f.update_layout(map=dict(style="white-bg" if sat else "carto-darkmatter", center=dict(lat=15.3, lon=77), zoom=5, layers=lay), margin=dict(l=0, r=0, t=0, b=0), height=h, showlegend=False, paper_bgcolor="#070d1c")
    return f