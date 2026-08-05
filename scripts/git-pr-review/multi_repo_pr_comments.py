import argparse
import os
import sys

from pr_utils import (
    copy_to_clipboard,
    fetch_issues_for_repo,
    format_issues_by_repo,
    load_dotenv,
    parse_repos_and_prs,
)

# =====================
# CONFIGURATION (see .env / .env.example, MULTI_REPO_* keys)
# =====================
load_dotenv()

OWNER = os.environ["MULTI_REPO_OWNER"]
REVIEWER = os.environ["MULTI_REPO_REVIEWER"]
REPOS_AND_PRS = parse_repos_and_prs(os.environ["MULTI_REPO_REPOS_AND_PRS"])
# =====================


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch PR review comments for one or more repos."
    )
    parser.add_argument(
        "--hide-resolved",
        action="store_true",
        help="Hide comments whose threads are marked as resolved.",
    )
    parser.add_argument(
        "--show-suggestions",
        action="store_true",
        help="Include Copilot's suppressed comments and show any genuine"
             " GitHub suggested-code blocks.",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy full output to clipboard",
    )
    args = parser.parse_args()

    issues_by_repo = {}
    for repo_name, pr_number in REPOS_AND_PRS:
        try:
            issues_by_repo[(repo_name, pr_number)] = fetch_issues_for_repo(
                OWNER, repo_name, pr_number, REVIEWER,
                hide_resolved=args.hide_resolved,
                include_suppressed=args.show_suggestions)
        except Exception as e:
            msg = f"Error fetching {OWNER}/{repo_name} PR #{pr_number}: {e}"
            print(msg, file=sys.stderr)
            issues_by_repo[(repo_name, pr_number)] = []

    output = format_issues_by_repo(
        issues_by_repo, show_suggestions=args.show_suggestions)
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
