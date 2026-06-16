import streamlit as st
import time
import json
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root palette ── */
:root {
  --bg-deep:    #0B0F1A;
  --bg-card:    #111827;
  --bg-input:   #1a2235;
  --accent1:    #6C63FF;   /* violet */
  --accent2:    #00D4AA;   /* teal   */
  --accent3:    #FF6B6B;   /* coral  */
  --accent4:    #FFB347;   /* amber  */
  --text-main:  #E8EAF0;
  --text-muted: #8B92A5;
  --border:     rgba(108,99,255,0.25);
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg-deep) !important;
  font-family: 'Space Grotesk', sans-serif;
  color: var(--text-main);
}
[data-testid="stSidebar"] {
  background: var(--bg-card) !important;
  border-right: 1px solid var(--border);
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero banner ── */
.hero {
  background: linear-gradient(135deg, #0f1729 0%, #1a1040 50%, #0d1f2d 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 40px 48px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; top:-80px; right:-80px;
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(108,99,255,0.18) 0%, transparent 70%);
  border-radius: 50%;
}
.hero::after {
  content: '';
  position: absolute; bottom:-60px; left:20%;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(0,212,170,0.12) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-eyebrow {
  font-size: 11px; font-weight: 600; letter-spacing: 3px;
  text-transform: uppercase; color: var(--accent2);
  margin-bottom: 12px;
}
.hero-title {
  font-size: 42px; font-weight: 700; line-height: 1.15;
  background: linear-gradient(135deg, #fff 0%, var(--accent1) 60%, var(--accent2) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
}
.hero-sub {
  font-size: 15px; color: var(--text-muted); max-width: 560px; line-height: 1.6;
}

/* ── Agent cards (sidebar) ── */
.agent-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 10px;
  display: flex; align-items: center; gap: 12px;
  transition: border-color .2s;
}
.agent-card:hover { border-color: var(--accent1); }
.agent-dot {
  width: 10px; height: 10px; border-radius: 50%;
  flex-shrink: 0;
}
.agent-name { font-size: 13px; font-weight: 600; color: var(--text-main); }
.agent-desc { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* ── Step progress bar ── */
.pipeline-bar {
  display: flex; gap: 6px; margin-bottom: 28px;
}
.pipeline-step {
  flex: 1; height: 4px; border-radius: 2px;
  background: rgba(255,255,255,0.08);
  transition: background .4s;
}
.pipeline-step.done   { background: var(--accent2); }
.pipeline-step.active { background: var(--accent1);
  box-shadow: 0 0 8px var(--accent1); }

/* ── Status badge ── */
.status-badge {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;
  letter-spacing: .4px;
}
.status-idle    { background:rgba(139,146,165,.15); color:var(--text-muted); }
.status-running { background:rgba(108,99,255,.18);  color:var(--accent1); }
.status-done    { background:rgba(0,212,170,.15);   color:var(--accent2); }
.status-error   { background:rgba(255,107,107,.15); color:var(--accent3); }
.pulse {
  width:8px;height:8px;border-radius:50%;
  animation: pulse 1.2s ease-in-out infinite;
}
.pulse-v{background:var(--accent1);}
.pulse-t{background:var(--accent2);}
.pulse-c{background:var(--accent3);}
@keyframes pulse {
  0%,100%{opacity:1;transform:scale(1);}
  50%{opacity:.4;transform:scale(.6);}
}

/* ── Log block ── */
.log-block {
  background: #070B12;
  border: 1px solid rgba(108,99,255,0.2);
  border-radius: 12px;
  padding: 18px 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12.5px;
  line-height: 1.7;
  color: #adb5c7;
  max-height: 320px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
.log-ts  { color: #4a5568; }
.log-ok  { color: var(--accent2); }
.log-err { color: var(--accent3); }
.log-inf { color: var(--accent1); }

/* ── Result sections ── */
.section-label {
  font-size: 11px; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--text-muted);
  margin: 28px 0 10px;
  display: flex; align-items: center; gap: 8px;
}
.section-label::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ── Result card ── */
.result-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px 28px;
  margin-bottom: 16px;
  line-height: 1.75;
  font-size: 14.5px;
  color: var(--text-main);
}
.result-card h1,h2,h3 { color:#fff; }

/* ── Metric row ── */
.metric-row {
  display: flex; gap: 12px; flex-wrap: wrap;
  margin-bottom: 24px;
}
.metric-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 22px;
  min-width: 130px; flex: 1;
  text-align: center;
}
.metric-val {
  font-size: 26px; font-weight: 700;
  background: linear-gradient(135deg,var(--accent1),var(--accent2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.metric-key { font-size: 11px; color: var(--text-muted); margin-top: 3px; letter-spacing:.5px;}

/* ── Input row ── */
.stTextInput > div > input {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text-main) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 15px !important;
  padding: 14px 18px !important;
}
.stTextInput > div > input:focus {
  border-color: var(--accent1) !important;
  box-shadow: 0 0 0 3px rgba(108,99,255,.2) !important;
}
.stTextInput > label { color: var(--text-muted) !important; font-size:13px !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent1), #9b8cff) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  padding: 12px 32px !important;
  letter-spacing: .3px;
  transition: opacity .2s, transform .15s !important;
  width: 100%;
}
.stButton > button:hover {
  opacity: .88 !important; transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
button[kind="secondary"] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid var(--border) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
  color: var(--text-main) !important;
  font-size: 14px !important;
  font-weight: 600 !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] { background: transparent !important; gap:4px; }
[data-baseweb="tab"] {
  background: rgba(255,255,255,.04) !important;
  border-radius: 8px 8px 0 0 !important;
  color: var(--text-muted) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 13px !important; font-weight: 600 !important;
  padding: 8px 20px !important;
  border: 1px solid transparent !important;
}
[aria-selected="true"][data-baseweb="tab"] {
  background: var(--bg-card) !important;
  color: var(--accent1) !important;
  border-color: var(--border) !important;
  border-bottom-color: var(--bg-card) !important;
}
[data-testid="stTabPanel"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 12px 12px 12px !important;
  padding: 24px !important;
}

/* ── History item ── */
.hist-item {
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(255,255,255,.07);
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: border-color .2s;
}
.hist-item:hover { border-color: var(--accent1); }
.hist-topic { font-size:13px; font-weight:600; color:var(--text-main); }
.hist-time  { font-size:11px; color:var(--text-muted); margin-top:2px; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
  background: rgba(0,212,170,.12) !important;
  border: 1px solid var(--accent2) !important;
  color: var(--accent2) !important;
  border-radius: 10px !important;
  font-size:13px !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: rgba(0,212,170,.22) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(108,99,255,.4); border-radius:3px; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
defaults = {
    "status":        "idle",      # idle | running | done | error
    "active_step":   0,
    "logs":          [],
    "search_result": "",
    "reader_result": "",
    "report":        "",
    "critic":        "",
    "last_topic":    "",
    "elapsed":       0.0,
    "history":       [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
STEPS = ["Search", "Deep Read", "Write Report", "Critique"]

def add_log(msg: str, kind: str = "info"):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({"ts": ts, "msg": msg, "kind": kind})

def render_logs():
    if not st.session_state.logs:
        st.markdown('<div class="log-block"><span class="log-ts">──</span>  Waiting for research to start…</div>',
                    unsafe_allow_html=True)
        return
    lines = []
    for entry in st.session_state.logs[-80:]:
        cls = {"ok":"log-ok","err":"log-err","info":"log-inf"}.get(entry["kind"],"")
        lines.append(
            f'<span class="log-ts">[{entry["ts"]}]</span> '
            f'<span class="{cls}">{entry["msg"]}</span>'
        )
    st.markdown(f'<div class="log-block">{"<br>".join(lines)}</div>', unsafe_allow_html=True)

def pipeline_bar(active: int):
    html = '<div class="pipeline-bar">'
    for i in range(len(STEPS)):
        cls = "done" if i < active else ("active" if i == active else "")
        html += f'<div class="pipeline-step {cls}" title="{STEPS[i]}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def status_badge():
    s = st.session_state.status
    if s == "idle":
        st.markdown('<span class="status-badge status-idle">● Idle</span>', unsafe_allow_html=True)
    elif s == "running":
        step = STEPS[min(st.session_state.active_step, len(STEPS)-1)]
        st.markdown(
            f'<span class="status-badge status-running">'
            f'<span class="pulse pulse-v"></span> Running · {step}</span>',
            unsafe_allow_html=True)
    elif s == "done":
        st.markdown('<span class="status-badge status-done">✓ Complete</span>', unsafe_allow_html=True)
    elif s == "error":
        st.markdown('<span class="status-badge status-error">✕ Error</span>', unsafe_allow_html=True)

def metric_row(topic: str, elapsed: float):
    word_count = len((st.session_state.report or "").split())
    src_count  = st.session_state.reader_result.count("http") if st.session_state.reader_result else 0
    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-box">
        <div class="metric-val">{elapsed:.0f}s</div>
        <div class="metric-key">Total Time</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{word_count:,}</div>
        <div class="metric-key">Report Words</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{src_count}</div>
        <div class="metric-key">Sources Read</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">4</div>
        <div class="metric-key">Agents Used</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CORE PIPELINE  (wraps your pipeline.py)
# ─────────────────────────────────────────────
def run_pipeline(topic: str):
    """Calls your real pipeline and streams progress into session state."""
    from pipline import run_multi_agents          # ← your actual pipeline.py

    st.session_state.status        = "running"
    st.session_state.active_step   = 0
    st.session_state.logs          = []
    st.session_state.search_result = ""
    st.session_state.reader_result = ""
    st.session_state.report        = ""
    st.session_state.critic        = ""
    st.session_state.last_topic    = topic

    add_log(f"Research started → {topic}", "info")
    add_log("Initialising Search Agent…", "info")
    t0 = time.time()

    try:
        state = run_multi_agents(topic)

        st.session_state.active_step   = 1
        add_log("Search Agent complete ✓", "ok")
        st.session_state.search_result = state.get("search_result", "")

        st.session_state.active_step   = 2
        add_log("Deep Reader Agent complete ✓", "ok")
        st.session_state.reader_result = state.get("Reader_results", "")

        st.session_state.active_step   = 3
        add_log("Writer chain complete ✓", "ok")
        st.session_state.report        = state.get("report", "")

        st.session_state.active_step   = 4
        add_log("Critic chain complete ✓", "ok")
        st.session_state.critic        = state.get("critic", "")

        st.session_state.elapsed = time.time() - t0
        st.session_state.status  = "done"
        add_log(f"All done in {st.session_state.elapsed:.1f}s 🎉", "ok")

        # save to history
        st.session_state.history.append({
            "topic":   topic,
            "time":    datetime.now().strftime("%d %b %Y · %H:%M"),
            "elapsed": st.session_state.elapsed,
            "report":  st.session_state.report,
            "critic":  st.session_state.critic,
        })

    except Exception as e:
        st.session_state.status = "error"
        add_log(f"ERROR: {e}", "err")
        st.error(f"Pipeline error: {e}")


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 18px;">
      <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;
                  color:#6C63FF;font-weight:700;margin-bottom:6px;">System</div>
      <div style="font-size:20px;font-weight:700;color:#fff;line-height:1.2;">
        Multi-AI<br>Research
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Status
    status_badge()
    st.markdown("<br>", unsafe_allow_html=True)

    # Agents
    st.markdown("""<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
                                color:#8B92A5;margin:12px 0 8px;font-weight:700;">Active Agents</div>""",
                unsafe_allow_html=True)
    agents = [
        ("#6C63FF", "🔍 Search Agent",  "Finds recent, reliable sources"),
        ("#00D4AA", "📖 Reader Agent",  "Deep-reads 3–5 top URLs"),
        ("#FFB347", "✍️  Writer Chain", "Synthesises a full report"),
        ("#FF6B6B", "🧐 Critic Chain",  "Reviews & scores the report"),
    ]
    for col, name, desc in agents:
        st.markdown(f"""
        <div class="agent-card">
          <div class="agent-dot" style="background:{col};
               box-shadow:0 0 6px {col};"></div>
          <div><div class="agent-name">{name}</div>
               <div class="agent-desc">{desc}</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # History
    if st.session_state.history:
        st.markdown("""<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
                                    color:#8B92A5;margin-bottom:8px;font-weight:700;">History</div>""",
                    unsafe_allow_html=True)
        for i, h in enumerate(reversed(st.session_state.history[-5:])):
            st.markdown(f"""
            <div class="hist-item">
              <div class="hist-topic">📋 {h['topic'][:32]}{'…' if len(h['topic'])>32 else ''}</div>
              <div class="hist-time">{h['time']} · {h['elapsed']:.0f}s</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:18px;left:12px;right:12px;
                font-size:10px;color:#4a5568;text-align:center;letter-spacing:.5px;">
      Multi-AI Research System v2.0
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Powered by LangChain · MistralAI · Multi-Agent Pipeline</div>
  <div class="hero-title">Deep Research,<br>On Demand</div>
  <div class="hero-sub">
    Four specialised AI agents work in sequence — searching the web, reading sources,
    writing a structured report, and self-critiquing the output — so you get
    research-grade intelligence in minutes.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Input row ──
col_inp, col_btn = st.columns([5, 1], gap="small")
with col_inp:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Research", disabled=(st.session_state.status == "running"))

# ── Pipeline progress bar ──
pipeline_bar(st.session_state.active_step if st.session_state.status == "running"
             else (len(STEPS) if st.session_state.status == "done" else 0))

# ── Step labels ──
cols = st.columns(len(STEPS))
for i, (c, label) in enumerate(zip(cols, STEPS)):
    active = (st.session_state.status == "running" and i == st.session_state.active_step)
    done   = (st.session_state.status == "done") or \
             (st.session_state.status == "running" and i < st.session_state.active_step)
    colour = "#00D4AA" if done else ("#6C63FF" if active else "#4a5568")
    c.markdown(f"<div style='text-align:center;font-size:11px;font-weight:600;"
               f"color:{colour};letter-spacing:.5px;'>{label}</div>",
               unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Trigger ──
if run_btn and topic.strip():
    run_pipeline(topic.strip())
    st.rerun()
elif run_btn and not topic.strip():
    st.warning("Please enter a research topic first.")


# ─────────────────────────────────────────────
# RESULTS TABS
# ─────────────────────────────────────────────
if st.session_state.status in ("running", "done", "error"):
    tab_live, tab_search, tab_read, tab_report, tab_critic = st.tabs(
        ["🔴 Live Log", "🔍 Search", "📖 Deep Read", "📄 Report", "🧐 Critic"]
    )

    # ── Live Log ──
    with tab_live:
        render_logs()
        if st.session_state.status == "running":
            time.sleep(0.8)
            st.rerun()

    # ── Search Results ──
    with tab_search:
        if st.session_state.search_result:
            st.markdown('<div class="section-label">Raw Search Output</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">{st.session_state.search_result}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#4a5568;padding:20px 0;">Search not started yet.</div>',
                        unsafe_allow_html=True)

    # ── Deep Read ──
    with tab_read:
        if st.session_state.reader_result:
            st.markdown('<div class="section-label">Deep Reader Analysis</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">{st.session_state.reader_result}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#4a5568;padding:20px 0;">Reader not started yet.</div>',
                        unsafe_allow_html=True)

    # ── Report ──
    with tab_report:
        if st.session_state.report:
            if st.session_state.status == "done":
                metric_row(st.session_state.last_topic, st.session_state.elapsed)

            st.markdown('<div class="section-label">Final Research Report</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">{st.session_state.report}</div>',
                        unsafe_allow_html=True)

            col_dl1, col_dl2, _ = st.columns([1, 1, 3])
            with col_dl1:
                st.download_button(
                    "⬇ Download .txt",
                    data=str(st.session_state.report),
                    file_name=f"report_{st.session_state.last_topic[:30].replace(' ','_')}.txt",
                    mime="text/plain",
                )
            with col_dl2:
                st.download_button(
                    "⬇ Download .md",
                    data=str(st.session_state.report),
                    file_name=f"report_{st.session_state.last_topic[:30].replace(' ','_')}.md",
                    mime="text/markdown",
                )
        else:
            st.markdown('<div style="color:#4a5568;padding:20px 0;">Report not generated yet.</div>',
                        unsafe_allow_html=True)

    # ── Critic ──
    with tab_critic:
        if st.session_state.critic:
            st.markdown('<div class="section-label">Critic Agent Feedback</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">{st.session_state.critic}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#4a5568;padding:20px 0;">Critic not run yet.</div>',
                        unsafe_allow_html=True)

elif st.session_state.status == "idle":
    # Empty state
    st.markdown("""
    <div style="text-align:center;padding:64px 0 40px;">
      <div style="font-size:52px;margin-bottom:16px;">🔬</div>
      <div style="font-size:18px;font-weight:600;color:#fff;margin-bottom:8px;">
        Ready to Research
      </div>
      <div style="font-size:14px;color:#8B92A5;max-width:380px;margin:0 auto;line-height:1.6;">
        Type any topic above and hit <strong style="color:#6C63FF">⚡ Research</strong> to
        activate all four agents.
      </div>
    </div>

    <div style="display:flex;gap:16px;flex-wrap:wrap;max-width:700px;margin:0 auto;">
      <div style="flex:1;min-width:180px;background:#111827;border:1px solid rgba(108,99,255,.2);
                  border-radius:14px;padding:20px;">
        <div style="font-size:22px;margin-bottom:8px;">🌐</div>
        <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:4px;">Live Web Search</div>
        <div style="font-size:12px;color:#8B92A5;">Fetches fresh results via search tools</div>
      </div>
      <div style="flex:1;min-width:180px;background:#111827;border:1px solid rgba(0,212,170,.2);
                  border-radius:14px;padding:20px;">
        <div style="font-size:22px;margin-bottom:8px;">📖</div>
        <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:4px;">Source Deep-Dive</div>
        <div style="font-size:12px;color:#8B92A5;">Scrapes & synthesises top 3–5 URLs</div>
      </div>
      <div style="flex:1;min-width:180px;background:#111827;border:1px solid rgba(255,179,71,.2);
                  border-radius:14px;padding:20px;">
        <div style="font-size:22px;margin-bottom:8px;">✍️</div>
        <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:4px;">Structured Report</div>
        <div style="font-size:12px;color:#8B92A5;">Full findings with stats & sources</div>
      </div>
      <div style="flex:1;min-width:180px;background:#111827;border:1px solid rgba(255,107,107,.2);
                  border-radius:14px;padding:20px;">
        <div style="font-size:22px;margin-bottom:8px;">🧐</div>
        <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:4px;">Self-Critique</div>
        <div style="font-size:12px;color:#8B92A5;">Critic agent scores & flags gaps</div>
      </div>
    </div>
    """, unsafe_allow_html=True)