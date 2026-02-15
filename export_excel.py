import pandas as pd

def export_excel(file_results, path):
    rows = []

    for r in file_results:
        rows.append({
            "filename": r["filename"],
            "lines": r["lines"],
            "complexity": r["complexity"],
            "functions": r["functions"],
            "classes": r["classes"],
            "complexity_density": r["complexity_density"],
            "analyzed_at": r["analyzed_at"]
        })

    df = pd.DataFrame(rows)

    # Sort by highest complexity density
    df = df.sort_values(
        by="complexity_density",
        ascending=False
    )

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="File Metrics"
        )

        worksheet = writer.sheets["File Metrics"]

        # ✅ OPENPYXL-CORRECT SYNTAX
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        worksheet.column_dimensions["A"].width = 70
        for col in ["B", "C", "D", "E", "F", "G"]:
            worksheet.column_dimensions[col].width = 18
