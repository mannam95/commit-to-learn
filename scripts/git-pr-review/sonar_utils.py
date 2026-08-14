"""Shared helpers for fetching SonarCloud PR analysis results."""
import json
import urllib.error
import urllib.parse
import urllib.request

SONAR_API_BASE = "https://sonarcloud.io/api"

NEW_CODE_METRICS = [
    "new_bugs",
    "new_vulnerabilities",
    "new_code_smells",
    "new_security_hotspots",
    "new_duplicated_lines_density",
    "new_coverage",
]


def build_project_key(owner, repo):
    """This org's SonarCloud projects follow the '{owner}_{repo}' convention."""
    return f"{owner}_{repo}"


def _get(path, token, **params):
    url = f"{SONAR_API_BASE}{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read())


def extract_quality_gate(data):
    return data["projectStatus"]


def _measure_value(measure):
    """
    'new_*' metrics are scoped to a leak period (the PR's new code vs the
    target branch), so their value lives under `periods`, not `value`.
    """
    periods = measure.get("periods") or []
    value = measure.get("value")
    if value is None and periods:
        value = periods[0].get("value")
    return value


def extract_new_code_measures(data):
    return {
        measure["metric"]: _measure_value(measure)
        for measure in data.get("component", {}).get("measures", [])
    }


def extract_new_issues(data):
    return data.get("issues", [])


def extract_duplications_by_file(data):
    """
    Duplication isn't modeled as a Sonar 'issue', so /api/issues/search can
    never surface it -- only files with actual new-code duplication are kept.
    """
    files = []
    for component in data.get("components", []):
        measures = {
            m["metric"]: _measure_value(m) for m in component.get("measures", [])
        }
        try:
            density = float(measures.get("new_duplicated_lines_density") or 0)
        except ValueError:
            density = 0
        if density <= 0:
            continue
        files.append({
            "path": component.get("path") or component.get("name", "N/A"),
            "density": measures.get("new_duplicated_lines_density"),
            "duplicated_lines": measures.get("new_duplicated_lines"),
        })
    return files


def extract_coverage_by_file(data):
    """
    Coverage isn't modeled as a Sonar 'issue' either. Only files that
    actually have new lines requiring coverage are kept -- a file with
    nothing to cover (e.g. types-only) has no 'new_coverage' value at all.
    """
    files = []
    for component in data.get("components", []):
        measures = {
            m["metric"]: _measure_value(m) for m in component.get("measures", [])
        }
        if measures.get("new_coverage") is None:
            continue
        files.append({
            "path": component.get("path") or component.get("name", "N/A"),
            "coverage": measures.get("new_coverage"),
            "uncovered_lines": measures.get("new_uncovered_lines"),
            "uncovered_conditions": measures.get("new_uncovered_conditions"),
        })
    return files


def extract_security_hotspots(data):
    return data.get("hotspots", [])


def fetch_quality_gate(org, token, owner, repo, pr_number):
    data = _get(
        "/qualitygates/project_status", token,
        organization=org, projectKey=build_project_key(owner, repo),
        pullRequest=pr_number)
    return extract_quality_gate(data)


def fetch_new_code_measures(org, token, owner, repo, pr_number):
    data = _get(
        "/measures/component", token,
        organization=org, component=build_project_key(owner, repo),
        pullRequest=pr_number, metricKeys=",".join(NEW_CODE_METRICS))
    return extract_new_code_measures(data)


def fetch_new_issues(org, token, owner, repo, pr_number):
    """
    Issues introduced by this PR's new code only. `inNewCodePeriod=true`
    scopes the search to the leak period, which for a PR is exactly its
    diff against the target branch -- not the project's existing backlog.
    """
    data = _get(
        "/issues/search", token,
        organization=org, componentKeys=build_project_key(owner, repo),
        pullRequest=pr_number, resolved="false", inNewCodePeriod="true",
        ps=500)
    return extract_new_issues(data)


def _fetch_component_tree(org, token, owner, repo, pr_number, metric_keys):
    return _get(
        "/measures/component_tree", token,
        organization=org, component=build_project_key(owner, repo),
        pullRequest=pr_number, qualifiers="FIL", strategy="leaves",
        metricKeys=",".join(metric_keys), ps=500)


def fetch_duplications_by_file(org, token, owner, repo, pr_number):
    data = _fetch_component_tree(
        org, token, owner, repo, pr_number,
        ["new_duplicated_lines_density", "new_duplicated_lines"])
    return extract_duplications_by_file(data)


def fetch_coverage_by_file(org, token, owner, repo, pr_number):
    data = _fetch_component_tree(
        org, token, owner, repo, pr_number,
        ["new_coverage", "new_uncovered_lines", "new_uncovered_conditions"])
    return extract_coverage_by_file(data)


def fetch_security_hotspots(org, token, owner, repo, pr_number):
    """
    Security Hotspots are a distinct concept from Issues in Sonar's model,
    so /api/issues/search never returns them -- this hits the dedicated
    hotspots endpoint instead. Leaving `status` unset defaults to
    TO_REVIEW-only, which is what actually needs attention on a fresh PR.
    """
    data = _get(
        "/hotspots/search", token,
        organization=org, projectKey=build_project_key(owner, repo),
        pullRequest=pr_number, ps=500)
    return extract_security_hotspots(data)


def _to_float(value, default=0.0):
    try:
        return float(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def fetch_report_for_repo(org, token, owner, repo, pr_number):
    try:
        measures = fetch_new_code_measures(org, token, owner, repo, pr_number)

        duplications_by_file = []
        if _to_float(measures.get("new_duplicated_lines_density")) > 0:
            duplications_by_file = fetch_duplications_by_file(
                org, token, owner, repo, pr_number)

        coverage_by_file = []
        if measures.get("new_coverage") is not None:
            coverage_by_file = fetch_coverage_by_file(
                org, token, owner, repo, pr_number)

        security_hotspots = []
        if _to_float(measures.get("new_security_hotspots")) > 0:
            security_hotspots = fetch_security_hotspots(
                org, token, owner, repo, pr_number)

        return {
            "quality_gate": fetch_quality_gate(
                org, token, owner, repo, pr_number),
            "measures": measures,
            "duplications_by_file": duplications_by_file,
            "coverage_by_file": coverage_by_file,
            "security_hotspots": security_hotspots,
            "issues": fetch_new_issues(org, token, owner, repo, pr_number),
        }
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"Sonar API error for {owner}/{repo} PR #{pr_number}: "
            f"{e.code} {e.reason}") from e


def format_sonar_report(reports_by_repo):
    """reports_by_repo: {(repo_name, pr_number): report_dict_or_None}"""
    lines = []
    for (repo_name, pr_number), report in reports_by_repo.items():
        lines.append(f"\n{'#' * 60}")
        lines.append(f"# SONAR: {repo_name}  |  PR: {pr_number}")
        lines.append(f"{'#' * 60}\n")

        if report is None:
            lines.append("  (no sonar report available)\n")
            continue

        gate = report["quality_gate"]
        lines.append(f"  quality gate: {gate['status']}")
        for condition in gate.get("conditions", []):
            # Whole-project conditions (e.g. overall ratings) aren't scoped
            # to this PR's new code and come back without periodIndex/actualValue.
            scope = "new code" if "periodIndex" in condition else "overall"
            actual = condition.get("actualValue", "n/a")
            lines.append(
                f"    - [{scope}] {condition.get('metricKey')}: {actual}"
                f" (status: {condition.get('status')})")
        lines.append("")

        lines.append("  new-code measures:")
        for metric, value in report["measures"].items():
            lines.append(f"    {metric}: {value}")
        lines.append("")

        duplications = report.get("duplications_by_file") or []
        if duplications:
            lines.append("  duplicated lines by file (new code):")
            for file_dup in duplications:
                try:
                    density = f"{float(file_dup['density']):.1f}"
                except (TypeError, ValueError):
                    density = file_dup["density"]
                lines.append(
                    f"    {file_dup['path']}: {density}%"
                    f" ({file_dup['duplicated_lines']} lines)")
            lines.append("")

        coverage_files = report.get("coverage_by_file") or []
        if coverage_files:
            lines.append("  coverage by file (new code):")
            for file_cov in coverage_files:
                try:
                    pct = f"{float(file_cov['coverage']):.1f}"
                except (TypeError, ValueError):
                    pct = file_cov["coverage"]
                lines.append(
                    f"    {file_cov['path']}: {pct}% coverage"
                    f" ({file_cov['uncovered_lines']} uncovered lines,"
                    f" {file_cov['uncovered_conditions']} uncovered conditions)")
            lines.append("")

        issues = report.get("issues") or []
        if issues:
            lines.append(f"  new issues ({len(issues)}):")
            for idx, issue in enumerate(issues, start=1):
                # Sonar issues also carry an 'author' (a real email address)
                # -- deliberately not included below, this report isn't the
                # place to surface who wrote a given line.
                lines.append(f"  issue{idx}")
                lines.append(
                    f"  type/severity: {issue.get('type')}"
                    f" / {issue.get('severity')}")
                lines.append("  message:")
                lines.append("  " + issue.get("message", ""))
                lines.append("  filename:")
                lines.append(
                    "  " + issue.get("component", "N/A").split(":", 1)[-1])
                if issue.get("line") is not None:
                    lines.append(f"  line: {issue['line']}")
                if issue.get("effort"):
                    lines.append(f"  effort: {issue['effort']}")
                if issue.get("tags"):
                    lines.append(f"  tags: {', '.join(issue['tags'])}")
                lines.append("\n  " + "-" * 50 + "\n")
        else:
            lines.append("  (no new issues)\n")

        hotspots = report.get("security_hotspots") or []
        if hotspots:
            lines.append(f"  security hotspots to review ({len(hotspots)}):")
            for idx, hotspot in enumerate(hotspots, start=1):
                # Hotspots also carry an 'author' (a real email address) --
                # deliberately not included below, same reasoning as issues.
                lines.append(f"  hotspot{idx}")
                lines.append(
                    f"  category/probability: {hotspot.get('securityCategory')}"
                    f" / {hotspot.get('vulnerabilityProbability')}")
                lines.append("  message:")
                lines.append("  " + hotspot.get("message", ""))
                lines.append("  filename:")
                lines.append(
                    "  " + hotspot.get("component", "N/A").split(":", 1)[-1])
                if hotspot.get("line") is not None:
                    lines.append(f"  line: {hotspot['line']}")
                lines.append("\n  " + "-" * 50 + "\n")

    return "\n".join(lines)
