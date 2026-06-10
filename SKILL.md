---
name: bosch-procedure-documentation
description: Create, rewrite, retrofit, or standardize Bosch internal Confluence procedure documents using the BD/ISA-CN template in PIX space. Preserves Confluence macros by working in storage format. Use when user mentions Confluence procedure docs, templates, macros, storage format, PIX, or Bosch internal documentation that should follow the standard procedure template.
---

# Bosch Procedure Documentation

## Default Template

- Space: `PIX`
- Page: `Template - Procedure Documentation`
- Page ID: `4961265865`

## Quick Start

### New page from template

1. Read template page in **storage** format (`convert_to_markdown=false`)
2. Read any source materials
3. Build content following the [Required Template Structure](#required-template-structure)
4. Create page with `content_format="storage"`, include `version_comment`

### Retrofit existing page

1. Read template page in **storage** format
2. Read target page in **storage** format
3. Extract the target page's actual business content
4. Rebuild the page on top of the template's storage structure
5. Insert extracted content into proper template sections
6. Update with `content_format="storage"` and useful page labels

## Essential Rules

1. **Always** read template pages with `convert_to_markdown=false` and write with `content_format="storage"`. Markdown corrupts macros.
2. Preserve these macros when present: `details`, `status`, `lastmodifier-date`, `lastmodifier`, `page-labels`, `toc`, `change-history`, `layout`.
3. Never embed attachment images as raw `<img>` pointing to `/download/attachments/...`. This crashes the Confluence editor.
4. Do not invent owner, access classification, or review metadata unless the user provides it.
5. Keep wording factual, operational, and audit-friendly. Avoid marketing language.

## Standard Workflow

**A. Clarify scope** — Determine: target page URL/ID, new vs existing page, source materials, metadata (Scope, Responsible, Access Level, Labels, Document status). Ask if missing.

**B. Read** — Read template and target (if exists) in **storage** format. Read supporting content as needed.

**C. Build template-first** — Start from template storage structure. Keep macros intact. Replace placeholder body content.

**D. Publish safely** — Write with `content_format="storage"`. Include `version_comment`. For image changes: keep known-good version for rollback, verify Edit mode after publishing.

## Required Template Structure

1. Metadata block inside the `details` macro
2. `Description & Purpose`
3. `Details`
4. `Others`
5. `References`
6. `Revision History`

---

See [REFERENCE.md](REFERENCE.md) for detailed guidance on:
- Image/attachment safety rules and safe alternatives
- Storage format quick reference (markdown vs storage)
- draw.io macro handling (Server/DC) with correct XML example
- MCP upload_attachment known bug fix (mcp-atlassian v0.21.1)
- Bosch key reference pages
- Metadata guidance (Scope, Responsible, Access Level, etc.)
- Writing style guide
- Retrofit pattern with checklist
- Full verification checklist
- Response pattern
