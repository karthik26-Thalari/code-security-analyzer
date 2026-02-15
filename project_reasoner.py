import json
from llm_engine import LLM

def reason_project(file_results, api_key):
    top = sorted(
        file_results,
        key=lambda x: x.get("risk_score", 0),
        reverse=True
    )[:20]

    summary = {
        "total_files": len(file_results),
        "files_with_risk": sum(
            1 for f in file_results
            if f.get("risk_score", 0) > 0
        ),
        "top_risky_files": top
    }

    prompt = f"""
You are a Senior Software Architect and Security Auditor.

You are analyzing a COMPLETE SOFTWARE PROJECT using preprocessed static analysis results.
All source files have already been scanned locally. No raw source code is provided.

Your goal is to explain:
- What this project is about
- How the codebase is structured
- What security and code-quality risks realistically exist
- Whether this project is production ready
- How it can be improved

========================
ANALYSIS CONTEXT
========================
The following JSON is a summarized view of the highest-risk findings
derived from the full codebase analysis:

{json.dumps(summary, indent=2)}

========================
REPORT REQUIREMENTS
========================

Produce a structured, professional report with the following sections:

1. Project Overview
- What this project appears to do
- Intended usage (learning / internal / prototype / production)
- Architectural patterns inferred from the analysis

2. Code Quality Assessment
- Overall maintainability
- Complexity and logic density concerns
- Areas of technical debt
- Testing or structure observations

3. Security Analysis
- Realistic security risks (not theoretical)
- Client-side trust issues
- Configuration and dependency risks
- What is NOT a security vulnerability

4. Exploitability Assessment
- Can this project be exploited as-is?
- Under what conditions would risks become real vulnerabilities?

5. Production Readiness Verdict
Choose ONE and justify clearly:
- NOT PRODUCTION READY
- CONDITIONALLY PRODUCTION READY
- PRODUCTION READY

6. Improvement Recommendations
- Quick wins
- Structural improvements
- Long-term hardening steps

7. Overall Rating
- Provide a numeric score from 0 to 10
- Explain what influenced the rating

8. Confidence Level
- Provide a confidence score between 0.0 and 1.0
- Explain uncertainty sources

========================
IMPORTANT RULES
========================
- Do NOT invent vulnerabilities
- Do NOT mention token limits or model behavior
- Base conclusions ONLY on the analysis provided
- Distinguish clearly between:
  * security vulnerabilities
  * code quality issues
  * process or tooling gaps
- Write in a professional audit tone

Generate the full report now.
"""

    llm = LLM(api_key)
    return llm.reason(prompt, max_tokens=3250)
