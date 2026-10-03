import streamlit as st
CSS = """<style>
.stApp{background:#070d1c;color:#dbe6ff}section[data-testid=stSidebar]{background:#0a1226;border-right:1px solid #16264a}
.card{background:#0e1a35;border:1px solid #1c3160;border-radius:12px;padding:14px;height:100%}
.lbl{font-size:11px;letter-spacing:.1em;color:#7f93bd;text-transform:uppercase}
.big{font-size:30px;font-weight:700;font-family:monospace}.red{color:#ff5a5f}.org{color:#ffa94d}.grn{color:#3ddc97}.cyn{color:#4cc9f0}
.banner{background:linear-gradient(90deg,#3a0d14,#0e1a35);border:1px solid #ff5a5f;border-radius:12px;padding:12px 16px;margin:8px 0}
.ok{background:#0d2a22;border:1px solid #3ddc97;border-radius:12px;padding:12px 16px;margin:8px 0}</style>"""
def apply(): st.markdown(CSS, unsafe_allow_html=True)
def kpi(col, label, v, sub, cls): col.markdown(f'<div class="card"><div class="lbl">{label}</div><div class="big {cls}">{v}</div><div class="lbl">{sub}</div></div>', unsafe_allow_html=True)