def reason_all(static, semantic, dataflow):
    hypotheses = []

    if static:
        hypotheses.append("Unsafe dynamic execution")
    if semantic["intent_mismatch"]:
        hypotheses.append("Security intent not implemented")
    if dataflow:
        hypotheses.append(dataflow)

    return hypotheses
