import os

def detect_file_type(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".py":
        return "python"
    if ext in {".js", ".jsx", ".ts"}:
        return "javascript"
    if ext in {".json", ".yaml", ".yml", ".env"}:
        return "config"
    if ext in {".md", ".txt"}:
        return "docs"

    return "unknown"
