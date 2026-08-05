"""Shared helpers for fetching and formatting PR review comments via `gh pr-review`."""
import json
import os
import re
import subprocess
import sys

SUGGESTION_RE = re.compile(r"```suggestion\r?\n(.*?)```", re.DOTALL)
SUPPRESSED_SECTION_RE = re.compile(
    r"(?:<summary>|^#{1,6}\s*)Suppressed comments?[^\n<]*"
    r"(?:</summary>)?\s*(.*?)(?=</details>|^#{1,6}\s|\Z)",
    re.DOTALL | re.IGNORECASE | re.MULTILINE)
SUPPRESSED_COMMENT_RE = re.compile(
    r"\*\*(?P<path>.+?):(?P<line>\d+)\*\*\s*\n"
    r"\*\s*(?P<comment>.*?)(?=\n```|\n\*\*|\Z)"
    r"(?:\n```[^\n]*\n(?P<context>.*?)```)?", re.DOTALL)


def load_dotenv(path=None):
    """
    Minimal `.env` loader (KEY=VALUE per line) so we don't need a dependency.
    A value may span multiple lines as a JSON array; '#' lines in between
    (e.g. commented-out entries) are skipped until the brackets balance.
    """
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        while value.count("[") > value.count("]") and i < len(lines):
            next_line = lines[i].strip()
            i += 1
            if not next_line or next_line.startswith("#"):
                continue
            value += " " + next_line
        os.environ.setdefault(key, value.strip("'\""))


REPO_PR_PAIR_RE = re.compile(r'\[\s*"([^"]+)"\s*,\s*(\d+)\s*\]')


def parse_repos_and_prs(raw):
    """
    Parse ["repo", pr_number] entries out of a (possibly multi-line) list.
    Commas between entries are not required, so commenting/uncommenting
    individual lines can't break the format.
    """
    return [(repo, int(pr_number))
            for repo, pr_number in REPO_PR_PAIR_RE.findall(raw or "")]


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


def is_comment_resolved(comment: dict) -> bool:
    """
    Best-effort check to see if a comment/thread is marked as resolved
    in the Copilot PR review JSON structure.
    """
    if "is_resolved" in comment:
        return bool(comment.get("is_resolved"))

    thread = comment.get("thread") or comment.get("review_thread") or {}
    if isinstance(thread, dict) and "is_resolved" in thread:
        return bool(thread.get("is_resolved"))

    return False


def extract_suggestions(body: str):
    """Extract committable ```suggestion``` code blocks from a comment body."""
    return [block.strip("\r\n") for block in SUGGESTION_RE.findall(body or "")]


def extract_review_summaries(data, reviewer):
    """
    Review-level bodies from the reviewer. For Copilot this holds the
    "Pull request overview", the per-file summary table, and any
    low-confidence suggestions that never appear as inline comments.
    """
    summaries = []
    for review in data.get("reviews", []):
        if review.get("author_login") != reviewer:
            continue
        body = (review.get("body") or "").strip()
        if body:
            summaries.append(body)
    return summaries


def extract_issues(owner, repo, pr_number, data, reviewer, hide_resolved=False):
    issues = []
    pr_url = f"https://github.com/{owner}/{repo}/pull/{pr_number}"

    for review in data.get("reviews", []):
        for comment in review.get("comments", []):
            if comment.get("author_login") != reviewer:
                continue

            if hide_resolved and is_comment_resolved(comment):
                continue

            # First reply by someone else (usually PR author)
            response = None
            for reply in comment.get("thread_comments", []):
                if reply.get("author_login") != reviewer:
                    response = reply.get("body")
                    break

            issues.append({
                "comment": comment.get("body", ""),
                "filename": comment.get("path", "N/A"),
                "line": comment.get("line"),
                "issue": pr_url,
                "response": response,
                "suggestions": extract_suggestions(comment.get("body", "")),
                "suppressed": False,
            })

    return issues


def extract_suppressed_issues(owner, repo, pr_number, data, reviewer):
    """Turn Copilot's suppressed findings in review bodies into issues."""
    issues = []
    pr_url = f"https://github.com/{owner}/{repo}/pull/{pr_number}"
    for review in data.get("reviews", []):
        if review.get("author_login") != reviewer:
            continue
        for section in SUPPRESSED_SECTION_RE.findall(review.get("body") or ""):
            for match in SUPPRESSED_COMMENT_RE.finditer(section.strip()):
                issues.append({
                    "comment": match.group("comment").strip(),
                    "filename": match.group("path").strip(),
                    "line": int(match.group("line")),
                    "issue": pr_url,
                    "response": None,
                    "suggestions": [],
                    "context": (match.group("context") or "").strip(),
                    "suppressed": True,
                })
    return issues


def fetch_issues_for_repo(owner, repo, pr_number, reviewer,
                           hide_resolved=False, include_suppressed=False):
    """Fetch inline issues and, optionally, Copilot's suppressed findings."""
    data = fetch_review_data(owner, repo, pr_number)
    issues = extract_issues(
        owner, repo, pr_number, data, reviewer, hide_resolved=hide_resolved)
    if include_suppressed:
        issues.extend(
            extract_suppressed_issues(owner, repo, pr_number, data, reviewer))
    return issues


def format_issues_by_repo(issues_by_repo, show_suggestions=False):
    """Return full output (for one or many repo/PR entries) as a string."""
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
            if issue.get("suppressed"):
                lines.append("  type:")
                lines.append("  suppressed Copilot comment")
            lines.append("  comment:")
            lines.append("  " + issue["comment"].replace("\n", "\n  "))
            lines.append("")
            if show_suggestions and not issue.get("suppressed"):
                lines.append("  suggested changeset:")
                if issue["suggestions"]:
                    for suggestion in issue["suggestions"]:
                        lines.append(
                            "  " + suggestion.replace("\n", "\n  "))
                else:
                    lines.append(
                        "  Unavailable: Copilot Suggested changesets are "
                        "not exposed by GitHub's public API.")
                lines.append("")
            lines.append("  filename:")
            lines.append("  " + issue["filename"])
            lines.append("")
            if issue.get("line") is not None:
                lines.append(f"  line: {issue['line']}")
                lines.append("")
            if issue.get("context"):
                lines.append("  code context:")
                lines.append(
                    "  " + issue["context"].replace("\n", "\n  "))
                lines.append("")
            lines.append("  response/reply if any:")
            resp = (issue["response"] or "No response").replace("\n", "\n  ")
            lines.append("  " + resp)
            lines.append("\n  " + "-" * 50 + "\n")

    return "\n".join(lines)


def print_issues_by_repo(issues_by_repo, show_suggestions=False):
    """Print issues grouped by repo."""
    print(format_issues_by_repo(issues_by_repo, show_suggestions))


def copy_to_clipboard(text):
    """Copy text to system clipboard. Returns True on success."""
    for cmd in (
        ["wl-copy"],
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["pbcopy"],
    ):
        try:
            subprocess.run(
                cmd,
                input=text,
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            return True
        except (FileNotFoundError,
                subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
    return False
