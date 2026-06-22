---
name: create-jira-subtasks
description: Break a Jira ticket into well-scoped sub-tasks grounded in the user's actual workspace work, then create them via the Atlassian MCP with every operational attribute inherited from the parent ticket. Use when the user asks to create / split / break down sub-tasks (子任务 / sub-task / subtask) for a Jira issue, or uses command-style phrasing like "/create-jira-subtasks PROJ-123".
allowed-tools: CallMcpTool, AskQuestion, Read, Glob, Grep, Shell(git:*)
---

# Create Jira Subtasks

## Overview

Produce a set of sub-tasks that (1) reflect what the user has actually built in the current workspace and (2) sit cleanly under the parent ticket: same project, same operational attributes, no scope drift.

**Hard invariant: two-pass creation.** Every subtask is created with the minimum payload (summary, description, issue_type, assignee, parent) first, then aligned to the parent's operational attributes in a separate update pass. Never put `labels` / `components` / `duedate` / `fixVersions` / `epic_link` on the create call. Doing so has caused real rework.

## Default Scope

### Does

- Create `Subtask`-type issues under a single parent.
- Mirror parent's operational attributes: `duedate`, `components`, `labels`, `fixVersions`, epic link.
- Use parent's `assignee` by default, unless the user specifies otherwise.

### Does not

- Modify the parent ticket.
- Transition status of anything. New subtasks stay at workflow default.
- Copy parent's `priority` / `reporter` / `status`.
- Create issue links or epics.
- Handle multiple parents per invocation. One parent per call.

## Supported Invocation Styles

Any of these triggers the skill:

```text
帮我给 BDPIX-1739 拆子任务
给 BDPIX-1739 创建 subtasks
split BDPIX-1739 into sub-tasks
break down BDPIX-1739
/create-jira-subtasks BDPIX-1739
```

If a full Jira URL is given, extract the issue key from it.

## Tool Preference

Use Atlassian MCP (`user-mcp-atlassian` or equivalent) for all Jira operations. Read the tool descriptor first if unsure of the schema. Primary tools:

- `jira_get_issue`: fetch parent and existing subtasks.
- `jira_search`: detect Subtask issuetype name, list existing subtasks.
- `jira_create_issue`: create each subtask.
- `jira_update_issue`: align attributes after creation.

## Workflow

```text
- [ ] 1. Read the parent ticket
- [ ] 2. Detect the Subtask issuetype name used in this project
- [ ] 3. List existing subtasks and avoid duplicates
- [ ] 4. Survey the user's recent workspace work
- [ ] 5. Draft a grounded subtask list
- [ ] 6. Preview and get user confirmation; iterate as needed
- [ ] 7. Create subtasks in parallel with minimum payload
- [ ] 8. Align every subtask to the parent in a single parallel update pass
- [ ] 9. Report back with keys and links
```

### Step 1. Read the parent ticket

```text
jira_get_issue(issue_key=<KEY>, fields="*all", comment_limit=10)
```

Extract and remember:

- `summary`, `description`: the subject and DoD / AC list.
- `issuetype`: note that parent may be `Open Item` / `Story` / `Epic`, while its subtasks still need to be `Subtask`.
- Operational attributes to mirror later: `duedate`, `components`, `labels`, `fixVersions`, epic link custom field.
- `assignee`: default assignee for subtasks.
- `project.key`: derive as `parent_key.split("-")[0]`. This is the target project for creation.

Detect the primary language of the parent's `summary` / `description`. Write subtask summaries and descriptions in that language. Default to English if unclear.

### Step 2. Detect the Subtask issuetype name

Different instances use `Subtask`, `Sub-task`, or `子任务`. Confirm by sampling:

```text
jira_search(
  jql="project = <PROJECT> AND issuetype in subTaskIssueTypes()",
  fields="issuetype",
  limit=1,
)
```

Use the exact string returned in `issue_type.name`. Do not reuse parent's `issuetype`; parent and subtask types are almost always different.

### Step 3. List existing subtasks

```text
jira_search(jql="parent = <KEY>", fields="summary,status,issuetype", limit=50)
```

If any exist, surface them in the preview and do not re-create equivalent ones.

### Step 4. Survey the user's recent workspace work

Ground the subtasks in what the user has actually done. Check, in priority order:

1. Source code and config directly under the project directory: `src/`, `Dockerfile`, `compose.yml`, `requirements.txt`, `tests/`.
2. Recent `README.md` / design docs in the repo.
3. Recent `git log --oneline -20` if this is a git repo.
4. Confluence pages referenced from the ticket `description` via `confluence_get_page`.

Build a mental inventory: which AC is done, which is in progress, which is untouched. Do not invent work the user has not done.

### Step 5. Draft the subtask list

**Do**

- Stay inside the parent's subject. If the ticket is "build X", do not add subtasks about downstream integration of X.
- Map to AC when the parent has Acceptance Criteria. Tag summaries with `[AC1]`, `[AC2/AC3]` when helpful.
- Prefer milestone-level granularity. Each subtask should be independently trackable.
- Mix current work, reflecting completed / in-progress items, and a small number of follow-ups that remain inside the parent's subject.
- Aim for 5-10 subtasks. Outside this range, reconsider granularity.
- Tone: current work uses delivery tense ("Implement X", "Validate Y"); follow-up uses forward-looking tense ("Productionize X", "Expand to Y").

**Do not**

- Split a single PoC into code-level chores such as `implement parser.py`, `implement chunker.py`, and so on.
- Add subtasks that depend on other teams / downstream products not named in the parent.
- Introduce `labels` / `components` that the parent does not have.
- Invent work the user has not done or committed to.

Description template in the parent ticket's language:

```text
Covers <ACx> of parent <PARENT-KEY>.

Goal
<one-paragraph outcome>

Scope
- <bulleted list grounded in the actual workspace artifacts>

Deliverables
- <what "done" looks like>

Non-goals
- <explicitly exclude anything that belongs to a sibling ticket>
```

### Step 6. Preview and confirm

Before any `jira_create_issue` call:

- Render candidates as a compact markdown table: `#`, `Summary`, `AC`.
- Use the `AskQuestion` tool when available with options like:
  - "Create all N"
  - "Create current-work items only"
  - "Create follow-ups only"
  - "Adjust first"

Only proceed after explicit user confirmation.

**Iteration is expected.** 2-3 revision rounds are normal. Typical feedback signals:

- "Too granular / too specific": collapse implementation detail into milestones.
- "Off-topic / don't consider X": cut drift and re-anchor on the DoD.
- "Give me more follow-ups": add follow-up items, still strictly inside subject.

Don't get defensive. Each rejection is a signal about intent. Re-draft the whole list, not just a patch, re-preview, and ask again.

### Step 7. Create subtasks (minimum payload)

Fire `jira_create_issue` calls in parallel, one per subtask. Include only:

```text
jira_create_issue(
  project_key=<PROJECT>,
  summary=<SUMMARY>,
  issue_type=<SUBTASK_TYPE_NAME>,
  assignee=<ASSIGNEE>,
  description=<MARKDOWN>,
  additional_fields='{"parent": "<PARENT-KEY>"}',
)
```

Do not set `labels`, `components`, `fixVersions`, `duedate`, or `epic_link` here. That is Step 8's job and guarantees alignment with the parent.

### Step 8. Align attributes to parent (mandatory)

Run in parallel for every newly created subtask:

```text
jira_update_issue(
  issue_key=<NEW-KEY>,
  fields='{"duedate": "<PARENT.duedate>", "labels": <PARENT.labels JSON>, "fixVersions": <PARENT.fixVersions JSON>}',
  components="<comma-separated parent component names>",
)
```

Rules:

- `labels` must equal parent's exactly. Do not append extras.
- `components` passes as comma-separated names in the dedicated argument, not inside `fields`.
- If parent has an Epic link, also set it via `additional_fields='{"epic_link": "<EPIC-KEY>"}'`.
- Skip any parent field that is null / empty. Do not write empty values.

### Step 9. Report

Use this output template and adapt headings to the parent ticket's language:

```markdown
已在 `<PARENT-KEY>` 下创建 N 个 subtask。

**Current work**

| Key | Summary | AC |
|---|---|---|
| [<KEY1>](<URL>) | ... | ... |

**Follow-up**

| Key | Summary |
|---|---|
| [<KEY>](<URL>) | ... |

Due Date / Components / Labels / Fix Versions 均已与父任务对齐。
```

## Principles

1. **Grounded.** Every subtask corresponds to something in the workspace or a natural next step on the same subject.
2. **On-topic.** Never exceed the parent's subject. When in doubt, drop it.
3. **Parent-consistent.** Operational attributes are inherited, not re-invented.
4. **Two-pass creation.** Minimum create, then align. Never mix.
5. **Preview-first.** First create call only after explicit confirmation.
6. **Idempotent-ish.** Always check existing subtasks.

## Anti-patterns

- Adding subtasks about downstream application integration for a "build a database" ticket.
- Splitting a single PoC into eight code-level chores.
- Introducing new `labels` / `components` that the parent does not have.
- Creating subtasks without a `parent` field, which makes them orphans.
- Skipping Step 8 alignment, leaving subtasks without Due Date / Components.
- Reusing `parent.issuetype` as the subtask issue type.
- Handling two parent tickets in one invocation.

## Quick Reference: MCP Payload Shapes

Create in parallel, one call per subtask:

```json
{
  "project_key": "BDPIX",
  "summary": "...",
  "issue_type": "Subtask",
  "assignee": "AGU2SZH",
  "description": "...markdown...",
  "additional_fields": "{\"parent\": \"BDPIX-1739\"}"
}
```

Align in parallel, one call per subtask:

```json
{
  "issue_key": "BDPIX-1792",
  "fields": "{\"duedate\": \"2026-05-29\", \"labels\": [\"Q2\"], \"fixVersions\": []}",
  "components": "BRP_2026"
}
```

Note: `additional_fields` and `fields` are JSON strings, not objects.
