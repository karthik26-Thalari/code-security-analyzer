import streamlit as st
import os
import re
import tempfile

from project_loader import load_zip, load_github
from utils import walk_project, Timer
from analyzer import analyze_file
from project_reasoner import reason_project
from export_excel import export_excel
from export_pdf import export_pdf
from visuals import (
    issue_distribution,
    severity_breakdown,
    file_hotspots
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Project Security Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Project Security & Quality Analyzer")
st.caption(
    "ZIP / GitHub → Vulnerabilities • Rating • Production Readiness • Reports"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenRouter API Key", type="password")
    st.divider()
    st.markdown(
        """
        **How this tool works**
        - Reads every source file
        - Preprocesses & extracts security signals
        - Scores local risk (no per-file LLM)
        - ONE LLM call for project-level judgment
        - Generates visuals & reports
        """
    )

# --------------------------------------------------
# SHARED ANALYSIS FUNCTION
# --------------------------------------------------
def run_analysis(root_path, project_name):
    timer = Timer()
    files = walk_project(root_path)

    st.success(f"Found {len(files)} source files")

    # ---------------- FILE PROCESSING LOG ----------------
    st.subheader("📜 File Processing Log")
    log_box = st.empty()
    progress = st.progress(0)

    file_results = []
    logs = []

    for i, file in enumerate(files):
        progress.progress((i + 1) / len(files))
        logs.append(f"📄 Reading: {file}")
        log_box.text("\n".join(logs[-15:]))

        try:
            with open(file, errors="ignore") as f:
                code = f.read()
            file_results.append(analyze_file(code, file))
        except Exception as e:
            file_results.append({
                "file": file,
                "category": "unknown",
                "signals": [str(e)],
                "risk_score": 1
            })

    progress.empty()
    st.success(f"Local analysis completed in {timer.elapsed()} seconds")

    # ---------------- PROJECT LEVEL LLM ----------------
    with st.spinner("🧠 Generating final project report (LLM reasoning)..."):
        final_report = reason_project(file_results, api_key)

    # ---------------- EXTRACT RATING ----------------
    rating = "N/A"
    match = re.search(r"(\d+(\.\d+)?)/10", final_report)
    if match:
        rating = match.group(1)

    # ---------------- VERDICT ----------------
    verdict = "UNKNOWN"
    fr = final_report.lower()
    if "not ready" in fr or "not production" in fr:
        verdict = "❌ NOT PRODUCTION READY"
    elif "conditional" in fr:
        verdict = "⚠️ CONDITIONALLY READY"
    else:
        verdict = "✅ NO CRITICAL BLOCKERS FOUND"

    # ---------------- SUMMARY METRICS ----------------
    files_with_risk = sum(1 for r in file_results if r.get("risk_score", 0) > 0)
    coverage = round((len(files) / max(len(files), 1)) * 100, 2)

    summary_data = {
        "Project Name": project_name,
        "Total Files": len(files),
        "Files With Risk": files_with_risk,
        "Analysis Coverage (%)": coverage,
        "Overall Rating": rating,
        "Production Readiness": verdict,
        "Confidence Level": "0.3"
    }

    # ---------------- SUMMARY UI ----------------
    st.divider()
    st.subheader("📊 Project Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Files Analyzed", len(files))
    c2.metric("Files With Risk", files_with_risk)
    c3.metric("Overall Rating", rating)

    st.subheader("🏁 Production Readiness Verdict")
    st.markdown(f"### {verdict}")

    # ---------------- VISUAL DASHBOARD ----------------
    st.divider()
    st.subheader("📈 Visual Insights")

    st.plotly_chart(
        issue_distribution(file_results),
        width="stretch"
    )

    st.plotly_chart(
        severity_breakdown(file_results),
        width="stretch"
    )

    hotspot_fig = file_hotspots(file_results)
    if hotspot_fig:
        st.plotly_chart(hotspot_fig, width="stretch")

    # ---------------- FINAL REPORT ----------------
    st.divider()
    st.subheader("🧠 Final LLM Project Report")
    st.write(final_report)

    # ---------------- EXPORTS ----------------
    with tempfile.TemporaryDirectory() as tmp:
        excel_path = os.path.join(tmp, "analysis_report.xlsx")
        pdf_path = os.path.join(tmp, "final_project_report.pdf")

        export_excel(
            file_results=file_results,
            path=excel_path
        )

        export_pdf(final_report, pdf_path)

        st.divider()
        st.subheader("⬇️ Download Reports")

        c1, c2 = st.columns(2)

        with c1:
            st.download_button(
                "📊 Download Excel Report",
                open(excel_path, "rb"),
                file_name="analysis_report.xlsx"
            )

        with c2:
            st.download_button(
                "📄 Download PDF Report",
                open(pdf_path, "rb"),
                file_name="final_project_report.pdf"
            )
# --------------------------------------------------
# TABS
# --------------------------------------------------
zip_tab, git_tab = st.tabs(["📦 ZIP Analysis", "🔗 GitHub Analysis"])

# ==================================================
# ZIP ANALYSIS TAB
# ==================================================
with zip_tab:
    st.subheader("📦 Analyze ZIP Project")

    zip_file = st.file_uploader(
        "Drag & drop ZIP here",
        type=["zip"],
        help="Max 200MB"
    )

    analyze_zip = st.button("🚀 Analyze ZIP Project", type="primary")

    if analyze_zip:
        if not api_key:
            st.error("Please enter your OpenRouter API key")
        elif not zip_file:
            st.error("Please upload a ZIP file")
        else:
            with st.spinner("Extracting ZIP..."):
                root = load_zip(zip_file)
            run_analysis(root, project_name="ZIP Project")

# ==================================================
# GITHUB ANALYSIS TAB
# ==================================================
with git_tab:
    st.subheader("🔗 Analyze GitHub Repository")

    repo_url = st.text_input(
        "GitHub Repo URL",
        placeholder="https://github.com/user/repo"
    )

    analyze_git = st.button("🚀 Analyze GitHub Repo", type="primary")

    if analyze_git:
        if not api_key:
            st.error("Please enter your OpenRouter API key")
        elif not repo_url:
            st.error("Please enter a GitHub repository URL")
        else:
            with st.spinner("Cloning repository..."):
                root = load_github(repo_url)
            run_analysis(root, project_name=repo_url)
