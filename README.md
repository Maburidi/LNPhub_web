# LNPhub Web

Streamlit portal for exploring a curated lipid nanoparticle dataset.

## Features

- Filter by study, cargo type, delivery value method, route, model, lipid class, helper lipid, and PEG lipid.
- Search by `il_id`, SMILES, record ID, study ID, or LNP ID.
- Render ionizable lipid structures with RDKit.
- Plot delivery, particle size, PDI, zeta potential, pKa, encapsulation efficiency, and molecular descriptors.
- Download filtered results as CSV.

## Repository Layout

```text
.
├── streamlit_app.py
├── requirements.txt
├── data/
│   └── LNPhub_public_two_studies.csv
├── notebooks/
│   └── LNPhub_web_colab.ipynb
└── .streamlit/
    └── config.toml
```

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy Online With Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Choose **Create app**.
4. Select the GitHub repository, branch, and `streamlit_app.py` as the entrypoint.
5. Deploy.

Streamlit Community Cloud reads `requirements.txt` from the repository root and installs the app dependencies automatically.

## Run From Google Colab

Open `notebooks/LNPhub_web_colab.ipynb` in Colab. The notebook installs the dependencies, clones or updates this repository, and launches the Streamlit app through a temporary public tunnel.

## Dataset Notes

The included CSV is a public two-study sample. Replace `data/LNPhub_public_two_studies.csv` with the full public curated dataset when it is ready, keeping the same column names where possible.
