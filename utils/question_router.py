import re

LOCAL_PATTERNS = [
    r"list.*files",
    r"count.*files",
    r"how many files",
    r"python files",
    r"javascript files",
    r"react components",
    r"show languages",
    r"languages used",
    r"requirements\.txt",
    r"package\.json",
    r"find.*file",
    r"where is",
]

TREE_EXPLAIN_PATTERNS = [
    r"explain.*folder",
    r"explain.*project structure",
    r"explain.*directory",
    r"describe.*folder",
    r"describe.*project structure",
]

LOCAL_TREE_PATTERNS = [
    r"show.*folder",
    r"show.*project structure",
    r"show.*tree",
    r"project tree",
    r"folder tree",
]

def classify_question(question: str) -> str:

    q = question.lower().strip()

    # Metadata + Gemini
    for pattern in TREE_EXPLAIN_PATTERNS:
        if re.search(pattern, q):
            return "metadata_llm"

    # Pure local metadata
    for pattern in LOCAL_TREE_PATTERNS:
        if re.search(pattern, q):
            return "local"

    for pattern in LOCAL_PATTERNS:
        if re.search(pattern, q):
            return "local"

    # Everything else
    return "gemini"