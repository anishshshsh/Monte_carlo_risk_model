import os
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np

from src.risk_model import load_risks, compute_scores
from src.visualizations import plot_heatmap, plot_top_risks
from src.monte_carlo import run_monte_carlo
from src.report import create_pdf_report

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="IB Risk Model", page_icon="📊", layout="wide")

ROOT = Path(__file__).parent
DEFAULT_CSV = ROOT / "data" / "risks.csv"  # <-- your original IB dataset

# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.title("⚙️ Settings")
# Removed theme selection to force dark mode
uploaded = st.sidebar.file_uploader("Upload risks CSV (optional)", type=["csv"])
trials = st.sidebar.number_input("Monte Carlo trials", min_value=1000, max_value=200000, value=10000, step=1000)
base_exposure = st.sidebar.number_input("Base exposure (₹)", min_value=10000, value=1_000_000, step=10000)
run_button = st.sidebar.button("Run Model")

# -------------------------
# Theme CSS (dark mode only)
# -------------------------
def apply_theme_css():
    css = """
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; color: #e6eef8; }
    .card { background: #121418; border-radius: 10px; padding: 16px; box-shadow: 0 6px 18px rgba(0,0,0,0.6); margin-bottom: 18px; color: #e6eef8; }
    table.dataframe th { background-color:#22262d !important; color:#fff !important; text-align:center; }
    table.dataframe td { text-align:center; padding:6px 8px; color:#e6eef8 !important; }
    .metric { text-align:center; padding:10px; border-radius:8px; color:#e6eef8; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

apply_theme_css()

# -------------------------
# Load data (default IB dataset if available)
# -------------------------
def load_default_df():
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            source = "Uploaded CSV"
        except Exception as e:
            st.sidebar.error(f"Failed to read uploaded CSV: {e}")
            df = pd.DataFrame()
            source = "Upload failed"
    else:
        if DEFAULT_CSV.exists():
            df = pd.read_csv(DEFAULT_CSV)
            source = str(DEFAULT_CSV.name)
        else:
            st.sidebar.warning("Default dataset not found at data/risks.csv. Please upload a valid risks CSV.")
            df = pd.DataFrame(columns=["Category", "Description", "Probability", "Impact"])
            source = "Empty"
    return df, source

df, source_name = load_default_df()

# -------------------------
# Top bar and quick metrics
# -------------------------
st.title("📊 Investment Banking Risk Model")
st.markdown(f"**Data source:** {source_name}")

# show basic cards if df not empty
if not df.empty:
    # try compute quick scores if Probability/Impact exist
    df_preview = df.copy()
    preview_ok = ("Probability" in df_preview.columns) and ("Impact" in df_preview.columns)
    if preview_ok:
        df_scored_preview = compute_scores(df_preview)
        total_risks = len(df_scored_preview)
        max_score = int(df_scored_preview['Score'].max())
        top_cat = df_scored_preview.loc[0, "Category"]
    else:
        total_risks = len(df_preview)
        max_score = "-"
        top_cat = "-"
else:
    total_risks = 0
    max_score = "-"
    top_cat = "-"

c1, c2, c3 = st.columns([1.5,1.5,2])
with c1:
    st.markdown(f"<div class='card'><h4>Total risks</h4><h2 style='margin-top:6px'>{total_risks}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><h4>Max score</h4><h2 style='margin-top:6px'>{max_score}</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='card'><h4>Top category</h4><h2 style='margin-top:6px'>{top_cat}</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# Show input table (styled, centered)
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Input risks (first 20 rows)")
if df.empty:
    st.info("No data available. Upload a risks CSV in the sidebar or place data/risks.csv in the project.")
else:
    # center numeric columns via styler and render as HTML
    try:
        styled = df.head(20).style.set_properties(**{'text-align':'center'})
        # ensure headers centered too
        styled = styled.set_table_styles([{'selector': 'th','props': [('text-align', 'center')]}])
        st.write(styled.to_html(), unsafe_allow_html=True)
    except Exception:
        # fallback
        st.dataframe(df.head(20), use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Run model and show outputs
# -------------------------
if run_button:
    if df.empty:
        st.error("No data to run. Upload a valid risks CSV or ensure data/risks.csv exists.")
    else:
        # compute and save scored results
        try:
            df_scored = compute_scores(df)
        except Exception as e:
            st.error(f"Error computing scores: {e}")
            st.stop()

        out_dir = ROOT / "outputs"
        out_dir.mkdir(exist_ok=True)
        scored_csv_path = out_dir / "risks_scored.csv"
        df_scored.to_csv(scored_csv_path, index=False)

        # top table (styled)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Scored Risks (top 20)")
        try:
            styled2 = df_scored.head(20).style.format({"Score":"{:.0f}"}).set_properties(**{'text-align':'center'})
            styled2 = styled2.set_table_styles([{'selector': 'th','props': [{'text-align': 'center'}]}])
            st.write(styled2.to_html(), unsafe_allow_html=True)
        except Exception:
            st.dataframe(df_scored.head(20), use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # visuals
        heatmap_path = out_dir / "risk_heatmap.png"
        top_path = out_dir / "top_risks.png"
        try:
            plot_heatmap(df_scored, str(heatmap_path))
            plot_top_risks(df_scored, str(top_path), top_n=10)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Visuals")
            st.image(str(heatmap_path), use_container_width=True)
            st.image(str(top_path), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not generate visuals: {e}")

        # Monte Carlo
        try:
            losses, summary = run_monte_carlo(df_scored, trials=int(trials), base_exposure=float(base_exposure))
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Monte Carlo Summary")
            st.write(summary)

            # histogram
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8,3.5))
            ax.hist(losses, bins=80)
            ax.set_xlabel("Total Loss (₹)")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Monte Carlo failed: {e}")

        # PDF report
        try:
            pdf_path = out_dir / "ib_risk_report.pdf"
            summary_lines = [
                f"Trials: {summary.get('trials', '')}",
                f"Mean loss: {summary.get('mean_loss',''):.2f}",
                f"Median loss: {summary.get('median_loss',''):.2f}",
                f"VaR(95%): {summary.get('VaR_95',''):.2f}",
                f"ES(95%): {summary.get('ES_95',''):.2f}"
            ]
            create_pdf_report(str(pdf_path), "IB Risk Model Report", "\n".join(summary_lines),
                              [str(heatmap_path), str(top_path), str(out_dir / "loss_distribution.png")])
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF report", f, file_name="ib_risk_report.pdf")
        except Exception as e:
            st.warning(f"Could not create/download PDF: {e}")

# -------------------------
# Footer / small help
# -------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Need help? Upload a CSV with columns: `Category, Description, Probability, Impact` (Probability & Impact in 1-5 scale).")
