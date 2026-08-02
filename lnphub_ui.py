from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


APP_NAME = "LNP-Hub"
LOGO_PATH = Path("assets/logo2_2.png")
WEBPAGE_ICON_PATH = Path("assets/webpage_icon.png")
BANNER_PATH = Path("assets/banner_head.png")
LAYERS_PATH = Path("assets/layers.png")
SLACK_ICON_PATH = Path("assets/icon_slack.png")
GITHUB_ICON_PATH = Path("assets/icon_github.png")
SLACK_URL = "https://join.slack.com/t/lnp-hub/shared_invite/zt-45ilvt7wm-~jd~__6p4Lo14Hd~XgUHew"
GITHUB_URL = "https://github.com/Maburidi/LNPhub_web"

NAV_ITEMS = [
    ("Home", "./?page=Home"),
    ("Overview", "./?page=Overview"),
    ("Datasets", "./?page=Datasets"),
    ("Lipid Viewer", "./?page=Lipid%20Viewer"),
    ("Documentation", "./?page=Documentation"),
    ("About", "./?page=About"),
]


def configure_page(page_title: str) -> None:
    st.set_page_config(
        page_title=f"{page_title} | {APP_NAME}",
        page_icon=str(WEBPAGE_ICON_PATH) if WEBPAGE_ICON_PATH.exists() else ":test_tube:",
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
                position: relative;
            }

            .lnp-topbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 18px;
                background: linear-gradient(135deg, #063638, #0b5558 56%, #083f43);
                border: 1px solid rgba(127, 212, 202, 0.34);
                border-radius: 8px;
                box-shadow: 0 12px 34px rgba(0, 106, 113, 0.2);
                margin: 0;
                padding: 6px 56px 6px 8px;
                position: sticky;
                top: 0;
                z-index: 50;
                backdrop-filter: blur(14px);
                margin-bottom: 0;
            }

            .lnp-brand-mark {
                display: flex;
                align-items: center;
                flex: 0 0 auto;
                height: 38px;
                justify-content: center;
                text-decoration: none;
            }

            .lnp-brand-mark img {
                display: block;
                height: 38px;
                object-fit: contain;
                width: 128px;
            }

            .lnp-nav {
                display: flex;
                flex-wrap: wrap;
                justify-content: flex-start;
                gap: 5px;
                margin-right: auto;
            }

            .lnp-nav a {
                color: rgba(231, 255, 250, 0.86);
                text-decoration: none;
                font-size: 0.94rem;
                font-weight: 700;
                min-height: 42px;
                padding: 10px 14px;
                border-radius: 6px;
                border: 1px solid transparent;
                box-sizing: border-box;
                transition: background 140ms ease, color 140ms ease, box-shadow 140ms ease;
            }

            .lnp-nav a:hover {
                background: rgba(127, 212, 202, 0.13);
                color: #dffff9;
            }

            .lnp-nav a.active {
                background: linear-gradient(135deg, #d7f2ee, #83dfd2);
                color: #063638;
                box-shadow: 0 7px 18px rgba(131, 223, 210, 0.34);
            }

            .lnp-topbar-github {
                align-items: center;
                display: inline-flex;
                justify-content: center;
                line-height: 0;
                margin-left: 6px;
                text-decoration: none;
                transition: filter 150ms ease, transform 150ms ease;
            }

            .lnp-topbar-github:hover {
                filter:
                    drop-shadow(0 8px 9px rgba(0, 20, 22, 0.6))
                    drop-shadow(0 0 10px rgba(127, 212, 202, 0.48));
                transform: translateY(-1px);
            }

            .lnp-topbar-github img {
                display: block;
                filter:
                    drop-shadow(0 7px 7px rgba(0, 20, 22, 0.7))
                    drop-shadow(0 0 9px rgba(127, 212, 202, 0.52));
                height: 34px;
                width: 34px;
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

            .lnp-social-links {
                align-items: center;
                display: flex;
                gap: 10px;
            }

            .lnp-banner-social-links {
                margin-left: 34px;
                margin-top: 14px;
            }

            .lnp-slack-button,
            .lnp-github-button {
                align-items: center;
                background: transparent;
                border: 0;
                box-shadow: none;
                display: inline-flex;
                height: auto;
                justify-content: center;
                padding: 0;
                text-decoration: none;
                transition: filter 150ms ease, transform 150ms ease;
                width: auto;
            }

            .lnp-slack-button:hover,
            .lnp-github-button:hover {
                filter:
                    drop-shadow(0 10px 12px rgba(0, 35, 38, 0.55))
                    drop-shadow(0 0 12px rgba(0, 126, 121, 0.48));
                transform: translateY(-2px);
            }

            .lnp-slack-button img {
                display: block;
                filter:
                    drop-shadow(0 10px 9px rgba(0, 30, 32, 0.78))
                    drop-shadow(0 3px 3px rgba(0, 0, 0, 0.34))
                    drop-shadow(0 0 12px rgba(0, 126, 121, 0.58));
                height: 92px;
                width: 92px;
            }

            .lnp-github-button img {
                display: block;
                filter:
                    drop-shadow(0 10px 9px rgba(0, 30, 32, 0.78))
                    drop-shadow(0 3px 3px rgba(0, 0, 0, 0.34))
                    drop-shadow(0 0 12px rgba(0, 126, 121, 0.58));
                height: 60px;
                width: 60px;
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
                text-align: center;
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
                text-align: center;
                z-index: 1;
            }

            .lnp-section-divider {
                background: linear-gradient(90deg, rgba(0, 106, 113, 0), rgba(0, 106, 113, 0.42), rgba(127, 212, 202, 0.72), rgba(0, 106, 113, 0));
                height: 2px;
                margin: 0 auto 30px;
                width: 100%;
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

            .lnp-layers-section {
                margin: 12px 0 36px;
                width: 100%;
            }

            .lnp-layers-figure {
                animation: lnp-layer-rise 700ms ease-out both;
                margin: 0 auto;
                max-width: 1280px;
                position: relative;
            }

            .lnp-layers-figure img {
                display: block;
                height: auto;
                width: 100%;
            }

            .lnp-layers-caption {
                color: #3f4647;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(1rem, 1.2vw, 1.18rem);
                font-weight: 300;
                line-height: 1.6;
                margin: 22px auto 0;
                max-width: none;
                text-align: center;
                width: 100%;
            }

            @keyframes lnp-layer-rise {
                from {
                    opacity: 0;
                    transform: translateY(12px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .lnp-studies-section {
                margin: 0 0 42px;
                width: 100%;
            }

            .lnp-section-heading {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(1.55rem, 2.1vw, 2.25rem);
                font-weight: 400;
                letter-spacing: 0;
                line-height: 1.16;
                margin: 0 0 8px;
                text-align: center;
            }

            .lnp-section-subtitle {
                color: #3f4647;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 1rem;
                font-weight: 300;
                line-height: 1.45;
                margin: 0 auto 18px;
                max-width: 880px;
                text-align: center;
            }

            .lnp-study-table-wrap {
                background:
                    linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(215, 242, 238, 0.72)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.16);
                border-radius: 8px;
                box-shadow:
                    0 18px 42px rgba(0, 106, 113, 0.11),
                    inset 0 1px 0 rgba(255, 255, 255, 0.86);
                overflow-x: auto;
                position: relative;
                width: 100%;
            }

            .lnp-study-table-wrap::before {
                background: linear-gradient(90deg, rgba(0, 106, 113, 0), rgba(127, 212, 202, 0.88), rgba(0, 106, 113, 0));
                content: "";
                height: 3px;
                left: 0;
                position: absolute;
                right: 0;
                top: 0;
            }

            .lnp-study-table {
                border-collapse: collapse;
                color: #253f43;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 0.96rem;
                min-width: 860px;
                width: 100%;
            }

            .lnp-study-table th {
                background: rgba(6, 54, 56, 0.96);
                color: rgba(231, 255, 250, 0.96);
                font-size: 0.78rem;
                font-weight: 650;
                letter-spacing: 0.06em;
                padding: 15px 18px;
                text-align: left;
            }

            .lnp-study-table th:nth-child(n+3),
            .lnp-study-table td:nth-child(n+3) {
                text-align: center;
                white-space: nowrap;
            }

            .lnp-study-table td {
                border-top: 1px solid rgba(0, 106, 113, 0.11);
                padding: 16px 18px;
                vertical-align: middle;
            }

            .lnp-study-table tbody tr {
                transition: background 160ms ease, transform 160ms ease;
            }

            .lnp-study-table tbody tr:hover {
                background: rgba(215, 242, 238, 0.54);
                transform: translateY(-1px);
            }

            .lnp-study-id {
                color: #006a71;
                font-weight: 650;
                white-space: nowrap;
            }

            .lnp-paper-link {
                color: #063638;
                font-weight: 420;
                text-decoration: none;
            }

            .lnp-paper-link:hover {
                color: #006a71;
                text-decoration: underline;
                text-underline-offset: 4px;
            }

            .lnp-study-count {
                color: #063638;
                font-size: 1.1rem;
                font-weight: 500;
            }

            .lnp-footer {
                background:
                    linear-gradient(135deg, #063638, #0b5558 58%, #083f43);
                border: 1px solid rgba(127, 212, 202, 0.22);
                border-radius: 8px;
                box-shadow: 0 18px 44px rgba(0, 106, 113, 0.18);
                color: rgba(231, 255, 250, 0.9);
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                margin: 38px 0 8px;
                overflow: hidden;
                padding: 24px 28px 18px;
                position: relative;
            }

            .lnp-footer::before {
                background: linear-gradient(90deg, rgba(0, 106, 113, 0), rgba(127, 212, 202, 0.84), rgba(0, 106, 113, 0));
                content: "";
                height: 3px;
                left: 0;
                position: absolute;
                right: 0;
                top: 0;
            }

            .lnp-footer-main {
                align-items: center;
                display: flex;
                gap: 24px;
                justify-content: space-between;
            }

            .lnp-footer-brand {
                align-items: center;
                display: flex;
                gap: 14px;
                min-width: 0;
            }

            .lnp-footer-logo {
                background-position: center;
                background-repeat: no-repeat;
                background-size: contain;
                flex: 0 0 auto;
                height: 46px;
                width: 150px;
            }

            .lnp-footer-copy {
                max-width: 680px;
            }

            .lnp-footer-title {
                color: #e7fffa;
                font-size: 1.05rem;
                font-weight: 520;
                line-height: 1.1;
                margin: 0 0 5px;
            }

            .lnp-footer-text {
                color: rgba(231, 255, 250, 0.76);
                font-size: 0.92rem;
                font-weight: 300;
                line-height: 1.45;
                margin: 0;
            }

            .lnp-footer-links {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                justify-content: flex-end;
            }

            .lnp-footer-links a {
                border: 1px solid rgba(127, 212, 202, 0.24);
                border-radius: 999px;
                color: #dffff9;
                font-size: 0.86rem;
                padding: 7px 11px;
                text-decoration: none;
                transition: background 140ms ease, border-color 140ms ease, color 140ms ease;
            }

            .lnp-footer-links a:hover {
                background: rgba(127, 212, 202, 0.14);
                border-color: rgba(127, 212, 202, 0.48);
                color: #ffffff;
            }

            .lnp-footer .lnp-social-links {
                gap: 8px;
            }

            .lnp-footer .lnp-slack-button,
            .lnp-footer .lnp-github-button {
                background: transparent;
                border: 0;
                box-shadow: none;
                height: auto;
                padding: 0;
                width: auto;
            }

            .lnp-footer .lnp-slack-button:hover,
            .lnp-footer .lnp-github-button:hover {
                background: transparent;
                box-shadow: none;
                filter:
                    drop-shadow(0 10px 12px rgba(0, 0, 0, 0.54))
                    drop-shadow(0 0 12px rgba(127, 212, 202, 0.44));
            }

            .lnp-footer .lnp-slack-button img {
                height: 48px;
                width: 48px;
            }

            .lnp-footer .lnp-github-button img {
                height: 38px;
                width: 38px;
            }

            .lnp-footer-bottom {
                align-items: center;
                border-top: 1px solid rgba(127, 212, 202, 0.16);
                color: rgba(231, 255, 250, 0.62);
                display: flex;
                flex-wrap: wrap;
                font-size: 0.82rem;
                gap: 10px;
                justify-content: space-between;
                line-height: 1.35;
                margin-top: 20px;
                padding-top: 14px;
            }

            .lnp-footer-bottom a {
                color: #dffff9;
                text-decoration: none;
            }

            .lnp-footer-bottom a:hover {
                color: #ffffff;
                text-decoration: underline;
            }

            .lnp-footer-contact {
                text-align: right;
            }

            div[data-testid="stRadio"] {
                background:
                    linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(215, 242, 238, 0.58)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.16);
                border-radius: 8px;
                box-shadow: 0 14px 32px rgba(0, 106, 113, 0.1);
                margin: 2px 0 24px;
                padding: 12px;
            }

            div[data-testid="stRadio"] [role="radiogroup"] {
                display: grid;
                gap: 8px;
                grid-template-columns: repeat(2, minmax(220px, 1fr));
            }

            div[data-testid="stRadio"] label {
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(0, 106, 113, 0.1);
                border-radius: 7px;
                color: #123f43;
                justify-content: center;
                padding: 10px 12px;
                text-align: center;
                transition: background 150ms ease, border-color 150ms ease, box-shadow 150ms ease, transform 150ms ease;
            }

            div[data-testid="stRadio"] label:has(input:checked) {
                background: linear-gradient(135deg, #d7f2ee, #83dfd2);
                border-color: rgba(0, 106, 113, 0.36);
                box-shadow: 0 10px 24px rgba(0, 106, 113, 0.15);
            }

            div[data-testid="stRadio"] label:hover {
                background: rgba(215, 242, 238, 0.82);
                border-color: rgba(0, 106, 113, 0.28);
                box-shadow: 0 8px 18px rgba(0, 106, 113, 0.1);
                transform: translateY(-1px);
            }

            div[data-testid="stRadio"] input:checked + div {
                color: #063638;
                font-weight: 760;
            }

            .lnp-dataset-placeholder {
                background:
                    linear-gradient(145deg, rgba(255, 255, 255, 0.88), rgba(215, 242, 238, 0.68)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.18);
                border-radius: 8px;
                box-shadow: 0 18px 42px rgba(0, 106, 113, 0.12);
                padding: 28px;
            }

            .lnp-dataset-placeholder h3 {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 1.5rem;
                font-weight: 420;
                margin: 0 0 10px;
            }

            .lnp-dataset-placeholder p {
                color: #31585c;
                font-size: 1.02rem;
                line-height: 1.58;
                margin: 0;
            }

            .lnp-download-panel {
                animation: lnp-card-arrive 560ms ease-out both;
                background:
                    radial-gradient(circle at 16% 0%, rgba(127, 212, 202, 0.34), rgba(127, 212, 202, 0) 34%),
                    linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(215, 242, 238, 0.7)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.18);
                border-radius: 8px;
                box-shadow: 0 18px 42px rgba(0, 106, 113, 0.12);
                margin: 0 0 12px;
                overflow: hidden;
                padding: 22px 26px;
                position: relative;
            }

            .lnp-download-panel::after {
                animation: lnp-stat-sheen 5.5s ease-in-out infinite;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.7), transparent);
                content: "";
                inset: 0;
                pointer-events: none;
                position: absolute;
                transform: translateX(-120%);
                z-index: 0;
            }

            .lnp-download-panel > div {
                position: relative;
                z-index: 1;
            }

            .lnp-download-kicker {
                color: #006a71;
                font-size: 0.78rem;
                font-weight: 760;
                letter-spacing: 0.08em;
                margin: 0 0 6px;
                text-transform: uppercase;
            }

            .lnp-download-panel h3 {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 1.7rem;
                font-weight: 420;
                letter-spacing: 0;
                line-height: 1.16;
                margin: 0 0 8px;
            }

            .lnp-download-panel h3 + p {
                color: #31585c;
                font-size: 1rem;
                line-height: 1.5;
                margin: 0;
            }

            .lnp-download-action {
                align-items: center;
                background: linear-gradient(135deg, #063638, #0b5558 58%, #0b6d6f);
                border: 1px solid rgba(127, 212, 202, 0.38);
                border-radius: 7px;
                box-shadow: 0 12px 26px rgba(0, 106, 113, 0.2);
                color: #ffffff !important;
                display: inline-flex;
                font-size: 0.96rem;
                font-weight: 520;
                justify-content: center;
                margin-top: 18px;
                min-height: 44px;
                padding: 0 18px;
                position: relative;
                text-decoration: none !important;
                transition: box-shadow 150ms ease, filter 150ms ease, transform 150ms ease;
            }

            .lnp-download-action:hover {
                border-color: rgba(127, 212, 202, 0.66);
                box-shadow: 0 16px 32px rgba(0, 106, 113, 0.28);
                color: #ffffff !important;
                filter: brightness(1.06);
                text-decoration: none !important;
                transform: translateY(-1px);
            }

            .lnp-download-action:visited,
            .lnp-download-action:active {
                color: #ffffff !important;
                text-decoration: none !important;
            }

            .lnp-download-action-grid {
                display: flex;
                align-items: flex-start;
                flex-direction: column;
                gap: 12px;
                margin-top: 18px;
            }

            .lnp-download-action-grid .lnp-download-action {
                margin-top: 0;
            }

            div[data-testid="stDownloadButton"] {
                margin: 8px 0 24px;
            }

            div[data-testid="stDownloadButton"] button {
                background: linear-gradient(135deg, #063638, #0b5558 58%, #0b6d6f);
                border: 1px solid rgba(127, 212, 202, 0.38);
                border-radius: 7px;
                box-shadow: 0 12px 26px rgba(0, 106, 113, 0.2);
                color: #e7fffa;
                font-weight: 760;
                min-height: 44px;
                transition: box-shadow 150ms ease, filter 150ms ease, transform 150ms ease;
            }

            div[data-testid="stDownloadButton"] button:hover {
                border-color: rgba(127, 212, 202, 0.66);
                box-shadow: 0 16px 32px rgba(0, 106, 113, 0.28);
                color: #ffffff;
                filter: brightness(1.06);
                transform: translateY(-1px);
            }

            .lnp-filter-heading {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 1.45rem;
                font-weight: 420;
                letter-spacing: 0;
                line-height: 1.1;
                margin: -2px 0 14px;
            }

            .lnp-overview-intro {
                animation: lnp-card-arrive 560ms ease-out both;
                background:
                    radial-gradient(circle at 12% 0%, rgba(127, 212, 202, 0.34), rgba(127, 212, 202, 0) 34%),
                    linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(215, 242, 238, 0.64)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.16);
                border-radius: 8px;
                box-shadow: 0 18px 42px rgba(0, 106, 113, 0.11);
                margin: 0 0 22px;
                padding: 24px 28px;
                position: relative;
            }

            .lnp-overview-intro h1 {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(2rem, 3.4vw, 3.2rem);
                font-weight: 380;
                letter-spacing: 0;
                line-height: 1.05;
                margin: 0 0 10px;
            }

            .lnp-overview-intro p {
                color: #31585c;
                font-size: 1.05rem;
                line-height: 1.58;
                margin: 0;
                max-width: 1060px;
            }

            .lnp-chart-label {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 1.22rem;
                font-weight: 420;
                letter-spacing: 0;
                margin: 14px 0 4px;
            }

            .lnp-chart-note {
                color: #5c6b70;
                font-size: 0.9rem;
                line-height: 1.42;
                margin: 0 0 10px;
            }

            .lnp-component-grid {
                display: grid;
                gap: 14px;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                margin: 12px 0 26px;
            }

            .lnp-component-card {
                animation: lnp-card-arrive 520ms ease-out both;
                align-content: start;
                background:
                    linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(215, 242, 238, 0.58)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.15);
                border-radius: 8px;
                box-shadow: 0 12px 30px rgba(0, 106, 113, 0.09);
                display: grid;
                gap: 7px;
                min-height: 118px;
                overflow: hidden;
                padding: 17px 17px 16px 20px;
                position: relative;
            }

            .lnp-component-card::before {
                background: linear-gradient(180deg, rgba(0, 106, 113, 0.72), rgba(127, 212, 202, 0.72));
                bottom: 0;
                content: "";
                left: 0;
                position: absolute;
                top: 0;
                width: 4px;
            }

            .lnp-component-label {
                color: #006a71;
                font-size: 0.76rem;
                font-weight: 760;
                letter-spacing: 0.08em;
                margin: 0;
                text-transform: uppercase;
            }

            .lnp-component-card h4 {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 1.08rem;
                font-weight: 440;
                letter-spacing: 0;
                line-height: 1.22;
                margin: 0;
                overflow-wrap: anywhere;
            }

            .lnp-component-ratio {
                color: #42666a;
                font-size: 0.96rem;
                font-weight: 520;
                line-height: 1.35;
                margin: 0;
                overflow-wrap: anywhere;
            }

            .lnp-bio-panel {
                animation: lnp-card-arrive 560ms ease-out both;
                margin: 10px 0 24px;
                padding: 0;
                position: relative;
            }

            .lnp-bio-panel::after {
                display: none;
            }

            .lnp-bio-heading {
                position: relative;
                z-index: 1;
            }

            .lnp-bio-heading p {
                color: #006a71;
                font-size: 0.78rem;
                font-weight: 780;
                letter-spacing: 0.08em;
                margin: 0 0 5px;
                text-transform: uppercase;
            }

            .lnp-bio-heading h3 {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(1.4rem, 2.4vw, 2.05rem);
                font-weight: 420;
                letter-spacing: 0;
                line-height: 1.12;
                margin: 0 0 16px;
            }

            .lnp-bio-card-grid {
                display: grid;
                gap: 12px;
                grid-template-columns: repeat(auto-fit, minmax(270px, 360px));
                justify-content: start;
                position: relative;
                z-index: 1;
            }

            .lnp-bio-card {
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid rgba(0, 106, 113, 0.12);
                border-radius: 8px;
                box-shadow: 0 14px 30px rgba(0, 106, 113, 0.1);
                min-height: 210px;
                padding: 18px;
            }

            .lnp-bio-card p {
                color: #5c6b70;
                font-size: 0.74rem;
                font-weight: 720;
                letter-spacing: 0.07em;
                line-height: 1.2;
                margin: 0 0 8px;
                text-transform: uppercase;
            }

            .lnp-bio-card h4 {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: clamp(2rem, 3.2vw, 3.1rem);
                font-weight: 420;
                letter-spacing: 0;
                line-height: 1;
                margin: 0 0 12px;
                overflow-wrap: anywhere;
            }

            .lnp-bio-context {
                color: #42666a;
                font-size: 0.9rem;
                line-height: 1.42;
                min-height: 2.55rem;
                overflow-wrap: anywhere;
            }

            .lnp-bio-rank {
                align-items: baseline;
                border-top: 1px solid rgba(0, 106, 113, 0.12);
                display: flex;
                justify-content: space-between;
                gap: 10px;
                margin-top: 14px;
                padding-top: 12px;
            }

            .lnp-bio-rank span {
                color: #5c6b70;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }

            .lnp-bio-rank strong {
                color: #063638;
                font-size: 1rem;
                font-weight: 760;
            }

            .lnp-bio-ribbon {
                background: linear-gradient(90deg, rgba(18, 60, 105, 0.14), rgba(127, 212, 202, 0.24));
                border-radius: 999px;
                height: 10px;
                margin: 13px 0 8px;
                overflow: visible;
                position: relative;
            }

            .lnp-bio-ribbon span {
                background: linear-gradient(90deg, #006a71, #7fd4ca);
                border-radius: inherit;
                display: block;
                height: 100%;
                min-width: 2px;
            }

            .lnp-bio-ribbon i {
                background: #063638;
                border: 2px solid #ffffff;
                border-radius: 50%;
                box-shadow: 0 4px 10px rgba(0, 35, 38, 0.26);
                height: 16px;
                position: absolute;
                top: 50%;
                transform: translate(-50%, -50%);
                width: 16px;
            }

            .lnp-bio-footnote {
                color: #5c6b70;
                font-size: 0.8rem;
                line-height: 1.35;
            }

            .lnp-structure-frame {
                align-items: center;
                background:
                    radial-gradient(circle at 50% 30%, rgba(215, 242, 238, 0.55), rgba(255,255,255,0) 54%),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.13);
                border-radius: 8px;
                box-shadow: 0 16px 36px rgba(0, 106, 113, 0.1);
                display: flex;
                justify-content: center;
                min-height: 460px;
                overflow: auto;
                padding: 12px;
            }

            .lnp-structure-frame svg {
                max-width: 100%;
            }

            .lnp-filter-layer {
                animation: lnp-card-arrive 420ms ease-out both;
                margin: 0 0 14px;
                padding: 0;
            }

            .lnp-filter-group-divider {
                background: linear-gradient(90deg, rgba(0, 106, 113, 0), rgba(0, 106, 113, 0.66), rgba(127, 212, 202, 0.9), rgba(0, 106, 113, 0));
                content: "";
                height: 2px;
                margin: 20px 0 13px;
                width: 100%;
            }

            .lnp-filter-layer-kicker {
                color: #063638;
                font-family: "HelveticaNeue-Light", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 1.18rem;
                font-weight: 420;
                letter-spacing: 0;
                line-height: 1.2;
                margin: 0 0 5px;
            }

            div[data-testid="stMultiSelect"] {
                margin-bottom: 10px;
            }

            div[data-testid="stMultiSelect"] label p {
                color: #063638;
                font-weight: 700;
                letter-spacing: 0;
            }

            div[data-baseweb="select"] > div {
                border-color: rgba(0, 106, 113, 0.18);
                border-radius: 7px;
                box-shadow: 0 8px 18px rgba(0, 106, 113, 0.06);
                transition: border-color 150ms ease, box-shadow 150ms ease;
            }

            div[data-baseweb="select"] > div:hover {
                border-color: rgba(0, 106, 113, 0.36);
                box-shadow: 0 10px 22px rgba(0, 106, 113, 0.1);
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
                    align-items: center;
                    gap: 8px;
                    overflow-x: auto;
                    padding-right: 10px;
                    position: static;
                    white-space: nowrap;
                }

                .lnp-nav {
                    flex-wrap: nowrap;
                    justify-content: flex-start;
                    margin-right: 0;
                }

                .lnp-brand-mark img {
                    height: 30px;
                    width: 100px;
                }

                .lnp-topbar-github img {
                    height: 26px;
                    width: 26px;
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

                .lnp-banner-social-links {
                    margin-left: 18px;
                    margin-top: 8px;
                }

                .lnp-slack-button,
                .lnp-github-button {
                    height: auto;
                    padding: 0;
                    width: auto;
                }

                .lnp-slack-button img {
                    height: 58px;
                    width: 58px;
                }

                .lnp-github-button img {
                    height: 42px;
                    width: 42px;
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

                .lnp-layers-section {
                    margin-top: 4px;
                }

                .lnp-layers-caption {
                    font-size: 0.96rem;
                    line-height: 1.5;
                }

                .lnp-section-heading {
                    font-size: 1.35rem;
                }

                div[data-testid="stRadio"] [role="radiogroup"] {
                    grid-template-columns: 1fr;
                }

                .lnp-study-table {
                    font-size: 0.9rem;
                    min-width: 760px;
                }

                .lnp-footer {
                    padding: 20px 18px 16px;
                }

                .lnp-footer-main {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .lnp-footer-links {
                    justify-content: flex-start;
                }

                .lnp-footer-logo {
                    height: 38px;
                    width: 124px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav(active: str) -> None:
    logo = logo_data_uri()
    github_icon = image_data_uri(GITHUB_ICON_PATH)
    logo_html = f'<img src="{logo}" alt="LNP-Hub logo">' if logo else ""
    github_html = (
        f'<a class="lnp-topbar-github" href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer" aria-label="Open the LNP-Hub GitHub repository"><img src="{github_icon}" alt=""></a>'
        if github_icon
        else ""
    )
    links = "\n".join(
        f'<a class="{"active" if label == active else ""}" href="{href}" target="_self" rel="self">{label}</a>'
        for label, href in NAV_ITEMS
    )
    st.markdown(
        f"""
        <div class="lnp-topbar">
            <a class="lnp-brand-mark" href="./?page=Home" target="_self" rel="self" aria-label="LNP-Hub home">
                {logo_html}
            </a>
            <nav class="lnp-nav">
                {links}
            </nav>
            {github_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_menu_logo() -> None:
    slack_icon = image_data_uri(SLACK_ICON_PATH)
    slack_link = (
        f'<a class="lnp-menu-slack" href="{SLACK_URL}" target="_blank" rel="noopener noreferrer" aria-label="Join the LNP-Hub Slack community"><img src="{slack_icon}" alt=""></a>'
        if slack_icon
        else ""
    )
    floating_slack = (
        f'<div class="lnp-menu-social">{slack_link}</div>'
        if slack_link
        else ""
    )
    st.markdown(
        f"""
        <style>
            .lnp-menu-social {{
                align-items: center;
                display: flex;
                flex-direction: column;
                gap: 8px;
                position: fixed;
                bottom: 22px;
                right: 22px;
                z-index: 80;
            }}

            .lnp-menu-social a {{
                align-items: center;
                display: inline-flex;
                justify-content: center;
                line-height: 0;
                text-decoration: none;
                transition: filter 150ms ease, transform 150ms ease;
            }}

            .lnp-menu-social a:hover {{
                filter:
                    drop-shadow(0 8px 9px rgba(0, 20, 22, 0.6))
                    drop-shadow(0 0 10px rgba(127, 212, 202, 0.48));
                transform: translateY(-1px);
            }}

            .lnp-menu-slack img {{
                display: block;
                filter:
                    drop-shadow(0 7px 7px rgba(0, 20, 22, 0.7))
                    drop-shadow(0 0 9px rgba(127, 212, 202, 0.52));
                height: 118px;
                width: 118px;
            }}

            @media (max-width: 720px) {{
                .lnp-menu-social {{
                    bottom: 16px;
                    gap: 7px;
                    right: 16px;
                }}

                .lnp-menu-slack img {{
                    height: 84px;
                    width: 84px;
                }}
            }}
        </style>
        {floating_slack}
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


def render_layers_section() -> None:
    layers = image_data_uri(LAYERS_PATH)
    if not layers:
        return

    st.markdown(
        f"""
        <section class="lnp-layers-section">
            <figure class="lnp-layers-figure">
                <img src="{layers}" alt="LNP-Hub layered data framework">
            </figure>
            <p class="lnp-layers-caption">
                LNP-Hub organizes lipid nanoparticle data across five interconnected levels, progressing from
                provenance and molecular definition to experimental context, physicochemical characterization,
                delivery performance, toxicity, viability, and broader biological outcomes. This layered framework
                captures the full experimental landscape required to connect LNP composition with function, while
                also highlighting the increasing scarcity of high-quality data at advanced biological levels. By
                standardizing information across these layers, LNP-Hub provides a structured foundation for
                mechanistic analysis, predictive modeling, and AI-driven discovery of safer and more effective
                nucleic acid delivery systems.
            </p>
            <div class="lnp-section-divider"></div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    logo = logo_data_uri()
    slack_icon = image_data_uri(SLACK_ICON_PATH)
    github_icon = image_data_uri(GITHUB_ICON_PATH)
    logo_style = f' style="background-image: url(&quot;{logo}&quot;)"' if logo else ""
    slack_button = (
        f'<a class="lnp-slack-button" href="{SLACK_URL}" target="_blank" rel="noopener noreferrer" aria-label="Join the LNP-Hub Slack community"><img src="{slack_icon}" alt=""></a>'
        if slack_icon
        else ""
    )
    github_button = (
        f'<a class="lnp-github-button" href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer" aria-label="Open the LNP-Hub GitHub repository"><img src="{github_icon}" alt=""></a>'
        if github_icon
        else ""
    )
    social_links = (
        f'<div class="lnp-social-links">{slack_button}{github_button}</div>'
        if slack_button or github_button
        else ""
    )

    st.markdown(
        f"""
        <footer class="lnp-footer">
            <div class="lnp-footer-main">
                <div class="lnp-footer-brand">
                    <div class="lnp-footer-logo"{logo_style} aria-label="LNP-Hub logo"></div>
                    <div class="lnp-footer-copy">
                        <p class="lnp-footer-title">LNP-Hub</p>
                        <p class="lnp-footer-text">
                            A curated, machine-readable resource for lipid nanoparticle formulation,
                            delivery performance, and AI-driven mRNA therapeutic discovery.
                        </p>
                    </div>
                </div>
                <nav class="lnp-footer-links" aria-label="Footer navigation">
                    <a href="./?page=Home" target="_self" rel="self">Home</a>
                    <a href="./?page=Overview" target="_self" rel="self">Overview</a>
                    <a href="./?page=Datasets" target="_self" rel="self">Datasets</a>
                    <a href="./?page=Lipid%20Viewer" target="_self" rel="self">Lipid Viewer</a>
                    <a href="./?page=Documentation" target="_self" rel="self">Documentation</a>
                    {social_links}
                </nav>
            </div>
            <div class="lnp-footer-bottom">
                <span class="lnp-footer-contact">
                    <a href="https://www.nus.edu.sg/" target="_blank" rel="noopener noreferrer">National University of Singapore</a>
                    | <a href="https://zhanggroup.org/" target="_blank" rel="noopener noreferrer">Zhang's Lab</a>
                    | +65-6601-1241
                    | Computing 1, 13 Computing Drive, Singapore 117417
                    | <a href="mailto:maburidi@nus.edu.sg">maburidi@nus.edu.sg</a>
                </span>
            </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )
