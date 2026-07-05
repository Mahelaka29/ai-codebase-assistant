def format_project_tree(tree):
    """
    Converts the project tree dictionary into a readable text
    that can be passed to Gemini.
    """

    lines = []

    for folder, files in sorted(tree.items()):

        lines.append(f"{folder}/")

        for file in sorted(files):
            lines.append(f"    ├── {file}")

        lines.append("")

    return "\n".join(lines)