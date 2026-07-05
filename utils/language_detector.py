from collections import Counter
import os

EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "React",
    ".tsx": "React",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".php": "PHP",
    ".go": "Go",
    ".rb": "Ruby",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".json": "JSON",
    ".sql": "SQL",
    ".md": "Markdown",
    ".xml": "XML",
    ".yml": "YAML",
    ".yaml": "YAML",
}

def detect_languages(files):
    counter = Counter()

    for file in files:
        ext = os.path.splitext(file["path"])[1].lower()
        if ext in EXTENSIONS:
            counter[EXTENSIONS[ext]] += 1

    return counter