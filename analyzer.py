import re
from datetime import datetime

CONTROL_KEYWORDS = re.compile(
    r"\b(if|elif|else|for|while|case|catch|try|except|switch)\b"
)

FUNCTION_PATTERNS = re.compile(
    r"\b(function\s+\w+|\bdef\s+\w+|\b[a-zA-Z_]\w*\s*\([^)]*\)\s*=>)\b"
)

CLASS_PATTERNS = re.compile(
    r"\b(class\s+\w+)\b"
)

def analyze_file(code: str, path: str):
    lines = code.splitlines()
    line_count = len(lines)

    complexity = len(CONTROL_KEYWORDS.findall(code))
    functions = len(FUNCTION_PATTERNS.findall(code))
    classes = len(CLASS_PATTERNS.findall(code))

    complexity_density = (
        complexity / line_count
        if line_count else 0
    )

    # 🔑 DERIVED RISK SCORE (0–10)
    risk_score = round(
        min(complexity_density * 10, 10), 2
    )

    return {
        "filename": path,
        "lines": line_count,
        "complexity": complexity,
        "functions": functions,
        "classes": classes,
        "complexity_density": round(complexity_density, 4),
        "risk_score": risk_score,             
        "analyzed_at": datetime.now().strftime("%H:%M.%S")
    }
