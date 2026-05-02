import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

API = "http://localhost:8000"

st.set_page_config(page_title="PortfolioAI Pro", page_icon="📊", layout="wide",
                   initial_sidebar_state="expanded")

# ─── Custom CSS Injection ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

/* Global Reset */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #f8fafc;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'JetBrains Mono', monospace !important;
    color: #ffffff;
    font-weight: 700 !important;
}

/* Backgrounds */
.stApp {
    background-color: #0f172a;
}
div[data-testid="stSidebar"] {
    background-color: #1e293b !important;
    border-right: 1px solid #334155;
}

/* Hide default streamit elements */
header[data-testid="stHeader"] { visibility: hidden; }
footer { visibility: hidden; }

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    width: 100%;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.4);
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
}

/* Inputs */
.stTextInput>div>div>input, .stNumberInput>div>div>input {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.5rem;
    transition: all 0.2s ease;
}
.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

/* Select Box & Sliders */
.stSelectbox>div>div {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
}
.stSlider>div>div>div>div { background-color: #3b82f6; }

/* Dataframes */
.stDataFrame {
    background-color: #1e293b;
    border-radius: 12px;
    border: 1px solid #334155;
    overflow: hidden;
}
div[data-testid="stDataFrame"] > div {
    background-color: #1e293b;
}

/* Custom Cards */
.custom-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid #334155;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.custom-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
}
.custom-card h4 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #f8fafc;
    font-size: 1.1rem;
}

/* Top Navbar */
.top-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: #1e293b;
    border-bottom: 1px solid #334155;
    margin-bottom: 2rem;
    border-radius: 0 0 12px 12px;
}

/* Metric Cards HTML */
.metric-card {
    background-color: #1e293b; 
    border-radius: 12px; 
    padding: 1.5rem; 
    border: 1px solid #334155; 
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); 
    transition: transform 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

COLORS = ["#3b82f6","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4","#f97316","#ec4899"]

# ─── Session State Init ────────────────────────────────────────────────────────
for key, val in {"token": None, "user": None, "page": "login"}.items():
    if key not in st.session_state:
        st.session_state[key] = val

if "holdings" not in st.session_state:
    st.session_state.holdings = [
        {"ticker":"AAPL","shares":10,"avg_cost":150.0},
        {"ticker":"MSFT","shares":5,"avg_cost":300.0},
    ]


# ─── API Helpers ───────────────────────────────────────────────────────────────
def api(endpoint, payload=None, method="POST", auth=False):
    headers = {"Content-Type": "application/json"}
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        if method == "GET":
            r = requests.get(f"{API}{endpoint}", headers=headers, timeout=60)
        else:
            r = requests.post(f"{API}{endpoint}", json=payload, headers=headers, timeout=90)
        if r.status_code == 401:
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Make sure backend is running.")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def dark_fig(figsize=(12, 4)):
    fig, ax = plt.subplots(figsize=figsize, facecolor="#1e293b")
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor('#1e293b')
    for s in ax.spines.values(): s.set_color("#334155")
    ax.tick_params(colors="#94a3b8", labelsize=8)
    ax.grid(color="#334155", linewidth=0.5, linestyle="--")
    ax.title.set_color("#f8fafc")
    ax.xaxis.label.set_color("#94a3b8")
    ax.yaxis.label.set_color("#94a3b8")
    return fig, ax

def render_metric_card(title, value, change=None, icon="📊"):
    change_html = ""
    if change is not None:
        color = "#10b981" if change >= 0 else "#ef4444"
        sign = "+" if change >= 0 else ""
        bg = "rgba(16, 185, 129, 0.1)" if change >= 0 else "rgba(239, 68, 68, 0.1)"
        change_html = f"<span style='color: {color}; background: {bg}; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;'>{sign}{change:.2f}%</span>"

    html = f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="color: #94a3b8; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{title}</span>
            <span style="font-size: 1.25rem;">{icon}</span>
        </div>
        <div style="font-size: 1.875rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem;">
            {value}
        </div>
        {change_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def logout():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.page = "login"
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH PAGES
# ═══════════════════════════════════════════════════════════════════════════════
def show_login():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2.5rem; margin-top: 6rem;'>
            <div style='background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 20px; border-radius: 16px; display: inline-flex; box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);'>
                <span style='font-size: 2.5rem; line-height: 1;'>📊</span>
            </div>
            <h1 style='margin-top: 1.5rem; font-size: 2.2rem;'>PortfolioAI Pro</h1>
            <p style='color: #94a3b8; font-size: 1.1rem;'>Sign in to your dashboard</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            email = st.text_input("Email", placeholder="you@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Sign In"):
                    if email and password:
                        with st.spinner("Authenticating..."):
                            res = api("/auth/login", {"email": email, "password": password})
                        if res:
                            st.session_state.token = res["access_token"]
                            st.session_state.user = res["user"]
                            st.session_state.page = "dashboard"
                            st.rerun()
                    else:
                        st.error("Please fill all fields.")
            with c2:
                if st.button("Register"):
                    st.session_state.page = "register"
                    st.rerun()


def show_register():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2.5rem; margin-top: 4rem;'>
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; display: inline-flex; box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);'>
                <span style='font-size: 2.5rem; line-height: 1;'>🚀</span>
            </div>
            <h1 style='margin-top: 1.5rem; font-size: 2.2rem;'>Create Account</h1>
            <p style='color: #94a3b8; font-size: 1.1rem;'>Join PortfolioAI Pro</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            name = st.text_input("Full Name", placeholder="Jane Doe", key="reg_name")
            email = st.text_input("Email", placeholder="you@example.com", key="reg_email")
            password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="reg_pass")
            confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="reg_confirm")
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Create Account"):
                    if not all([name, email, password, confirm]):
                        st.error("Please fill all fields.")
                    elif password != confirm:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        with st.spinner("Creating account..."):
                            res = api("/auth/register", {"name": name, "email": email, "password": password})
                        if res:
                            st.session_state.token = res["access_token"]
                            st.session_state.user = res["user"]
                            st.session_state.page = "dashboard"
                            st.rerun()
            with c2:
                if st.button("Back to Login"):
                    st.session_state.page = "login"
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def show_dashboard():
    user = st.session_state.user

    # Top Navbar
    st.markdown(f"""
    <div class="top-navbar">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5rem;">📊</span>
            <span style="font-weight: 700; font-size: 1.2rem; font-family: 'JetBrains Mono', monospace;">PortfolioAI Pro</span>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="color: #94a3b8;">Welcome, <strong style="color: #f8fafc;">{user['name']}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<div style='padding: 1rem 0; margin-bottom: 1rem;'>", unsafe_allow_html=True)
        page = st.radio("Navigation", [
            "🏠 Home",
            "📈 Live Market",
            "💼 Portfolio Tracker",
            "🎯 Optimization",
            "🤖 AI Prediction",
            "⚡ Technical Analysis",
            "🔍 Stock Screener",
            "📰 News Sentiment",
            "🚨 Alerts",
            "📁 My Portfolios",
            "👤 Profile",
            "ℹ️ About",
        ], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪 Logout"):
            logout()

    # ══════════════════════════════════════════════════════════════════════════
    # HOME / DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    if page == "🏠 Home":
        with st.spinner("Loading portfolio insights..."):
            track_res = api("/portfolio/track", {"holdings": st.session_state.holdings})
            
            # Use current holdings for recommendations, fallback to tech stocks
            tickers = [h["ticker"] for h in st.session_state.holdings]
            if not tickers: tickers = ["AAPL", "MSFT", "GOOGL"]
            
            rec_res = api("/portfolio/recommend", {
                "tickers": tickers,
                "period": "1y",
                "risk_level": "medium",
                "investment_amount": 10000,
                "time_horizon": 12
            })
            
            sim_res = api("/portfolio/simulate", {
                "tickers": tickers,
                "investment_amount": 10000,
                "days": 252,
                "simulations": 50,
                "period": "1y",
                "risk_level": "medium"
            })
            
            alerts_res = api("/alerts/check", {"ticker": tickers[0] if tickers else "AAPL", "price_target": 0, "stop_loss": 0})

        if track_res:
            s = track_res["summary"]
            
            # Metrics Row
            c1, c2, c3 = st.columns(3)
            with c1: render_metric_card("Total Investment", f"${s['total_invested']:,.2f}", icon="💰")
            with c2: render_metric_card("Current Value", f"${s['total_current_value']:,.2f}", icon="📈")
            with c3: render_metric_card("Profit / Loss", f"${s['total_pnl']:,.2f}", change=s['total_pnl_pct'], icon="⚖️")

            st.markdown("<br>", unsafe_allow_html=True)

            # Charts Row
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown("<div class='custom-card'><h4>🍩 Asset Allocation</h4>", unsafe_allow_html=True)
                if result_holdings := track_res.get("holdings", []):
                    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#1e293b")
                    labels = [h["ticker"] for h in result_holdings]
                    sizes = [h["current_value"] for h in result_holdings]
                    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=COLORS[:len(labels)],
                            textprops={"color":"#f8fafc","fontsize":9}, pctdistance=0.75, 
                            wedgeprops=dict(width=0.4, edgecolor='#1e293b', linewidth=2))
                    ax.set_title("")
                    st.pyplot(fig)
                    plt.close()
                else:
                    st.info("No holdings to display.")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_chart2:
                st.markdown("<div class='custom-card'><h4>📈 Portfolio Growth Projection</h4>", unsafe_allow_html=True)
                if sim_res and "sample_paths" in sim_res:
                    fig, ax = dark_fig((6, 4))
                    paths = sim_res["sample_paths"]
                    for path in paths[:10]: # Show a few paths
                        ax.plot(path, alpha=0.2, linewidth=1, color="#94a3b8")
                    
                    # Expected path
                    avg_path = np.mean(paths, axis=0)
                    ax.plot(avg_path, color="#3b82f6", linewidth=2.5, label="Expected Path")
                    ax.set_ylabel("Value ($)")
                    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v/1000:.0f}k"))
                    ax.legend(facecolor="#0f172a", edgecolor="#334155", labelcolor="#f8fafc", fontsize=8)
                    st.pyplot(fig)
                    plt.close()
                else:
                    st.info("Simulation data unavailable.")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Sections Row
            col_sec1, col_sec2 = st.columns(2)
            with col_sec1:
                st.markdown("<div class='custom-card'><h4>🎯 Recommended Action</h4>", unsafe_allow_html=True)
                if rec_res:
                    sent = rec_res["sentiment"]
                    signal = sent["signal"]
                    color = "#10b981" if "BUY" in signal else "#ef4444" if "SELL" in signal or "REDUCE" in signal else "#f59e0b"
                    
                    st.markdown(f"""
                    <div style='background: {color}22; padding: 1rem; border-radius: 8px; border-left: 4px solid {color}; margin-bottom: 1rem;'>
                        <h3 style='color: {color}; margin: 0; font-size: 1.5rem;'>{signal}</h3>
                        <p style='margin: 0; color: #cbd5e1; font-size: 0.9rem; margin-top: 4px;'>Based on medium risk optimization</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    alloc = rec_res["allocation"]
                    df = pd.DataFrame(alloc).rename(columns={"ticker":"Ticker", "weight_pct":"Target %", "shares":"Shares"})
                    st.dataframe(df.style.format({"Target %":"{:.1f}%"}), hide_index=True, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_sec2:
                st.markdown("<div class='custom-card'><h4>🚨 Active Notifications</h4>", unsafe_allow_html=True)
                if alerts_res and alerts_res.get("alerts"):
                    for alert in alerts_res["alerts"][:4]:
                        clr = {"SUCCESS":"#10b981","INFO":"#3b82f6","WARNING":"#f59e0b","DANGER":"#ef4444"}.get(alert["severity"],"#6b7280")
                        icon = {"SUCCESS":"✅","INFO":"ℹ️","WARNING":"⚠️","DANGER":"🚨"}.get(alert["severity"],"•")
                        st.markdown(f"""
                        <div style='border-left: 3px solid {clr}; padding: 12px 16px; margin-bottom: 10px; background: #0f172a; border-radius: 6px; display: flex; align-items: start; gap: 12px;'>
                            <span style='font-size: 1.2rem;'>{icon}</span>
                            <div>
                                <strong style='color: #f8fafc; font-size: 0.95rem; display: block; margin-bottom: 2px;'>{alert['type']}</strong>
                                <span style='color: #94a3b8; font-size: 0.85rem;'>{alert['message']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='text-align: center; padding: 2rem; color: #64748b;'>
                        <span style='font-size: 2rem;'>🔕</span>
                        <p style='margin-top: 8px;'>No active alerts at the moment.</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════════════════════
    # LIVE MARKET
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "📈 Live Market":
        st.markdown("# `📈 Live Market`")
        col1, col2 = st.columns([3,1])
        with col1: ticker = st.text_input("Ticker", "AAPL").upper()
        with col2:
            interval = st.selectbox("Interval", ["5m","15m","30m","1h"])
            load = st.button("Load Chart")

        if load:
            with st.spinner("Fetching..."):
                quote = api("/market/live", {"tickers": [ticker]})
                intraday = api("/market/intraday", {"ticker": ticker, "interval": interval})

            if quote and "error" not in quote[0]:
                q = quote[0]
                c1,c2,c3,c4,c5 = st.columns(5)
                c1.metric("Price", f"${q['price']:,.2f}", f"{q['change_pct']:+.2f}%")
                c2.metric("Open", f"${q['open']:,.2f}")
                c3.metric("High", f"${q['high']:,.2f}")
                c4.metric("Low", f"${q['low']:,.2f}")
                c5.metric("Volume", f"{q['volume']:,}")

                col1, col2, col3 = st.columns(3)
                col1.metric("Market Cap", f"${q.get('market_cap',0)/1e9:.1f}B" if q.get('market_cap') else "N/A")
                col2.metric("P/E Ratio", q.get('pe_ratio','N/A'))
                col3.metric("52W Range", f"${q.get('52w_low','?')} - ${q.get('52w_high','?')}")

            if intraday and intraday.get("close"):
                close = intraday["close"]
                volume = intraday.get("volume",[])
                timestamps = intraday["timestamps"]
                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                fig, axes = plt.subplots(2,1, figsize=(12,6), facecolor="#1e293b",
                                         gridspec_kw={"height_ratios":[3,1]})
                for ax in axes:
                    ax.set_facecolor("#0f172a")
                    for s in ax.spines.values(): s.set_color("#334155")
                    ax.tick_params(colors="#94a3b8", labelsize=7)
                    ax.grid(color="#334155", linewidth=0.5, linestyle="--")
                x = range(len(close))
                clr = "#10b981" if close[-1]>=close[0] else "#ef4444"
                axes[0].fill_between(x, close, alpha=0.15, color=clr)
                axes[0].plot(x, close, color=clr, linewidth=1.5)
                axes[0].set_title(f"{ticker} Intraday ({interval})", color="#f8fafc")
                axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.2f}"))
                step = max(1, len(timestamps)//8)
                axes[0].set_xticks(list(x)[::step])
                axes[0].set_xticklabels([str(timestamps[i])[-8:-3] for i in range(0,len(timestamps),step)], rotation=30)
                if volume:
                    vc = ["#10b981" if i==0 or close[i]>=close[i-1] else "#ef4444" for i in range(len(volume))]
                    axes[1].bar(x, volume, color=vc, alpha=0.8, width=0.8)
                    axes[1].set_title("Volume", color="#f8fafc", fontsize=9)
                    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{v/1e6:.1f}M"))
                plt.tight_layout()
                st.pyplot(fig); plt.close()
                st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PORTFOLIO TRACKER
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "💼 Portfolio Tracker":
        st.markdown("# `💼 Portfolio Tracker`")
        col1,col2,col3,col4 = st.columns([2,1,2,1])
        with col1: nt = st.text_input("Ticker", key="nt").upper()
        with col2: ns = st.number_input("Shares", min_value=0.001, value=1.0, key="ns")
        with col3: nc = st.number_input("Avg Cost ($)", min_value=0.01, value=100.0, key="nc")
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Add"):
                if nt: st.session_state.holdings.append({"ticker":nt,"shares":ns,"avg_cost":nc})

        st.dataframe(pd.DataFrame(st.session_state.holdings), use_container_width=True, hide_index=True)
        if st.button("📊 Analyze Portfolio"):
            with st.spinner("Fetching live prices..."):
                result = api("/portfolio/track", {"holdings": st.session_state.holdings})
            if result:
                s = result["summary"]
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("Invested", f"${s['total_invested']:,.2f}")
                c2.metric("Current Value", f"${s['total_current_value']:,.2f}")
                c3.metric("Total P&L", f"${s['total_pnl']:,.2f}", f"{s['total_pnl_pct']:+.2f}%")
                c4.metric("Holdings", s["num_holdings"])

                rows = [{"Ticker":h["ticker"],"Shares":h["shares"],"Avg":f"${h['avg_cost']:.2f}",
                         "Price":f"${h['current_price']:.2f}","Value":f"${h['current_value']:,.2f}",
                         "P&L":f"${h['pnl']:,.2f}","P&L%":f"{h['pnl_pct']:+.2f}%",
                         "Weight":f"{h['allocation_pct']:.1f}%"} for h in result["holdings"]]
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,4), facecolor="#1e293b")
                for ax in [ax1,ax2]: ax.set_facecolor("#1e293b")
                labels = [h["ticker"] for h in result["holdings"]]
                sizes = [h["current_value"] for h in result["holdings"]]
                pnls = [h["pnl_pct"] for h in result["holdings"]]
                ax1.pie(sizes, labels=labels, autopct="%1.1f%%", colors=COLORS[:len(labels)],
                        textprops={"color":"#9ca3af","fontsize":9}, pctdistance=0.8)
                ax1.set_title("Allocation", color="#f8fafc")
                bc = ["#10b981" if p>=0 else "#ef4444" for p in pnls]
                ax2.bar(labels, pnls, color=bc, width=0.6)
                ax2.axhline(0, color="#334155", linewidth=1)
                ax2.set_title("P&L %", color="#f8fafc")
                ax2.set_facecolor("#0f172a")
                for s_spine in ax2.spines.values(): s_spine.set_color("#334155")
                ax2.tick_params(colors="#94a3b8")
                ax2.grid(color="#334155", linewidth=0.5)
                st.pyplot(fig); plt.close()
                st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # OPTIMIZATION
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "🎯 Optimization":
        st.markdown("# `🎯 Portfolio Optimization`")
        col1,col2,col3,col4 = st.columns(4)
        with col1: opt_tickers = st.text_input("Tickers","AAPL,MSFT,GOOGL,AMZN,BTC-USD")
        with col2: investment = st.number_input("Investment ($)", min_value=100.0, value=10000.0)
        with col3: risk_level = st.selectbox("Risk Level", ["low","medium","high"], index=1)
        with col4: time_horizon = st.slider("Horizon (months)", 1, 120, 12)

        col1,col2,col3 = st.columns(3)
        with col1: period = st.selectbox("Period", ["6mo","1y","2y","5y"], index=2)
        with col2: simulations = st.slider("MC Simulations", 100, 2000, 1000, 100)
        with col3: sim_days = st.slider("Sim Days", 30, 504, 252, 30)

        run = st.button("▶ Run Optimization")
        if run:
            tickers = [t.strip().upper() for t in opt_tickers.split(",") if t.strip()]
            payload = {"tickers":tickers,"period":period,"risk_level":risk_level}

            with st.spinner("Optimizing..."):
                rec = api("/portfolio/recommend", {**payload,"investment_amount":investment,"time_horizon":time_horizon})
                sim = api("/portfolio/simulate", {**payload,"investment_amount":investment,"days":sim_days,"simulations":simulations})

            if rec:
                ps = rec["portfolio_stats"]
                sent = rec["sentiment"]
                signal_colors = {"STRONG BUY":"#10b981","BUY":"#3b82f6","HOLD":"#f59e0b","REDUCE":"#ef4444"}
                c1,c2,c3,c4,c5 = st.columns(5)
                c1.metric("Expected Return", f"{ps['expected_return']*100:.2f}%")
                c2.metric("Volatility", f"{ps['volatility']*100:.2f}%")
                c3.metric("Sharpe Ratio", f"{ps['sharpe_ratio']:.3f}")
                c4.metric("Max Drawdown", f"{ps['max_drawdown']*100:.2f}%")
                c5.metric("Signal", sent["signal"])

                col1,col2 = st.columns([1,2])
                with col1:
                    alloc = rec["allocation"]
                    df_alloc = pd.DataFrame(alloc)
                    df_alloc.columns = ["Ticker","Weight %","$ Amount"]
                    st.dataframe(df_alloc.style.format({"Weight %":"{:.2f}%","$ Amount":"${:,.2f}"}),
                                 hide_index=True, use_container_width=True)
                    for alert in rec["alerts"]:
                        icons = {"OK":"✅","INFO":"ℹ️","WARNING":"⚠️","DANGER":"🚨"}
                        st.markdown(f"{icons.get(alert['type'],'•')} {alert['message']}")

                    # Save portfolio button
                    st.markdown("---")
                    save_name = st.text_input("Portfolio Name", "My Portfolio")
                    if st.button("💾 Save Portfolio"):
                        save_payload = {
                            "name": save_name,
                            "tickers": tickers,
                            "risk_level": risk_level,
                            "investment_amount": investment,
                            "time_horizon": time_horizon,
                            "allocation": alloc,
                            "expected_return": ps["expected_return"],
                            "volatility": ps["volatility"],
                            "sharpe_ratio": ps["sharpe_ratio"],
                        }
                        res = api("/portfolio/save", save_payload, auth=True)
                        if res:
                            st.success(f"✅ Saved! (ID: {res['portfolio_id']})")

                with col2:
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    proj = rec["projection"]
                    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,4), facecolor="#1e293b")
                    ax1.set_facecolor("#1e293b")
                    labels = [a["ticker"] for a in alloc]
                    sizes = [a["weight_pct"] for a in alloc]
                    w, _, at = ax1.pie(sizes, labels=labels, autopct="%1.1f%%",
                                      colors=COLORS[:len(labels)], pctdistance=0.8,
                                      textprops={"color":"#9ca3af","fontsize":8})
                    for a in at: a.set_color("#f8fafc")
                    ax1.set_title("Weights", color="#f8fafc")

                    ax2.set_facecolor("#0f172a")
                    for s_spine in ax2.spines.values(): s_spine.set_color("#334155")
                    ax2.tick_params(colors="#94a3b8", labelsize=8)
                    ax2.barh(["Pessimistic","Base","Optimistic"],
                             [proj["pessimistic"],proj["base"],proj["optimistic"]],
                             color=["#ef4444","#3b82f6","#10b981"], height=0.5)
                    ax2.axvline(investment, color="#94a3b8", linestyle="--", linewidth=1)
                    ax2.set_title(f"{time_horizon}-Month Projection", color="#f8fafc")
                    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}"))
                    ax2.grid(color="#334155", linewidth=0.5, axis="x")
                    plt.tight_layout()
                    st.pyplot(fig); plt.close()
                    st.markdown("</div>", unsafe_allow_html=True)

            if sim:
                st.markdown("#### Monte Carlo Simulation")
                col1,col2 = st.columns([2,1])
                with col1:
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    fig, ax = dark_fig((12,4))
                    for path in sim.get("sample_paths",[]):
                        ax.plot(path, alpha=0.12, linewidth=0.7, color="#3b82f6")
                    ax.axhline(investment, color="#94a3b8", linewidth=1, linestyle="--")
                    ax.set_title(f"Monte Carlo ({simulations:,} runs · {sim_days} days)")
                    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}"))
                    st.pyplot(fig); plt.close()
                    st.markdown("</div>", unsafe_allow_html=True)
                with col2:
                    pct = sim["percentiles"]
                    st.dataframe(pd.DataFrame([{"Percentile":f"P{k}","Value":f"${float(v):,.0f}"} for k,v in pct.items()]),
                                 hide_index=True, use_container_width=True)
                    st.metric("Prob. Profit", f"{sim['prob_profit']*100:.1f}%")
                    st.metric("Prob. Loss >20%", f"{sim['prob_loss_20pct']*100:.1f}%")

    # ══════════════════════════════════════════════════════════════════════════
    # AI PREDICTION
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "🤖 AI Prediction":
        st.markdown("# `🤖 AI Price Prediction`")
        col1,col2,col3 = st.columns(3)
        with col1: pred_tickers = st.text_input("Tickers","AAPL,MSFT")
        with col2: days_ahead = st.slider("Days Ahead",1,30,7)
        with col3: pred_period = st.selectbox("Training Period",["1y","2y","3y"],index=1)

        if st.button("🔮 Run Prediction"):
            tickers = [t.strip().upper() for t in pred_tickers.split(",") if t.strip()]
            with st.spinner("Training models..."):
                result = api("/ai/predict",{"tickers":tickers,"days_ahead":days_ahead,"period":pred_period})
            if result:
                for ticker, pred in result.items():
                    if "error" in pred: st.warning(f"{ticker}: {pred['error']}"); continue
                    st.markdown(f"### `{ticker}`")
                    ens = pred["ensemble"]
                    c1,c2,c3,c4 = st.columns(4)
                    c1.metric("Current", f"${pred['current_price']:,.2f}")
                    c2.metric(f"Day {days_ahead}", f"${ens['predictions'][-1]:,.2f}",
                              f"{(ens['predictions'][-1]-pred['current_price'])/pred['current_price']*100:+.2f}%")
                    c3.metric("Signal", ens["signal"])
                    c4.metric("Direction", ens["direction"])

                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    fig, ax = dark_fig((12,3))
                    hist = pred["historical_tail"]
                    ax.plot(range(len(hist)), hist, color="#3b82f6", linewidth=1.5, label="Historical")
                    x_pred = range(len(hist)-1, len(hist)+days_ahead-1)
                    ax.plot(x_pred, [hist[-1]]+pred["linear_regression"]["predictions"][:-1],
                            color="#f59e0b", linewidth=1, linestyle="--",
                            label=f"Linear Reg (MAPE:{pred['linear_regression']['mape']:.1f}%)")
                    ax.plot(x_pred, [hist[-1]]+pred["random_forest"]["predictions"][:-1],
                            color="#10b981", linewidth=1, linestyle="--",
                            label=f"Random Forest (MAPE:{pred['random_forest']['mape']:.1f}%)")
                    ax.plot(x_pred, [hist[-1]]+ens["predictions"][:-1],
                            color="#8b5cf6", linewidth=2, label="Ensemble")
                    ax.axvline(len(hist)-1, color="#334155", linestyle=":", linewidth=1)
                    ax.set_title(f"{ticker} — {days_ahead}-Day Forecast")
                    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.2f}"))
                    ax.legend(fontsize=8, facecolor="#1e293b", edgecolor="#334155", labelcolor="#e5e7eb")
                    st.pyplot(fig); plt.close()
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # TECHNICAL ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "⚡ Technical Analysis":
        st.markdown("# `⚡ Technical Analysis`")
        col1,col2 = st.columns([3,1])
        with col1: tech_tickers = st.text_input("Tickers","AAPL,MSFT,TSLA")
        with col2: tech_period = st.selectbox("Period",["3mo","6mo","1y","2y"],index=2)
        if st.button("⚡ Analyze"):
            tickers = [t.strip().upper() for t in tech_tickers.split(",") if t.strip()]
            with st.spinner("Computing indicators..."):
                result = api("/technical/indicators",{"tickers":tickers,"period":tech_period})
                mkt = api("/market/data",{"tickers":tickers,"period":tech_period})
            if result:
                for ticker, ind in result.items():
                    st.markdown(f"### `{ticker}`")
                    signal = ind.get("signal",{})
                    action = signal.get("action","HOLD")
                    clrs = {"STRONG BUY":"#10b981","BUY":"#3b82f6","HOLD":"#f59e0b","SELL":"#f97316","STRONG SELL":"#ef4444"}
                    st.markdown(f"**Signal:** <span style='color:{clrs.get(action,'#6b7280')};font-weight:700;font-size:1.1em'>{action}</span>",
                                unsafe_allow_html=True)
                    for r in signal.get("reasons",[]): st.caption(f"  → {r}")

                    rsi=ind.get("rsi",{}); macd=ind.get("macd",{}); bb=ind.get("bollinger",{})
                    c1,c2,c3,c4 = st.columns(4)
                    c1.metric("RSI(14)", f"{rsi.get('value',0):.1f}", rsi.get("signal",""))
                    c2.metric("MACD", f"{macd.get('macd',0):.3f}", macd.get("trend",""))
                    c3.metric("BB Position", bb.get("position",""))
                    c4.metric("BB %B", f"{bb.get('pct_b',0):.1f}%")

                    prices = mkt["prices"].get(ticker,[]) if mkt else []
                    if prices and rsi.get("series"):
                        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                        fig, axes = plt.subplots(3,1, figsize=(12,8), facecolor="#1e293b",
                                                gridspec_kw={"height_ratios":[3,1,1]})
                        for ax in axes:
                            ax.set_facecolor("#0f172a")
                            for s in ax.spines.values(): s.set_color("#334155")
                            ax.tick_params(colors="#94a3b8", labelsize=7)
                            ax.grid(color="#334155", linewidth=0.5, linestyle="--")
                        x = range(len(prices))
                        axes[0].plot(x, prices, color="#3b82f6", linewidth=1.5)
                        if bb.get("upper_series"):
                            ub=bb["upper_series"][-len(prices):]; lb=bb["lower_series"][-len(prices):]
                            x2=range(len(prices)-len(ub), len(prices))
                            axes[0].fill_between(x2, lb, ub, alpha=0.1, color="#8b5cf6")
                            axes[0].plot(x2, ub, color="#8b5cf6", linewidth=0.8, linestyle="--")
                            axes[0].plot(x2, lb, color="#8b5cf6", linewidth=0.8, linestyle="--")
                        axes[0].set_title(f"{ticker} + Bollinger Bands", color="#f8fafc")
                        axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}"))
                        rsi_s=rsi.get("series",[])
                        if rsi_s:
                            x_r=range(len(prices)-len(rsi_s), len(prices))
                            axes[1].plot(x_r, rsi_s, color="#f59e0b", linewidth=1.2)
                            axes[1].axhline(70, color="#ef4444", linewidth=0.8, linestyle="--", alpha=0.7)
                            axes[1].axhline(30, color="#10b981", linewidth=0.8, linestyle="--", alpha=0.7)
                            axes[1].set_title("RSI(14)", color="#f8fafc", fontsize=9)
                            axes[1].set_ylim(0,100)
                        macd_s=macd.get("macd_series",[]); sig_s=macd.get("signal_series",[])
                        if macd_s:
                            x_m=range(len(prices)-len(macd_s), len(prices))
                            axes[2].plot(x_m, macd_s, color="#3b82f6", linewidth=1.2, label="MACD")
                            axes[2].plot(x_m, sig_s, color="#ef4444", linewidth=1.2, label="Signal")
                            hist_v=[m-s for m,s in zip(macd_s,sig_s)]
                            axes[2].bar(x_m, hist_v, color=["#10b981" if h>=0 else "#ef4444" for h in hist_v], alpha=0.4, width=1)
                            axes[2].set_title("MACD", color="#f8fafc", fontsize=9)
                            axes[2].axhline(0, color="#334155", linewidth=0.8)
                            axes[2].legend(fontsize=7, facecolor="#1e293b", edgecolor="#334155", labelcolor="#e5e7eb")
                        plt.tight_layout()
                        st.pyplot(fig); plt.close()
                        st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STOCK SCREENER
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "🔍 Stock Screener":
        st.markdown("# `🔍 Stock Screener`")
        col1,col2,col3 = st.columns(3)
        with col1:
            min_return = st.slider("Min Annual Return %",-20,50,5)/100
            top_n = st.slider("Top N",5,30,10)
        with col2:
            max_vol = st.slider("Max Volatility %",10,80,40)/100
            scr_period = st.selectbox("Period",["6mo","1y","2y"],index=1)
        with col3:
            min_sharpe = st.slider("Min Sharpe",0.0,3.0,0.5,0.1)

        if st.button("🔍 Run Screener"):
            with st.spinner("Screening..."):
                result = api("/screener/run",{"min_return":min_return,"max_volatility":max_vol,
                                              "min_sharpe":min_sharpe,"period":scr_period,"top_n":top_n})
            if result and "results" in result:
                st.success(f"**{result['passed']}** stocks passed out of **{result['total_screened']}** screened.")
                rows = result["results"]
                if rows:
                    df = pd.DataFrame(rows)
                    df.columns = [c.replace("_"," ").title() for c in df.columns]
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    fig, axes = plt.subplots(1,2, figsize=(14,4), facecolor="#1e293b")
                    tp = [r["ticker"] for r in rows[:10]]
                    for ax in axes:
                        ax.set_facecolor("#0f172a")
                        for s in ax.spines.values(): s.set_color("#334155")
                        ax.tick_params(colors="#94a3b8", labelsize=8)
                        ax.grid(color="#334155", linewidth=0.5, axis="x", linestyle="--")
                    axes[0].barh(tp,[r["annual_return_pct"] for r in rows[:10]], color=COLORS[:len(tp)])
                    axes[0].set_title("Annual Return %", color="#f8fafc")
                    axes[1].barh(tp,[r["sharpe_ratio"] for r in rows[:10]], color=COLORS[:len(tp)])
                    axes[1].set_title("Sharpe Ratio", color="#f8fafc")
                    plt.tight_layout()
                    st.pyplot(fig); plt.close()
                    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # NEWS SENTIMENT
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "📰 News Sentiment":
        st.markdown("# `📰 News Sentiment`")
        sent_tickers = st.text_input("Tickers","AAPL,MSFT,GOOGL,TSLA")
        if st.button("📰 Analyze"):
            tickers = [t.strip().upper() for t in sent_tickers.split(",") if t.strip()]
            with st.spinner("Analyzing news..."):
                result = api("/sentiment/analyze",{"tickers":tickers})
            if result:
                rows = [{"Ticker":t,"Sentiment":d["overall_sentiment"],"Score":f"{d['avg_score']:+.3f}",
                         "Articles":d["total_articles"],"Positive":d["positive_count"],
                         "Negative":d["negative_count"]} for t,d in result.items()]
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                fig, axes = plt.subplots(1,2, figsize=(14,4), facecolor="#1e293b")
                for ax in axes:
                    ax.set_facecolor("#0f172a")
                    for s in ax.spines.values(): s.set_color("#334155")
                    ax.tick_params(colors="#94a3b8", labelsize=8)
                    ax.grid(color="#334155", linewidth=0.5, axis="y", linestyle="--")
                t_labels = list(result.keys())
                scores = [result[t]["avg_score"] for t in t_labels]
                axes[0].bar(t_labels, scores,
                            color=["#10b981" if s>0.1 else "#ef4444" if s<-0.1 else "#f59e0b" for s in scores], width=0.5)
                axes[0].axhline(0, color="#334155", linewidth=1)
                axes[0].set_title("Sentiment Score", color="#f8fafc")
                x = range(len(t_labels))
                axes[1].bar(x, [result[t]["positive_count"] for t in t_labels], label="Positive", color="#10b981", width=0.25)
                axes[1].bar([i+0.25 for i in x], [result[t]["negative_count"] for t in t_labels], label="Negative", color="#ef4444", width=0.25)
                axes[1].bar([i+0.5 for i in x], [result[t]["neutral_count"] for t in t_labels], label="Neutral", color="#6b7280", width=0.25)
                axes[1].set_xticks([i+0.25 for i in x]); axes[1].set_xticklabels(t_labels)
                axes[1].set_title("Article Distribution", color="#f8fafc")
                axes[1].legend(fontsize=8, facecolor="#1e293b", edgecolor="#334155", labelcolor="#e5e7eb")
                plt.tight_layout()
                st.pyplot(fig); plt.close()
                st.markdown("</div>", unsafe_allow_html=True)

                for ticker, data in result.items():
                    if data["articles"]:
                        st.markdown(f"#### `{ticker}` Latest News")
                        for art in data["articles"][:5]:
                            e = "🟢" if art["sentiment"]=="Positive" else "🔴" if art["sentiment"]=="Negative" else "⚪"
                            st.markdown(f"{e} **{art['title']}**  \n<small>{art['source']} · {art['published']}</small>",
                                        unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ALERTS
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "🚨 Alerts":
        st.markdown("# `🚨 Smart Alerts`")
        col1,col2,col3 = st.columns(3)
        with col1: alert_ticker = st.text_input("Ticker","AAPL").upper()
        with col2: price_target = st.number_input("Price Target ($)", min_value=0.0, value=0.0)
        with col3: stop_loss = st.number_input("Stop Loss ($)", min_value=0.0, value=0.0)

        if st.button("🚨 Check Alerts"):
            with st.spinner("Checking..."):
                result = api("/alerts/check",{"ticker":alert_ticker,
                                              "price_target":price_target if price_target>0 else None,
                                              "stop_loss":stop_loss if stop_loss>0 else None})
            if result:
                c1,c2,c3 = st.columns(3)
                c1.metric("Price", f"${result['current_price']:,.2f}")
                c2.metric("Day Change", f"{result['day_change_pct']:+.2f}%")
                c3.metric("Active Alerts", result["alert_count"])
                for alert in result["alerts"]:
                    icons = {"SUCCESS":"✅","INFO":"ℹ️","WARNING":"⚠️","DANGER":"🚨"}
                    clr = {"SUCCESS":"#10b981","INFO":"#3b82f6","WARNING":"#f59e0b","DANGER":"#ef4444"}.get(alert["severity"],"#6b7280")
                    st.markdown(f"<div style='border-left:3px solid {clr};padding:8px 12px;margin:6px 0;"
                                f"background:#1e293b;border-radius:4px'>"
                                f"{icons.get(alert['severity'],'•')} <b>[{alert['type']}]</b> {alert['message']}</div>",
                                unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # MY PORTFOLIOS
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "📁 My Portfolios":
        st.markdown("# `📁 Saved Portfolios`")
        if st.button("🔄 Load My Portfolios"):
            with st.spinner("Loading..."):
                result = api("/portfolio/history", method="GET", auth=True)
            if result is not None:
                if not result:
                    st.info("No saved portfolios yet. Go to 🎯 Optimization and save one!")
                else:
                    for p in result:
                        with st.expander(f"📊 {p['name']} — {p['risk_level'].upper()} — ${p['investment_amount']:,.0f} — {p['created_at'][:10]}"):
                            c1,c2,c3 = st.columns(3)
                            c1.metric("Expected Return", f"{(p['expected_return'] or 0)*100:.2f}%")
                            c2.metric("Volatility", f"{(p['volatility'] or 0)*100:.2f}%")
                            c3.metric("Sharpe Ratio", f"{p['sharpe_ratio'] or 0:.3f}")
                            st.caption(f"Tickers: {', '.join(p['tickers'])}")
                            if p.get("allocation"):
                                df = pd.DataFrame(p["allocation"])
                                df.columns = ["Ticker","Weight %","$ Amount"]
                                st.dataframe(df.style.format({"Weight %":"{:.2f}%","$ Amount":"${:,.2f}"}),
                                             hide_index=True, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PROFILE
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "👤 Profile":
        st.markdown("# `👤 Profile`")
        with st.spinner("Loading profile..."):
            profile = api("/user/profile", method="GET", auth=True)
        if profile:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                st.markdown("### Account Info")
                st.metric("Name", profile["name"])
                st.metric("Email", profile["email"])
                st.metric("Portfolios Saved", profile["portfolio_count"])
                st.caption(f"Member since: {profile['created_at'][:10]}")
                st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ABOUT
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "ℹ️ About":
        st.markdown("# `ℹ️ About PortfolioAI Pro`")
        
        st.markdown("""
        <div class="custom-card" style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 1rem;">
                <div style='background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 12px; border-radius: 12px; display: inline-flex;'>
                    <span style='font-size: 1.5rem; line-height: 1;'>📊</span>
                </div>
                <h3 style="margin: 0;">Modern AI Financial Assistant</h3>
            </div>
            <p style="color: #cbd5e1; line-height: 1.6; font-size: 1.05rem;">
                A production-ready financial portfolio recommendation system. 
                Leveraging FastAPI for high-performance backend processing, machine learning for predictions, and a modern, fully responsive SaaS UI.
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
            <div class="custom-card">
                <h4 style="display: flex; align-items: center; gap: 8px;"><span>🧠</span> AI Price Prediction</h4>
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Ensemble models (Random Forest + Linear Regression) to predict short-term price movement and direction.</p>
            </div>
            <div class="custom-card">
                <h4 style="display: flex; align-items: center; gap: 8px;"><span>🎯</span> Portfolio Optimization</h4>
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Efficient Frontier allocation with scipy SLSQP targeting your chosen risk level to maximize Sharpe Ratio.</p>
            </div>
            <div class="custom-card">
                <h4 style="display: flex; align-items: center; gap: 8px;"><span>📰</span> News Sentiment</h4>
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">NLP-based sentiment scoring on the latest financial news to gauge overall market mood.</p>
            </div>
            <div class="custom-card">
                <h4 style="display: flex; align-items: center; gap: 8px;"><span>⚡</span> Technical Analysis</h4>
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Real-time RSI, MACD, and Bollinger Bands tracking with automated buy/sell/hold signal generation.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("`PortfolioAI Pro v3.0` · FastAPI + Python Backend · Not financial advice")

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.token:
    show_dashboard()
elif st.session_state.page == "register":
    show_register()
else:
    show_login()
