from __future__ import annotations

import streamlit as st

from lnphub_ui import configure_page, render_top_nav


configure_page("Documentation")
render_top_nav("Documentation")

st.title("Documentation")
st.caption("Working notes for users who want to explore, reproduce, or extend LNP-Hub.")

st.markdown(
    """
    ### Quick Start

    Use **Start** to filter the dataset, search by lipid identifiers or SMILES,
    open lipid-level pages, plot numeric readouts, and download filtered records.

    ### Local Development

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    streamlit run streamlit_app.py
    ```

    ### Data File

    The app currently reads `data/LNPhub_public_two_studies.csv`.
    Keep the same core column names when replacing the sample with the full curated dataset.

    ### Molecule Rendering

    RDKit parses `il_smiles` values and renders ionizable lipid structures on the
    Lipid Viewer page. Rows with missing or unparsable SMILES are handled gracefully.
    """
)

st.markdown("### Core Pages")
st.page_link("streamlit_app.py", label="Home")
st.page_link("pages/2_Start.py", label="Start")
st.page_link("pages/3_Data_Catalog.py", label="Data Catalog")
st.page_link("pages/1_Lipid_Viewer.py", label="Lipid Viewer")
