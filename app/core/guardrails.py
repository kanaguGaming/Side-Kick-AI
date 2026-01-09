import re

def is_code_present(text: str) -> bool:
    """Detects if the LLM leaked code blocks."""
    patterns = [r"```", r"def ", r"int main", r"public class"]
    return any(re.search(p, text) for p in patterns)

def clean_response(text: str) -> str:
    if is_code_present(text):
        return "I can't give you the code directly. Let's look at the logic instead: What part of the algorithm is confusing?"
    return text