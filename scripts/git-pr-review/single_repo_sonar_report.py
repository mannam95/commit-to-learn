import argparse
import os
import sys

import sonar_utils
from pr_utils import copy_to_clipboard, load_dotenv

# =====================
# CONFIGURATION (see .env / .env.example)
# Reuses SINGLE_REPO_OWNER/NAME/PR_NUMBER from single_repo_pr_comments.py --
# the Sonar project key is derived as '{owner}_{repo}' and the PR number is
# the same one CI already reported to Sonar.
# =====================
load_dotenv()

OWNER = os.environ["SINGLE_REPO_OWNER"]
REPO = os.environ["SINGLE_REPO_NAME"]
PR_NUMBER = int(os.environ["SINGLE_REPO_PR_NUMBER"])

SONAR_ORG = os.environ["SONAR_ORG"]
SONAR_TOKEN = os.environ["SONAR_TOKEN"]
# =====================


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch SonarCloud PR analysis for a single repo/PR."
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy full output to clipboard",
    )
    args = parser.parse_args()

    try:
        report = sonar_utils.fetch_report_for_repo(
            SONAR_ORG, SONAR_TOKEN, OWNER, REPO, PR_NUMBER)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        report = None

    output = sonar_utils.format_sonar_report({(REPO, PR_NUMBER): report})
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
