import os
import shutil
import zipfile


TEMP_DIR = "temp"


def extract_zip(uploaded_zip):
    """
    Extracts the uploaded ZIP file and returns the project directory.
    """

    os.makedirs(TEMP_DIR, exist_ok=True)

    project_name = os.path.splitext(uploaded_zip.name)[0]
    extract_path = os.path.join(TEMP_DIR, project_name)

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)

    os.makedirs(extract_path)

    zip_path = os.path.join(TEMP_DIR, uploaded_zip.name)

    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.getbuffer())

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    os.remove(zip_path)

    # Some ZIPs contain a single root folder.
    items = os.listdir(extract_path)

    if len(items) == 1:
        inner = os.path.join(extract_path, items[0])

        if os.path.isdir(inner):
            return inner

    return extract_path