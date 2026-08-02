from __future__ import annotations

import base64
from html import escape
from io import StringIO
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import plotly.express as px
import streamlit as st

from lnphub_ui import configure_page, inject_menu_logo, render_footer, render_home_banner, render_layers_section

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
except ImportError:  # pragma: no cover - exercised only when RDKit is absent.
    Chem = None
    Draw = None


DATA_PATH = Path("data/LNPhub_public_two_studies.csv")

STUDY_TITLE_FALLBACKS = {
    "LNPhub_BL_2023": "Combinatorial design of nanoparticles for pulmonary mRNA delivery and genome editing",
    "LNPhub_YX_2025": (
        "Antimicrobial peptide delivery to lung as peptibody mRNA in anti-inflammatory lipids "
        "treats multidrug-resistant bacterial pneumonia"
    ),
}

TITLE_COLUMNS = [
    "paper_title",
    "publication_title",
    "article_title",
    "manuscript_title",
    "study_title",
    "title",
]

LINK_COLUMNS = ["publication_link", "paper_link", "article_link", "url", "doi"]

FILTER_COLUMNS = [
    "study_id",
    "cargo_type",
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

FILTER_GROUPS = [
    (
        "Level 1 | Provenance & IDs",
        ["study_id"],
    ),
    (
        "Level 2 | Molecule & Formulation Definition",
        [
            "cargo_type",
            "il_class",
            "il_subclass",
            "il_architecture_type",
            "helper_lipid_name",
            "peg_lipid_name",
        ],
    ),
    (
        "Level 3 | Process & Experimental Context",
        ["route_of_administration", "model", "model_type", "model_target"],
    ),
]

FILTER_LABELS = {
    "study_id": "Study ID",
    "cargo_type": "Cargo Type",
    "route_of_administration": "Route of Administration",
    "model": "Model",
    "model_type": "Model Type",
    "model_target": "Model Target",
    "il_class": "Ionizable Lipid Class",
    "il_subclass": "Ionizable Lipid Subclass",
    "il_architecture_type": "Ionizable Lipid Architecture Type",
    "helper_lipid_name": "Helper Lipid Name",
    "peg_lipid_name": "PEG Lipid Name",
}

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


def filter_label(column: str) -> str:
    return FILTER_LABELS.get(column, column.replace("_", " ").title())


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    visible_filters = set(available_columns(df, FILTER_COLUMNS))

    for group_name, group_columns in FILTER_GROUPS:
        visible_group_columns = [column for column in group_columns if column in visible_filters]
        if not visible_group_columns:
            continue

        st.markdown(
            f"""
            <div class="lnp-filter-group-divider"></div>
            <section class="lnp-filter-layer">
                <p class="lnp-filter-layer-kicker">{escape(group_name.split("|", 1)[-1].strip())}</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        filter_cols = st.columns(min(3, len(visible_group_columns)))
        for index, column in enumerate(visible_group_columns):
            options = filtered_options(df[column])
            if not options:
                continue

            label = filter_label(column)
            with filter_cols[index % len(filter_cols)]:
                selected = st.multiselect(
                    label,
                    options=options,
                    default=[],
                    key=f"filter_{column}",
                    placeholder=f"Any {label}",
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
    metrics = [
        ("Experimental Records", f"{len(df):,}"),
        ("Studies", f"{df['study_id'].nunique():,}" if "study_id" in df else "0"),
        ("Ionizable Lipids", f"{df['il_id'].nunique():,}" if "il_id" in df else "0"),
        ("LNP Formulations", f"{df['lnp_id'].nunique():,}" if "lnp_id" in df else "0"),
    ]
    stat_tiles = "\n".join(
        f"""
        <div class="lnp-stat-tile">
            <div class="lnp-stat-label">{label}</div>
            <div class="lnp-stat-value">{value}</div>
        </div>
        """
        for label, value in metrics
    )
    st.markdown(
        f"""
        <section class="lnp-stat-grid">
            {stat_tiles}
        </section>
        """,
        unsafe_allow_html=True,
    )


def first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for column in candidates:
        if column in df.columns:
            return column
    return None


def normalize_publication_link(value: object) -> str:
    link = "" if pd.isna(value) else str(value).strip()
    if not link:
        return ""
    if link.startswith(("http://", "https://")):
        return link
    if link.startswith("doi:"):
        return f"https://doi.org/{link[4:].strip()}"
    if "/" in link and link[:2].isdigit():
        return f"https://doi.org/{link}"
    return link


def render_studies_table(df: pd.DataFrame) -> None:
    if "study_id" not in df.columns or df.empty:
        return

    title_column = first_existing_column(df, TITLE_COLUMNS)
    link_column = first_existing_column(df, LINK_COLUMNS)
    rows = []

    for study_id, study_df in df.groupby("study_id", dropna=True, sort=True):
        study_id_text = str(study_id)
        title = STUDY_TITLE_FALLBACKS.get(study_id_text, study_id_text)
        if title_column:
            titles = study_df[title_column].dropna().astype(str).str.strip()
            titles = titles[titles != ""]
            if not titles.empty:
                title = titles.iloc[0]

        link = ""
        if link_column:
            links = study_df[link_column].dropna().map(normalize_publication_link)
            links = links[links != ""]
            if not links.empty:
                link = links.iloc[0]

        records = len(study_df)
        ionizable_lipids = study_df["il_id"].nunique() if "il_id" in study_df else 0
        formulations = study_df["lnp_id"].nunique() if "lnp_id" in study_df else 0
        paper_html = (
            f'<a class="lnp-paper-link" href="{escape(link, quote=True)}" target="_blank" rel="noopener noreferrer">'
            f'{escape(title)} <span aria-hidden="true">&nearr;</span></a>'
            if link
            else escape(title)
        )
        rows.append(
            "<tr>"
            f'<td><span class="lnp-study-id">{escape(study_id_text)}</span></td>'
            f"<td>{paper_html}</td>"
            f'<td><span class="lnp-study-count">{records:,}</span></td>'
            f'<td><span class="lnp-study-count">{ionizable_lipids:,}</span></td>'
            f'<td><span class="lnp-study-count">{formulations:,}</span></td>'
            "</tr>"
        )

    table_html = (
        '<section class="lnp-studies-section">'
        '<h2 class="lnp-section-heading">LNP Libraries</h2>'
        '<p class="lnp-section-subtitle">'
        "Source publications currently represented in LNP-Hub, summarized directly from the loaded dataset."
        "</p>"
        '<div class="lnp-study-table-wrap">'
        '<table class="lnp-study-table">'
        "<thead><tr>"
        "<th>Study ID</th>"
        "<th>Paper</th>"
        "<th>Records</th>"
        "<th>Ionizable Lipids</th>"
        "<th>LNP Formulations</th>"
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
        "</div>"
        "</section>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


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
        <h2 class="lnp-portal-tagline">
            LNP-Hub: Enabling Structure&ndash;Function Modeling, AI-Driven LNP Discovery,
            and Next-Generation mRNA Delivery
        </h2>
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
        <div class="lnp-section-divider"></div>
        """,
        unsafe_allow_html=True,
    )

    show_metric_row(data)
    render_layers_section()
    render_studies_table(data)


def render_curated_experimental_libraries(data: pd.DataFrame) -> None:
    working_data = data
    full_csv = working_data.to_csv(index=False).encode("utf-8")
    full_csv_href = base64.b64encode(full_csv).decode("ascii")
    st.markdown(
        f"""
        <section class="lnp-download-panel">
            <div>
                <p class="lnp-download-kicker">Curated Experimental Libraries</p>
                <h3>Download All Curated Libraries</h3>
                <p>
                    Export the complete curated LNP-Hub experimental dataset as a machine-readable CSV file.
                </p>
                <a
                    class="lnp-download-action"
                    href="data:text/csv;base64,{full_csv_href}"
                    download="lnphub_curated_experimental_libraries.csv"
                >
                    Download all curated libraries as CSV
                </a>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="lnp-section-divider"></div>
        <h3 class="lnp-filter-heading">Filter by:</h3>
        """,
        unsafe_allow_html=True,
    )

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


def render_virtual_screening_libraries() -> None:
    st.markdown(
        """
        <section class="lnp-dataset-placeholder">
            <h3>Virtual Screening Libraries</h3>
            <p>
                Virtual lipid libraries for computational screening and model-guided prioritization
                will be organized here as LNP-Hub expands.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_datasets(data: pd.DataFrame) -> None:
    st.markdown('<div class="lnp-dataset-drawer">', unsafe_allow_html=True)
    selected_dataset = st.radio(
        "Dataset library",
        ["Curated Experimental Libraries", "Virtual Screening Libraries"],
        horizontal=True,
        label_visibility="collapsed",
        key="dataset_library_menu",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if selected_dataset == "Curated Experimental Libraries":
        render_curated_experimental_libraries(data)
    else:
        render_virtual_screening_libraries()


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
        ### Quick Guide

        Use **Datasets** to filter the dataset, search by lipid identifiers or SMILES,
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
home_tab, datasets_tab, lipid_tab, docs_tab, about_tab = st.tabs(
    ["Home", "Datasets", "Lipid Viewer", "Documentation", "About"]
)

with home_tab:
    render_home(data)

with datasets_tab:
    render_datasets(data)

with lipid_tab:
    render_lipid_viewer(data)

with docs_tab:
    render_documentation()

with about_tab:
    render_about()

render_footer()
