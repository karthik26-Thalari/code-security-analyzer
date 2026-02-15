def final_verdict(llm_output):
    text = llm_output.lower()
    if "exploitable" in text and "high" in text:
        return "❌ NOT PRODUCTION READY"
    if "fix" in text:
        return "⚠️ CONDITIONALLY SAFE AFTER FIXES"
    return "✅ NO CRITICAL EXPLOIT FOUND"
