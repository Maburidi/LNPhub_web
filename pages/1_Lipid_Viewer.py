from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
except ImportError:  # pragma: no cover - exercised only when RDKit is absent.
    Chem = None
    Draw = None


DATA_PATH = Path("data/LNPhub_public_two_studies.csv")

IDENTITY_COLUMNS = [
    "il_id",
    "il_smiles",
    "il_class",
    "il_subclass",
    "il_architecture_type",
    "il_head_architecture",
    "il_head_class",
    "il_linker_class",
    "il_tail_count",
]

FORMULATION_COLUMNS = [
    "helper_lipid_name",
    "helper_lipid_molratio",
    "cholesterol_name",
    "cholesterol_molratio",
    "peg_lipid_name",
    "peg_lipid_molratio",
    "peg_mw",
    "il_molratio",
    "il_to_nucleicacid_massratio",
    "il_to_nucleicacid_chargeratio",
    "total_lipid_to_cargo_ratio",
]

DESCRIPTOR_COLUMNS = [
    "molecular_weight",
    "heavy_atoms",
    "rings",
    "aromatic_rings",
    "rotatable_bonds",
    "van_der_waals_molecular_volume",
    "topological_polar_surface_area",
    "hydrogen_bond_donors",
    "hydrogen_bond_acceptors",
    "logp",
    "molar_refractivity",
    "fraction_sp3_carbons",
    "nitrogen_count",
    "has_ester",
    "has_carbonate",
    "has_disulfide",
]

OUTCOME_COLUMNS = [
    "study_id",
    "lnp_id",
    "cargo_type",
    "route_of_administration",
    "model",
    "model_type",
    "model_target",
    "particle_size_nm",
    "pdi",
    "zeta_potential_mv",
    "encapsulation_efficiency_percent",
    "measured_pka",
    "delivery_value",
    "delivery_value_method",
]


st.set_page_config(
    page_title="LNPhub Lipid Viewer",
    page_icon=":test_tube:",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_csv(csv_bytes: bytes | None = None) -> pd.DataFrame:
    if csv_bytes is not None:
        return pd.read_csv(StringIO(csv_bytes.decode("utf-8-sig")))
    return pd.read_csv(DATA_PATH)


def available_columns(df: pd.DataFrame, candidates: list[str]) -> list[str]:
    return [column for column in candidates if column in df.columns]


def filtered_options(series: pd.Series) -> list[str]:
    values = series.dropna().astype(str)
    values = values[values.str.strip() != ""]
    return sorted(values.unique().tolist())


def first_value(df: pd.DataFrame, column: str) -> str:
    if column not in df.columns:
        return ""
    values = df[column].dropna().astype(str)
    values = values[values.str.strip() != ""]
    return values.iloc[0] if not values.empty else ""


def details_table(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for column in available_columns(df, columns):
        value = first_value(df, column)
        if value:
            rows.append({"Field": column, "Value": value})
    return pd.DataFrame(rows)


def structure_svg(smiles: str) -> str | None:
    if Chem is None or Draw is None or not smiles:
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    return Draw.MolsToGridImage([mol], molsPerRow=1, subImgSize=(720, 460), useSVG=True)


def query_value(name: str) -> str:
    value = st.query_params.get(name, "")
    if isinstance(value, list):
        return value[0] if value else ""
    return value


data = load_csv()
lipids = filtered_options(data["il_id"]) if "il_id" in data.columns else []
requested_il = query_value("il_id")

st.page_link("streamlit_app.py", label="Back to dataset", icon=":material/table:")
st.title("Lipid Viewer")

if not lipids:
    st.info("No ionizable lipid IDs are available in the dataset.")
    st.stop()

selected_index = lipids.index(requested_il) if requested_il in lipids else 0
selected_il = st.selectbox("Ionizable lipid", lipids, index=selected_index)
if selected_il != requested_il:
    st.query_params["il_id"] = selected_il

lipid_data = data[data["il_id"].astype(str) == selected_il].copy()
smiles = first_value(lipid_data, "il_smiles")

st.subheader(selected_il)

metric_cols = st.columns(4)
metric_cols[0].metric("Records", f"{len(lipid_data):,}")
metric_cols[1].metric("Studies", f"{lipid_data['study_id'].nunique():,}" if "study_id" in lipid_data else "0")
metric_cols[2].metric("LNPs", f"{lipid_data['lnp_id'].nunique():,}" if "lnp_id" in lipid_data else "0")
metric_cols[3].metric("Cargo types", f"{lipid_data['cargo_type'].nunique():,}" if "cargo_type" in lipid_data else "0")

left, right = st.columns([1, 1])

with left:
    st.markdown("#### Structure")
    if Chem is None:
        st.warning("RDKit is not installed in this Python environment, so structures cannot be rendered here.")
    elif not smiles:
        st.info("No SMILES string is available for this lipid.")
    else:
        svg = structure_svg(smiles)
        if svg is None:
            st.warning("RDKit could not parse this SMILES string.")
        else:
            st.markdown(svg, unsafe_allow_html=True)
        st.code(smiles, language="text")

with right:
    st.markdown("#### Identity")
    identity = details_table(lipid_data, IDENTITY_COLUMNS)
    if identity.empty:
        st.info("No lipid identity metadata is available.")
    else:
        st.dataframe(identity, hide_index=True, width="stretch")

st.markdown("#### Formulation")
formulation = details_table(lipid_data, FORMULATION_COLUMNS)
if formulation.empty:
    st.info("No formulation metadata is available.")
else:
    st.dataframe(formulation, hide_index=True, width="stretch")

st.markdown("#### Molecular Descriptors")
descriptors = details_table(lipid_data, DESCRIPTOR_COLUMNS)
if descriptors.empty:
    st.info("No molecular descriptors are available.")
else:
    st.dataframe(descriptors, hide_index=True, width="stretch")

st.markdown("#### Matching Records")
record_columns = available_columns(lipid_data, OUTCOME_COLUMNS)
st.dataframe(lipid_data[record_columns], hide_index=True, width="stretch", height=420)

csv = lipid_data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download lipid records",
    data=csv,
    file_name=f"{selected_il}_records.csv",
    mime="text/csv",
)
