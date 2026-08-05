import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import multi_repo_pr_comments as subject
import pr_utils


class CopilotSuppressedCommentTests(unittest.TestCase):
    def test_suppressed_comments_are_returned_as_issues(self):
        data = {
            "reviews": [{
                "author_login": subject.REVIEWER,
                "body": """## Pull request overview

Overview that should not be printed.

<details>
<summary>Suppressed comments (1)</summary>

**src/example.py:42**
* Handle the empty value before calling the parser.
```python
value = parse(raw)
```
</details>
""",
                "comments": [],
            }]
        }

        issues = pr_utils.extract_suppressed_issues(
            "owner", "repo", 7, data, subject.REVIEWER)

        self.assertEqual(1, len(issues))
        self.assertEqual("src/example.py", issues[0]["filename"])
        self.assertEqual(42, issues[0]["line"])
        self.assertEqual(
            "Handle the empty value before calling the parser.",
            issues[0]["comment"],
        )
        self.assertEqual("value = parse(raw)", issues[0]["context"])

    def test_suppressed_heading_inside_review_details_is_parsed(self):
        data = {
            "reviews": [{
                "author_login": subject.REVIEWER,
                "body": """<details>
<summary>Review details</summary>

### Suppressed comments (1)

**src/query.py:222**
* Apply the deleted-parent guard to the parent name.
```
parent_name = row.name
```

- **Files reviewed:** 2/2 changed files
</details>
""",
                "comments": [],
            }]
        }

        issues = pr_utils.extract_suppressed_issues(
            "owner", "repo", 7, data, subject.REVIEWER)

        self.assertEqual(1, len(issues))
        self.assertEqual("src/query.py", issues[0]["filename"])
        self.assertEqual(222, issues[0]["line"])

    def test_output_reports_copilot_changeset_is_not_in_public_api(self):
        issues = [{
            "comment": "Handle the empty value.",
            "filename": "src/example.py",
            "line": 42,
            "issue": "https://github.com/owner/repo/pull/7",
            "response": None,
            "suggestions": [],
            "context": "",
            "suppressed": False,
        }]

        output = subject.format_issues_by_repo(
            {("repo", 7): issues}, show_suggestions=True)

        self.assertIn("line: 42", output)
        self.assertNotIn("review summary:", output)
        self.assertIn("suggested changeset:", output)
        self.assertIn("not exposed by GitHub's public API", output)


if __name__ == "__main__":
    unittest.main()
