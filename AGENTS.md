# skills-merged

Collection of agent skills for OpenCode. No build, test, or CI pipeline.

## What lives where

| Directory | Entrypoint | For |
|-----------|-----------|-----|
| `bosch-brand-style-guide/` | `SKILL.md` | Bosch corporate design one-pagers (HTML/CSS) |
| `bosch-procedure-documentation/` | `SKILL.md` + `REFERENCE.md` | Bosch Confluence procedure docs in storage format |
| `create-jira-subtasks/` | `SKILL.md` | Breaking Jira tickets into grounded subtasks |
| `jira-description-updater/` | `SKILL.md` + `scripts/atlassian_rest_fallback.py` | Writing DoD-style Jira descriptions |

## Key workflow notes

- **Skills are not installed via npm.** They're loaded by opencode.json `skills` array or placed in `~/.config/opencode/skills/`. No package manager, no lockfile, no build step.
- **`jira-description-updater` REST fallback** (`scripts/atlassian_rest_fallback.py`): requires env vars (`JIRA_URL`, `JIRA_PERSONAL_TOKEN`, `CONFLUENCE_URLS`, etc.) sourced before use. See its `README.md` for the full list. The script covers Jira + Confluence reads/writes across multiple Confluence instances.
- **`bosch-procedure-documentation`** always reads/writes Confluence in **storage format** (`convert_to_markdown=false`) — markdown corrupts macros. `REFERENCE.md` has detailed macro safety rules and a known MCP upload_attachment bug fix.
- **Git remotes**: GitHub (`github.com/Feb17/skills`) + Bosch internal GitLab. Push to both via `origin` (see `README.md` for URLs).
- **No tests, no linting, no typechecking, no formatter config.** Changes are reviewed manually.

## Agent skills

### Issue tracker

Issues live on GitHub Issues (`github.com/Feb17/skills`). External PRs are not a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles map to labels `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout. See `docs/agents/domain.md`.
