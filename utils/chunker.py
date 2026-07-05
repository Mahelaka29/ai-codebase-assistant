from typing import List, Dict


def chunk_code(
    code_files: List[Dict],
    chunk_size: int = 1200,
    overlap: int = 200
):
    chunks = []

    for file in code_files:

        content = file["content"]
        source = file["path"]

        start = 0

        while start < len(content):

            end = start + chunk_size

            chunk = content[start:end]

            chunks.append({
                "text": chunk,
                "source": source,
                "start": start,
                "end": min(end, len(content))
            })

            start += chunk_size - overlap

    return chunks