import argparse
import json
import subprocess
import sys

# =====================
# CONFIGURATION
# =====================
OWNER = "myorg"
REVIEWER = "myusername"

REPOS_AND_PRS = [
    ("myrepo1", 1),
    ("myrepo2", 2),
    ("myrepo3", 3),
]


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


def fetch_review_data(owner, repo, pr_number):
    return run_cmd([
        "gh", "pr-review", "review", "view",
        str(pr_number),
        "--repo", f"{owner}/{repo}",
    ])


def extract_issues(owner, repo, pr_number, data):
    issues = []
    pr_url = f"https://github.com/{owner}/{repo}/pull/{pr_number}"

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


def fetch_issues_for_repo(owner, repo, pr_number):
    """Fetch review data and return list of issues for one repo/PR."""
    data = fetch_review_data(owner, repo, pr_number)
    return extract_issues(owner, repo, pr_number, data)


def format_issues_by_repo(issues_by_repo):
    """Return full output as a string."""
    lines = []
    for repo_key, issues in issues_by_repo.items():
        repo_name, pr_number = repo_key
        lines.append(f"\n{'#' * 60}")
        lines.append(f"# REPO: {repo_name}  |  PR: {pr_number}")
        lines.append(f"{'#' * 60}\n")

        if not issues:
            lines.append("  (no issues)\n")
            continue

        for idx, issue in enumerate(issues, start=1):
            lines.append(f"  issue{idx}")
            lines.append("  comment:")
            lines.append("  " + issue["comment"].replace("\n", "\n  "))
            lines.append("")
            lines.append("  filename:")
            lines.append("  " + issue["filename"])
            lines.append("")
            lines.append("  response/reply if any:")
            resp = (issue["response"] or "No response").replace("\n", "\n  ")
            lines.append("  " + resp)
            lines.append("\n  " + "-" * 50 + "\n")

    return "\n".join(lines)


def print_issues_by_repo(issues_by_repo):
    """Print issues grouped by repo."""
    print(format_issues_by_repo(issues_by_repo))


def copy_to_clipboard(text):
    """Copy text to system clipboard. Returns True on success."""
    # Wayland
    try:
        subprocess.run(
            ["wl-copy"],
            input=text,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    # X11: xclip
    try:
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    # X11: xsel
    try:
        subprocess.run(
            ["xsel", "--clipboard", "--input"],
            input=text,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    # macOS
    try:
        subprocess.run(
            ["pbcopy"],
            input=text,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch PR review comments by repo.")
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy full output to clipboard",
    )
    args = parser.parse_args()

    issues_by_repo = {}

    for repo_name, pr_number in REPOS_AND_PRS:
        try:
            issues = fetch_issues_for_repo(OWNER, repo_name, pr_number)
            issues_by_repo[(repo_name, pr_number)] = issues
        except Exception as e:
            msg = f"Error fetching {OWNER}/{repo_name} PR #{pr_number}: {e}"
            print(msg, file=sys.stderr)
            issues_by_repo[(repo_name, pr_number)] = []

    output = format_issues_by_repo(issues_by_repo)
    print(output)

    if args.copy:
        if copy_to_clipboard(output):
            print("\n(Copied to clipboard.)", file=sys.stderr)
        else:
            print(
                "\n(Copy failed: on Linux install wl-copy (Wayland) or"
                " xclip (X11), e.g. apt install wl-clipboard or"
                " apt install xclip)",
                file=sys.stderr,
            )
