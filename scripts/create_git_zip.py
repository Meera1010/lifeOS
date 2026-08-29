"""
LifeOS Repository Zip Creator — Compresses entire workspace including .git directory.
"""

import os
import zipfile

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
OUTPUT_ZIP_PATH = os.path.join(PROJECT_ROOT, "lifeOS_with_git.zip")

def create_zip():
    print(f"Creating zip archive including .git folder at: {OUTPUT_ZIP_PATH}")
    total_files = 0

    with zipfile.ZipFile(OUTPUT_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Exclude the generated zip file itself and pycache
            if "lifeOS_with_git.zip" in files:
                files.remove("lifeOS_with_git.zip")

            for file in files:
                if file.endswith(".pyc") or "__pycache__" in root:
                    continue

                abs_filepath = os.path.join(root, file)
                rel_filepath = os.path.relpath(abs_filepath, PROJECT_ROOT)

                # Store with lifeOS/ root folder in zip
                arcname = os.path.join("lifeOS", rel_filepath)
                zipf.write(abs_filepath, arcname)
                total_files += 1

    file_size_mb = round(os.path.getsize(OUTPUT_ZIP_PATH) / (1024 * 1024), 2)
    print(f"Zip creation complete: {total_files} files packaged ({file_size_mb} MB).")

if __name__ == "__main__":
    create_zip()
