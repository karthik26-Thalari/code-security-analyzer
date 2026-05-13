# 🧠 AI Project Security & Quality Analyzer

A **Streamlit-based AI security auditing tool** that scans any Python/JavaScript codebase for vulnerabilities, code quality issues, and production readiness. Accepts a **ZIP file** or a **GitHub URL**, runs multi-pass local static analysis, and uses a single **OpenRouter LLM call** to generate a professional audit report — exportable as Excel and PDF.

---

## ✨ Features

- 📦 **Two input modes** — upload a ZIP file or paste any public GitHub repo URL
- 🔍 **Multi-pass local analysis** — static, semantic, dataflow, and complexity passes with zero per-file LLM cost
- 🧠 **One LLM call** for a full project-level audit report (security risks, production readiness verdict, rating out of 10)
- 📊 **Interactive visual dashboard** — issue distribution pie chart, severity bar chart, file hotspot ranking
- 📄 **Downloadable reports** — Excel (per-file metrics) and PDF (full LLM report)
- ⚡ **Fast** — local analysis completes in seconds; only the final reasoning step uses the LLM

---

## 🗂️ Project Structure

```
code-security-analyzer-main/
│
├── app.py                    # Main Streamlit app — UI, tabs, orchestration
│
├── analyzer.py               # Per-file metrics: complexity, functions, classes, risk score
├── preprocess.py             # Danger keyword detection, file classification, signal extraction
├── project_reasoner.py       # Builds LLM prompt from top risky files, calls LLM
├── llm_engine.py             # OpenRouter API client (LLM wrapper)
│
├── static_pass.py            # AST-based static analysis (eval/exec, bare try)
├── semantic_pass.py          # Comment/security-intent mismatch detection
├── dataflow_pass.py          # Taint tracking — untrusted input → dangerous sink
├── reasoning_pass.py         # Combines all pass outputs into hypotheses
│
├── file_router.py            # Detects file type by extension
├── project_loader.py         # ZIP extraction and GitHub repo cloning
├── utils.py                  # File walker, timer, ignored directory list
├── verdict.py                # Maps LLM output to a final verdict label
│
├── visuals.py                # Plotly charts: pie, bar, horizontal bar (hotspots)
├── export_excel.py           # Exports per-file metrics to .xlsx with formatting
├── export_pdf.py             # Exports LLM report text to .pdf via ReportLab
└── final_report_generator.py # Alternate report generator (extended prompt variant)
```

---

## 🔬 How the Analysis Pipeline Works

```
Input (ZIP / GitHub URL)
        ↓
  File Walker (utils.py)
        ↓
  Per-File Analysis (analyzer.py)
  ├── Complexity density → risk score (0–10)
  ├── Function & class counts
  └── Control flow keyword count
        ↓
  Preprocessing (preprocess.py)
  ├── Danger keyword detection (eval, exec, pickle, subprocess…)
  ├── File classification (core / config / test / docs / vendor)
  └── Risk scoring with category adjustments
        ↓
  Analysis Passes
  ├── static_pass.py   → AST: eval/exec usage, bare try blocks
  ├── semantic_pass.py → Comment vs. security-term mismatch
  └── dataflow_pass.py → Taint: user input → dangerous sink
        ↓
  Top 20 risky files → ONE LLM call (project_reasoner.py)
        ↓
  Structured Report + Verdict + Rating
        ↓
  Visual Dashboard + Excel + PDF exports
```

---

## ⚙️ Prerequisites

- Python **3.9+**
- An **OpenRouter API key** — get one free at [openrouter.ai/keys](https://openrouter.ai/keys)
- `git` installed on your system PATH (required for GitHub analysis)

---

## 🚀 Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/your-username/code-security-analyzer.git
cd code-security-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit plotly pandas openpyxl reportlab gitpython requests
```

### 4. Run the app

```bash
streamlit run app.py
```

Then open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🖥️ How to Use

1. **Enter your OpenRouter API key** in the sidebar
2. Choose a tab:
   - **📦 ZIP Analysis** — drag and drop a `.zip` of your project
   - **🔗 GitHub Analysis** — paste a public GitHub repo URL (e.g. `https://github.com/user/repo`)
3. Click **Analyze** and watch the file processing log
4. Review the **summary metrics**, **verdict**, and **visual dashboard**
5. Read the full **LLM audit report**
6. Download the **Excel** or **PDF** report

---

## 📊 What the LLM Report Covers

The AI auditor produces a structured report with 8 sections:

| Section | Content |
|---|---|
| **Project Overview** | What the project does, intended use, architecture patterns |
| **Code Quality Assessment** | Maintainability, complexity, technical debt |
| **Security Analysis** | Realistic risks, config issues, what is NOT a vulnerability |
| **Exploitability Assessment** | Can it be exploited as-is? Under what conditions? |
| **Production Readiness Verdict** | NOT READY / CONDITIONALLY READY / READY |
| **Improvement Recommendations** | Quick wins, structural fixes, long-term hardening |
| **Overall Rating** | Score out of 10 with explanation |
| **Confidence Level** | 0.0–1.0 score with uncertainty sources |

---

## 🚨 Danger Signals Detected

The local analysis flags these patterns without any LLM call:

| Signal | Risk |
|---|---|
| `eval()` / `exec()` | Dynamic code execution |
| `subprocess` / `os.system` | Shell command injection risk |
| `pickle` | Unsafe deserialization |
| `yaml.load` | Unsafe YAML parsing |
| `open(` | File system access |
| `input(` | Unvalidated user input |
| Hardcoded `password` / `secret` / `token` in config files | Credential exposure |
| Untrusted input flowing to `eval`/`exec`/`query` | Taint/dataflow vulnerability |

---

## 📁 Supported File Types

| Language | Extensions |
|---|---|
| Python | `.py` |
| JavaScript / TypeScript | `.js`, `.jsx`, `.ts` |
| Java | `.java` |
| C / C++ | `.c`, `.cpp` |
| Config | `.json`, `.yaml`, `.yml`, `.env` |
| Docs | `.md`, `.txt` |

Ignored automatically: `node_modules/`, `.git/`, `__pycache__/`, `venv/`

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `LLM ERROR (401)` | Check your OpenRouter API key in the sidebar |
| `LLM ERROR: Request timed out` | The model took >120s — try again or switch to a faster model in `llm_engine.py` |
| GitHub clone fails | Ensure `git` is installed and the repo is public |
| `ModuleNotFoundError` | Run `pip install streamlit plotly pandas openpyxl reportlab gitpython requests` |
| PDF looks garbled | Long lines are truncated at 100 chars — this is a known limitation of the simple PDF renderer |

---

## 🔑 Changing the LLM Model

The default model is `xiaomi/mimo-v2-flash:free`. To change it, edit `llm_engine.py`:

```python
class LLM:
    def __init__(
        self,
        api_key,
        model="meta-llama/llama-3.1-70b-instruct:free",  # ← change here
        ...
    ):
```

Any model available on [openrouter.ai/models](https://openrouter.ai/models) works.

---

## 📄 License

This project is open source. Feel free to fork, modify, and extend it.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/) — UI framework
- [OpenRouter](https://openrouter.ai/) — LLM API gateway
- [Plotly](https://plotly.com/python/) — Interactive charts
- [ReportLab](https://www.reportlab.com/) — PDF generation
- [GitPython](https://gitpython.readthedocs.io/) — GitHub repo cloning
