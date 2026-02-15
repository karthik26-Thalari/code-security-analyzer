def run_dataflow(code):
    sources = ["input","request","args","params"]
    sinks = ["eval","exec","system","query"]

    tainted = [s for s in sources if s in code.lower()]
    dangerous = [s for s in sinks if s in code.lower()]

    if tainted and dangerous:
        return "Untrusted input flows into dangerous sink"

    return None
