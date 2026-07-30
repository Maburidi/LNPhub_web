from __future__ import annotations

import pandas as pd
import streamlit as st

from lnphub_ui import configure_page, render_top_nav


DATA_PATH = "data/LNPhub_public_two_studies.csv"

COLUMN_GROUPS = {
    "Study and records": ["record_id", "study_id", "publication_link", "lnp_id"],
    "Ionizable lipid chemistry": [
        "il_id",
        "il_smiles",
        "il_class",
        "il_subclass",
        "il_architecture_type",
        "il_head_class",
        "il_linker_class",
        "il_tail_count",
    ],
    "Formulation": [
        "helper_lipid_name",
        "helper_lipid_molratio",
        "cholesterol_name",
        "cholesterol_molratio",
        "peg_lipid_name",
        "peg_lipid_molratio",
        "il_molratio",
    ],
    "Biology and delivery": [
        "cargo_type",
        "route_of_administration",
        "model",
        "model_type",
        "model_target",
        "delivery_value",
        "delivery_value_method",
    ],
    "Physicochemical measurements": [
        "particle_size_nm",
        "pdi",
        "zeta_potential_mv",
        "encapsulation_efficiency_percent",
        "measured_pka",
    ],
    "Molecular descriptors": [
        "molecular_weight",
        "heavy_atoms",
        "rings",
        "rotatable_bonds",
        "topological_polar_surface_area",
        "logp",
        "molar_refractivity",
    ],
}


configure_page("Data")
render_top_nav("Data")


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def non_empty_count(df: pd.DataFrame, column: str) -> int:
    values = df[column].dropna().astype(str)
    return int((values.str.strip() != "").sum())


data = load_data()

st.title("Data Catalog")
st.caption("Coverage summary for the current public sample bundled with the portal.")

metric_cols = st.columns(4)
metric_cols[0].metric("Records", f"{len(data):,}")
metric_cols[1].metric("Columns", f"{len(data.columns):,}")
metric_cols[2].metric("Studies", f"{data['study_id'].nunique():,}" if "study_id" in data else "0")
metric_cols[3].metric("Lipids", f"{data['il_id'].nunique():,}" if "il_id" in data else "0")

st.markdown("### Column Groups")
for group_name, columns in COLUMN_GROUPS.items():
    available = [column for column in columns if column in data.columns]
    if not available:
        continue
    with st.expander(group_name, expanded=group_name in {"Study and records", "Ionizable lipid chemistry"}):
        summary = pd.DataFrame(
            {
                "column": available,
                "non_empty_records": [non_empty_count(data, column) for column in available],
                "unique_values": [data[column].nunique(dropna=True) for column in available],
            }
        )
        st.dataframe(summary, hide_index=True, width="stretch")

st.markdown("### Studies")
study_columns = [column for column in ["study_id", "publication_link", "cargo_type", "delivery_value_method"] if column in data.columns]
if "study_id" in data.columns:
    studies = (
        data.groupby("study_id", dropna=False)
        .agg(records=("record_id", "count"), ionizable_lipids=("il_id", "nunique"), lnps=("lnp_id", "nunique"))
        .reset_index()
    )
    st.dataframe(studies, hide_index=True, width="stretch")
else:
    st.info("No study_id column is available.")

st.markdown("### Preview")
preview_columns = study_columns + [column for column in ["lnp_id", "il_id", "il_class", "model_type"] if column in data.columns]
st.dataframe(data[preview_columns].head(100), hide_index=True, width="stretch", height=360)
