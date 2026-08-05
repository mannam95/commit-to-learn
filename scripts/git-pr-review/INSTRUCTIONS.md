# git-pr-review — agent instructions

Scripts that fetch PR review comments (Copilot + human) via the `gh pr-review`
GitHub CLI extension, for one repo/PR or many at once.

## Layout

- `pr_utils.py` — all shared logic (fetching, parsing, formatting, `.env`
  loading, clipboard copy). Both entry-point scripts are thin wrappers around
  this module. Anything reusable belongs here, not duplicated across scripts.
- `single_repo_pr_comments.py` — one repo/PR, config from `SINGLE_REPO_*`.
- `multi_repo_pr_comments.py` — many repos/PRs, config from `MULTI_REPO_*`.
- `.env` — real config (gitignored, has org-specific values). Copy from
  `.env.example` to bootstrap.
- `.env.example` — template with generic placeholder values. Keep it free of
  any real org/repo/reviewer names.
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

`fetch_review_data`/`run_cmd` shell out to `gh pr-review`, which needs GitHub
auth and network access. There's no way to exercise the real fetch path
locally — everything else (parsing, formatting, `.env` loading) is covered by
`tests/` and can be run directly.
