import argparse
import os
import sys

import sonar_utils
from pr_utils import copy_to_clipboard, load_dotenv, parse_repos_and_prs

# =====================
# CONFIGURATION (see .env / .env.example)
# Reuses MULTI_REPO_OWNER/REPOS_AND_PRS from multi_repo_pr_comments.py --
# the Sonar project key is derived as '{owner}_{repo}' and the PR numbers
# are the same ones CI already reported to Sonar.
# =====================
load_dotenv()

OWNER = os.environ["MULTI_REPO_OWNER"]
REPOS_AND_PRS = parse_repos_and_prs(os.environ["MULTI_REPO_REPOS_AND_PRS"])

SONAR_ORG = os.environ["SONAR_ORG"]
SONAR_TOKEN = os.environ["SONAR_TOKEN"]
# =====================


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch SonarCloud PR analysis for one or more repos."
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy full output to clipboard",
    )
    args = parser.parse_args()

    reports_by_repo = {}
    for repo_name, pr_number in REPOS_AND_PRS:
        try:
            reports_by_repo[(repo_name, pr_number)] = (
                sonar_utils.fetch_report_for_repo(
                    SONAR_ORG, SONAR_TOKEN, OWNER, repo_name, pr_number))
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            reports_by_repo[(repo_name, pr_number)] = None

    output = sonar_utils.format_sonar_report(reports_by_repo)
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
