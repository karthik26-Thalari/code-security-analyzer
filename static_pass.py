import ast

def run_static(code):
    tree = ast.parse(code)
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func,"id"):
            if node.func.id in {"eval","exec"}:
                issues.append("Use of eval/exec")

        if isinstance(node, ast.Try) and not node.handlers:
            issues.append("Bare try without except")

    return issues
