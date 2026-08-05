import argparse
import os
import sys

from pr_utils import (
    copy_to_clipboard,
    fetch_issues_for_repo,
    format_issues_by_repo,
    load_dotenv,
)

# =====================
# CONFIGURATION (see .env / .env.example, SINGLE_REPO_* keys)
# =====================
load_dotenv()

OWNER = os.environ["SINGLE_REPO_OWNER"]
REPO = os.environ["SINGLE_REPO_NAME"]
PR_NUMBER = int(os.environ["SINGLE_REPO_PR_NUMBER"])
REVIEWER = os.environ["SINGLE_REPO_REVIEWER"]
# =====================


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch PR review comments for a single repo/PR."
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

    try:
        issues = fetch_issues_for_repo(
            OWNER, REPO, PR_NUMBER, REVIEWER,
            hide_resolved=args.hide_resolved,
            include_suppressed=args.show_suggestions)
    except Exception as e:
        print(f"Error fetching {OWNER}/{REPO} PR #{PR_NUMBER}: {e}",
              file=sys.stderr)
        issues = []

    output = format_issues_by_repo(
        {(REPO, PR_NUMBER): issues}, show_suggestions=args.show_suggestions)
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
