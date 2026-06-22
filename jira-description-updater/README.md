# jira-description-updater

用于**快速补全和更新 Jira issue description** 的本地 skill。

它适合处理这类场景：
- 当前 Jira description 只是模板
- issue 只有零散 AC，需要整理成完整 DoD 风格
- 需要自动去 **Jira + Confluence** 搜索上下文后再补全描述
- 希望生成出来的 description 可以直接用于后续跟踪或 closure 前整理

## 这个 skill 会做什么

默认只做一件事：

**更新 Jira issue 的 description**

它会按下面的顺序工作：

1. 读取目标 Jira issue
2. 优先分析相关 Jira 上下文
   - linked issues
   - parent / subtasks
   - epic
   - comments / changelog
3. 再去 Confluence 搜索相关文档
4. 基于 Jira + Confluence 上下文生成完整 description
5. 把新的 description 写回 Jira
6. 返回本次引用的文档链接

## 不会默认做什么

这个 skill **默认不会**：

- 更新 title
- 写 closure comment
- 修改其他字段

如果需要这些能力，建议拆成单独 skill，避免职责变重。

## 适合的请求方式

这个 skill 支持两种触发风格：

### 1) 自然语言

```text
更新 BDPIX-1705 的 description
帮我补全 BDPIX-1607 的 description
update BDPIX-1662 description
```

### 2) 命令式写法

```text
/update-jira-desc BDPIX-1705
```

> 注意：当前环境里没有真正注册的 slash command 系统，`/update-jira-desc ...` 是约定式写法，用于让 agent 更稳定识别你的意图。

## 生成出来的 description 风格

默认生成这类结构：

```markdown
**DoD(Definition of Done):**

As a Operator/Service Owner I want to <goal>
so that <business / operational value>.

Acceptance criteria (goals which should be achieved) are defined
All acceptance criteria are covered/validated
* AC1: ...
* AC2: ...
* AC3: ...
* AC4: ...
* Documentation is done and up to date (if required) and linked to the ticket:
** <Doc 1>: <URL>
** <Doc 2>: <URL>
* Ticket is set to status closed and review by the Ticket owner
```

特点：
- 有明确的 **As a / so that**
- AC 更完整、可追踪
- 会自动把相关 Confluence 文档写进去
- 对 planned task / in-progress task / 接近 closure 的 ticket，会自动调整语气

## Jira / Confluence 证据优先级

为了减少“拍脑袋补内容”，这个 skill 会按这个优先级判断信息来源：

1. 当前 issue 本身
2. linked issues / parent / epic / nearby Jira context
3. Confluence 文档

Confluence 的作用是：
- 补充正式术语
- 提供文档链接
- 强化架构 / runbook / onboarding / value 等背景

而不是覆盖更明确的 Jira 事实。

## MCP 与 REST 的执行策略

默认策略：

1. **优先使用 `mcp-atlassian` 工具**
2. 如果 MCP 不可用、持续失败、或不能完成操作，再回退到 **REST API**

也就是说：
- 正常情况下，skill 用 MCP 直接完成 Jira / Confluence 查询与 Jira 更新
- REST API 是兜底路径，不是默认首选
- 如果当前 MCP 只能覆盖一个 Confluence 实例，而你的环境里同时存在多个 Confluence（例如 `/confluence` 和 `/confluence2`），则由 REST fallback 负责做 **跨实例搜索**

### 关于多个 Confluence 实例

当前 stock `mcp-atlassian` 的限制是：

- **一个 MCP server 只能连接一个 Confluence base URL**
- 不能在一个 server 里同时原生搜索 `.../confluence` 和 `.../confluence2`

因此这个 skill 的推荐行为是：

1. 先用 MCP 查询当前已接入的 Jira / Confluence
2. 如果需要跨多个 Confluence 实例补充资料，再用 REST fallback 去做 federated search

如果以后你单独部署两个 `mcp-atlassian` server，也可以继续保留这个 REST fallback 作为兜底。

## REST fallback helper

这个 skill 自带一个脚本：

```text
scripts/atlassian_rest_fallback.py
```

它支持以下能力：

- `jira-get-issue`
- `jira-search`
- `jira-update-description`
- `confluence-search`
- `confluence-get-page`

### 示例

```bash
# 读取 issue
python3 scripts/atlassian_rest_fallback.py jira-get-issue BDPIX-1705 --fields '*all'

# Jira 搜索
python3 scripts/atlassian_rest_fallback.py jira-search --jql 'project = BDPIX AND summary ~ "Portal"' --compact

# Confluence 搜索
python3 scripts/atlassian_rest_fallback.py confluence-search --query 'ISA-CN Portal' --compact

# 多实例 Confluence 联合搜索
python3 scripts/atlassian_rest_fallback.py confluence-search --query 'MS Defender' --compact

# 按完整页面 URL 读取页面（适合 comment 里已经有 confluence2 链接）
python3 scripts/atlassian_rest_fallback.py confluence-get-page --url 'https://inside-docupedia.bosch.com/confluence2/spaces/37146430/pages/860734767/Known+issues+after+MS+Defender+installation' --compact

# 更新 description
python3 scripts/atlassian_rest_fallback.py jira-update-description BDPIX-1705 --description-file /tmp/new-description.md
```

## 环境变量配置

如果要使用 REST fallback，需要先配置环境变量。

### Jira

- `JIRA_BASE_URL`
- `JIRA_URL`（别名，适合 on-prem 配置）
- `JIRA_USERNAME`（bearer 模式可选）
- `JIRA_TOKEN` 或 `JIRA_PASSWORD`
- `JIRA_PERSONAL_TOKEN`（别名）
- `JIRA_AUTH_MODE=auto|basic|bearer`
- `JIRA_API_PATH`（默认 `/rest/api/2`）

### Confluence

- `CONFLUENCE_BASE_URL`
- `CONFLUENCE_URL`（别名，适合 on-prem 配置）
- `CONFLUENCE_URLS` / `CONFLUENCE_BASE_URLS`（逗号分隔，多实例）
- `CONFLUENCE_URL_2`、`CONFLUENCE_URL_3` ...（可选编号别名）
- `CONFLUENCE_USERNAME`（bearer 模式可选）
- `CONFLUENCE_TOKEN` 或 `CONFLUENCE_PASSWORD`
- `CONFLUENCE_PERSONAL_TOKEN`（别名）
- `CONFLUENCE_AUTH_MODE=auto|basic|bearer`
- `CONFLUENCE_API_PATH`（默认 `/rest/api`）

如果没有单独配置 Confluence 认证，脚本会尽量复用 Jira 的认证信息。

### on-prem + Personal Access Token 的最小配置

如果你们内网用的是本地部署 Jira / Confluence，并且认证方式是 Personal Access Token，通常可以直接这样配：

```bash
export JIRA_URL="https://jira.your-company.com"
export JIRA_PERSONAL_TOKEN="your_personal_access_token"

export CONFLUENCE_URL="https://confluence.your-company.com"
export CONFLUENCE_PERSONAL_TOKEN="your_personal_access_token"
```

在 `auto` 模式下，如果只提供 token / personal token，fallback helper 会自动按 **Bearer** 方式处理。

### 多个 Confluence 的推荐配置

如果你们内网同时存在多个 Confluence，比如：

- `https://inside-docupedia.bosch.com/confluence`
- `https://inside-docupedia.bosch.com/confluence2`

推荐这样配置：

```bash
export CONFLUENCE_URLS="https://inside-docupedia.bosch.com/confluence,https://inside-docupedia.bosch.com/confluence2"
export CONFLUENCE_PERSONAL_TOKEN="your_personal_access_token"
```

这样 `confluence-search` 会自动对所有已配置实例做联合搜索，并在结果里附带 `source_base_url`。

## 推荐的本地配置方式

建议不要把这些凭据写进项目仓库。

推荐做法：

```bash
cat > ~/.atlassian-rest-env <<'EOF'
export JIRA_URL="https://jira.your-company.com"
export JIRA_PERSONAL_TOKEN="your_personal_access_token"

export CONFLUENCE_URLS="https://inside-docupedia.bosch.com/confluence,https://inside-docupedia.bosch.com/confluence2"
export CONFLUENCE_PERSONAL_TOKEN="your_personal_access_token"
EOF
```

使用前：

```bash
source ~/.atlassian-rest-env
```

## 输出结果

更新成功后，期望输出类似：

```markdown
已更新 `BDPIX-1705` 的 description。

参考文档：
- <Confluence page 1>
- <Confluence page 2>
```

如果没有找到可用的 Confluence 文档，也会明确说明。

## 适用场景

推荐用于：
- 季度 task description 补全
- Open Item / project task description 整理
- operational / platform / integration / POC / security enhancement 类 ticket

## 不适用场景

不建议用于：
- 只需要改 1 行 description 的超小改动
- 需要同时更新 title / comment / status 的复合操作
- 内容完全未知、且 Jira / Confluence 上下文都很弱的 ticket

## 文件结构

```text
jira-description-updater/
├── README.md
├── SKILL.md
└── scripts/
    └── atlassian_rest_fallback.py
```
