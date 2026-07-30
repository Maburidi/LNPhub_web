from __future__ import annotations

import streamlit as st

from lnphub_ui import configure_page, render_top_nav


configure_page("About")
render_top_nav("About")

st.title("About LNP-Hub")
st.caption("A curated data commons for lipid nanoparticle formulation and delivery science.")

st.markdown(
    """
    LNP-Hub is being built as a public web portal for curated lipid nanoparticle
    records across studies, chemistries, formulations, biological models, and
    delivery readouts.

    The current version focuses on making the sample dataset easy to inspect:
    users can filter records, search identifiers and SMILES, render molecule
    structures, explore numeric trends, and export the result set.
    """
)

st.markdown(
    """
    <section class="lnp-band">
        <div class="lnp-card-grid">
            <div class="lnp-card">
                <h3>Purpose</h3>
                <p>Make curated LNP formulation records discoverable and reusable for experimental and computational work.</p>
            </div>
            <div class="lnp-card">
                <h3>Audience</h3>
                <p>Researchers working across delivery, lipid chemistry, RNA therapeutics, and machine learning.</p>
            </div>
            <div class="lnp-card">
                <h3>Status</h3>
                <p>This is an early public portal scaffold. The Home page and documentation will be expanded next.</p>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)
