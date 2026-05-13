---
name: bosch-procedure-documentation
description: Use when creating, rewriting, migrating, standardizing, or adding images/attachments to Bosch internal Confluence documents in PIX, especially when preserving Confluence macros and editor compatibility matters.
---

# Bosch Procedure Documentation

Use this skill when the user wants to create, rewrite, migrate, or standardize a Bosch internal Confluence document with the PIX procedure template.

Default template:

- Space: `PIX`
- Page: `Template - Procedure Documentation`
- Page ID: `4961265865`

## Primary Goal

Produce Bosch internal documentation that:

1. follows the PIX procedure template structure
2. preserves Confluence macros
3. uses concise, reviewable enterprise wording
4. can be published directly to Confluence

## Mandatory Rules

1. **Do not use markdown as the source of truth** when applying this template to Confluence pages.
2. Always read the template page with:
   - `convert_to_markdown=false`
3. Always update target pages with:
   - `content_format="storage"`
4. Preserve or recreate these template macros when applicable:
   - `details`
   - `status`
   - `lastmodifier-date`
   - `lastmodifier`
   - `page-labels`
   - `toc`
   - `change-history`
   - `layout`
5. If the target page was previously rewritten in markdown and macros were lost, rebuild the page from template storage content.
6. Do not invent owner, access classification, or review metadata unless the user explicitly provides it.
7. Keep wording factual and operational. Avoid marketing language.
8. **Never embed Confluence attachment images as raw HTML `<img>` that points to `/download/attachments/...` or `inside-docupedia.../download/attachments/...`.** This can make the page view appear updated while the Confluence editor crashes with a System Error.
9. Treat image insertion as a high-risk storage update. If editor compatibility cannot be verified immediately, upload the files as attachments and link/reference them textually instead of embedding them in the page body.

## Confluence Images And Attachments

When adding images to an existing Confluence page:

1. Prefer official source links or page attachments with clear source attribution.
2. Upload images as attachments first; verify the attachment list before touching page body storage.
3. Do not insert SVG attachments into the page body unless the target Confluence instance is known to render and edit SVG safely. Prefer PNG/JPEG for inline display.
4. Do not use raw HTML `<img>` for internal Confluence attachments. Do not use absolute or relative `download/attachments` URLs in page storage.
5. Do not assume that `confluence_update_page` success means the page is healthy. A page can save successfully but fail when opened in the editor.
6. For production pages, make the smallest possible image change, then verify both:
   - the page can be read back in storage format
   - the page can still be opened in Confluence Edit mode
7. If Edit mode fails after an image update, immediately restore the last known editable storage version before attempting another image strategy.

Safe alternatives when inline image rendering is uncertain:

- add an attachment and include a normal text link to it
- add a source URL in `References`
- ask the user to insert the uploaded attachment through the Confluence editor UI
- test the exact storage markup on a disposable child page before updating the production page

## Supported Tasks

- create a new Bosch internal procedure page from the PIX template
- retrofit an existing Confluence page to the PIX template
- migrate freeform content into the template structure
- fill template sections based on source material
- add images or attachments to an existing Confluence documentation page
- preserve and restore macros in a broken template-based page

## Standard Workflow

### A. Clarify scope

Before writing, determine:

- target page URL or page ID
- whether this is a new page or an existing page update
- source material to transform
- any required metadata values:
  - Scope
  - Responsible
  - Access Level
  - Last Review handling
  - Labels
  - Document status

If metadata is missing, ask for it. If the user wants a quick draft, leave template placeholders in place rather than fabricating values.

### B. Read source and template

1. Read the PIX template page in **storage** format.
2. Read the target page in **storage** format if it already exists.
3. Read any source page or supporting content in markdown or storage as needed.

### C. Build from template-first, not markdown-first

When updating a page:

1. start from the template's storage structure
2. keep the template macro layout intact
3. replace placeholder body content with document-specific content
4. keep revision history macro intact
5. keep TOC and metadata macros intact

### D. Publish safely

When writing back to Confluence:

- use `content_format="storage"`
- include a clear `version_comment`
- add useful page labels when available
- for image/attachment changes, keep a known-good historical version ready for rollback
- after publishing image/attachment changes, verify the page still opens in Edit mode before claiming completion

## Required Template Structure

Every page should retain this high-level structure unless the user explicitly requests otherwise:

1. metadata block inside the template details macro
2. `Description & Purpose`
3. `Details`
4. `Others`
5. `References`
6. `Revision History`

## Metadata Guidance

### Scope

One concise sentence describing what the document covers.

### Responsible

Use the actual owner if provided. Otherwise keep template placeholder behavior.

### Access Level

Preserve the template's status macros unless the user specifies the actual classification.

### Last Review

Prefer the template's automatic last-modifier macros.

### Labels

Use Confluence page labels in addition to visible content when possible.

### Document status

Preserve the status macros. Set the actual intended state only when the user specifies it or clearly implies it.

## Writing Style

- concise
- structured
- audit-friendly
- specific
- neutral tone

Prefer:

- short explanatory paragraphs
- bullet lists for scope and navigation
- tables for coverage, ownership, or comparisons
- explicit links to related Bosch internal pages

Avoid:

- vague claims
- promotional wording
- unexplained abbreviations when the audience may not know them
- removing useful dynamic template elements

## Retrofit Pattern For Existing Pages

When the user says "apply the template" to an existing page, do this:

1. read template page storage
2. read target page content
3. extract the target page's actual business content
4. rebuild the target page on top of the template storage structure
5. insert the extracted content into the proper template sections
6. update page labels if appropriate
7. verify that storage content still contains the expected macros

## Verification Checklist

Before finishing, confirm:

- target page uses template structure
- macro-bearing sections still exist in storage content
- content is mapped into the correct sections
- placeholders were preserved where information is missing
- references and links still work
- version comment explains the update
- for image changes, no raw internal `download/attachments` image URLs were written into storage
- for image changes, the user or browser verification confirms Edit mode still opens

## Example Triggers

- "Use the PIX procedure template for this Confluence page"
- "Rewrite this Bosch internal doc with the standard template"
- "Copy the Procedure Documentation template and fill in the content"
- "Why are the Confluence macros missing after update?"

## Response Pattern

Prefer concise execution updates such as:

- "Reading template and target page storage content."
- "Rebuilding the page from template storage so macros are preserved."
- "Updating Confluence with storage format and labels."
- "Uploading image files as attachments first; not embedding them until Edit mode can be verified."

When done, return:

- page URL
- whether macros were preserved/restored
- any remaining placeholders needing user input
