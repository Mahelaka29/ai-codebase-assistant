from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".sql",
    ".md",
    ".txt"
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "venv",
    "__pycache__",
    ".next",
    ".idea",
    ".vscode",
    "coverage",
    "temp"
}


def read_code_files(project_path):
    code_files = []

    project_path = Path(project_path)

    for file_path in project_path.rglob("*"):

        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(project_path)
        if any(part in IGNORE_DIRS for part in relative_path.parent.parts):
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if not content.strip():
                continue

            code_files.append({
                "path": str(relative_path).replace("\\", "/"),
                "content": content
            })

        except Exception:
            continue

    return code_files