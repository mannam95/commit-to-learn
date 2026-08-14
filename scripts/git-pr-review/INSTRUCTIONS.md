# git-pr-review — agent instructions

Scripts that fetch PR review data for one repo/PR or many at once: review
comments (Copilot + human, via the `gh pr-review` GitHub CLI extension) and
SonarCloud code-quality analysis (via the SonarCloud REST API).

## Layout

- `pr_utils.py` — shared logic for the GitHub-comments scripts (fetching,
  parsing, formatting, `.env` loading, clipboard copy).
- `single_repo_pr_comments.py` / `multi_repo_pr_comments.py` — GitHub PR
  review comments, config from `SINGLE_REPO_*` / `MULTI_REPO_*`.
- `sonar_utils.py` — shared logic for the Sonar scripts (fetching quality
  gate status, new-code measures, and new issues from the SonarCloud API;
  formatting the report).
- `single_repo_sonar_report.py` / `multi_repo_sonar_report.py` — SonarCloud
  PR analysis, reusing the same `SINGLE_REPO_*` / `MULTI_REPO_*` owner/repo/PR
  config plus `SONAR_ORG` / `SONAR_TOKEN`. Every entry-point script is a thin
  wrapper around its `*_utils.py` module — reusable logic belongs there, not
  duplicated across scripts.
- `.env` — real config (gitignored, has org-specific values, including the
  Sonar token). Copy from `.env.example` to bootstrap.
- `.env.example` — template with generic placeholder values. Keep it free of
  any real org/repo/reviewer/token values.
- `tests/` — plain stdlib `unittest`, no pytest dependency required (though
  `pytest tests/` also works). One test file per source module being tested.

## Conventions to keep following

- **No new dependencies.** Everything here runs with the stdlib. The `.env`
  loader in `pr_utils.load_dotenv` is a deliberately tiny hand-rolled parser
  instead of `python-dotenv` — keep it that way unless there's a real reason
  to add a dependency.
- **Both scripts must stay symmetric.** Same CLI flags (`--hide-resolved`,
  `--show-suggestions`, `--copy`), same output format
  (`pr_utils.format_issues_by_repo`), same config source (`.env`). If you
  change one script's behavior, mirror it in the other, or move the change
  into `pr_utils.py` so both get it for free.
- **`MULTI_REPO_REPOS_AND_PRS` is comma-optional on purpose.** It's parsed
  with `pr_utils.REPO_PR_PAIR_RE` (regex), not `json.loads`, specifically so
  that commenting/uncommenting individual `["repo", pr]` lines in `.env`
  can't break the file by leaving a dangling/missing comma. Don't switch this
  back to strict JSON parsing.
- **No secrets/org names in `.env.example` or in this repo's tracked files.**
  Real values (org name, repo names, PR numbers, reviewer logins) only ever
  go in the gitignored `.env`.
- **Comments-as-toggles style.** Config alternatives (other repos, other
  reviewers) are kept as commented-out lines in `.env` rather than deleted,
  so switching context is a one-line uncomment. Preserve this when editing
  `.env` — don't delete a commented alternative unless asked to.
- **The Sonar scripts don't duplicate owner/repo/PR config.** They read
  `SINGLE_REPO_*`/`MULTI_REPO_*` directly and derive the SonarCloud project
  key as `f"{owner}_{repo}"` (`sonar_utils.build_project_key`) — this org's
  convention. Only `SONAR_ORG`/`SONAR_TOKEN` are Sonar-specific env vars.
- **Sonar issues/measures are new-code-only, on purpose.** `fetch_new_issues`
  passes `inNewCodePeriod=true`, which scopes to the PR's diff against its
  target branch — not the project's whole existing issue backlog. Don't drop
  that param; it's the whole point of a per-PR report.
- **Network calls (`urllib`) don't get wrapped in a try/except that swallows
  errors.** `sonar_utils.fetch_report_for_repo` re-raises as `RuntimeError`
  with repo/PR context so the caller can print it and keep going for the
  other repos in a multi-repo run.

## Running tests

From this directory:

```
python3 -m unittest discover -s tests -t .
```

or `python3 -m pytest tests/`. Both work; `tests/__init__.py` exists solely
to make `unittest discover` happy on Python 3.11+, and each test file also
inserts the parent directory onto `sys.path` so it can be run directly
(`python3 tests/test_pr_utils.py`) without any discovery flags.

## Things you cannot verify in a sandbox

`fetch_review_data`/`run_cmd` shell out to `gh pr-review`, and
`sonar_utils._get` calls the SonarCloud API over HTTPS — both need real auth
and network access. There's no way to exercise either real fetch path
locally — everything else (parsing, formatting, `.env` loading) is covered by
`tests/` and can be run directly. `sonar_utils.py` is split so the network
call (`_get`) is separate from the pure parsing functions
(`extract_quality_gate`, `extract_new_code_measures`, `extract_new_issues`),
which is what makes the parsing testable without hitting the network —
keep new Sonar logic split the same way.
