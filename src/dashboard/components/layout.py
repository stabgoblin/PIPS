"""Reusable visual language for the planning dashboard."""
import streamlit as st


def apply_theme():
    st.markdown('''<style>
    .block-container {max-width: 1400px; padding-top: 2rem; padding-bottom: 3rem;}
    .pips-brand {display: flex; align-items: center; gap: 12px; padding: 6px 0 14px;}
    .pips-logo {display: grid; place-items: center; width: 40px; height: 40px;
        background: #167d8d; color: white; border-radius: 12px; font-weight: 800; font-size: 22px;}
    .pips-brand strong {font-size: 20px; letter-spacing: .08em;}
    .pips-tagline {display: block; font-size: 12px; color: #617582; margin-top: 1px;}
    .st-key-module_navigation {background: #f3f6f8; padding: 8px; border: 1px solid #e0e8ed;
        border-radius: 14px; margin-bottom: 24px;}
    .st-key-module_navigation button {min-height: 44px; border: 0; font-weight: 600;
        transition: background .15s ease, box-shadow .15s ease;}
    .st-key-module_navigation button[kind="secondary"] {background: transparent; color: #435b69;}
    .st-key-module_navigation button[kind="secondary"]:hover {background: #e2edef; color: #126573;}
    .st-key-module_navigation button[kind="primary"] {box-shadow: 0 3px 8px #167d8d26;}
    .st-key-module_navigation button:focus-visible {outline: 3px solid #65b6c2; outline-offset: 2px;}
    @media (max-width: 900px) {
        .st-key-module_navigation [data-testid="stHorizontalBlock"] {flex-wrap: wrap; gap: 6px;}
        .st-key-module_navigation [data-testid="stColumn"] {min-width: calc(33.33% - 6px); flex: 1 1 calc(33.33% - 6px);}
    }
    @media (max-width: 480px) {
        .st-key-module_navigation [data-testid="stColumn"] {min-width: calc(50% - 6px); flex-basis: calc(50% - 6px);}
        h1 {font-size: 1.8rem !important;}
    }
    h1 {letter-spacing: -.035em; font-size: 2.35rem !important;}
    h2, h3 {letter-spacing: -.02em;}
    [data-testid="stMetric"] {border: 1px solid #dce4e8; border-radius: 12px;
        padding: 16px 18px;}
    [data-testid="stMetricLabel"] {font-size: .85rem;}
    [data-testid="stSidebar"] {border-right: 1px solid #dce4e8;}
    .stButton > button, .stFormSubmitButton > button {border-radius: 8px;}
    </style>''', unsafe_allow_html=True)


def page_header(title, subtitle=""):
    st.title(title)
    if subtitle:
        st.write(subtitle)
    st.divider()


def show_result(result):
    status = result.get("status")
    message = result.get("message", "No response available")
    if status == "ok":
        st.success(message)
    elif status == "pending":
        st.info(message)
    else:
        st.error(message)


def sidebar_footer(api_base_url):
    st.caption("Plan capacity. Understand access. Compare locations.")
    with st.expander("Connection settings"):
        st.caption(f"API: {api_base_url}")
        st.caption("Use API Status to check the backend connection.")
