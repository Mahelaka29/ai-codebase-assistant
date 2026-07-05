import os


def answer_local_question(question, code_files, languages, tree):
    """
    Returns a local answer string if the question can be answered
    without Gemini. Returns None otherwise.
    """

    q = question.lower()

    # ----------------------------
    # Count files
    # ----------------------------
    if "count" in q or "how many files" in q:
        return f"Total source files: {len(code_files)}"

    # ----------------------------
    # Show languages
    # ----------------------------
    if "language" in q:
        lines = ["Languages detected:\n"]

        for lang, count in languages.items():
            lines.append(f"- {lang}: {count}")

        return "\n".join(lines)

    # ----------------------------
    # List Python files
    # ----------------------------
    if "python files" in q:

        files = [
            f["path"]
            for f in code_files
            if f["path"].endswith(".py")
        ]

        if not files:
            return "No Python files found."

        return "\n".join(files)

    # ----------------------------
    # Find package.json
    # ----------------------------
    if "package.json" in q:

        for f in code_files:
            if os.path.basename(f["path"]) == "package.json":
                return f"Found:\n{f['path']}"

        return "package.json not found."

    # ----------------------------
    # Find requirements.txt
    # ----------------------------
    if "requirements.txt" in q:

        for f in code_files:
            if os.path.basename(f["path"]) == "requirements.txt":
                return f"Found:\n{f['path']}"

        return "requirements.txt not found."

    # ----------------------------
    # Show project tree
    # ----------------------------
    if "tree" in q or "folder structure" in q or "project structure" in q:

        output = []

        for folder, files in sorted(tree.items()):

            output.append(folder)

            for file in sorted(files):
                output.append(f"   └── {file}")

        return "\n".join(output)

    return None