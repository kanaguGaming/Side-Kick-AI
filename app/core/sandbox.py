import subprocess

def check_code_syntax(code: str, language: str = "python"):
    if language == "python":
        try:
            compile(code, '<string>', 'exec')
            return "Syntax looks clean."
        except SyntaxError as e:
            return f"Syntax Error: {e.msg} at line {e.lineno}"
    return "Language sandbox not implemented."