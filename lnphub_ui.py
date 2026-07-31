from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


APP_NAME = "LNP-Hub"
LOGO_PATH = Path("assets/logo2_2.png")
BANNER_PATH = Path("assets/banner_head.png")

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
        initial_sidebar_state="collapsed",
    )
    inject_theme()


def logo_data_uri() -> str:
    if not LOGO_PATH.exists():
        return ""
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def image_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
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
                padding-top: 0;
                padding-left: 1.4rem;
                padding-right: 1.4rem;
                max-width: 1540px;
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
                background: linear-gradient(135deg, #063638, #0b5558 56%, #083f43);
                border: 1px solid rgba(127, 212, 202, 0.34);
                border-radius: 8px;
                box-shadow: 0 12px 34px rgba(0, 106, 113, 0.2);
                display: flex;
                gap: 4px;
                margin: 0;
                padding: 6px;
                position: sticky;
                top: 0;
                z-index: 50;
                backdrop-filter: blur(14px);
            }

            .stTabs [data-baseweb="tab"],
            .stTabs [role="tab"] {
                border-radius: 6px;
                color: rgba(231, 255, 250, 0.86);
                font-weight: 700;
                min-height: 42px;
                padding: 0 14px;
                transition: background 140ms ease, color 140ms ease, box-shadow 140ms ease;
            }

            .stTabs [data-baseweb="tab"]:hover,
            .stTabs [role="tab"]:hover {
                background: rgba(127, 212, 202, 0.13);
                color: #dffff9;
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #d7f2ee, #83dfd2);
                color: #063638;
                box-shadow: 0 7px 18px rgba(131, 223, 210, 0.34);
            }

            .stTabs [data-baseweb="tab-highlight"] {
                display: none;
            }

            .stTabs [role="tabpanel"] {
                padding-top: 0;
            }

            .lnp-home-banner {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(217, 229, 226, 0.88);
                border-radius: 8px;
                box-shadow: 0 14px 32px rgba(0, 106, 113, 0.1);
                margin: 0 0 24px;
                overflow: hidden;
                position: relative;
            }

            .lnp-home-banner img {
                display: block;
                height: auto;
                width: 100%;
            }

            .lnp-banner-copy {
                color: #3f4647;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                left: 184px;
                position: absolute;
                top: 34px;
            }

            .lnp-banner-copy h1 {
                color: #3f4647;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(1.8rem, 3.35vw, 3.55rem);
                font-weight: 300;
                letter-spacing: 0;
                line-height: 0.88;
                margin: 0;
            }

            .lnp-banner-copy p {
                color: #3f4647;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(1.05rem, 1.95vw, 1.8rem);
                font-weight: 300;
                line-height: 1.08;
                margin: -3px 0 0;
                max-width: 720px;
            }

            .lnp-portal-tagline {
                animation: lnp-tagline-rise 650ms ease-out both;
                background: transparent;
                border: 0;
                color: #063638 !important;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
                font-size: 1.92rem !important;
                font-weight: 400 !important;
                letter-spacing: 0 !important;
                line-height: 1.22 !important;
                margin: -2px auto 28px !important;
                max-width: 1240px;
                padding: 0 12px 14px;
                position: relative;
                text-align: center;
                text-shadow: 0 8px 22px rgba(0, 106, 113, 0.12);
            }

            .lnp-portal-tagline::after {
                animation: lnp-tagline-glow 4.5s ease-in-out infinite;
                background: linear-gradient(90deg, rgba(0, 106, 113, 0), rgba(0, 106, 113, 0.68), rgba(127, 212, 202, 0.95), rgba(0, 106, 113, 0));
                bottom: 0;
                content: "";
                height: 2px;
                left: 22%;
                position: absolute;
                right: 22%;
            }

            .lnp-portal-tagline::before {
                display: none;
            }

            @keyframes lnp-tagline-rise {
                from {
                    opacity: 0;
                    transform: translateY(8px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes lnp-tagline-glow {
                0%, 100% {
                    opacity: 0.42;
                    transform: scaleX(0.72);
                }
                50% {
                    opacity: 1;
                    transform: scaleX(1);
                }
            }

            .lnp-ai-intro {
                color: #3f4647;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(1.02rem, 1.3vw, 1.28rem);
                font-weight: 300;
                line-height: 1.58;
                margin: -4px 0 28px;
                max-width: none;
                width: 100%;
            }

            .lnp-foundation-box {
                background:
                    linear-gradient(135deg, rgba(215, 242, 238, 0.92), rgba(255, 255, 255, 0.82) 56%, rgba(127, 212, 202, 0.28)),
                    #effbf8;
                border: 1px solid rgba(0, 106, 113, 0.18);
                border-radius: 8px;
                box-shadow:
                    0 18px 42px rgba(0, 106, 113, 0.12),
                    inset 0 1px 0 rgba(255, 255, 255, 0.82);
                color: #254447;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(1rem, 1.2vw, 1.18rem);
                font-weight: 300;
                line-height: 1.62;
                margin: 0 0 30px;
                overflow: hidden;
                padding: 24px 28px 24px 34px;
                position: relative;
                width: 100%;
            }

            .lnp-foundation-box::before {
                background: linear-gradient(180deg, #006a71, #7fd4ca);
                bottom: 18px;
                content: "";
                left: 16px;
                position: absolute;
                top: 18px;
                width: 4px;
            }

            .lnp-foundation-box::after {
                background: radial-gradient(circle, rgba(127, 212, 202, 0.28), rgba(127, 212, 202, 0));
                content: "";
                height: 170px;
                position: absolute;
                right: -70px;
                top: -85px;
                width: 170px;
            }

            .lnp-foundation-box p {
                margin: 0;
                position: relative;
                z-index: 1;
            }

            .lnp-stat-grid {
                display: grid;
                gap: 16px;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                margin: 0 0 30px;
            }

            .lnp-stat-tile {
                animation: lnp-stat-float 5.2s ease-in-out infinite;
                background:
                    linear-gradient(145deg, rgba(255, 255, 255, 0.92), rgba(215, 242, 238, 0.82)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.16);
                border-radius: 8px;
                box-shadow:
                    0 16px 34px rgba(0, 106, 113, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.86);
                min-height: 128px;
                overflow: hidden;
                padding: 22px 18px 20px;
                position: relative;
                text-align: center;
            }

            .lnp-stat-tile:nth-child(2) {
                animation-delay: 0.25s;
            }

            .lnp-stat-tile:nth-child(3) {
                animation-delay: 0.5s;
            }

            .lnp-stat-tile:nth-child(4) {
                animation-delay: 0.75s;
            }

            .lnp-stat-tile::before {
                background: linear-gradient(90deg, rgba(0, 106, 113, 0), rgba(127, 212, 202, 0.55), rgba(0, 106, 113, 0));
                content: "";
                height: 3px;
                left: 18%;
                position: absolute;
                right: 18%;
                top: 0;
            }

            .lnp-stat-tile::after {
                animation: lnp-stat-sheen 6.5s ease-in-out infinite;
                background: linear-gradient(110deg, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.56), rgba(255, 255, 255, 0));
                content: "";
                height: 180%;
                left: -72%;
                position: absolute;
                top: -40%;
                transform: rotate(12deg);
                width: 44%;
            }

            .lnp-stat-label {
                color: #006a71;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 0.82rem;
                font-weight: 650;
                letter-spacing: 0.08em;
                line-height: 1.2;
                margin-bottom: 12px;
                position: relative;
                z-index: 1;
            }

            .lnp-stat-value {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(2.15rem, 3.2vw, 3.45rem);
                font-weight: 300;
                letter-spacing: 0;
                line-height: 1;
                position: relative;
                z-index: 1;
            }

            @keyframes lnp-stat-float {
                0%, 100% {
                    box-shadow:
                        0 16px 34px rgba(0, 106, 113, 0.1),
                        inset 0 1px 0 rgba(255, 255, 255, 0.86);
                    transform: translateY(0);
                }
                50% {
                    box-shadow:
                        0 22px 42px rgba(0, 106, 113, 0.16),
                        inset 0 1px 0 rgba(255, 255, 255, 0.9);
                    transform: translateY(-4px);
                }
            }

            @keyframes lnp-stat-sheen {
                0%, 45% {
                    left: -72%;
                }
                70%, 100% {
                    left: 128%;
                }
            }

            .lnp-hero {
                padding: 20px 0 30px;
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
                color: #063638;
                font-weight: 820;
            }

            .lnp-hero p.lnp-lede {
                max-width: 760px;
                margin-top: 12px;
                color: #123f43 !important;
                font-size: clamp(1.18rem, 2vw, 1.7rem) !important;
                font-weight: 650 !important;
                line-height: 1.42 !important;
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
                .block-container {
                    padding-left: 0.75rem;
                    padding-right: 0.75rem;
                }

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

                .lnp-banner-copy {
                    left: 32px;
                    top: 8px;
                }

                .lnp-banner-copy h1 {
                    font-size: 1.55rem;
                }

                .lnp-banner-copy p {
                    font-size: 0.85rem;
                    margin-top: -2px;
                    max-width: 260px;
                }

                .lnp-portal-tagline {
                    font-size: 1.12rem;
                    margin: -8px auto 14px;
                }

                .lnp-ai-intro {
                    font-size: 0.98rem;
                    line-height: 1.5;
                    margin-top: -8px;
                }

                .lnp-foundation-box {
                    font-size: 0.96rem;
                    line-height: 1.5;
                    padding: 18px 18px 18px 28px;
                }

                .lnp-stat-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }

                .lnp-stat-tile {
                    min-height: 112px;
                    padding: 18px 12px 16px;
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


def inject_menu_logo() -> None:
    logo = logo_data_uri()
    if not logo:
        return

    top_tablist_selector = (
        '[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] '
        '> [data-testid="stTabs"] > div:first-child > div:first-child '
        '> [role="tablist"]'
    )

    st.markdown(
        f"""
        <style>
            {top_tablist_selector}::before {{
                background-image: url("{logo}");
                background-position: center;
                background-repeat: no-repeat;
                background-size: contain;
                content: "";
                display: inline-block;
                flex: 0 0 auto;
                height: 38px;
                margin: 0 12px 0 4px;
                width: 128px;
            }}

            @media (max-width: 720px) {{
                {top_tablist_selector}::before {{
                    height: 30px;
                    margin-right: 8px;
                    width: 100px;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home_banner() -> None:
    banner = image_data_uri(BANNER_PATH)
    if not banner:
        return

    st.markdown(
        f"""
        <div class="lnp-home-banner">
            <img src="{banner}" alt="LNP-Hub header banner">
            <div class="lnp-banner-copy">
                <h1>Lipid Nanoparticles Hub</h1>
                <p>Artificial Intelligence for mRNA Therapeutic Science</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
