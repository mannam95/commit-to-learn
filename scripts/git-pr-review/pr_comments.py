import json
import subprocess
import sys

# PRE-REQS:
# - gh CLI installed
# - gh CLI authenticated
# - gh extension install agynio/gh-pr-review
#   (https://github.com/agynio/gh-pr-review)

# =====================
# CONFIGURATION
# =====================
OWNER = "myorg"     # change if needed
REPO = "myrepo"     # change if needed
PR_NUMBER = 1       # change if needed
REVIEWER = "myusername"     # change if needed
# =====================


def run_cmd(cmd):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print("Command failed:")
        print(result.stderr)
        sys.exit(1)

    return json.loads(result.stdout)


def fetch_review_data():
    return run_cmd([
        "gh", "pr-review", "review", "view",
        str(PR_NUMBER),
        "--repo", f"{OWNER}/{REPO}",
    ])


def extract_issues(data):
    issues = []
    pr_url = f"https://github.com/{OWNER}/{REPO}/pull/{PR_NUMBER}"

    for review in data.get("reviews", []):
        for comment in review.get("comments", []):
            if comment.get("author_login") != REVIEWER:
                continue

            # First reply by someone else (usually PR author)
            response = None
            for reply in comment.get("thread_comments", []):
                if reply.get("author_login") != REVIEWER:
                    response = reply.get("body")
                    break

            issues.append({
                "comment": comment.get("body", ""),
                "filename": comment.get("path", "N/A"),
                "issue": pr_url,
                "response": response
            })

    return issues


def print_issues(issues):
    for idx, issue in enumerate(issues, start=1):
        print(f"issue{idx}")
        print("comment:")
        print(issue["comment"])
        print()
        print("filename:")
        print(issue["filename"])
        print()
        print("response/reply if any:")
        print(issue["response"] or "No response")
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    data = fetch_review_data()
    issues = extract_issues(data)
    print_issues(issues)
