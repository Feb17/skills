# Bosch Procedure Documentation — Reference

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

## Confluence Storage Format Quick Reference

| Scenario | Format | Notes |
|----------|--------|-------|
| Plain page (no macros) | `content_format="markdown"` | Use markdown for simple content |
| Pages with macros (e.g. `auitabs`, `drawio`, `details`) | `content_format="storage"` | Must use storage format; macros get corrupted by markdown escaping |
| Macros referencing attachments | storage | Macro parameters reference attachment filenames |

## Confluence Macros — Special Cases

### draw.io Macro (Server/DC)

**Core principle**: draw.io diagram data **must** be uploaded as a page attachment. The macro references it via the `diagramName` parameter. Inline XML is not supported.

**Correct approach (storage format):**

```xml
<ac:structured-macro ac:name="drawio" ac:schema-version="1">
  <ac:parameter ac:name="diagramName">monitoring-architecture.drawio</ac:parameter>
  <ac:parameter ac:name="simple">0</ac:parameter>
  <ac:parameter ac:name="zoom">1</ac:parameter>
  <ac:parameter ac:name="lbox">1</ac:parameter>
  <ac:parameter ac:name="revision">1</ac:parameter>
  <ac:parameter ac:name="pageSize">false</ac:parameter>
  <ac:parameter ac:name="links"/>
  <ac:parameter ac:name="tbstyle"/>
</ac:structured-macro>
```

**Procedure:**

1. Generate a `.drawio` file using the draw.io desktop app (or CLI)
2. Upload the `.drawio` file as an attachment to the Confluence page
3. Insert the macro above into the page's storage content; `diagramName` points to the attachment filename
4. Some Confluence instances also require a `.drawio.png` preview image (generate via File → Export as → PNG with Embed Diagram in the draw.io editor)

**Common mistakes:**

| Incorrect usage | Symptom |
|-----------------|---------|
| `<ac:parameter ac:name="name">file.drawio</ac:parameter>` | "Diagram attachment access error" |
| `<ac:parameter ac:name="xml"><![CDATA[...]]></ac:parameter>` | Diagram does not render at all (plugin does not support inline XML) |

### Known Bug — MCP upload_attachment (mcp-atlassian v0.21.1)

**Location**: `~/.config/opencode/mcp-servers/node_modules/mcp-atlassian/dist/atlassian/apis/confluence/attachments.py`

**Issues (two):**

1. Uses `"nocheck"` as the `X-Atlassian-Token` value → **should be `"no-check"`**
2. Server/DC instance uses `put()` for upload HTTP method → **should be `post()`**

**Fix**: Edit the corresponding lines in `attachments.py`, then restart the MCP process.

## Bosch Confluence Key References

Commonly referenced Bosch Confluence pages related to this template (documented in the SZH5 ME Operation project):

| Page | Description |
|------|-------------|
| `4.4.0 Mandatory Documentation in Runbooks` | 10 document topics required by OSC |
| `4.4 Runbooks` | Runbook is the KMS — includes guides, troubleshooting, and FAQs |
| `ITOM_Template_V3.1` | ITOM template (product-level operations manual) |

## Supported Tasks

- create a new Bosch internal procedure page from the BD/ISA-CN template
- retrofit an existing Confluence page to the PIX template
- migrate freeform content into the template structure
- fill template sections based on source material
- add images or attachments to an existing Confluence documentation page
- preserve and restore macros in a broken template-based page

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

When the user says "apply the template" to an existing page:

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
