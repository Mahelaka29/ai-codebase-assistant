from collections import defaultdict

def build_tree(files):
    tree = defaultdict(list)

    for file in files:
        parts = file["path"].replace("\\", "/").split("/")
        folder = "/".join(parts[:-1]) if len(parts) > 1 else "Root"
        tree[folder].append(parts[-1])

    return dict(tree)