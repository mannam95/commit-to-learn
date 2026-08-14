import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sonar_utils


class BuildProjectKeyTests(unittest.TestCase):
    def test_joins_owner_and_repo_with_underscore(self):
        self.assertEqual(
            "some-org_some-repo",
            sonar_utils.build_project_key("some-org", "some-repo"),
        )


class ExtractNewCodeMeasuresTests(unittest.TestCase):
    def test_reads_value_from_periods_when_top_level_value_missing(self):
        data = {
            "component": {
                "measures": [
                    {"metric": "new_bugs", "periods": [{"index": 1, "value": "0"}]},
                    {"metric": "new_coverage", "periods": [{"index": 1, "value": "87.5"}]},
                ]
            }
        }
        self.assertEqual(
            {"new_bugs": "0", "new_coverage": "87.5"},
            sonar_utils.extract_new_code_measures(data),
        )

    def test_prefers_top_level_value_when_present(self):
        data = {"component": {"measures": [{"metric": "new_bugs", "value": "3"}]}}
        self.assertEqual(
            {"new_bugs": "3"}, sonar_utils.extract_new_code_measures(data))

    def test_missing_measures_returns_empty_dict(self):
        self.assertEqual({}, sonar_utils.extract_new_code_measures({"component": {}}))


class ExtractNewIssuesTests(unittest.TestCase):
    def test_returns_issues_list(self):
        data = {"issues": [{"key": "abc"}]}
        self.assertEqual([{"key": "abc"}], sonar_utils.extract_new_issues(data))

    def test_missing_issues_returns_empty_list(self):
        self.assertEqual([], sonar_utils.extract_new_issues({}))


class ExtractDuplicationsByFileTests(unittest.TestCase):
    def _component(self, path, density, duplicated_lines):
        return {
            "path": path,
            "measures": [
                {
                    "metric": "new_duplicated_lines_density",
                    "periods": [{"index": 1, "value": density}],
                },
                {
                    "metric": "new_duplicated_lines",
                    "periods": [{"index": 1, "value": duplicated_lines}],
                },
            ],
        }

    def test_drops_files_with_zero_duplication(self):
        data = {"components": [
            self._component("src/clean.ts", "0.0", "0"),
            self._component("src/dup.ts", "24.2", "22"),
        ]}

        files = sonar_utils.extract_duplications_by_file(data)

        self.assertEqual(
            [{"path": "src/dup.ts", "density": "24.2", "duplicated_lines": "22"}],
            files,
        )

    def test_no_components_returns_empty_list(self):
        self.assertEqual([], sonar_utils.extract_duplications_by_file({}))


class ExtractCoverageByFileTests(unittest.TestCase):
    def _component(self, path, measures):
        return {
            "path": path,
            "measures": [
                {"metric": key, "periods": [{"index": 1, "value": value}]}
                for key, value in measures.items()
            ],
        }

    def test_drops_files_with_nothing_to_cover(self):
        data = {"components": [
            self._component("src/no_new_lines.go", {
                "new_uncovered_lines": "0",
                "new_uncovered_conditions": "0",
            }),
            self._component("src/add_location.go", {
                "new_coverage": "50.0",
                "new_uncovered_lines": "1",
                "new_uncovered_conditions": "0",
            }),
        ]}

        files = sonar_utils.extract_coverage_by_file(data)

        self.assertEqual(
            [{
                "path": "src/add_location.go",
                "coverage": "50.0",
                "uncovered_lines": "1",
                "uncovered_conditions": "0",
            }],
            files,
        )

    def test_no_components_returns_empty_list(self):
        self.assertEqual([], sonar_utils.extract_coverage_by_file({}))


class ExtractSecurityHotspotsTests(unittest.TestCase):
    def test_returns_hotspots_list(self):
        data = {"hotspots": [{"key": "abc"}]}
        self.assertEqual([{"key": "abc"}], sonar_utils.extract_security_hotspots(data))

    def test_missing_hotspots_returns_empty_list(self):
        self.assertEqual([], sonar_utils.extract_security_hotspots({}))


class FormatSonarReportTests(unittest.TestCase):
    def test_reports_missing_data_without_raising(self):
        output = sonar_utils.format_sonar_report({("repo", 7): None})
        self.assertIn("SONAR: repo", output)
        self.assertIn("no sonar report available", output)

    def test_formats_quality_gate_measures_and_issues(self):
        report = {
            "quality_gate": {
                "status": "ERROR",
                "conditions": [
                    {"metricKey": "new_bugs", "actualValue": "1", "status": "ERROR"},
                ],
            },
            "measures": {"new_duplicated_lines_density": "4.2"},
            "issues": [{
                "type": "BUG",
                "severity": "MAJOR",
                "message": "Fix the null check.",
                "component": "some-org_some-repo:src/foo.py",
                "line": 42,
            }],
        }

        output = sonar_utils.format_sonar_report({("repo", 7): report})

        self.assertIn("quality gate: ERROR", output)
        self.assertIn("new_bugs: 1", output)
        self.assertIn("new_duplicated_lines_density: 4.2", output)
        self.assertIn("Fix the null check.", output)
        self.assertIn("src/foo.py", output)
        self.assertIn("line: 42", output)

    def test_shows_effort_and_tags_but_never_leaks_author_email(self):
        report = {
            "quality_gate": {"status": "OK", "conditions": []},
            "measures": {},
            "issues": [{
                "type": "CODE_SMELL",
                "severity": "CRITICAL",
                "message": "Refactor this function to reduce its "
                            "Cognitive Complexity from 21 to the 15 allowed.",
                "component": "some-org_some-repo:src/services/queryClient.ts",
                "line": 210,
                "effort": "11min",
                "tags": ["brain-overload", "editable-source"],
                "author": "someone@example.com",
            }],
        }

        output = sonar_utils.format_sonar_report({("repo", 7): report})

        self.assertIn("effort: 11min", output)
        self.assertIn("tags: brain-overload, editable-source", output)
        self.assertNotIn("someone@example.com", output)

    def test_handles_whole_project_conditions_without_actual_value(self):
        # Regression: overall-rating conditions (not scoped to the PR's new
        # code) come back without periodIndex/actualValue at all.
        report = {
            "quality_gate": {
                "status": "ERROR",
                "conditions": [
                    {
                        "status": "OK",
                        "metricKey": "reliability_rating",
                        "comparator": "GT",
                        "errorThreshold": "1",
                    },
                    {
                        "status": "ERROR",
                        "metricKey": "new_duplicated_lines_density",
                        "comparator": "GT",
                        "periodIndex": 1,
                        "errorThreshold": "3",
                        "actualValue": "3.5",
                    },
                ],
            },
            "measures": {},
            "issues": [],
        }

        output = sonar_utils.format_sonar_report({("repo", 7): report})

        self.assertIn("[overall] reliability_rating: n/a", output)
        self.assertIn("[new code] new_duplicated_lines_density: 3.5", output)

    def test_omits_duplication_section_when_no_files_reported(self):
        report = {
            "quality_gate": {"status": "OK", "conditions": []},
            "measures": {},
            "issues": [],
        }
        output = sonar_utils.format_sonar_report({("repo", 7): report})
        self.assertNotIn("duplicated lines by file", output)

    def test_lists_duplicated_files_with_density_rounded(self):
        report = {
            "quality_gate": {"status": "OK", "conditions": []},
            "measures": {},
            "duplications_by_file": [{
                "path": "src/components/CoreDetailSection/fields/LinksField.tsx",
                "density": "24.175824175824175",
                "duplicated_lines": "22",
            }],
            "issues": [],
        }
        output = sonar_utils.format_sonar_report({("repo", 7): report})
        self.assertIn(
            "src/components/CoreDetailSection/fields/LinksField.tsx: 24.2%"
            " (22 lines)",
            output,
        )

    def test_no_new_issues_is_reported_explicitly(self):
        report = {
            "quality_gate": {"status": "OK", "conditions": []},
            "measures": {},
            "issues": [],
        }
        output = sonar_utils.format_sonar_report({("repo", 7): report})
        self.assertIn("no new issues", output)

    def test_lists_coverage_by_file(self):
        report = {
            "quality_gate": {"status": "OK", "conditions": []},
            "measures": {},
            "coverage_by_file": [{
                "path": "internal/domains/location/app/commands/add_location.go",
                "coverage": "50.0",
                "uncovered_lines": "1",
                "uncovered_conditions": "0",
            }],
            "issues": [],
        }
        output = sonar_utils.format_sonar_report({("repo", 7): report})
        self.assertIn(
            "internal/domains/location/app/commands/add_location.go: 50.0%"
            " coverage (1 uncovered lines, 0 uncovered conditions)",
            output,
        )

    def test_shows_hotspots_even_when_there_are_no_issues(self):
        # Regression: hotspots used to sit after an early `continue` that
        # fired whenever the issues list was empty, silently dropping them.
        report = {
            "quality_gate": {"status": "OK", "conditions": []},
            "measures": {},
            "issues": [],
            "security_hotspots": [{
                "securityCategory": "sql-injection",
                "vulnerabilityProbability": "HIGH",
                "message": "Make sure using this SQL query is safe.",
                "component": "some-org_some-repo:src/db.go",
                "line": 12,
                "author": "someone@example.com",
            }],
        }

        output = sonar_utils.format_sonar_report({("repo", 7): report})

        self.assertIn("no new issues", output)
        self.assertIn("security hotspots to review (1):", output)
        self.assertIn("sql-injection / HIGH", output)
        self.assertIn("Make sure using this SQL query is safe.", output)
        self.assertIn("src/db.go", output)
        self.assertIn("line: 12", output)
        self.assertNotIn("someone@example.com", output)


if __name__ == "__main__":
    unittest.main()
