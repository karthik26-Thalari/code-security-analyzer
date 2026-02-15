import plotly.express as px
import pandas as pd
from collections import Counter

# ==================================================
# ISSUE DISTRIBUTION
# ==================================================
# Shows how many files contain any detected signals
# vs completely clean files
# ==================================================
def issue_distribution(file_results):
    counts = Counter()

    for r in file_results:
        if r.get("risk_score", 0) > 0:
            counts["Files With Risk"] += 1
        else:
            counts["Clean Files"] += 1

    if not counts:
        counts["No Data"] = 1

    df = pd.DataFrame({
        "Category": list(counts.keys()),
        "Count": list(counts.values())
    })

    fig = px.pie(
        df,
        names="Category",
        values="Count",
        title="Issue Distribution"
    )

    return fig


# ==================================================
# SEVERITY BREAKDOWN
# ==================================================
# Buckets files by derived risk score
# ==================================================
def severity_breakdown(file_results):
    severity = Counter()

    for r in file_results:
        score = r.get("risk_score", 0)

        if score >= 8:
            severity["HIGH"] += 1
        elif score >= 4:
            severity["MEDIUM"] += 1
        elif score > 0:
            severity["LOW"] += 1

    if not severity:
        severity["NONE"] = 1

    df = pd.DataFrame({
        "Severity": list(severity.keys()),
        "Count": list(severity.values())
    })

    fig = px.bar(
        df,
        x="Severity",
        y="Count",
        text="Count",
        title="Risk Severity Breakdown"
    )

    fig.update_layout(
        xaxis_title="Severity Level",
        yaxis_title="Number of Files"
    )

    return fig


# ==================================================
# FILE HOTSPOTS
# ==================================================
# Highlights the most risk-heavy files
# ==================================================
def file_hotspots(file_results, top_n=10):
    hotspot = Counter()

    for r in file_results:
        filename = r.get("filename")
        if not filename:
            continue
        hotspot[filename] += r.get("risk_score", 0)

    if not hotspot:
        return None

    top = hotspot.most_common(top_n)

    df = pd.DataFrame(
        top,
        columns=["File", "Risk Score"]
    )

    fig = px.bar(
        df,
        x="Risk Score",
        y="File",
        orientation="h",
        title="Top Risky Files"
    )

    fig.update_layout(
        xaxis_title="Accumulated Risk Score",
        yaxis_title="File"
    )

    return fig
