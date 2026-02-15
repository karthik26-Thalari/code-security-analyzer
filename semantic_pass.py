import re

def run_semantic(code):
    comments = [l for l in code.splitlines() if l.strip().startswith("#")]
    promises = re.findall(r"(sanitize|validate|secure|auth)", code, re.I)

    return {
        "comments": len(comments),
        "security_terms": len(promises),
        "intent_mismatch": bool(comments) and not bool(promises)
    }
