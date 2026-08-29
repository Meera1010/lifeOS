"""
LifeOS Real Source-Code Line-of-Code (LOC) Audit Script
"""

import os
import sys

# Directory to audit
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

IGNORE_DIRS = {".git", "__pycache__", "venv", ".pytest_cache", "instance", ".idea", ".vscode", "scratch", ".system_generated"}
VALID_EXTENSIONS = {".py", ".js", ".css", ".html", ".md", ".json", ".txt", ".example"}

def count_file_loc(filepath):
    """Counts non-blank lines in a source code file."""
    lines_count = 0
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_str = line.strip()
            if line_str: # Non-blank line
                lines_count += 1
    return lines_count

def run_loc_audit():
    total_files = 0
    total_loc = 0
    prod_loc = 0
    cat_counts = {
        "Python (Backend, Models, Services, Routes)": 0,
        "JavaScript (Frontend UI, Router, Views, API)": 0,
        "CSS (Stylesheets & Design Tokens)": 0,
        "HTML (SPA Shell & Templates)": 0,
        "Tests (backend/tests)": 0,
        "Documentation & Configuration (.md, .txt, .env)": 0
    }

    print("======================================================================")
    print("REAL SOURCE-CODE LOC AUDIT -- LIFEOS PLATFORM")
    print("======================================================================")

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTENSIONS:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, PROJECT_ROOT).replace("\\", "/")
                file_loc = count_file_loc(filepath)
                
                total_files += 1
                total_loc += file_loc

                is_test_or_doc = rel_path.startswith("backend/tests/") or rel_path.startswith("docs/") or rel_path.startswith("scripts/")

                if ext == ".py":
                    if rel_path.startswith("backend/tests/"):
                        cat_counts["Tests (backend/tests)"] += file_loc
                    else:
                        cat_counts["Python (Backend, Models, Services, Routes)"] += file_loc
                        if not is_test_or_doc:
                            prod_loc += file_loc
                elif ext == ".js":
                    cat_counts["JavaScript (Frontend UI, Router, Views, API)"] += file_loc
                    if not is_test_or_doc:
                        prod_loc += file_loc
                elif ext == ".css":
                    cat_counts["CSS (Stylesheets & Design Tokens)"] += file_loc
                    if not is_test_or_doc:
                        prod_loc += file_loc
                elif ext == ".html":
                    cat_counts["HTML (SPA Shell & Templates)"] += file_loc
                    if not is_test_or_doc:
                        prod_loc += file_loc
                else:
                    cat_counts["Documentation & Configuration (.md, .txt, .env)"] += file_loc

    print(f"Total Source Code Files Audited: {total_files}")
    print("----------------------------------------------------------------------")
    for cat, loc in cat_counts.items():
        print(f"  * {cat.ljust(50)}: {loc:,} LOC")
    print("----------------------------------------------------------------------")
    print(f"TOTAL PRODUCTION SOURCE-CODE LOC (Excl tests/docs): {prod_loc:,} LINES")
    print(f"TOTAL ALL-INCLUSIVE SOURCE-CODE LOC              : {total_loc:,} LINES")
    print("======================================================================")

    return total_files, total_loc, prod_loc

if __name__ == "__main__":
    run_loc_audit()
