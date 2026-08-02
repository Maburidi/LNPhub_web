from __future__ import annotations

import base64
from html import escape
from io import StringIO
from pathlib import Path
from urllib.parse import quote, urlparse

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from lnphub_ui import configure_page, inject_menu_logo, render_footer, render_home_banner, render_layers_section, render_top_nav

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw
    RDKIT_IMPORT_ERROR = ""
except ImportError as error:  # pragma: no cover - exercised only when RDKit is absent.
    Chem = None
    Draw = None
    AllChem = None
    RDKIT_IMPORT_ERROR = str(error)

try:
    import py3Dmol
except ImportError:  # pragma: no cover - exercised only when py3Dmol is absent.
    py3Dmol = None


DATA_PATH = Path("data/LNPhub_public_two_studies.csv")

VIRTUAL_LIBRARY_FILES = [
    ("Download 3CR Virtual Library", Path("data/vl_3CR_300.csv"), "3CR"),
    ("Download 4CR Virtual Library", Path("data/vl_4CR_300.csv"), "4CR"),
    ("Download Multi-Tail Lipidoid Virtual Library", Path("data/vl_MultiLipidoid_300.csv"), "Multi-Tail Lipidoid"),
]

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

VIRTUAL_FILTER_GROUPS = [
    (
        "Virtual Library & IDs",
        ["Virtual Library", "REACTION_TYP", "ARCHITECTURE"],
    ),
]

VIRTUAL_FILTER_LABELS = {
    "Virtual Library": "Virtual Library",
    "LIPID_ID": "Lipid ID",
    "IL_SMILES": "Ionizable Lipid SMILES",
    "IL_head_id": "Ionizable Lipid Head ID",
    "IL_head_SMILES": "Ionizable Lipid Head SMILES",
    "REACTION_TYP": "Reaction Type",
    "ARCHITECTURE": "Architecture",
    "Isocyanide_id": "Isocyanide ID",
    "Ketone_id": "Ketone ID",
    "Carboxylic_acid_id": "Carboxylic Acid ID",
    "Tail1_id": "Tail 1 ID",
    "Tail2_id": "Tail 2 ID",
    "Tail3_id": "Tail 3 ID",
    "Tail4_id": "Tail 4 ID",
    "Active_Site_Class": "Active Site Class",
    "N_Tails": "Number of Tails",
}

VIRTUAL_SEARCH_COLUMNS = [
    "Virtual Library",
    "LIPID_ID",
    "IL_SMILES",
    "IL_head_id",
    "IL_head_SMILES",
    "Isocyanide_id",
    "Isocyanide_SMILES",
    "Ketone_id",
    "Ketone_SMILES",
    "Carboxylic_acid_id",
    "Carboxylic_SMILES",
    "Tail1_id",
    "Tail1_SMILES",
    "Tail2_id",
    "Tail2_SMILES",
    "Tail3_id",
    "Tail3_SMILES",
    "Tail4_id",
    "Tail4_SMILES",
    "ARCHITECTURE",
    "REACTION_TYP",
]

BUILDING_BLOCK_COLUMNS = [
    ("Head", ["il_head_smiles", "head_smiles", "head_smile", "IL_head_SMILES"]),
    ("Linker", ["il_linker_smiles", "linker_smiles", "linker_smile"]),
    ("Tail 1", ["il_tail1_smiles", "tail1_smiles", "tail1_smile", "Tail1_SMILES"]),
    ("Tail 2", ["il_tail2_smiles", "tail2_smiles", "tail2_smile", "Tail2_SMILES"]),
]

VIRTUAL_COMPONENT_ID_COLUMNS = {
    "IL_head_SMILES": "IL_head_id",
    "Isocyanide_SMILES": "Isocyanide_id",
    "Ketone_SMILES": "Ketone_id",
    "Carboxylic_SMILES": "Carboxylic_acid_id",
    "Tail1_SMILES": "Tail1_id",
    "Tail2_SMILES": "Tail2_id",
    "Tail3_SMILES": "Tail3_id",
    "Tail4_SMILES": "Tail4_id",
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

BIOLOGICAL_READOUT_PREFIXES = (
    "cellular_",
    "editing_",
    "uptake_",
    "viability_",
    "toxicity_",
)

BIOLOGICAL_READOUT_KEYWORDS = (
    "delivery",
    "protein_abundance",
    "mrna_binding",
)


configure_page("Portal")
inject_menu_logo()


PAGE_NAMES = ["Home", "Overview", "Datasets", "Lipid Viewer", "Documentation", "About"]
PAGE_PATHS = {
    "/": "Home",
    "/overview": "Overview",
    "/datasets": "Datasets",
    "/lipid-viewer": "Lipid Viewer",
    "/documentation": "Documentation",
    "/about": "About",
}


def query_param_value(name: str) -> str:
    value = st.query_params.get(name, "")
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value) if value is not None else ""


def active_page() -> str:
    page = query_param_value("page").replace("_", " ").strip()
    if page in PAGE_NAMES:
        return page

    streamlit_context = getattr(st, "context", None)
    if streamlit_context is not None:
        current_path = urlparse(str(streamlit_context.url)).path.rstrip("/") or "/"
        if current_path in PAGE_PATHS:
            return PAGE_PATHS[current_path]

    return "Home"


def normalize_path_url() -> None:
    components.html(
        """
        <script>
            const parentUrl = new URL(window.parent.location.href);
            if (parentUrl.pathname !== "/" && parentUrl.searchParams.has("page")) {
                parentUrl.pathname = "/";
                window.parent.history.replaceState({}, "", parentUrl.toString());
            }
        </script>
        """,
        height=0,
    )


@st.cache_data(show_spinner=False)
def load_csv(csv_bytes: bytes | None = None) -> pd.DataFrame:
    if csv_bytes is not None:
        return pd.read_csv(StringIO(csv_bytes.decode("utf-8-sig")))
    return pd.read_csv(DATA_PATH)


@st.cache_data(show_spinner=False)
def load_virtual_libraries() -> pd.DataFrame:
    frames = []
    for _label, path, library_name in VIRTUAL_LIBRARY_FILES:
        if not path.exists():
            continue
        frame = pd.read_csv(path)
        frame.insert(0, "Virtual Library", library_name)
        frames.append(frame)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False)


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(df[column], errors="coerce")


def available_columns(df: pd.DataFrame, candidates: list[str]) -> list[str]:
    return [column for column in candidates if column in df.columns]


def filtered_options(series: pd.Series) -> list[str]:
    values = series.dropna().astype(str)
    values = values[values.str.strip() != ""]
    return sorted(values.unique().tolist())


def single_tick_selector(label: str, options: list[str], key: str, label_visibility: str = "visible") -> str:
    if not options:
        return ""
    if hasattr(st, "pills"):
        selected = st.pills(
            label,
            options,
            selection_mode="single",
            key=key,
            label_visibility=label_visibility,
        )
        if selected is None:
            selected = options[0]
        return selected
    return st.radio(
        label,
        options,
        horizontal=True,
        key=key,
        label_visibility=label_visibility,
    )


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


def virtual_filter_label(column: str) -> str:
    return VIRTUAL_FILTER_LABELS.get(column, column.replace("_", " ").title())


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


def apply_virtual_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    visible_filters = set(df.columns)

    for group_name, group_columns in VIRTUAL_FILTER_GROUPS:
        visible_group_columns = [column for column in group_columns if column in visible_filters]
        if not visible_group_columns:
            continue

        st.markdown(
            f"""
            <div class="lnp-filter-group-divider"></div>
            <section class="lnp-filter-layer">
                <p class="lnp-filter-layer-kicker">{escape(group_name)}</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        filter_cols = st.columns(min(3, len(visible_group_columns)))
        for index, column in enumerate(visible_group_columns):
            options = filtered_options(df[column])
            if not options:
                continue

            label = virtual_filter_label(column)
            with filter_cols[index % len(filter_cols)]:
                selected = st.multiselect(
                    label,
                    options=options,
                    default=[],
                    key=f"virtual_filter_{column}",
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


def apply_virtual_search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    query = query.strip().lower()
    if not query:
        return df

    columns = available_columns(df, VIRTUAL_SEARCH_COLUMNS)
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


def show_rdkit_warning() -> None:
    message = "RDKit is not available in this Python environment, so structures cannot be rendered here."
    if RDKIT_IMPORT_ERROR:
        message = f"{message} Import error: {RDKIT_IMPORT_ERROR}"
    st.warning(message)


def render_2d_structure(smiles: str) -> None:
    svg = structure_svg(smiles, width=720, height=460)
    if svg is None:
        st.warning("RDKit could not parse this SMILES string.")
        return

    components.html(
        f"""
        <style>
            body {{
                margin: 0;
            }}

            .lnp-structure-frame {{
                align-items: center;
                background:
                    radial-gradient(circle at 50% 30%, rgba(215, 242, 238, 0.55), rgba(255,255,255,0) 54%),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.13);
                border-radius: 8px;
                box-shadow: 0 16px 36px rgba(0, 106, 113, 0.1);
                box-sizing: border-box;
                display: flex;
                justify-content: center;
                min-height: 480px;
                overflow: auto;
                padding: 12px;
                width: 100%;
            }}

            .lnp-structure-frame svg {{
                height: auto;
                max-height: 456px;
                max-width: 100%;
            }}
        </style>
        <div class="lnp-structure-frame">
            {svg}
        </div>
        """,
        height=500,
    )


def svg_body(svg: str) -> str:
    lines = [
        line
        for line in svg.splitlines()
        if not line.lstrip().startswith("<?xml") and not line.lstrip().startswith("<!DOCTYPE")
    ]
    return "\n".join(lines)


def render_building_block_viewers(lipid_data: pd.DataFrame) -> None:
    block_cards = []
    for label, candidates in BUILDING_BLOCK_COLUMNS:
        smiles = component_value(lipid_data, candidates)
        svg = ""
        if smiles != "Not reported":
            rendered = structure_svg(smiles, width=260, height=190)
            if rendered is not None:
                svg = svg_body(rendered)

        block_cards.append(
            f"""
            <article class="lnp-block-card">
                <p>{escape(label)}</p>
                <div class="lnp-block-structure">{svg}</div>
            </article>
            """
        )

    components.html(
        f"""
        <style>
            body {{
                margin: 0;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }}

            .lnp-block-grid {{
                display: grid;
                gap: 12px;
                grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
                width: 100%;
            }}

            .lnp-block-card {{
                background:
                    linear-gradient(145deg, rgba(255,255,255,0.94), rgba(215,242,238,0.56)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.14);
                border-radius: 8px;
                box-shadow: 0 12px 28px rgba(0, 106, 113, 0.09);
                box-sizing: border-box;
                min-height: 248px;
                overflow: hidden;
                padding: 12px;
            }}

            .lnp-block-card p {{
                color: #063638;
                font-size: 0.86rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                margin: 0 0 8px;
                text-transform: uppercase;
            }}

            .lnp-block-structure {{
                align-items: center;
                background: rgba(255,255,255,0.76);
                border: 1px dashed rgba(0, 106, 113, 0.16);
                border-radius: 7px;
                display: flex;
                justify-content: center;
                min-height: 198px;
                overflow: auto;
                padding: 8px;
            }}

            .lnp-block-structure svg {{
                height: auto;
                max-height: 190px;
                max-width: 100%;
            }}
        </style>
        <section class="lnp-block-grid">
            {"".join(block_cards)}
        </section>
        """,
        height=560,
    )


def virtual_component_columns(lipid_data: pd.DataFrame) -> list[str]:
    columns = []
    for column in lipid_data.columns:
        if column == "IL_SMILES":
            continue
        if column.upper().endswith("SMILES") and first_value(lipid_data, column):
            columns.append(column)
    return columns


def render_virtual_component_viewers(lipid_data: pd.DataFrame) -> None:
    component_columns = virtual_component_columns(lipid_data)
    if not component_columns:
        st.info("No virtual building block SMILES are available for this lipid.")
        return

    block_cards = []
    for index, smiles_column in enumerate(component_columns, start=1):
        smiles = first_value(lipid_data, smiles_column)
        id_column = VIRTUAL_COMPONENT_ID_COLUMNS.get(smiles_column)
        component_id = first_value(lipid_data, id_column) if id_column else ""
        svg = ""
        rendered = structure_svg(smiles, width=260, height=190)
        if rendered is not None:
            svg = svg_body(rendered)

        block_cards.append(
            f"""
            <article class="lnp-block-card">
                <p>Component {index}</p>
                <small>{escape(component_id) if component_id else "&nbsp;"}</small>
                <div class="lnp-block-structure">{svg}</div>
            </article>
            """
        )

    height = min(900, 300 + ((len(block_cards) - 1) // 2) * 270)
    components.html(
        f"""
        <style>
            body {{
                margin: 0;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }}

            .lnp-block-grid {{
                display: grid;
                gap: 12px;
                grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
                width: 100%;
            }}

            .lnp-block-card {{
                background:
                    linear-gradient(145deg, rgba(255,255,255,0.94), rgba(215,242,238,0.56)),
                    #ffffff;
                border: 1px solid rgba(0, 106, 113, 0.14);
                border-radius: 8px;
                box-shadow: 0 12px 28px rgba(0, 106, 113, 0.09);
                box-sizing: border-box;
                min-height: 268px;
                overflow: hidden;
                padding: 12px;
            }}

            .lnp-block-card p {{
                color: #063638;
                font-size: 0.86rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                margin: 0;
                text-transform: uppercase;
            }}

            .lnp-block-card small {{
                color: #42666a;
                display: block;
                font-size: 0.76rem;
                line-height: 1.2;
                margin: 4px 0 8px;
                min-height: 0.92rem;
                overflow-wrap: anywhere;
            }}

            .lnp-block-structure {{
                align-items: center;
                background: rgba(255,255,255,0.76);
                border: 1px dashed rgba(0, 106, 113, 0.16);
                border-radius: 7px;
                display: flex;
                justify-content: center;
                min-height: 198px;
                overflow: auto;
                padding: 8px;
            }}

            .lnp-block-structure svg {{
                height: auto;
                max-height: 190px;
                max-width: 100%;
            }}
        </style>
        <section class="lnp-block-grid">
            {"".join(block_cards)}
        </section>
        """,
        height=height,
    )


def structure_molblock_3d(smiles: str) -> str | None:
    if Chem is None or AllChem is None or not smiles:
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    params.maxIterations = 1000
    status = AllChem.EmbedMolecule(mol, params)
    if status != 0:
        params.useRandomCoords = True
        status = AllChem.EmbedMolecule(mol, params)
    if status != 0:
        status = AllChem.EmbedMolecule(mol, randomSeed=42, useRandomCoords=True, maxAttempts=1000)
    if status != 0:
        return None

    try:
        AllChem.MMFFOptimizeMolecule(mol, maxIters=250)
    except Exception:
        try:
            AllChem.UFFOptimizeMolecule(mol, maxIters=250)
        except Exception:
            pass

    return Chem.MolToMolBlock(mol)


def render_3d_structure(smiles: str) -> None:
    if py3Dmol is None:
        st.info("3D viewing needs py3Dmol. It has been added to requirements.txt for deployment.")
        return

    molblock = structure_molblock_3d(smiles)
    if molblock is None:
        st.warning("RDKit could not generate a 3D conformer for this lipid.")
        return

    viewer = py3Dmol.view(width="100%", height=460)
    viewer.addModel(molblock, "sdf")
    viewer.setStyle({"stick": {"radius": 0.18}, "sphere": {"scale": 0.28}})
    viewer.setBackgroundColor("0xf7faf9")
    viewer.zoomTo()
    components.html(viewer._make_html(), height=480)


def component_value(df: pd.DataFrame, value_columns: list[str]) -> str:
    for column in value_columns:
        value = first_value(df, column)
        if value:
            return value
    return "Not reported"


def component_ratio(df: pd.DataFrame, ratio_columns: list[str]) -> str:
    for column in ratio_columns:
        value = first_value(df, column)
        if value:
            return f"Ratio: {value}"
    return "-"


def render_lipid_component_cards(lipid_data: pd.DataFrame) -> None:
    ionizable_lipid_id = component_value(lipid_data, ["il_id"])
    components_data = [
        {
            "label": "Ionizable Lipid",
            "name": ionizable_lipid_id,
            "ratio": component_ratio(lipid_data, ["il_molratio"]),
        },
        {
            "label": "Helper Lipid",
            "name": component_value(lipid_data, ["helper_lipid_name"]),
            "ratio": component_ratio(lipid_data, ["helper_lipid_molratio"]),
        },
        {
            "label": "Cholesterol",
            "name": component_value(lipid_data, ["cholesterol_name"]),
            "ratio": component_ratio(lipid_data, ["cholesterol_molratio"]),
        },
        {
            "label": "PEG Lipid",
            "name": component_value(lipid_data, ["peg_lipid_name"]),
            "ratio": component_ratio(lipid_data, ["peg_lipid_molratio"]),
        },
        {
            "label": "Cargo",
            "name": component_value(lipid_data, ["cargo_type"]),
            "ratio": "",
        },
    ]
    cards = "\n".join(
        f"""
        <article class="lnp-component-card">
            <p class="lnp-component-label">{escape(item["label"])}</p>
            <h4>{escape(item["name"])}</h4>
            {f'<p class="lnp-component-ratio">{escape(str(item["ratio"]))}</p>' if item["ratio"] else ""}
        </article>
        """
        for item in components_data
    )
    st.markdown(
        f"""
        <section class="lnp-component-grid">
            {cards}
        </section>
        """,
        unsafe_allow_html=True,
    )


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


def lipid_page_url(lnp_id: str) -> str:
    return f"./?page=Lipid_Viewer&lnp_id={quote(lnp_id)}"


def virtual_lipid_page_url(lipid_id: str) -> str:
    return f"./?page=Lipid_Viewer&virtual_lipid_id={quote(lipid_id)}"


def dataset_table(df: pd.DataFrame) -> None:
    display_df = df.copy()
    column_config = {}

    if "lnp_id" in display_df.columns:
        display_df.insert(
            0,
            "lipid_page",
            display_df["lnp_id"].fillna("").astype(str).apply(
                lambda value: lipid_page_url(value) if value.strip() else ""
            ),
        )
        column_config["lipid_page"] = st.column_config.LinkColumn(
            "Open",
            display_text="View Lipid",
            help="Open this LNP formulation on the Lipid Viewer page.",
        )

    st.dataframe(
        display_df,
        width="stretch",
        height=520,
        hide_index=True,
        column_config=column_config,
    )


def virtual_dataset_table(df: pd.DataFrame) -> None:
    column_order = [
        "Virtual Library",
        "LIPID_ID",
        "IL_SMILES",
        "REACTION_TYP",
        "ARCHITECTURE",
        "IL_head_id",
        "Tail1_id",
        "Tail2_id",
        "Tail3_id",
        "Tail4_id",
        "Isocyanide_id",
        "Ketone_id",
        "Carboxylic_acid_id",
        "Active_Site_Class",
        "N_Tails",
    ]
    ordered_columns = [column for column in column_order if column in df.columns]
    remaining_columns = [column for column in df.columns if column not in ordered_columns]
    display_df = df[ordered_columns + remaining_columns].copy()
    column_config = {}

    if "LIPID_ID" in display_df.columns:
        display_df.insert(
            0,
            "lipid_page",
            display_df["LIPID_ID"].fillna("").astype(str).apply(
                lambda value: virtual_lipid_page_url(value) if value.strip() else ""
            ),
        )
        column_config["lipid_page"] = st.column_config.LinkColumn(
            "Open",
            display_text="View Lipid",
            help="Open this virtual lipid on the Lipid Viewer page.",
        )

    st.dataframe(
        display_df,
        width="stretch",
        height=520,
        hide_index=True,
        column_config=column_config,
    )


def show_virtual_metric_row(df: pd.DataFrame) -> None:
    metrics = [
        ("Virtual Records", f"{len(df):,}"),
        ("Virtual Libraries", f"{df['Virtual Library'].nunique():,}" if "Virtual Library" in df else "0"),
        ("Reaction Types", f"{df['REACTION_TYP'].nunique():,}" if "REACTION_TYP" in df else "0"),
        ("Architectures", f"{df['ARCHITECTURE'].nunique():,}" if "ARCHITECTURE" in df else "0"),
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


OVERVIEW_COLORS = ["#006a71", "#7fd4ca", "#123c69", "#f3a261", "#2f8f83", "#86c7bd"]


def apply_overview_theme(fig, height: int = 360):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.72)",
        font={"family": "Helvetica Neue, Helvetica, Arial, sans-serif", "color": "#172329"},
        margin={"l": 18, "r": 18, "t": 42, "b": 24},
        colorway=OVERVIEW_COLORS,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(0, 106, 113, 0.12)", zeroline=False)
    return fig


def count_by_column(df: pd.DataFrame, column: str, name: str, top_n: int | None = None) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame(columns=[name, "Records"])
    counts = (
        df[column]
        .fillna("Unknown")
        .astype(str)
        .replace("", "Unknown")
        .value_counts()
        .rename_axis(name)
        .reset_index(name="Records")
    )
    if top_n is not None:
        counts = counts.head(top_n)
    return counts


def plot_records_by_study(data: pd.DataFrame) -> None:
    chart_data = count_by_column(data, "study_id", "Study ID")
    if chart_data.empty:
        return
    fig = px.bar(
        chart_data,
        x="Study ID",
        y="Records",
        color="Study ID",
        text="Records",
        title="Experimental Records by Study",
        color_discrete_sequence=OVERVIEW_COLORS,
    )
    fig.update_traces(textposition="outside", marker_line_color="rgba(255,255,255,0.9)", marker_line_width=1.5)
    st.plotly_chart(apply_overview_theme(fig, 380), use_container_width=True)


def plot_route_distribution(data: pd.DataFrame) -> None:
    chart_data = count_by_column(data, "route_of_administration", "Route")
    if chart_data.empty:
        return
    fig = px.pie(
        chart_data,
        names="Route",
        values="Records",
        hole=0.56,
        title="Route of Administration",
        color_discrete_sequence=OVERVIEW_COLORS,
    )
    fig.update_traces(textinfo="percent+label", pull=[0.03] * len(chart_data), marker={"line": {"color": "#ffffff", "width": 2}})
    st.plotly_chart(apply_overview_theme(fig, 380), use_container_width=True)


def plot_model_targets(data: pd.DataFrame) -> None:
    chart_data = count_by_column(data, "model_target", "Model Target", top_n=10)
    if chart_data.empty:
        return
    fig = px.bar(
        chart_data.sort_values("Records"),
        x="Records",
        y="Model Target",
        orientation="h",
        title="Top Biological Targets",
        color="Records",
        color_continuous_scale=["#d7f2ee", "#7fd4ca", "#006a71"],
    )
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(apply_overview_theme(fig, 380), use_container_width=True)


def plot_lipid_chemistry(data: pd.DataFrame) -> None:
    columns = ["il_class", "il_subclass", "il_architecture_type"]
    if not all(column in data.columns for column in columns):
        return
    chart_data = (
        data[columns]
        .fillna("Unknown")
        .astype(str)
        .groupby(columns, dropna=False)
        .size()
        .reset_index(name="Records")
    )
    fig = px.sunburst(
        chart_data,
        path=columns,
        values="Records",
        title="Ionizable Lipid Chemistry Landscape",
        color="Records",
        color_continuous_scale=["#d7f2ee", "#7fd4ca", "#006a71"],
    )
    fig.update_traces(marker={"line": {"color": "#ffffff", "width": 1.4}})
    st.plotly_chart(apply_overview_theme(fig, 430), use_container_width=True)


def plot_numeric_distributions(data: pd.DataFrame) -> None:
    numeric_columns = [
        "delivery_value",
        "particle_size_nm",
        "pdi",
        "zeta_potential_mv",
        "measured_pka",
        "encapsulation_efficiency_percent",
    ]
    frames = []
    for column in available_columns(data, numeric_columns):
        values = numeric_series(data, column).dropna()
        if values.empty:
            continue
        frames.append(pd.DataFrame({"Measurement": filter_label(column), "Value": values}))
    if not frames:
        return
    chart_data = pd.concat(frames, ignore_index=True)
    fig = px.box(
        chart_data,
        x="Measurement",
        y="Value",
        color="Measurement",
        points="outliers",
        title="Measured Property Distributions",
        color_discrete_sequence=OVERVIEW_COLORS,
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_overview_theme(fig, 420), use_container_width=True)


def biological_readout_columns(df: pd.DataFrame) -> list[str]:
    readout_columns = []
    for column in df.columns:
        normalized = column.lower()
        if column.endswith("_method"):
            continue
        looks_biological = normalized.startswith(BIOLOGICAL_READOUT_PREFIXES) or any(
            keyword in normalized for keyword in BIOLOGICAL_READOUT_KEYWORDS
        )
        if looks_biological and numeric_series(df, column).notna().any():
            readout_columns.append(column)
    return readout_columns


def readout_label(column: str) -> str:
    replacements = {
        "delivery_value": "Delivery Value",
        "delivery_relative_to_spikevax_value": "Delivery Relative to Spikevax",
        "protein_abundance_value": "Protein Abundance",
        "mRNA_binding_efficiency_percent": "mRNA Binding Efficiency (%)",
    }
    if column in replacements:
        return replacements[column]
    label = column.replace("_", " ").replace("/", " / ")
    label = label.replace("percent", "%").replace("value", "").strip()
    return label.title()


def biological_readout_long(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    context_columns = available_columns(
        df,
        ["record_id", "delivery_value_method", "route_of_administration", "model", "model_type", "model_target"],
    )
    for column in biological_readout_columns(df):
        values = numeric_series(df, column)
        for row_index, value in values.dropna().items():
            row = {context_column: df.loc[row_index, context_column] for context_column in context_columns}
            row["Column"] = column
            row["Measurement"] = readout_label(column)
            row["Value"] = value
            rows.append(row)
    return pd.DataFrame(rows)


def readout_direction(column: str) -> str:
    normalized = column.lower()
    if any(term in normalized for term in ["toxicity", "hemolysis", "alt_", "ast_", "bun_", "urea", "cera"]):
        return "lower"
    if any(
        term in normalized
        for term in ["delivery", "uptake", "editing", "viability", "protein_abundance", "mrna_binding"]
    ):
        return "higher"
    return "neutral"


def format_readout_value(value: float) -> str:
    if pd.isna(value):
        return "Not reported"
    absolute_value = abs(float(value))
    if absolute_value >= 100:
        return f"{value:,.0f}"
    if absolute_value >= 10:
        return f"{value:,.2f}"
    return f"{value:,.3f}".rstrip("0").rstrip(".")


def readout_context(row: pd.Series) -> str:
    context_bits = []
    for column in ["delivery_value_method", "model_target", "route_of_administration", "model_type"]:
        value = str(row.get(column, "")).strip()
        if value and value.lower() != "nan":
            context_bits.append(value)
    return " | ".join(context_bits) if context_bits else "Context not reported"


def readout_comparison(study_data: pd.DataFrame, row: pd.Series) -> dict[str, str | float]:
    column = str(row["Column"])
    selected_value = float(row["Value"])
    comparison_data = study_data.copy()
    method = str(row.get("delivery_value_method", "")).strip()
    if column == "delivery_value" and method and method.lower() != "nan" and "delivery_value_method" in comparison_data:
        comparison_data = comparison_data[comparison_data["delivery_value_method"].fillna("").astype(str) == method]

    values = numeric_series(comparison_data, column).dropna()
    if values.empty:
        return {"rank": "Not available", "percentile": 0.0, "n": "0", "direction": "neutral"}

    direction = readout_direction(column)
    if direction == "lower":
        rank = int((values < selected_value).sum() + 1)
        percentile = float((values >= selected_value).mean() * 100)
    elif direction == "higher":
        rank = int((values > selected_value).sum() + 1)
        percentile = float((values <= selected_value).mean() * 100)
    else:
        rank = int((values < selected_value).sum() + 1)
        percentile = float((values <= selected_value).mean() * 100)

    return {
        "rank": f"{rank:,} / {len(values):,}",
        "percentile": max(0.0, min(100.0, percentile)),
        "n": f"{len(values):,}",
        "direction": direction,
    }


def render_biological_readout(lipid_data: pd.DataFrame, study_data: pd.DataFrame) -> None:
    readout_df = biological_readout_long(lipid_data)
    if readout_df.empty:
        st.markdown(
            """
            <section class="lnp-bio-panel">
                <div class="lnp-bio-heading">
                    <p>Selected LNP Readouts</p>
                    <h3>No numeric biological readouts are available for this LNP.</h3>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    cards = []
    seen_cards = set()
    preferred_rows = []
    for column, group in readout_df.groupby("Column", sort=False):
        direction = readout_direction(str(column))
        if direction == "lower":
            preferred_rows.append(group.sort_values("Value", ascending=True).iloc[0])
        else:
            preferred_rows.append(group.sort_values("Value", ascending=False).iloc[0])

    for row in preferred_rows:
        if pd.isna(row.get("Value")):
            continue
        comparison = readout_comparison(study_data, row)
        percentile = float(comparison["percentile"])
        direction = str(comparison["direction"])
        direction_text = {
            "higher": "Higher values rank better",
            "lower": "Lower values rank better",
            "neutral": "Position within study distribution",
        }[direction]
        card_key = (
            str(row["Column"]),
            format_readout_value(float(row["Value"])),
            readout_context(row),
        )
        if card_key in seen_cards:
            continue
        seen_cards.add(card_key)
        cards.append(
            {
                "measurement": str(row["Measurement"]),
                "value": format_readout_value(float(row["Value"])),
                "context": readout_context(row),
                "rank": str(comparison["rank"]),
                "percentile": f"{percentile:.0f}%",
                "percentile_value": percentile,
                "direction": direction_text,
            }
        )

    if not cards:
        st.markdown(
            """
            <section class="lnp-bio-panel">
                <div class="lnp-bio-heading">
                    <p>Selected LNP Readouts</p>
                    <h3>No numeric biological readouts are available for this LNP.</h3>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    card_html = "\n".join(
        f"""
        <article class="lnp-bio-card">
            <p>{escape(item["measurement"])}</p>
            <h4>{escape(item["value"])}</h4>
            <div class="lnp-bio-context">{escape(item["context"])}</div>
            <div class="lnp-bio-rank">
                <span>Study rank</span>
                <strong>{escape(item["rank"])}</strong>
            </div>
            <div class="lnp-bio-ribbon" aria-label="Percentile within study">
                <span style="width: {item["percentile_value"]:.1f}%"></span>
                <i style="left: {item["percentile_value"]:.1f}%"></i>
            </div>
            <div class="lnp-bio-footnote">
                {escape(item["percentile"])} percentile | {escape(item["direction"])}
            </div>
        </article>
        """
        for item in cards
    )
    st.markdown(
        f"""
        <section class="lnp-bio-panel">
            <div class="lnp-bio-heading">
                <p>Selected LNP Readouts</p>
                <h3>Biological values and within-study significance</h3>
            </div>
            <div class="lnp-bio-card-grid">
                {card_html}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_overview(data: pd.DataFrame) -> None:
    st.markdown(
        """
        <section class="lnp-overview-intro">
            <h1>Curated Dataset Overview</h1>
            <p>
                A visual summary of the experimental LNP-Hub dataset, highlighting study coverage,
                lipid chemistry, experimental context, and measured formulation or delivery properties.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    show_metric_row(data)

    st.markdown('<div class="lnp-section-divider"></div>', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<h3 class="lnp-chart-label">Study Coverage</h3><p class="lnp-chart-note">Record counts across curated experimental studies.</p>', unsafe_allow_html=True)
        plot_records_by_study(data)
    with right:
        st.markdown('<h3 class="lnp-chart-label">Administration Context</h3><p class="lnp-chart-note">Distribution of experimental administration routes.</p>', unsafe_allow_html=True)
        plot_route_distribution(data)

    st.markdown('<div class="lnp-section-divider"></div>', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<h3 class="lnp-chart-label">Biological Coverage</h3><p class="lnp-chart-note">Most represented biological targets in the curated records.</p>', unsafe_allow_html=True)
        plot_model_targets(data)
    with right:
        st.markdown('<h3 class="lnp-chart-label">Lipid Chemistry</h3><p class="lnp-chart-note">Ionizable lipid classes, subclasses, and architecture types.</p>', unsafe_allow_html=True)
        plot_lipid_chemistry(data)

    st.markdown('<div class="lnp-section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h3 class="lnp-chart-label">Experimental Measurements</h3><p class="lnp-chart-note">Distribution of numeric delivery and physicochemical readouts where available.</p>', unsafe_allow_html=True)
    plot_numeric_distributions(data)


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
                <a class="lnp-download-action" href="data:text/csv;base64,{full_csv_href}" download="lnphub_curated_experimental_libraries.csv">Download all curated libraries as CSV</a>
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
    virtual_data = load_virtual_libraries()
    download_links = []
    for label, path, _library_name in VIRTUAL_LIBRARY_FILES:
        if not path.exists():
            continue
        encoded_csv = base64.b64encode(path.read_bytes()).decode("ascii")
        download_links.append(
            f'<a class="lnp-download-action" href="data:text/csv;base64,{encoded_csv}" '
            f'download="{escape(path.name)}">{escape(label)}</a>'
        )

    actions_html = "".join(download_links)
    st.markdown(
        f"""
        <section class="lnp-download-panel">
            <div>
                <p class="lnp-download-kicker">Virtual Screening Libraries</p>
                <h3>Download All Virtual Libraries</h3>
                <p>
                    Export virtual lipid libraries as a machine-readable CSV file.
                </p>
                <div class="lnp-download-action-grid">{actions_html}</div>
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

    if virtual_data.empty:
        st.info("No virtual screening library files are available in the data folder.")
        return

    filtered_virtual_data = apply_virtual_filters(virtual_data)
    query = st.text_input(
        "Search Lipid ID, SMILES, building block IDs, architecture, or reaction type",
        placeholder="Example: LNPhub_1V00000001",
        key="virtual_search",
    )
    filtered_virtual_data = apply_virtual_search(filtered_virtual_data, query)
    show_virtual_metric_row(filtered_virtual_data)
    virtual_dataset_table(filtered_virtual_data)

    filtered_virtual_csv = filtered_virtual_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered virtual library CSV",
        data=filtered_virtual_csv,
        file_name="lnphub_filtered_virtual_libraries.csv",
        mime="text/csv",
        key="download_filtered_virtual_libraries",
    )


def render_datasets(data: pd.DataFrame) -> None:
    selected_dataset = st.radio(
        "Dataset library",
        ["Curated Experimental Libraries", "Virtual Screening Libraries"],
        horizontal=True,
        label_visibility="collapsed",
        key="dataset_library_menu",
    )

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
        show_rdkit_warning()
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
    st.caption("Inspect lipid structures, formulation components, identity metadata, and molecular descriptors.")

    experimental_mode = "Lipid Viewer of Experimental Libraries"
    virtual_mode = "Lipid Viewer of Virtual Libraries"
    virtual_lipid_id = query_param_value("virtual_lipid_id")
    requested_experimental_id = query_param_value("lnp_id") or query_param_value("il_id")
    deeplink_key = ""
    if virtual_lipid_id:
        deeplink_key = f"virtual:{virtual_lipid_id}"
    elif requested_experimental_id:
        deeplink_key = f"experimental:{requested_experimental_id}"

    if deeplink_key and st.session_state.get("_lipid_viewer_mode_deeplink") != deeplink_key:
        st.session_state["lipid_viewer_library_mode"] = virtual_mode if virtual_lipid_id else experimental_mode
        st.session_state["_lipid_viewer_mode_deeplink"] = deeplink_key
    if st.session_state.get("lipid_viewer_library_mode") not in {experimental_mode, virtual_mode}:
        st.session_state["lipid_viewer_library_mode"] = experimental_mode

    selected_mode = st.radio(
        "Lipid viewer library",
        [experimental_mode, virtual_mode],
        horizontal=True,
        label_visibility="collapsed",
        key="lipid_viewer_library_mode",
    )
    st.markdown('<div class="lnp-section-divider"></div>', unsafe_allow_html=True)

    if selected_mode == virtual_mode:
        virtual_data = load_virtual_libraries()
        render_virtual_lipid_viewer(virtual_data, virtual_lipid_id)
    else:
        render_experimental_lipid_viewer(data)


def render_experimental_lipid_viewer(data: pd.DataFrame) -> None:
    study_options = filtered_options(data["study_id"]) if "study_id" in data.columns else []
    if not study_options:
        st.info("No Study IDs are available in the dataset.")
        return

    requested_lnp = query_param_value("lnp_id")
    requested_il = query_param_value("il_id")
    requested_rows = pd.DataFrame()
    if requested_lnp and "lnp_id" in data.columns:
        requested_rows = data[data["lnp_id"].fillna("").astype(str) == requested_lnp]
    if requested_rows.empty and requested_il and "il_id" in data.columns:
        requested_rows = data[data["il_id"].fillna("").astype(str) == requested_il]
        requested_lnp = first_value(requested_rows, "lnp_id")
    requested_study = first_value(requested_rows, "study_id")

    requested_study_state_key = "_lipid_viewer_requested_study"
    requested_study_token = requested_lnp or requested_il
    if (
        requested_study in study_options
        and requested_study_token
        and st.session_state.get(requested_study_state_key) != requested_study_token
    ):
        st.session_state["lipid_viewer_study"] = requested_study
        st.session_state[requested_study_state_key] = requested_study_token
    if st.session_state.get("lipid_viewer_study") not in study_options:
        st.session_state["lipid_viewer_study"] = study_options[0]

    selected_study = single_tick_selector("Study ID", study_options, key="lipid_viewer_study")
    study_data = data[data["study_id"].astype(str) == selected_study].copy()

    formulations = filtered_options(study_data["lnp_id"]) if "lnp_id" in study_data.columns else []
    if not formulations:
        st.info("No LNP IDs are available for this study.")
        return

    requested_lnp_state_key = "_lipid_viewer_requested_lnp"
    if requested_lnp in formulations and st.session_state.get(requested_lnp_state_key) != requested_lnp:
        st.session_state["lipid_viewer_lnp"] = requested_lnp
        st.session_state[requested_lnp_state_key] = requested_lnp
    if st.session_state.get("lipid_viewer_lnp") not in formulations:
        st.session_state["lipid_viewer_lnp"] = formulations[0]

    selected_lnp = st.selectbox("LNP ID", formulations, key="lipid_viewer_lnp")
    lipid_data = study_data[study_data["lnp_id"].astype(str) == selected_lnp].copy()
    smiles = first_value(lipid_data, "il_smiles")

    st.subheader(selected_lnp)

    render_lipid_component_cards(lipid_data)

    left, right = st.columns([1, 1])
    with left:
        st.markdown("#### Structure")
        if Chem is None:
            show_rdkit_warning()
        elif not smiles:
            st.info("No SMILES string is available for this lipid.")
        else:
            two_d_tab, three_d_tab = st.tabs(["2D Structure", "3D Structure"])
            with two_d_tab:
                render_2d_structure(smiles)
            with three_d_tab:
                render_3d_structure(smiles)
            with st.expander("SMILES", expanded=False):
                st.code(smiles, language="text")

        if Chem is not None:
            st.markdown("#### Building Blocks")
            render_building_block_viewers(lipid_data)

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

    csv = lipid_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Lipid Records",
        data=csv,
        file_name=f"{selected_lnp}_records.csv",
        mime="text/csv",
    )

    st.markdown('<div class="lnp-section-divider"></div>', unsafe_allow_html=True)
    render_biological_readout(lipid_data, study_data)


def render_virtual_lipid_viewer(virtual_data: pd.DataFrame, requested_lipid_id: str) -> None:
    library_options = filtered_options(virtual_data["Virtual Library"]) if "Virtual Library" in virtual_data.columns else []
    if not library_options:
        st.info("No virtual libraries are available.")
        return

    requested_library = ""
    if requested_lipid_id and "LIPID_ID" in virtual_data.columns:
        requested_rows = virtual_data[virtual_data["LIPID_ID"].fillna("").astype(str) == requested_lipid_id]
        requested_library = first_value(requested_rows, "Virtual Library")

    requested_library_state_key = "_virtual_lipid_viewer_requested_library"
    if (
        requested_library in library_options
        and st.session_state.get(requested_library_state_key) != requested_lipid_id
    ):
        st.session_state["virtual_lipid_library"] = requested_library
        st.session_state[requested_library_state_key] = requested_lipid_id
    if st.session_state.get("virtual_lipid_library") not in library_options:
        st.session_state["virtual_lipid_library"] = library_options[0]

    selected_library = single_tick_selector(
        "Virtual Library",
        library_options,
        key="virtual_lipid_library",
    )
    library_data = virtual_data[virtual_data["Virtual Library"].astype(str) == selected_library].copy()
    virtual_ids = filtered_options(library_data["LIPID_ID"]) if "LIPID_ID" in library_data.columns else []
    if not virtual_ids:
        st.info("No virtual lipid IDs are available for this library.")
        return

    requested_virtual_state_key = "_virtual_lipid_viewer_requested_id"
    if (
        requested_lipid_id in virtual_ids
        and st.session_state.get(requested_virtual_state_key) != requested_lipid_id
    ):
        st.session_state["virtual_lipid_viewer_id"] = requested_lipid_id
        st.session_state[requested_virtual_state_key] = requested_lipid_id
    if st.session_state.get("virtual_lipid_viewer_id") not in virtual_ids:
        st.session_state["virtual_lipid_viewer_id"] = virtual_ids[0]

    selected_lipid = st.selectbox("Virtual Lipid ID", virtual_ids, key="virtual_lipid_viewer_id")
    lipid_data = library_data[library_data["LIPID_ID"].astype(str) == selected_lipid].copy()
    smiles = first_value(lipid_data, "IL_SMILES")

    st.subheader(selected_lipid)
    st.caption("Virtual screening library lipid")

    left, right = st.columns([1, 1])
    with left:
        st.markdown("#### Structure")
        if Chem is None:
            show_rdkit_warning()
        elif not smiles:
            st.info("No SMILES string is available for this virtual lipid.")
        else:
            two_d_tab, three_d_tab = st.tabs(["2D Structure", "3D Structure"])
            with two_d_tab:
                render_2d_structure(smiles)
            with three_d_tab:
                render_3d_structure(smiles)
            with st.expander("SMILES", expanded=False):
                st.code(smiles, language="text")

        if Chem is not None:
            st.markdown("#### Virtual Building Blocks")
            render_virtual_component_viewers(lipid_data)

    with right:
        st.markdown("#### Virtual Library Metadata")
        identity_columns = available_columns(
            lipid_data,
            [
                "Virtual Library",
                "LIPID_ID",
                "REACTION_TYP",
                "ARCHITECTURE",
                "IL_head_id",
                "Isocyanide_id",
                "Ketone_id",
                "Carboxylic_acid_id",
                "Tail1_id",
                "Tail2_id",
                "Tail3_id",
                "Tail4_id",
                "Active_Site_Class",
                "N_Tails",
            ],
        )
        if identity_columns:
            st.dataframe(details_table(lipid_data, identity_columns), hide_index=True, width="stretch")
        else:
            st.info("No virtual lipid metadata is available.")

    csv = lipid_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Lipid Records",
        data=csv,
        file_name=f"{selected_lipid}_records.csv",
        mime="text/csv",
        key="download_virtual_lipid_records",
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


def render_about() -> None:
    st.title("About LNP-Hub")
    st.caption("A curated data commons for lipid nanoparticle formulation and delivery science.")
    st.markdown(
        """
        LNP-Hub is being built as a public web portal for curated lipid nanoparticle
        records across studies, chemistries, formulations, biological models, and
        delivery readouts.
        """
    )


data = load_csv()
page = active_page()
render_top_nav(page)
normalize_path_url()

if page == "Home":
    render_home(data)
elif page == "Overview":
    render_overview(data)
elif page == "Datasets":
    render_datasets(data)
elif page == "Lipid Viewer":
    render_lipid_viewer(data)
elif page == "Documentation":
    render_documentation()
elif page == "About":
    render_about()

render_footer()
