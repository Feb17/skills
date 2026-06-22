# create-jira-subtasks

Cursor/agent skill that breaks a Jira ticket into well-scoped sub-tasks, grounded in the user's actual workspace work, and creates them via the Atlassian MCP with every operational attribute inherited from the parent.

## Install

```bash
npx skills add https://github.com/Feb17/create-jira-subtasks -g -y
```

## Use It When

- A parent Jira ticket has a DoD / AC list but no subtasks yet.
- You've done real implementation / PoC work in the current workspace and want to back-fill the parent ticket with structured sub-tasks.
- You want sub-tasks to inherit Due Date, Components, Labels, Fix Versions from the parent instead of drifting.

This skill is deliberately narrow: it creates sub-tasks and nothing else. It does not modify the parent, transition status, or create linked issues / epics.

## Invocation Styles

Both natural-language and command-style requests work:

```text
帮我给 BDPIX-1739 拆子任务
给 BDPIX-1739 创建 subtasks
split BDPIX-1739 into sub-tasks
break down BDPIX-1739
/create-jira-subtasks BDPIX-1739
```

If you give a full Jira URL, the agent extracts the issue key. One invocation = one parent.

## What The Agent Will Do

1. Read the parent ticket: summary, DoD/AC, duedate, components, labels, fixVersions, assignee, epic link.
2. Detect the project's Subtask issuetype name (`Subtask` / `Sub-task` / `子任务` vary by instance).
3. List existing subtasks to avoid duplicates.
4. Survey the current workspace: source code, Dockerfile, README, recent git commits.
5. Draft a subtask list, typically 5-10 items mixing current-work and follow-up.
6. Preview with you and iterate until you approve. 2-3 revision rounds are normal.
7. Create subtasks in parallel with a minimum payload.
8. Align Due Date / Components / Labels / Fix Versions / epic link to the parent in a single update pass.
9. Report back with issue keys and links.

## Why Two Passes

Creating with all fields at once has caused drift and cleanup:

- `jira_create_issue` sometimes accepts but silently drops fields that need separate permissions or different field names.
- Ad-hoc labels added for "organization" drift from the parent and need cleanup.
- Parent and subtask schemas do not always overlap 1:1.

Doing two passes guarantees alignment with the parent and makes cleanup straightforward.

## Reference Run

Parent: `BDPIX-1739` - `Task3.39_Build up a Vector Database of ISA-CN Operation Knowledge Base`

Workspace context surveyed: `rag-ingest/` package, `Dockerfile`, `compose.yml`, and `tests/`.

Drafting rounds: 3

- Round 1: too granular, with 11 implementation-level chores.
- Round 2: scope crept into downstream application integration.
- Round 3: accepted, with 5 current-work items and 4 follow-up items.

Subtasks created: `BDPIX-1792` through `BDPIX-1800`.

Parent attributes mirrored onto every subtask: `duedate=2026-05-29`, `components=[BRP_2026]`, `labels=[Q2]`, `fixVersions=[]`.

Lesson that drove the two-pass flow: adding ad-hoc labels during creation required a cleanup pass. The skill now forbids setting `labels` / `components` / `duedate` / `fixVersions` / `epic_link` in the create call.

## File Structure

```text
create-jira-subtasks/
├── README.md
└── SKILL.md
```

## Not Included

- REST API fallback helper. The skill currently depends on an Atlassian MCP.
- Cross-project / multi-parent batch. Intentionally unsupported to keep the agent from over-reaching.
