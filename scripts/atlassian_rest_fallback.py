#!/usr/bin/env python3
"""REST fallback helper for jira-description-updater skill.

This script is intentionally small and dependency-light. It provides the core
REST operations needed when mcp-atlassian tools are unavailable:

- Read Jira issue details
- Search Jira issues by JQL
- Update Jira issue description
- Search Confluence pages by text or raw CQL

Authentication supports either:
- Basic auth with username + token/password
- Bearer token auth
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_JIRA_API_PATH = "/rest/api/2"
DEFAULT_CONFLUENCE_API_PATH = "/rest/api"


def _first_env(*names: str) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def _trim_trailing_slash(value: str) -> str:
    return value[:-1] if value.endswith("/") else value


def _read_description(args: argparse.Namespace) -> str:
    if args.description is not None:
        return args.description
    if args.description_file:
        with open(args.description_file, "r", encoding="utf-8") as handle:
            return handle.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit(
        "Description input required: use --description, --description-file, or stdin."
    )


def _build_basic_auth(username: str, password: str) -> str:
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


@dataclass
class ServiceConfig:
    base_url: str
    api_path: str
    auth_header: str


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def _resolve_auth(prefix: str) -> ServiceConfig:
    base_url = _first_env(f"{prefix}_BASE_URL", f"{prefix}_URL")
    if not base_url:
        raise SystemExit(
            f"Missing required environment variable: {prefix}_BASE_URL or {prefix}_URL"
        )

    auth_mode = _first_env(f"{prefix}_AUTH_MODE") or "auto"
    auth_mode = auth_mode.lower()
    username = _first_env(f"{prefix}_USERNAME", f"{prefix}_USER", f"{prefix}_EMAIL")
    token = _first_env(
        f"{prefix}_TOKEN",
        f"{prefix}_PERSONAL_TOKEN",
        f"{prefix}_PASSWORD",
    )
    api_path = _first_env(f"{prefix}_API_PATH") or (
        DEFAULT_JIRA_API_PATH if prefix == "JIRA" else DEFAULT_CONFLUENCE_API_PATH
    )

    if auth_mode not in {"auto", "basic", "bearer"}:
        raise SystemExit(f"Invalid {prefix}_AUTH_MODE: {auth_mode}")

    auth_header = ""
    if auth_mode == "basic":
        if not username or not token:
            raise SystemExit(
                f"{prefix}_AUTH_MODE=basic requires {prefix}_USERNAME and {prefix}_TOKEN/PASSWORD"
            )
        auth_header = _build_basic_auth(username, token)
    elif auth_mode == "bearer":
        if not token:
            raise SystemExit(
                f"{prefix}_AUTH_MODE=bearer requires {prefix}_TOKEN/PASSWORD"
            )
        auth_header = f"Bearer {token}"
    else:
        if username and token:
            auth_header = _build_basic_auth(username, token)
        elif token:
            auth_header = f"Bearer {token}"
        else:
            raise SystemExit(
                f"Unable to resolve auth for {prefix}. Set {prefix}_USERNAME + {prefix}_TOKEN/PASSWORD or {prefix}_TOKEN for bearer auth."
            )

    return ServiceConfig(
        base_url=_trim_trailing_slash(base_url),
        api_path=api_path if api_path.startswith("/") else f"/{api_path}",
        auth_header=auth_header,
    )


def _resolve_confluence_auth() -> ServiceConfig:
    if _first_env("CONFLUENCE_BASE_URL", "CONFLUENCE_URL"):
        return _resolve_auth("CONFLUENCE")

    jira_cfg = _resolve_auth("JIRA")
    return ServiceConfig(
        base_url=jira_cfg.base_url,
        api_path=_first_env("CONFLUENCE_API_PATH") or DEFAULT_CONFLUENCE_API_PATH,
        auth_header=jira_cfg.auth_header,
    )


def _resolve_confluence_auths() -> list[ServiceConfig]:
    explicit_urls = _first_env("CONFLUENCE_URLS", "CONFLUENCE_BASE_URLS")
    numbered_urls = []
    for key, value in os.environ.items():
        if not value:
            continue
        if re.fullmatch(r"CONFLUENCE_(?:BASE_)?URL_\d+", key):
            numbered_urls.append(value.strip())

    single_url = _first_env("CONFLUENCE_BASE_URL", "CONFLUENCE_URL")

    urls: list[str] = []
    if single_url:
        urls.append(single_url)
    if explicit_urls:
        urls.extend(part.strip() for part in explicit_urls.split(","))
    urls.extend(numbered_urls)
    urls = _dedupe_preserve_order(urls)

    if not urls:
        return [_resolve_confluence_auth()]

    auth_mode = _first_env("CONFLUENCE_AUTH_MODE") or "auto"
    username = _first_env("CONFLUENCE_USERNAME", "CONFLUENCE_USER", "CONFLUENCE_EMAIL")
    token = _first_env(
        "CONFLUENCE_TOKEN",
        "CONFLUENCE_PERSONAL_TOKEN",
        "CONFLUENCE_PASSWORD",
    )
    api_path = _first_env("CONFLUENCE_API_PATH") or DEFAULT_CONFLUENCE_API_PATH

    if not token and not username:
        # Reuse Jira auth when no dedicated Confluence auth exists.
        jira_cfg = _resolve_auth("JIRA")
        return [
            ServiceConfig(
                base_url=_trim_trailing_slash(url),
                api_path=api_path if api_path.startswith("/") else f"/{api_path}",
                auth_header=jira_cfg.auth_header,
            )
            for url in urls
        ]

    original_env_url = os.environ.get("CONFLUENCE_URL")
    original_env_base_url = os.environ.get("CONFLUENCE_BASE_URL")
    configs: list[ServiceConfig] = []
    try:
        for url in urls:
            os.environ["CONFLUENCE_URL"] = url
            os.environ["CONFLUENCE_BASE_URL"] = url
            configs.append(_resolve_auth("CONFLUENCE"))
    finally:
        if original_env_url is None:
            os.environ.pop("CONFLUENCE_URL", None)
        else:
            os.environ["CONFLUENCE_URL"] = original_env_url
        if original_env_base_url is None:
            os.environ.pop("CONFLUENCE_BASE_URL", None)
        else:
            os.environ["CONFLUENCE_BASE_URL"] = original_env_base_url

    return configs


def _request_json(
    cfg: ServiceConfig,
    method: str,
    path: str,
    *,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> Any:
    url = f"{cfg.base_url}{cfg.api_path}{path}"
    if query:
        clean_query = {k: v for k, v in query.items() if v not in (None, "")}
        if clean_query:
            url = f"{url}?{urllib.parse.urlencode(clean_query, doseq=True)}"

    data = None
    headers = {
        "Accept": "application/json",
        "Authorization": cfg.auth_header,
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {"status": response.status}
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            parsed = payload
        error_obj = {
            "status": exc.code,
            "reason": exc.reason,
            "url": url,
            "error": parsed,
        }
        print(json.dumps(error_obj, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(1) from exc


def _compact_issue(issue: dict[str, Any]) -> dict[str, Any]:
    fields = issue.get("fields", {})
    return {
        "id": issue.get("id"),
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "status": (fields.get("status") or {}).get("name"),
        "assignee": (
            (fields.get("assignee") or {}).get("displayName")
            or (fields.get("assignee") or {}).get("name")
        ),
        "labels": fields.get("labels") or [],
        "issuetype": (fields.get("issuetype") or {}).get("name"),
    }


def cmd_jira_get_issue(args: argparse.Namespace) -> None:
    cfg = _resolve_auth("JIRA")
    result = _request_json(
        cfg,
        "GET",
        f"/issue/{args.issue_key}",
        query={
            "fields": args.fields,
            "expand": args.expand,
        },
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_jira_search(args: argparse.Namespace) -> None:
    cfg = _resolve_auth("JIRA")
    result = _request_json(
        cfg,
        "GET",
        "/search",
        query={
            "jql": args.jql,
            "fields": args.fields,
            "expand": args.expand,
            "startAt": args.start_at,
            "maxResults": args.limit,
        },
    )
    if args.compact:
        compact = {
            "total": result.get("total"),
            "startAt": result.get("startAt"),
            "maxResults": result.get("maxResults"),
            "issues": [_compact_issue(issue) for issue in result.get("issues", [])],
        }
        print(json.dumps(compact, ensure_ascii=False, indent=2))
        return
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_jira_update_description(args: argparse.Namespace) -> None:
    cfg = _resolve_auth("JIRA")
    description = _read_description(args)
    result = _request_json(
        cfg,
        "PUT",
        f"/issue/{args.issue_key}",
        body={"fields": {"description": description}},
    )
    print(
        json.dumps(
            {"status": "ok", "issue_key": args.issue_key, "result": result},
            ensure_ascii=False,
            indent=2,
        )
    )


def _looks_like_cql(query: str) -> bool:
    lowered = query.lower()
    return any(
        token in lowered
        for token in (
            "type=",
            "space=",
            "title~",
            "text~",
            "siteSearch",
            "lastmodified",
            "label=",
        )
    )


def _build_cql(query: str) -> str:
    escaped = query.replace('"', '\\"')
    if _looks_like_cql(query):
        return query
    return f'type=page AND text ~ "{escaped}"'


def _build_page_url(result: dict[str, Any], cfg: ServiceConfig) -> str | None:
    links = result.get("_links") or {}
    webui = links.get("webui") or links.get("tinyui")
    base = links.get("base") or cfg.base_url
    if webui:
        if webui.startswith("http://") or webui.startswith("https://"):
            return webui
        return f"{_trim_trailing_slash(base)}{webui}"
    return None


def _compact_confluence_item(
    item: dict[str, Any], cfg: ServiceConfig
) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "title": item.get("title"),
        "type": item.get("type"),
        "space": ((item.get("space") or {}).get("key")),
        "url": _build_page_url(item, cfg),
        "source_base_url": cfg.base_url,
    }


def _parse_page_id_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    if "pageId" in query and query["pageId"]:
        return query["pageId"][0]
    match = re.search(r"/pages/(\d+)/", parsed.path)
    if match:
        return match.group(1)
    raise SystemExit("Could not extract Confluence page id from URL")


def _config_matches_url(cfg: ServiceConfig, url: str) -> bool:
    return _trim_trailing_slash(url).startswith(_trim_trailing_slash(cfg.base_url))


def cmd_confluence_get_page(args: argparse.Namespace) -> None:
    page_id = args.page_id or _parse_page_id_from_url(args.url)
    configs = _resolve_confluence_auths()

    if args.url:
        matching = [cfg for cfg in configs if _config_matches_url(cfg, args.url)]
        if matching:
            configs = matching

    last_error: SystemExit | None = None
    for cfg in configs:
        try:
            result = _request_json(
                cfg,
                "GET",
                f"/content/{page_id}",
                query={
                    "expand": args.expand,
                },
            )
            if args.compact:
                compact = _compact_confluence_item(result, cfg)
                compact["body_storage"] = (
                    (((result.get("body") or {}).get("storage") or {}).get("value"))
                    if args.include_body
                    else None
                )
                print(json.dumps(compact, ensure_ascii=False, indent=2))
                return
            result["source_base_url"] = cfg.base_url
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        except SystemExit as exc:
            last_error = exc
            continue

    if last_error is not None:
        raise last_error
    raise SystemExit("Unable to fetch Confluence page")


def cmd_confluence_search(args: argparse.Namespace) -> None:
    configs = _resolve_confluence_auths()
    cql = args.query if args.raw_cql else _build_cql(args.query)
    merged_results: list[dict[str, Any]] = []
    seen_keys: set[str] = set()

    for cfg in configs:
        result = _request_json(
            cfg,
            "GET",
            "/content/search",
            query={
                "cql": cql,
                "limit": args.limit,
                "expand": "space,version",
            },
        )

        for item in result.get("results", []):
            compact_item = _compact_confluence_item(item, cfg)
            dedupe_key = (
                compact_item.get("url") or f"{cfg.base_url}:{compact_item.get('id')}"
            )
            if dedupe_key in seen_keys:
                continue
            seen_keys.add(dedupe_key)
            merged_results.append(compact_item)

    if args.compact:
        print(
            json.dumps(
                {
                    "results": merged_results,
                    "size": len(merged_results),
                    "instances_searched": [cfg.base_url for cfg in configs],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print(
        json.dumps(
            {
                "results": merged_results,
                "size": len(merged_results),
                "instances_searched": [cfg.base_url for cfg in configs],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Atlassian REST fallback helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    jira_get = subparsers.add_parser("jira-get-issue", help="Get Jira issue details")
    jira_get.add_argument("issue_key")
    jira_get.add_argument("--fields", default="*all")
    jira_get.add_argument("--expand", default="")
    jira_get.set_defaults(func=cmd_jira_get_issue)

    jira_search = subparsers.add_parser(
        "jira-search", help="Search Jira issues with JQL"
    )
    jira_search.add_argument("--jql", required=True)
    jira_search.add_argument(
        "--fields", default="summary,description,status,assignee,labels"
    )
    jira_search.add_argument("--expand", default="")
    jira_search.add_argument("--start-at", type=int, default=0)
    jira_search.add_argument("--limit", type=int, default=10)
    jira_search.add_argument(
        "--compact", action="store_true", help="Return a reduced issue structure"
    )
    jira_search.set_defaults(func=cmd_jira_search)

    jira_update = subparsers.add_parser(
        "jira-update-description", help="Update Jira issue description"
    )
    jira_update.add_argument("issue_key")
    jira_update.add_argument("--description")
    jira_update.add_argument("--description-file")
    jira_update.set_defaults(func=cmd_jira_update_description)

    conf_search = subparsers.add_parser(
        "confluence-search", help="Search Confluence pages"
    )
    conf_search.add_argument("--query", required=True)
    conf_search.add_argument("--limit", type=int, default=10)
    conf_search.add_argument(
        "--raw-cql", action="store_true", help="Treat --query as raw CQL"
    )
    conf_search.add_argument(
        "--compact", action="store_true", help="Return reduced page metadata"
    )
    conf_search.set_defaults(func=cmd_confluence_search)

    conf_get = subparsers.add_parser(
        "confluence-get-page", help="Get Confluence page by id or URL"
    )
    conf_get.add_argument("page_id", nargs="?")
    conf_get.add_argument("--url")
    conf_get.add_argument("--expand", default="space,version,body.storage")
    conf_get.add_argument("--compact", action="store_true")
    conf_get.add_argument(
        "--include-body",
        action="store_true",
        help="Include body.storage content in compact mode",
    )
    conf_get.set_defaults(func=cmd_confluence_get_page)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
