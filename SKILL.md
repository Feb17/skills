---
name: jira-description-updater
description: Update a Jira issue description into a complete DoD-style format using Jira context plus related Confluence documents. Use when the user asks to update an issue description, improve a Jira description, or uses command-style requests like "/update-jira-desc BDPIX-1705".
allowed-tools: Bash(python:*), Bash(python3:*)
---

# Jira Description Updater

## Overview

Update a Jira issue description into a complete, closure-ready, DoD-style format.

This skill is optimized for operational / project-tracking tickets where the current description is a template or only partially filled.

The skill must:
1. Read the target Jira issue.
2. Inspect nearby Jira context, especially linked issues / parent / epic.
3. Search Confluence for related documentation using the enriched Jira context.
4. Generate a complete description with explicit acceptance criteria.
5. Write the description back to Jira.
6. Report which Confluence pages were used.

Default scope: **description only**. Do not update title or comments unless the user explicitly asks.

## Tool Preference

Use this execution order by default:

1. **Prefer `mcp-atlassian` tools** for Jira and Confluence reads/writes.
2. **Fallback to direct REST API** only when the required `mcp-atlassian` capability is unavailable, failing consistently, or clearly cannot complete the requested operation.

Fallback rules:
- Try MCP first for normal issue lookup, related issue lookup, Confluence search, and Jira description update.
- Use REST API only as a backup path, not as the first choice.
- Keep the same behavior and output format regardless of whether MCP or REST API is used.
- If fallback is used, mention it briefly in the final response.
- For Confluence specifically, if the current MCP server only covers one instance and the environment contains multiple Confluence base URLs, use REST fallback to search across all configured Confluence instances.

## REST Fallback Helper

This skill includes a helper script for REST fallback:

`scripts/atlassian_rest_fallback.py`

Use it only when MCP is unavailable or failing.

### Environment variables

Assume the user has already configured the required local Atlassian environment according to `README.md`.

Keep `README.md` as the source of truth for:
- Jira / Confluence environment variables
- on-prem PAT examples
- multi-Confluence configuration
- REST fallback setup details

Current limitation note:
- stock `mcp-atlassian` does **not** natively search multiple Confluence base URLs in one server process
- therefore, for environments like `/confluence` + `/confluence2`, keep MCP as the first attempt and use REST fallback for federated multi-instance search when needed

### REST helper examples

```bash
# Get full Jira issue context
python3 scripts/atlassian_rest_fallback.py jira-get-issue BDPIX-1705 --fields '*all' --expand changelog

# Search related Jira issues
python3 scripts/atlassian_rest_fallback.py jira-search --jql 'project = BDPIX AND summary ~ "Portal"'

# Search Confluence by text
python3 scripts/atlassian_rest_fallback.py confluence-search --query 'ISA-CN Portal'

# Search across multiple configured Confluence instances
python3 scripts/atlassian_rest_fallback.py confluence-search --query 'MS Defender' --compact

# Get Confluence page by full URL or page id
python3 scripts/atlassian_rest_fallback.py confluence-get-page --url 'https://inside-docupedia.bosch.com/confluence2/spaces/37146430/pages/860734767/Known+issues+after+MS+Defender+installation' --compact

# Update Jira description from a file
python3 scripts/atlassian_rest_fallback.py jira-update-description BDPIX-1705 --description-file /tmp/new-description.md
```

## Supported Invocation Styles

Treat all of the following as triggers for this skill:

- `更新 BDPIX-1705 的 description`
- `帮我补全 BDPIX-1607 的 description`
- `update BDPIX-1662 description`
- `/update-jira-desc BDPIX-1705`

If the user gives a full Jira URL, extract the issue key from it.

## Primary Goal

Produce a description that reads like a well-maintained operational ticket:
- clear **As a / I want / so that** statement
- concrete, realistic **AC1..ACn**
- documented **Confluence links** when available
- close-ready ending line

The skill should prefer grounded content over generic filler.

## Workflow

### 1) Resolve the target issue

Use Jira tools to load:
- issue summary
- current description
- status
- labels
- assignee / reporter
- comments
- linked issues / parent / subtasks / epic context when available
- changelog when it helps understand the task direction

Minimum expected read:
- `jira_get_issue(issue_key, fields="*all")`

### 2) Expand Jira context before searching Confluence

Do this step by default before searching Confluence.

Priority order:
1. linked issues
2. parent / subtasks
3. epic-related tickets
4. previous update comments that reveal scope or blockers
5. similarly named tickets in the same project

Use only the amount of extra Jira context needed to avoid guessing.

The purpose of this step is to enrich the search vocabulary and avoid weak Confluence matches.

At minimum, try to extract from nearby Jira context:
- platform / system names
- workstream keywords
- implementation scope
- related document names or demand references
- dependent tasks or follow-up themes

### 3) Search Confluence for related documents

Always search Confluence after the Jira-context expansion step.

Search strategy, in order:
1. exact or near-exact issue summary terms
2. core nouns from the summary and description
3. system / platform names from the ticket (for example: Portal, Rancher, ServiceNow, Zabbix, RB-PAM, Airflow, ADDA)
4. names found in linked issues / parent / epic / comments
5. demand or reference ticket IDs found in Jira context when those IDs are known to have related documentation

If Jira comments already contain direct Confluence URLs, treat those URLs as strong evidence.
- Try MCP first when the configured Confluence instance matches.
- If MCP cannot read those pages because they belong to another Confluence base URL (for example `/confluence2`), use the REST fallback helper to fetch or validate them.

Prefer pages that provide one or more of the following:
- architecture
- introduction / overview
- runbook
- onboarding
- value overview
- implementation or requirement notes
- operating or validation instructions

Use the best 1-5 results. Do not stuff weakly related links into the description.

If no useful Confluence document is found, continue with Jira-only context.

### 3a) Evidence priority

When drafting, prefer evidence in this order:
1. target issue itself
2. linked issues / parent / epic / nearby Jira context
3. Confluence documents found from that enriched context

Confluence should strengthen and document the description, not override stronger Jira evidence.

### 4) Draft the description

Use this structure by default:

```markdown
**DoD(Definition of Done):**

As a Operator/Service Owner I want to <goal>
so that <business / operational value>.

Acceptance criteria (goals which should be achieved) are defined
All acceptance criteria are covered/validated
* AC1: ...
* AC2: ...
* AC3: ...
* AC4: ... (optional)
* Documentation is done and up to date (if required) and linked to the ticket:
** <Doc 1>: <URL or issue reference>
** <Doc 2>: <URL or issue reference>
* Ticket is set to status closed and review by the Ticket owner
```

### 5) Writing rules

#### Do
- Keep the description specific to the ticket scope.
- Use realistic acceptance criteria based on evidence from Jira / Confluence.
- Write documentation links directly into the description when relevant pages exist.
- Use concise operational language.
- Prefer 3-5 acceptance criteria.
- Include follow-up or phased wording when the task is clearly exploratory or partially dependent on other teams.

#### Do not
- invent implementation details with no backing context
- overpromise completed outcomes for a future / still-open ticket
- add title or comment content unless requested
- mention any example issue used internally as inspiration
- add unrelated Confluence links just to fill the template

### 6) Tone by ticket type

#### If the ticket is a planned Q2 / future task
Use forward-looking language:
- `I want to ...`
- `will be validated`
- `follow-up actions are documented`
- `integration is implemented or prototyped`

#### If the ticket is already clearly near completion
Use delivery-oriented language:
- `is implemented and validated`
- `is completed`
- `is documented`

### 7) Update Jira

Write the new description back with `jira_update_issue`.

After the update, return:
- issue key
- updated summary
- short 1-2 sentence recap
- list of Confluence pages used

## Confluence Relevance Heuristic

A page is worth linking when it materially improves the description by giving:
- official terminology
- architecture or operating scope
- implementation context
- onboarding or runbook evidence
- validation / business value context

If multiple pages overlap, keep the clearest and most useful ones only.

## Ambiguity Handling

Ask a targeted question only when a wrong guess would materially distort the description.

Examples:
- multiple unrelated systems share the same keyword
- the issue is too empty and Confluence results split into different initiatives
- the ticket appears to cover more than one workstream

Otherwise, proceed directly.

## Example Success Pattern

A strong result usually includes:
- one clear purpose statement
- 3-5 ACs grounded in actual work items
- 1-5 documentation links
- wording that matches the task maturity (planned vs in progress vs close-ready)

## Output Back To User

After updating, respond briefly in this format:

```markdown
已更新 `ISSUE-1234` 的 description。

参考文档：
- <Confluence page 1>
- <Confluence page 2>
```

If no Confluence documents were used, say so explicitly.
