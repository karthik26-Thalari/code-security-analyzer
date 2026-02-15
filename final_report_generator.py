from llm_engine import LLM

def generate_final_report(file_results, api_key):
    summary = []

    for r in file_results:
        summary.append({
            "file": r["file"],
            "issues": r.get("static", []) + r.get("notes", []),
            "dataflow": r.get("dataflow")
        })

    context = {
        "total_files": len(file_results),
        "findings": summary
    }

    prompt = f"""
You are a senior security architect and software quality reviewer.

Given the following structured analysis of a software project:

{context}

Produce a COMPLETE PROJECT REPORT with:

1. Overall project summary
2. Security risk analysis
3. Bug & quality assessment
4. Exploitability discussion (realistic attack scenarios)
5. Overall rating (0–10)
6. Is the project production ready? (YES/NO/CONDITIONAL)
7. Top 5 fixes that matter most
8. Long-term improvement advice

Be clear, professional, and realistic.
"""

    llm = LLM(api_key)
    return llm.reason(prompt)
