import os
import re

# ----------------------------
# CONFIG
# ----------------------------
MAX_LINES = 500
TOP_N_FOR_LLM = 20

DANGEROUS_KEYWORDS = {
    "eval": "Use of eval()",
    "exec": "Use of exec()",
    "subprocess": "Shell execution",
    "os.system": "Shell execution",
    "pickle": "Unsafe deserialization",
    "yaml.load": "Unsafe YAML load",
    "input(": "User input handling",
    "argparse": "CLI argument parsing",
    "open(": "File system access",
}

# ----------------------------
# NORMALIZATION
# ----------------------------
def normalize_code(code: str) -> str:
    lines = code.splitlines()
    if len(lines) > MAX_LINES:
        lines = lines[:MAX_LINES]
    return "\n".join(lines)

# ----------------------------
# FILE CLASSIFICATION
# ----------------------------
def classify_file(path: str) -> str:
    p = path.lower()

    if any(x in p for x in ["node_modules", "venv", ".git"]):
        return "vendor"
    if "test" in p or p.endswith("_test.py"):
        return "test"
    if p.endswith((".md", ".rst")):
        return "docs"
    if p.endswith((".json", ".yaml", ".yml", ".env")):
        return "config"
    return "core"

# ----------------------------
# SIGNAL EXTRACTION
# ----------------------------
def extract_signals(code: str, category: str):
    signals = []

    for key, desc in DANGEROUS_KEYWORDS.items():
        if key in code:
            signals.append(desc)

    if category == "config":
        if re.search(r"(password|secret|token|key)", code, re.I):
            signals.append("Possible hardcoded secret")

    if category == "docs":
        if "todo" in code.lower() or "fixme" in code.lower():
            signals.append("Unresolved TODO/FIXME")

    return list(set(signals))

# ----------------------------
# RISK SCORING
# ----------------------------
def score_risk(signals, category):
    score = 0

    for s in signals:
        if "Shell" in s:
            score += 5
        elif "User input" in s:
            score += 4
        elif "deserialization" in s:
            score += 5
        elif "secret" in s:
            score += 5
        else:
            score += 2

    if category == "config":
        score += 3
    if category == "test":
        score -= 2
    if category == "docs":
        score -= 3

    return max(score, 0)

# ----------------------------
# MAIN PREPROCESS FUNCTION
# ----------------------------
def preprocess_file(path: str, code: str):
    category = classify_file(path)
    normalized = normalize_code(code)
    signals = extract_signals(normalized, category)
    risk = score_risk(signals, category)

    return {
        "file": path,
        "category": category,
        "signals": signals,
        "risk_score": risk
    }

# ----------------------------
# PROJECT PREPROCESSING
# ----------------------------
def preprocess_project(file_results):
    """
    Takes raw analyzer output and prepares LLM-safe summaries
    """

    all_files = []
    risky_files = []

    for r in file_results:
        entry = {
            "file": r["file"],
            "category": r.get("category", "unknown"),
            "signals": r.get("signals", []),
            "risk_score": r.get("risk_score", 0)
        }
        all_files.append(entry)

        if entry["risk_score"] > 0:
            risky_files.append(entry)

    risky_files.sort(key=lambda x: x["risk_score"], reverse=True)

    return {
        "total_files": len(all_files),
        "files_with_risk": len(risky_files),
        "top_risky_files": risky_files[:TOP_N_FOR_LLM],
        "coverage": round(len(all_files) / max(len(all_files), 1), 2)
    }
