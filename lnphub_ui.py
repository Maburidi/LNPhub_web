from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


APP_NAME = "LNP-Hub"
LOGO_PATH = Path("assets/logo.png")

NAV_ITEMS = [
    ("Home", "./"),
    ("Start", "./Start"),
    ("Data", "./Data_Catalog"),
    ("Lipid Viewer", "./Lipid_Viewer"),
    ("Documentation", "./Documentation"),
    ("About", "./About"),
]


def configure_page(page_title: str) -> None:
    st.set_page_config(
        page_title=f"{page_title} | {APP_NAME}",
        page_icon=":test_tube:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()


@st.cache_data(show_spinner=False)
def logo_data_uri() -> str:
    if not LOGO_PATH.exists():
        return ""
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def inject_theme() -> None:
    st.markdown(
        """
        <style>
            :root {
                --lnp-ink: #172329;
                --lnp-muted: #5c6b70;
                --lnp-teal: #006a71;
                --lnp-cyan: #7fd4ca;
                --lnp-aqua: #d7f2ee;
                --lnp-blue: #123c69;
                --lnp-gold: #f3a261;
                --lnp-surface: #ffffff;
                --lnp-bg: #f7faf9;
                --lnp-border: #d9e5e2;
            }

            .stApp {
                background:
                    linear-gradient(180deg, rgba(215, 242, 238, 0.52), rgba(247, 250, 249, 0.72) 260px),
                    var(--lnp-bg);
                color: var(--lnp-ink);
            }

            header[data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"],
            [data-testid="collapsedControl"],
            section[data-testid="stSidebar"],
            [data-testid="stSidebarNav"] {
                display: none;
            }

            .block-container {
                padding-top: 0.35rem;
                max-width: 1180px;
            }

            .lnp-topbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 24px;
                padding: 10px 0 12px;
                margin-bottom: 0;
            }

            .lnp-brand {
                display: flex;
                align-items: center;
                gap: 12px;
                min-width: 218px;
                color: var(--lnp-ink);
                text-decoration: none;
            }

            .lnp-brand img {
                width: 58px;
                height: 58px;
                object-fit: cover;
                border-radius: 8px;
                box-shadow: 0 6px 18px rgba(0, 106, 113, 0.16);
            }

            .lnp-brand-text {
                display: flex;
                flex-direction: column;
                line-height: 1.05;
            }

            .lnp-brand-name {
                font-size: 1.06rem;
                font-weight: 760;
                letter-spacing: 0;
            }

            .lnp-brand-subtitle {
                margin-top: 5px;
                color: var(--lnp-muted);
                font-size: 0.78rem;
            }

            .lnp-nav {
                display: flex;
                flex-wrap: wrap;
                justify-content: flex-end;
                gap: 5px;
            }

            .lnp-nav a {
                color: var(--lnp-blue);
                text-decoration: none;
                font-size: 0.92rem;
                font-weight: 650;
                padding: 9px 12px;
                border-radius: 6px;
                border: 1px solid transparent;
            }

            .lnp-nav a:hover {
                background: rgba(0, 106, 113, 0.09);
                border-color: rgba(0, 106, 113, 0.18);
                color: var(--lnp-teal);
            }

            .lnp-nav a.active {
                color: #ffffff;
                background: linear-gradient(135deg, var(--lnp-teal), #218a83);
                border-color: var(--lnp-teal);
            }

            .stTabs [data-baseweb="tab-list"],
            .stTabs [role="tablist"] {
                align-items: center;
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(217, 229, 226, 0.95);
                border-radius: 8px;
                box-shadow: 0 10px 30px rgba(18, 60, 105, 0.08);
                display: flex;
                gap: 4px;
                margin: 0 0 24px;
                padding: 6px;
                position: sticky;
                top: 0;
                z-index: 50;
                backdrop-filter: blur(14px);
            }

            .stTabs [data-baseweb="tab"],
            .stTabs [role="tab"] {
                border-radius: 6px;
                color: var(--lnp-blue);
                font-weight: 700;
                min-height: 42px;
                padding: 0 14px;
                transition: background 140ms ease, color 140ms ease, box-shadow 140ms ease;
            }

            .stTabs [data-baseweb="tab"]:hover,
            .stTabs [role="tab"]:hover {
                background: rgba(0, 106, 113, 0.08);
                color: var(--lnp-teal);
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, var(--lnp-teal), #218a83);
                color: #ffffff;
                box-shadow: 0 6px 16px rgba(0, 106, 113, 0.22);
            }

            .stTabs [data-baseweb="tab-highlight"] {
                display: none;
            }

            .stTabs [role="tabpanel"] {
                padding-top: 2px;
            }

            .lnp-hero {
                padding: 42px 0 32px;
            }

            .lnp-kicker {
                color: var(--lnp-teal);
                font-weight: 750;
                text-transform: uppercase;
                font-size: 0.8rem;
                letter-spacing: 0.08em;
                margin-bottom: 10px;
            }

            .lnp-hero h1 {
                max-width: 880px;
                font-size: clamp(2.1rem, 5vw, 4.3rem);
                line-height: 1.02;
                letter-spacing: 0;
                margin: 0;
                color: var(--lnp-ink);
            }

            .lnp-lede {
                max-width: 760px;
                margin-top: 18px;
                color: var(--lnp-muted);
                font-size: 1.12rem;
                line-height: 1.65;
            }

            .lnp-band {
                padding: 30px 0;
                border-top: 1px solid var(--lnp-border);
            }

            .lnp-card-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
                gap: 14px;
                margin-top: 18px;
            }

            .lnp-card {
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid var(--lnp-border);
                border-radius: 8px;
                padding: 18px;
                box-shadow: 0 8px 28px rgba(18, 60, 105, 0.06);
            }

            .lnp-card h3 {
                margin: 0 0 8px;
                font-size: 1.02rem;
                color: var(--lnp-ink);
                letter-spacing: 0;
            }

            .lnp-card p {
                margin: 0;
                color: var(--lnp-muted);
                line-height: 1.55;
                font-size: 0.94rem;
            }

            @media (max-width: 720px) {
                .lnp-topbar {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .lnp-nav {
                    justify-content: flex-start;
                }

                .stTabs [data-baseweb="tab-list"],
                .stTabs [role="tablist"] {
                    overflow-x: auto;
                    position: static;
                    white-space: nowrap;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav(active: str) -> None:
    logo = logo_data_uri()
    logo_html = f'<img src="{logo}" alt="LNP-Hub logo">' if logo else ""
    links = "\n".join(
        f'<a class="{"active" if label == active else ""}" href="{href}" target="_self" rel="self">{label}</a>'
        for label, href in NAV_ITEMS
    )
    st.markdown(
        f"""
        <div class="lnp-topbar">
            <a class="lnp-brand" href="./" target="_self" rel="self">
                {logo_html}
                <span class="lnp-brand-text">
                    <span class="lnp-brand-name">LNP-Hub</span>
                    <span class="lnp-brand-subtitle">Curated nanoparticle commons</span>
                </span>
            </a>
            <nav class="lnp-nav">
                {links}
            </nav>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header() -> None:
    logo = logo_data_uri()
    logo_html = f'<img src="{logo}" alt="LNP-Hub logo">' if logo else ""
    st.markdown(
        f"""
        <div class="lnp-topbar">
            <a class="lnp-brand" href="./" target="_self" rel="self">
                {logo_html}
                <span class="lnp-brand-text">
                    <span class="lnp-brand-name">LNP-Hub</span>
                    <span class="lnp-brand-subtitle">Curated nanoparticle commons</span>
                </span>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
