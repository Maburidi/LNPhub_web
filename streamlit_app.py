from __future__ import annotations

from io import StringIO
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import plotly.express as px
import streamlit as st

from lnphub_ui import configure_page, inject_menu_logo, render_home_banner

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
except ImportError:  # pragma: no cover - exercised only when RDKit is absent.
    Chem = None
    Draw = None


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


configure_page("Portal")
inject_menu_logo()


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


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    filter_cols = st.columns(3)
    visible_filters = available_columns(df, FILTER_COLUMNS)

    for index, column in enumerate(visible_filters):
        options = filtered_options(df[column])
        if not options:
            continue

        selected = filter_cols[index % 3].multiselect(
            column.replace("_", " "),
            options=options,
            default=[],
            key=f"filter_{column}",
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


def structure_svg(smiles: str, width: int = 360, height: int = 240) -> str | None:
    if Chem is None or Draw is None or not smiles:
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    return Draw.MolsToGridImage([mol], molsPerRow=1, subImgSize=(width, height), useSVG=True)


def show_metric_row(df: pd.DataFrame) -> None:
    cols = st.columns(4)
    cols[0].metric("Records", f"{len(df):,}")
    cols[1].metric("Studies", f"{df['study_id'].nunique():,}" if "study_id" in df else "0")
    cols[2].metric("Ionizable lipids", f"{df['il_id'].nunique():,}" if "il_id" in df else "0")
    cols[3].metric("LNPs", f"{df['lnp_id'].nunique():,}" if "lnp_id" in df else "0")


def lipid_page_url(il_id: str) -> str:
    return f"./Lipid_Viewer?il_id={quote(il_id)}"


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


def render_home(data: pd.DataFrame) -> None:
    render_home_banner()

    st.markdown(
        """
        <p class="lnp-ai-intro">
            Artificial intelligence is emerging as a powerful foundation for the rational design of lipid nanoparticles
            and the next generation of mRNA therapeutics. By integrating lipid structure, formulation composition,
            manufacturing conditions, and biological performance, AI can uncover complex relationships that are
            difficult to resolve through conventional experimentation alone. These models can guide the selection
            and optimization of ionizable lipids, predict critical properties such as potency, stability,
            biodistribution, tissue selectivity, and tolerability, and help prioritize the most promising formulations
            before costly experimental validation. By reducing empirical trial and error while complementing
            mechanistic insight, AI has the potential to accelerate LNP discovery, improve the precision and safety
            of mRNA delivery, and enable the development of more effective and broadly accessible RNA medicines.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="lnp-foundation-box">
            <p>
                LNP-Hub is designed to provide the data foundation needed to advance artificial intelligence-driven
                lipid nanoparticle discovery and mRNA therapeutics. By bringing together standardized information on
                lipid structures, formulation composition, manufacturing conditions, physicochemical properties,
                biological models, delivery performance, and safety, LNP-Hub transforms fragmented experimental
                evidence into a structured and machine-readable resource. This integrated framework will support the
                development, benchmarking, and validation of predictive and generative AI models, enabling researchers
                to identify structure-function relationships, prioritize promising ionizable lipids and formulations,
                and reduce dependence on costly trial-and-error experimentation. By connecting high-quality data with
                computational design and experimental validation, LNP-Hub aims to accelerate the discovery of safer,
                more potent, and tissue-selective delivery systems and to serve as a foundational infrastructure for
                the next generation of mRNA medicines.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    show_metric_row(data)

    st.markdown(
        """
        <section class="lnp-band">
            <div class="lnp-card-grid">
                <div class="lnp-card">
                    <h3>Filterable Records</h3>
                    <p>Explore studies, cargo types, routes, models, helper lipids, PEG lipids, and delivery readouts.</p>
                </div>
                <div class="lnp-card">
                    <h3>Molecular Structures</h3>
                    <p>Open individual ionizable lipids and render their structures directly from SMILES with RDKit.</p>
                </div>
                <div class="lnp-card">
                    <h3>Assay Context</h3>
                    <p>Connect delivery values with formulation ratios, particle properties, pKa, zeta, and model metadata.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_start(data: pd.DataFrame) -> None:
    st.title("Start")
    st.caption("Filter, search, visualize, and export the curated LNP dataset.")

    uploaded_file = st.file_uploader("Upload a curated LNPhub CSV", type=["csv"], key="start_upload")
    working_data = load_csv(uploaded_file.getvalue()) if uploaded_file is not None else data

    filtered_data = apply_filters(working_data)
    query = st.text_input(
        "Search il_id, SMILES, record_id, study_id, or lnp_id",
        placeholder="Example: YX_TS1",
        key="start_search",
    )
    filtered_data = apply_search(filtered_data, query)
    show_metric_row(filtered_data)

    table_tab, structures_tab, plots_tab = st.tabs(["Dataset", "Structures", "Plots"])
    with table_tab:
        dataset_table(filtered_data)
        csv = filtered_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download filtered CSV",
            data=csv,
            file_name="lnphub_filtered.csv",
            mime="text/csv",
        )

    with structures_tab:
        render_structure_browser(filtered_data)

    with plots_tab:
        render_plot_explorer(filtered_data)


def render_structure_browser(df: pd.DataFrame) -> None:
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

    selected_il = st.selectbox(
        "Ionizable lipid",
        molecules["il_id"].astype(str).tolist(),
        key="start_structure_lipid",
    )
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


def render_plot_explorer(df: pd.DataFrame) -> None:
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
    x_axis = left.selectbox("X axis", numeric_columns, index=0, key="plot_x_axis")
    default_y_index = min(1, len(numeric_columns) - 1)
    y_axis = right.selectbox("Y axis", numeric_columns, index=default_y_index, key="plot_y_axis")

    color_options = ["None"] + available_columns(
        df,
        ["study_id", "cargo_type", "delivery_value_method", "route_of_administration", "model_type"],
    )
    color_by = color_col.selectbox("Color", color_options, key="plot_color_by")
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
    st.plotly_chart(fig, use_container_width=True)


def render_lipid_viewer(data: pd.DataFrame) -> None:
    st.title("Lipid Viewer")

    lipids = filtered_options(data["il_id"]) if "il_id" in data.columns else []
    if not lipids:
        st.info("No ionizable lipid IDs are available in the dataset.")
        return

    selected_il = st.selectbox("Ionizable lipid", lipids, key="lipid_viewer_lipid")
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
            svg = structure_svg(smiles, width=720, height=460)
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
    st.dataframe(formulation, hide_index=True, width="stretch")

    st.markdown("#### Molecular Descriptors")
    descriptors = details_table(lipid_data, DESCRIPTOR_COLUMNS)
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


def render_data_catalog(data: pd.DataFrame) -> None:
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
                    "non_empty_records": [
                        int((data[column].dropna().astype(str).str.strip() != "").sum())
                        for column in available
                    ],
                    "unique_values": [data[column].nunique(dropna=True) for column in available],
                }
            )
            st.dataframe(summary, hide_index=True, width="stretch")

    st.markdown("### Studies")
    if "study_id" in data.columns:
        studies = (
            data.groupby("study_id", dropna=False)
            .agg(records=("record_id", "count"), ionizable_lipids=("il_id", "nunique"), lnps=("lnp_id", "nunique"))
            .reset_index()
        )
        st.dataframe(studies, hide_index=True, width="stretch")
    else:
        st.info("No study_id column is available.")


def render_documentation() -> None:
    st.title("Documentation")
    st.caption("Working notes for users who want to explore, reproduce, or extend LNP-Hub.")
    st.markdown(
        """
        ### Quick Start

        Use **Start** to filter the dataset, search by lipid identifiers or SMILES,
        inspect molecule structures, plot numeric readouts, and download filtered records.

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
        """
    )


def render_about() -> None:
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


data = load_csv()
home_tab, start_tab, data_tab, lipid_tab, docs_tab, about_tab = st.tabs(
    ["Home", "Start", "Data", "Lipid Viewer", "Documentation", "About"]
)

with home_tab:
    render_home(data)

with start_tab:
    render_start(data)

with data_tab:
    render_data_catalog(data)

with lipid_tab:
    render_lipid_viewer(data)

with docs_tab:
    render_documentation()

with about_tab:
    render_about()
