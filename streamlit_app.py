from __future__ import annotations

from io import StringIO
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
except ImportError:  # pragma: no cover - exercised only when RDKit is absent.
    Chem = None
    Draw = None


APP_TITLE = "LNPhub"
DATA_PATH = Path("data/LNPhub_public_two_studies.csv")

FILTER_COLUMNS = [
    "study_id",
    "cargo_type",
    "delivery_value_method",
    "route_of_administration",
    "model",
    "model_type",
    "model_target",
    "il_class",
    "il_subclass",
    "il_architecture_type",
    "helper_lipid_name",
    "peg_lipid_name",
]

PLOT_COLUMNS = [
    "delivery_value",
    "particle_size_nm",
    "pdi",
    "zeta_potential_mv",
    "measured_pka",
    "encapsulation_efficiency_percent",
    "molecular_weight",
    "logp",
    "topological_polar_surface_area",
    "rotatable_bonds",
]

SEARCH_COLUMNS = [
    "record_id",
    "study_id",
    "lnp_id",
    "il_id",
    "il_smiles",
    "helper_lipid_smiles",
    "cholesterol_smiles",
    "peg_lipid_smiles",
]


st.set_page_config(
    page_title="LNPhub",
    page_icon=":test_tube:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_csv(csv_bytes: bytes | None = None) -> pd.DataFrame:
    if csv_bytes is not None:
        return pd.read_csv(StringIO(csv_bytes.decode("utf-8-sig")))
    return pd.read_csv(DATA_PATH)


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(df[column], errors="coerce")


def available_columns(df: pd.DataFrame, candidates: list[str]) -> list[str]:
    return [column for column in candidates if column in df.columns]


def filtered_options(series: pd.Series) -> list[str]:
    values = series.dropna().astype(str)
    values = values[values.str.strip() != ""]
    return sorted(values.unique().tolist())


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    st.sidebar.header("Filters")

    for column in available_columns(df, FILTER_COLUMNS):
        options = filtered_options(df[column])
        if not options:
            continue

        selected = st.sidebar.multiselect(
            column.replace("_", " "),
            options=options,
            default=[],
        )
        if selected:
            filtered = filtered[filtered[column].astype(str).isin(selected)]

    return filtered


def apply_search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    query = query.strip().lower()
    if not query:
        return df

    columns = available_columns(df, SEARCH_COLUMNS)
    if not columns:
        return df

    search_frame = df[columns].fillna("").astype(str)
    mask = search_frame.apply(
        lambda col: col.str.lower().str.contains(query, regex=False),
        axis=0,
    ).any(axis=1)
    return df[mask]


def structure_svg(smiles: str) -> str | None:
    if Chem is None or Draw is None or not smiles:
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    return Draw.MolsToGridImage([mol], molsPerRow=1, subImgSize=(360, 240), useSVG=True)


def show_metric_row(df: pd.DataFrame) -> None:
    cols = st.columns(4)
    cols[0].metric("Records", f"{len(df):,}")
    cols[1].metric("Studies", f"{df['study_id'].nunique():,}" if "study_id" in df else "0")
    cols[2].metric("Ionizable lipids", f"{df['il_id'].nunique():,}" if "il_id" in df else "0")
    cols[3].metric("LNPs", f"{df['lnp_id'].nunique():,}" if "lnp_id" in df else "0")


def plot_explorer(df: pd.DataFrame) -> None:
    numeric_columns = [
        column
        for column in available_columns(df, PLOT_COLUMNS)
        if numeric_series(df, column).notna().any()
    ]

    if not numeric_columns:
        st.info("No numeric plotting columns are available after filtering.")
        return

    plot_df = df.copy()
    for column in numeric_columns:
        plot_df[column] = numeric_series(plot_df, column)

    left, right, color_col = st.columns([1, 1, 1])
    x_axis = left.selectbox("X axis", numeric_columns, index=0)
    default_y_index = min(1, len(numeric_columns) - 1)
    y_axis = right.selectbox("Y axis", numeric_columns, index=default_y_index)

    color_options = ["None"] + available_columns(
        df,
        ["study_id", "cargo_type", "delivery_value_method", "route_of_administration", "model_type"],
    )
    color_by = color_col.selectbox("Color", color_options)
    color = None if color_by == "None" else color_by

    chart_df = plot_df.dropna(subset=[x_axis, y_axis])
    if chart_df.empty:
        st.info("No rows have values for both selected axes.")
        return

    hover_columns = available_columns(
        chart_df,
        ["record_id", "study_id", "lnp_id", "il_id", "model_type", "model_target"],
    )
    fig = px.scatter(
        chart_df,
        x=x_axis,
        y=y_axis,
        color=color,
        hover_data=hover_columns,
        marginal_x="histogram",
        marginal_y="histogram",
        height=520,
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, width="stretch")


def structure_browser(df: pd.DataFrame) -> None:
    if "il_id" not in df.columns or "il_smiles" not in df.columns:
        st.info("This dataset does not include both il_id and il_smiles columns.")
        return

    molecules = (
        df[["il_id", "il_smiles"]]
        .dropna()
        .drop_duplicates()
        .sort_values("il_id")
        .reset_index(drop=True)
    )
    molecules = molecules[molecules["il_smiles"].astype(str).str.strip() != ""]

    if molecules.empty:
        st.info("No molecule structures are available after filtering.")
        return

    selected_il = st.selectbox("Ionizable lipid", molecules["il_id"].astype(str).tolist())
    row = molecules[molecules["il_id"].astype(str) == selected_il].iloc[0]
    smiles = str(row["il_smiles"])

    if Chem is None:
        st.warning("RDKit is not installed in this Python environment, so structures cannot be rendered here.")
    else:
        svg = structure_svg(smiles)
        if svg is None:
            st.warning("RDKit could not parse this SMILES string.")
        else:
            st.markdown(svg, unsafe_allow_html=True)

    st.code(smiles, language="text")


def lipid_page_url(il_id: str) -> str:
    return f"./Lipid_Viewer?il_id={quote(il_id)}"


def lipid_launcher(df: pd.DataFrame) -> None:
    if "il_id" not in df.columns:
        return

    lipids = filtered_options(df["il_id"])
    if not lipids:
        return

    left, right = st.columns([3, 1])
    selected_il = left.selectbox("Lipid page", lipids)
    if right.button("Open structure page", width="stretch"):
        st.query_params["il_id"] = selected_il
        st.switch_page("pages/1_Lipid_Viewer.py")


def dataset_table(df: pd.DataFrame) -> None:
    display_df = df.copy()
    column_config = {}

    if "il_id" in display_df.columns:
        display_df.insert(
            0,
            "lipid_page",
            display_df["il_id"].fillna("").astype(str).apply(
                lambda value: lipid_page_url(value) if value.strip() else ""
            ),
        )
        column_config["lipid_page"] = st.column_config.LinkColumn(
            "Open",
            display_text="View lipid",
            help="Open this ionizable lipid on the structure page.",
        )

    st.dataframe(
        display_df,
        width="stretch",
        height=520,
        hide_index=True,
        column_config=column_config,
    )


uploaded_file = st.sidebar.file_uploader("Upload a curated LNPhub CSV", type=["csv"])

if uploaded_file is not None:
    data = load_csv(uploaded_file.getvalue())
else:
    data = load_csv()

st.title(APP_TITLE)
st.caption("Curated lipid nanoparticle formulation and delivery dataset explorer")

filtered_data = apply_sidebar_filters(data)
query = st.text_input("Search il_id, SMILES, record_id, study_id, or lnp_id", placeholder="Example: YX_TS1")
filtered_data = apply_search(filtered_data, query)

show_metric_row(filtered_data)

tab_table, tab_structures, tab_plots = st.tabs(["Dataset", "Structures", "Plots"])

with tab_table:
    lipid_launcher(filtered_data)
    dataset_table(filtered_data)
    csv = filtered_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        data=csv,
        file_name="lnphub_filtered.csv",
        mime="text/csv",
    )

with tab_structures:
    structure_browser(filtered_data)

with tab_plots:
    plot_explorer(filtered_data)
