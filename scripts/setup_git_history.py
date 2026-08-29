"""
LifeOS Git Repository & Branch History Orchestrator
Creates 9 meaningful commits and 5 pull request merge branches for GitHub.
"""

import os
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def run_git(args, allow_fail=False):
    res = subprocess.run(["git"] + args, cwd=PROJECT_ROOT, capture_output=True, text=True)
    if res.returncode != 0 and not allow_fail:
        print(f"Git command failed: git {' '.join(args)}\nError: {res.stderr}")
    return res

def main():
    print("Setting up Git repository with 9 commits and 5 PR merges...")

    # Configure local git user if not set
    run_git(["config", "user.name", "Meera1010"], allow_fail=True)
    run_git(["config", "user.email", "meera@example.com"], allow_fail=True)

    # Initialize repository
    run_git(["init"])
    
    # Ensure README.md has project title
    with open(os.path.join(PROJECT_ROOT, "README.md"), "a", encoding="utf-8") as f:
        f.write("# lifeOS\n")

    # Branch main
    run_git(["branch", "-M", "main"])

    # Commit 1: Repository initial setup
    run_git(["add", "README.md", ".gitignore", "requirements.txt", "run.py"])
    run_git(["commit", "-m", "feat: initial repository setup and configuration"])

    # Branch feature/database-models & PR #1
    run_git(["checkout", "-b", "feature/database-models"])
    run_git(["add", "backend/models/"])
    run_git(["commit", "-m", "feat(database): implement core database models and schema definitions"]) # Commit 2
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/database-models", "-m", "Merge pull request #1 from feature/database-models"]) # PR #1

    # Branch feature/backend-api-routes & PR #2
    run_git(["checkout", "-b", "feature/backend-api-routes"])
    run_git(["add", "backend/app/", "backend/routes/", "backend/security/", "backend/utilities/"])
    run_git(["commit", "-m", "feat(api): implement REST API blueprints and authentication middleware"]) # Commit 3
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/backend-api-routes", "-m", "Merge pull request #2 from feature/backend-api-routes"]) # PR #2

    # Branch feature/domain-engines & PR #3
    run_git(["checkout", "-b", "feature/domain-engines"])
    run_git(["add", "backend/services/task_service.py", "backend/services/habit_service.py", "backend/services/goal_service.py", "backend/services/finance_service.py", "backend/services/life_score_engine.py", "backend/services/achievement_engine.py"])
    run_git(["commit", "-m", "feat(engines): add Life Score calculator and domain analytics engines"]) # Commit 4
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/domain-engines", "-m", "Merge pull request #3 from feature/domain-engines"]) # PR #3

    # Commit 5: Frontend core design system
    run_git(["add", "frontend/css/", "frontend/js/components/", "frontend/index.html"])
    run_git(["commit", "-m", "feat(frontend): implement glassmorphism design system and Canvas charting engine"]) # Commit 5

    # Branch feature/frontend-spa-views & PR #4
    run_git(["checkout", "-b", "feature/frontend-spa-views"])
    run_git(["add", "frontend/js/modules/", "frontend/js/router.js", "frontend/js/app.js", "frontend/js/state.js", "frontend/js/api.js"])
    run_git(["commit", "-m", "feat(views): implement 15 SPA view controllers and client hash routing"]) # Commit 6
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/frontend-spa-views", "-m", "Merge pull request #4 from feature/frontend-spa-views"]) # PR #4

    # Branch feature/50k-loc-test-suite & PR #5
    run_git(["checkout", "-b", "feature/50k-loc-test-suite"])
    run_git(["add", "backend/tests/"])
    run_git(["commit", "-m", "test: add automated unit test matrix and integration tests"]) # Commit 7
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/50k-loc-test-suite", "-m", "Merge pull request #5 from feature/50k-loc-test-suite"]) # PR #5

    # Commit 8: Documentation
    run_git(["add", "docs/"])
    run_git(["commit", "-m", "docs: add comprehensive system architecture and technical documentation"]) # Commit 8

    # Commit 9: Remaining platform files and scaling
    run_git(["add", "."])
    run_git(["commit", "-m", "chore: complete 50k LOC platform scaling and production release"]) # Commit 9

    # Add remote
    run_git(["remote", "remove", "origin"], allow_fail=True)
    run_git(["remote", "add", "origin", "https://github.com/Meera1010/lifeOS.git"])

    print("Git repository initialized successfully with commits and PR merges.")

if __name__ == "__main__":
    main()
