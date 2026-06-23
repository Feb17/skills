---
name: bosch-brand-style-guide
description: Applies Bosch corporate design rules when generating or reviewing HTML/CSS, layout, typography, color, imagery, logo use, the top supergraphic gradient ribbon, full-width header patterns (as on bosch.com), and accessibility for one-pagers and web UI. Use when the user asks for a design review, UI/UX feedback, brand compliance check, Bosch brand guidelines, corporate design, one-pagers, landing pages, or Bosch-branded collateral in any project.
---

# Bosch brand style guide (one-pager HTML/CSS)

## Instructions

Act as an expert front-end developer and brand designer. When **creating** or **reviewing** design (HTML/CSS, layout, components, visuals, or copy tone), apply the Bosch brand rules below unless the user specifies otherwise.

For **reviews**, call out violations with concrete fixes (e.g. wrong colors, spacing off the 8px grid, Bosch Red overuse, weak contrast, logo clear space, missing or misplaced **supergraphic** / header ribbon, generic imagery or `alt` text).

## Dos and don'ts

| Do | Don't |
| :--- | :--- |
| Use a clean, grid-based layout. | Do not use shadows, arbitrary decorative UI gradients, or 3D effects. |
| Include the **official Bosch supergraphic** (top gradient strip) at the top; keep all main page content **below** that header band (see below). | Omit the supergraphic or place body content above it (visually or in DOM order). |
| Use ample white space with the 8px spacing system. | Do not use colors outside the official palette. |
| Use "Bosch Office Sans" or the specified fallbacks. | Do not use Bosch Red (`--bosch-red`) for anything other than the logo or a single primary CTA. |
| Use authentic, human-centric imagery. | Do not use purely decorative or abstract shapes. |
| Meet WCAG AA text contrast. | Do not place content or other elements inside the logo clear space. |

Load **Bosch Office Sans** only according to your organization’s font licensing and delivery policy (CDN, internal host, or local files).

---

## CSS setup — variables and base styles

Start from this foundation:

```css
:root {
  /* Color palette */
  --bosch-red: #e0000a;
  --bosch-purple: #54003c;
  --bosch-blue: #007bc0;
  --bosch-green: #6dbf24;
  --color-text: #000000;
  --color-background: #ffffff;
  --color-background-alt: #f2f2f2;
  --color-border: #cccccc;

  /* Typography */
  --font-primary: "Bosch Office Sans", "Helvetica Neue", helvetica, arial, sans-serif;
  --font-weight-regular: 400;
  --font-weight-bold: 700;

  /* Spacing unit (8px grid) */
  --space-unit: 8px;
}

body {
  font-family: var(--font-primary);
  font-weight: var(--font-weight-regular);
  color: var(--color-text);
  background-color: var(--color-background);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

---

## Layout and spacing

Use **integer multiples** of `--space-unit` for margins, padding, and gaps (not arbitrary pixel values).

- **Small gap:** `calc(var(--space-unit) * 2)` (16px)
- **Medium gap:** `calc(var(--space-unit) * 4)` (32px)
- **Large gap:** `calc(var(--space-unit) * 8)` (64px)

---

## Typography

- **Headings (`h1`–`h3`):** `font-family: var(--font-primary);` and `font-weight: var(--font-weight-bold);`
- **Body (`p`, `li`):** `font-family: var(--font-primary);` and `font-weight: var(--font-weight-regular);`

---

## Components

### Buttons

- **Primary (CTA):** Solid fill. Prefer `--bosch-blue` or `--bosch-purple`. Reserve `--bosch-red` for at most one critical primary CTA per view.

```css
.btn-primary {
  background-color: var(--bosch-blue);
  color: var(--color-background);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border: none;
  font-weight: var(--font-weight-bold);
  text-decoration: none;
  display: inline-block;
}
```

- **Secondary:** Outline style.

```css
.btn-secondary {
  background-color: transparent;
  color: var(--bosch-blue);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border: 2px solid var(--bosch-blue);
  font-weight: var(--font-weight-bold);
}
```

### Form inputs

Minimal, clear fields; keep focus visible and on-brand.

```css
.form-input {
  font-family: var(--font-primary);
  padding: calc(var(--space-unit) * 2);
  border: 1px solid var(--color-border);
  width: 100%;
}

.form-input:focus {
  outline: 2px solid var(--bosch-blue);
  border-color: transparent;
}
```

---

## Logo

- **Placement:** Header, **top-left** on a white (or very light) bar—matches public Bosch web properties: supergraphic → white header row → logo and navigation.
- **Clear space:** No text or UI may intrude; minimum clear space equals the height of the “B” in the logo.
- **Variant:** Full-color Bosch logo (armature + **BOSCH** wordmark) on white or light grey (`--color-background-alt`).
- **Markup pattern (production-style):** Wrap the logo in a home link for accessibility and UX: `<a class="header-brand-logo" href="/" aria-label="Bosch home">` … `</a>`.
- **Inline SVG:** Always use the official SVG below verbatim. Do NOT substitute simplified shapes, `<circle>` approximations, or `<text>` elements. The wordmark uses `#ed0007`; the armature uses `#000000`.
- **Compact header bar (bosch.com–style):** Logo link as flex container, `height: 24px` on the inner `svg` so the mark scales correctly to the white bar height.

### Official Bosch logo SVG — always use this exact markup, never recreate

```html
<a class="header-brand-logo" href="/" aria-label="Bosch home">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 433 97" aria-hidden="true" focusable="false">
    <g fill="none">
      <g fill="#ed0007" fill-rule="evenodd">
        <path d="M185.2,46.88a13.77,13.77,0,0,0,8.8-13c0-11.7-8.3-17.5-19.7-17.5H144.4V80h32.5c10,0,19.8-7,19.8-17.7C196.7,49.58,185.2,47,185.2,46.88ZM160,29.58h11.6a5.66,5.66,0,0,1,6,5.31q0,.34,0,.69a5.93,5.93,0,0,1-6,5.81H159.9Zm11.7,37.1H160.1V54.18h11.3c5.7,0,8.4,2.5,8.4,6.2C179.8,65,176.4,66.68,171.7,66.68Z"></path>
        <path d="M231.1,14.78c-18.4,0-29.2,14.7-29.2,33.3s10.8,33.3,29.2,33.3,29.2-14.6,29.2-33.3S249.6,14.78,231.1,14.78Zm0,51.4c-9,0-13.5-8.1-13.5-18.1s4.5-18,13.5-18,13.6,8.1,13.6,18C244.7,58.18,240.1,66.18,231.1,66.18Z"></path>
        <path d="M294.2,41.38l-2.2-.5c-5.4-1.1-9.7-2.5-9.7-6.4,0-4.2,4.1-5.9,7.7-5.9a17.86,17.86,0,0,1,13,5.9l9.9-9.8c-4.5-5.1-11.8-10-23.2-10-13.4,0-23.6,7.5-23.6,20,0,11.4,8.2,17,18.2,19.1l2.2.5c8.3,1.7,11.4,3,11.4,7,0,3.8-3.4,6.3-8.6,6.3-6.2,0-11.8-2.7-16.1-8.2l-10.1,10c5.6,6.7,12.7,11.9,26.4,11.9,11.9,0,24.6-6.8,24.6-20.7C314.3,46.08,303.3,43.28,294.2,41.38Z"></path>
        <path d="M349.7,66.18c-7,0-14.3-5.8-14.3-18.5,0-11.3,6.8-17.6,13.9-17.6,5.6,0,8.9,2.6,11.5,7.1l12.8-8.5c-6.4-9.7-14-13.8-24.5-13.8-19.2,0-29.6,14.9-29.6,32.9,0,18.9,11.5,33.7,29.4,33.7,12.6,0,18.6-4.4,25.1-13.8L361.1,59C358.5,63.18,355.7,66.18,349.7,66.18Z"></path>
        <polygon points="416.3 16.38 416.3 39.78 397 39.78 397 16.38 380.3 16.38 380.3 79.98 397 79.98 397 54.88 416.3 54.88 416.3 79.98 433 79.98 433 16.38 416.3 16.38"></polygon>
      </g>
      <g fill="#000000">
        <path d="M48.2.18a48.2,48.2,0,1,0,48.2,48.2A48.2,48.2,0,0,0,48.2.18Zm0,91.9a43.7,43.7,0,1,1,43.7-43.7,43.71,43.71,0,0,1-43.7,43.7Z"></path>
        <path d="M68.1,18.28H64.8v16.5H31.7V18.28H28.3a36.06,36.06,0,0,0,0,60.2h3.4V62H64.8v16.5h3.3a36.05,36.05,0,0,0,0-60.2ZM27.1,72A31.59,31.59,0,0,1,24.47,27.4a32.51,32.51,0,0,1,2.63-2.62Zm37.7-14.6H31.7V39.28H64.8Zm4.5,14.5v-10h0V34.78h0v-10a31.65,31.65,0,0,1,2.39,44.71A33.68,33.68,0,0,1,69.3,71.88Z"></path>
      </g>
    </g>
  </svg>
</a>
```

```css
.header-brand-logo {
  display: flex;
  align-items: center;
  height: 100%;
  text-decoration: none;
  flex-shrink: 0;
}

.header-brand-logo svg {
  height: 24px;
  width: auto;
}
```

---

## Top masthead gradient ribbon (supergraphic)

The thin **full-width multicolor bar** at the very top of Bosch sites is the **supergraphic** (official Bosch SVG with gradient fills—not a hand-authored CSS `linear-gradient`). Treat it as **brand artwork**.

**Visual stack (reference: public Bosch homepage)**

1. **Supergraphic** — 6px-tall strip, edge-to-edge.
2. **White header row** — logo left; primary nav / utilities right; flat UI (no shadows on the bar).
3. **Page body** — hero and all other content **below** this header region.

**All primary page content** should sit **below** the header block in DOM and visually—nothing scrolls “above” the supergraphic except what lives inside the fixed header area.

### Official supergraphic data URI — always use this, never hand-author a gradient

```
data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHdpZHRoPSI3MjAiIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgNzIwIDMwMCI+PHN0eWxlPi5zdDd7ZmlsbDojOTQxYjFlfTwvc3R5bGU+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEuNTUgLTMuMykiPjxsaW5lYXJHcmFkaWVudCBpZD0iU1ZHSURfMV8iIHgxPSIxMTguOTgiIHgyPSI4NDIuMDgiIHkxPSItMzIuNjYzIiB5Mj0iLTMyLjY2MyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxIDAgMCAtMSAtMTE4Ljk4IDEyMC41NCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM5NTIzMzEiLz48c3RvcCBvZmZzZXQ9Ii4wMzYiIHN0b3AtY29sb3I9IiM5MjFDMUQiLz48c3RvcCBvZmZzZXQ9Ii4wODUiIHN0b3AtY29sb3I9IiNCMDI3MzkiLz48c3RvcCBvZmZzZXQ9Ii4xMjQiIHN0b3AtY29sb3I9IiNBRDFGMjQiLz48c3RvcCBvZmZzZXQ9Ii4xNTEiIHN0b3AtY29sb3I9IiNDNzIwMjYiLz48c3RvcCBvZmZzZXQ9Ii4xNyIgc3RvcC1jb2xvcj0iI0Q0MjAyNyIvPjxzdG9wIG9mZnNldD0iLjE3NiIgc3RvcC1jb2xvcj0iI0NDMjQzMSIvPjxzdG9wIG9mZnNldD0iLjE4OSIgc3RvcC1jb2xvcj0iI0I3MkI0QyIvPjxzdG9wIG9mZnNldD0iLjIwNyIgc3RvcC1jb2xvcj0iIzk1MzM3MSIvPjxzdG9wIG9mZnNldD0iLjIxNCIgc3RvcC1jb2xvcj0iIzg4MzU3RiIvPjxzdG9wIG9mZnNldD0iLjI0NCIgc3RvcC1jb2xvcj0iIzg1MzY4MSIvPjxzdG9wIG9mZnNldD0iLjI2NCIgc3RvcC1jb2xvcj0iIzZGMzY4QiIvPjxzdG9wIG9mZnNldD0iLjI5MSIgc3RvcC1jb2xvcj0iIzM5NDI4RiIvPjxzdG9wIG9mZnNldD0iLjMyNCIgc3RvcC1jb2xvcj0iIzIzM0Q3RCIvPjxzdG9wIG9mZnNldD0iLjQxOCIgc3RvcC1jb2xvcj0iIzMyMkM2RiIvPjxzdG9wIG9mZnNldD0iLjQ5NCIgc3RvcC1jb2xvcj0iIzJBMzg4NSIvPjxzdG9wIG9mZnNldD0iLjU1OCIgc3RvcC1jb2xvcj0iIzFENjJBMSIvPjxzdG9wIG9mZnNldD0iLjU3IiBzdG9wLWNvbG9yPSIjMjc2Q0E1Ii8+PHN0b3Agb2Zmc2V0PSIuNjEiIHN0b3AtY29sb3I9IiM0MzhFQjMiLz48c3RvcCBvZmZzZXQ9Ii42NCIgc3RvcC1jb2xvcj0iIzU1QTVCQyIvPjxzdG9wIG9mZnNldD0iLjY1NiIgc3RvcC1jb2xvcj0iIzVDQUZCRiIvPjxzdG9wIG9mZnNldD0iLjY3OCIgc3RvcC1jb2xvcj0iIzU2QUJCRCIvPjxzdG9wIG9mZnNldD0iLjcwNiIgc3RvcC1jb2xvcj0iIzQzOUZCOCIvPjxzdG9wIG9mZnNldD0iLjczNyIgc3RvcC1jb2xvcj0iIzE4OEVBRiIvPjxzdG9wIG9mZnNldD0iLjc0MyIgc3RvcC1jb2xvcj0iIzAzOEJBRSIvPjxzdG9wIG9mZnNldD0iLjc5IiBzdG9wLWNvbG9yPSIjMDY5MjkyIi8+PHN0b3Agb2Zmc2V0PSIuODg3IiBzdG9wLWNvbG9yPSIjMDVBMTRCIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMDM5MjdFIi8+PC9saW5lYXJHcmFkaWVudD48cGF0aCBkPSJNMCAwaDcyMy4xdjMwNi40SDB6IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzFfKSIvPjxsaW5lYXJHcmFkaWVudCBpZD0iU1ZHSURfMl8iIHgxPSIzMjUuMDgiIHgyPSIyMzUuOTgiIHkxPSItMTA5LjI2IiB5Mj0iLTEwOS4yNiIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxIDAgMCAtMSAtMTE4Ljk4IDEyMC41NCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM4OTM2ODAiLz48c3RvcCBvZmZzZXQ9Ii4zMzUiIHN0b3AtY29sb3I9IiM4OTM2ODAiLz48c3RvcCBvZmZzZXQ9Ii41MDIiIHN0b3AtY29sb3I9IiM4RDMxNkQiLz48c3RvcCBvZmZzZXQ9Ii44NCIgc3RvcC1jb2xvcj0iIzkwMjk0RCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzkwMjU0MSIvPjwvbGluZWFyR3JhZGllbnQ+PHBhdGggZD0iTTE3NS4xIDE1My4yIDExNyAzMDYuNGg4OS4xeiIgc3R5bGU9ImZpbGw6dXJsKCNTVkdJRF8yXykiLz48bGluZWFyR3JhZGllbnQgaWQ9IlNWR0lEXzNfIiB4MT0iNDc4LjkzIiB4Mj0iNDQ2LjU1IiB5MT0iMTIwLjI0IiB5Mj0iLTgyLjI4NCIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxIDAgMCAtMSAtMTE4Ljk4IDEyMC41NCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiMzMjJDNkYiLz48c3RvcCBvZmZzZXQ9Ii4yNDMiIHN0b3AtY29sb3I9IiMzMjJDNkYiLz48c3RvcCBvZmZzZXQ9Ii40NiIgc3RvcC1jb2xvcj0iIzMwMkY3MiIvPjxzdG9wIG9mZnNldD0iLjcxNiIgc3RvcC1jb2xvcj0iIzJBM0E3RSIvPjxzdG9wIG9mZnNldD0iLjk5IiBzdG9wLWNvbG9yPSIjMTU0QTkzIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMTM0Qjk0Ii8+PC9saW5lYXJHcmFkaWVudD48cGF0aCBkPSJtMjg4LjQgMTUzLjIgMjIuMyAxNTMuMmg0Ny40VjBoLTQ1LjJ6IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzNfKSIvPjxsaW5lYXJHcmFkaWVudCBpZD0iU1ZHSURfNF8iIHgxPSIyOTQuMDgiIHgyPSIzNzIuODgiIHkxPSItMzIuNjYzIiB5Mj0iLTMyLjY2MyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxIDAgMCAtMSAtMTE4Ljk4IDEyMC41NCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM2RjM3OEQiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMzQTQyOTEiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGQ9Im0xNzUuMSAxNTMuMiAzMSAxNTMuMiA0Ny44LTE1My4yTDIwOS40IDB6IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzRfKSIvPjxsaW5lYXJHcmFkaWVudCBpZD0iU1ZHSURfNV8iIHgxPSI0MzEuODgiIHgyPSIzMjUuMDgiIHkxPSItMzIuNjYzIiB5Mj0iLTMyLjY2MyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxIDAgMCAtMSAtMTE4Ljk4IDEyMC41NCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiMyMzNEN0QiLz48c3RvcCBvZmZzZXQ9Ii4yNDkiIHN0b3AtY29sb3I9IiMyOTNEN0QiLz48c3RvcCBvZmZzZXQ9Ii41NDUiIHN0b3AtY29sb3I9IiMzQTNDODAiLz48c3RvcCBvZmZzZXQ9Ii44NjIiIHN0b3AtY29sb3I9IiM1MTNCODQiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiM1RDNBODYiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGQ9Im0yNTMuOSAxNTMuMi00Ny44IDE1My4yaDEwNC42bC0yMi4zLTE1My4yTDMxMi45IDBIMjA5LjR6IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzVfKSIvPjxwYXRoIGQ9Ik0xMTYuMSAwSDU1Ljd2OTQuOGwzNC4yIDU4LjQtMzQuMiA1OC40djk0LjhIMTE3TDk1LjIgMTUzLjJ6IiBzdHlsZT0iZmlsbDojYWYyMDI0Ii8+PGxpbmVhckdyYWRpZW50IGlkPSJTVkdJRF82XyIgeDE9IjMyOS4xMSIgeDI9IjIzMi42NyIgeTE9IjQzLjkzNyIgeTI9IjQzLjkzNyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxIDAgMCAtMSAtMTE4Ljk4IDEyMC41NCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM4OTM2ODAiLz48c3RvcCBvZmZzZXQ9Ii4zMzUiIHN0b3AtY29sb3I9IiM4OTM2ODAiLz48c3RvcCBvZmZzZXQ9Ii41MDIiIHN0b3AtY29sb3I9IiM4RDMxNkQiLz48c3RvcCBvZmZzZXQ9Ii44NCIgc3RvcC1jb2xvcj0iIzkwMjk0RCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzkwMjU0MSIvPjwvbGluZWFyR3JhZGllbnQ+PHBhdGggZD0iTTE3NS4xIDE1My4yIDIwOS40IDBoLTkzLjN6IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzZfKSIvPjxwYXRoIGZpbGw9IiM5NDFiMWUiIGQ9Ik01NS43IDk0LjhWMEgweiIgY2xhc3M9InN0NyIvPjxwYXRoIGQ9Im01NS43IDIxMS42IDM0LjItNTguNC0zNC4yLTU4LjR6IiBzdHlsZT0iZmlsbDojYjEyNzM5Ii8+PHBhdGggZmlsbD0iIzk0MWIxZSIgZD0iTTU1LjcgMjExLjYgMCAzMDYuNGg1NS43eiIgY2xhc3M9InN0NyIvPjxwYXRoIGQ9Ik01NS43IDk0LjggMCAwdjMwNi40bDU1LjctOTQuOHoiIHN0eWxlPSJmaWxsOiM5NTI0MzIiLz48cGF0aCBkPSJNMTE2LjEgMCA5NS4yIDE1My4yIDExNyAzMDYuNGw1OC4xLTE1My4yeiIgc3R5bGU9ImZpbGw6I2Q0MjAyNyIvPjxsaW5lYXJHcmFkaWVudCBpZD0iU1ZHSURfN18iIHgxPSI3NDguOTYiIHgyPSI3NDguOTYiIHkxPSIxMjAuNDQiIHkyPSItMTg2LjA2IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDEgMCAwIC0xIC0xMTguOTggMTIwLjU0KSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzk0QkU1NSIvPjxzdG9wIG9mZnNldD0iLjA0NCIgc3RvcC1jb2xvcj0iIzkzQkQ1OCIvPjxzdG9wIG9mZnNldD0iLjM4OSIgc3RvcC1jb2xvcj0iIzhCQkM2QSIvPjxzdG9wIG9mZnNldD0iLjcxNSIgc3RvcC1jb2xvcj0iIzg2QkM3NSIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzg0QkM3OSIvPjwvbGluZWFyR3JhZGllbnQ+PHBhdGggZD0iTTY0MS42IDI1OS42YzEuNy0yNS40IDEwLTU0LjYgMTguOC04NS42IDEuNC01IDIuOC0xMCA0LjItMTUuMXEtMi4xLTguMjUtNC4yLTE2LjJjLTguOC0zMy4zLTE3LTY0LjctMTguOC05Mi0xLjQtMjEuMiAxLjQtMzcgOC45LTUwLjZoLTQ1LjljLTcuNSAxOC4zLTEwLjMgMjkuMS04LjkgNTAuMyAxLjcgMjcuMyAxMCA1OC43IDE4LjggOTIgMTMgNDkuMyAyOCAxMDYuMiAyMy4yIDE2NC4yaDEyLjljLTcuNi0xMi44LTEwLjQtMjcuMy05LTQ3IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzdfKSIvPjxsaW5lYXJHcmFkaWVudCBpZD0iU1ZHSURfOF8iIHgxPSI2NTMuNzYiIHgyPSI3MzMuNDkiIHkxPSIxMTcuMjkiIHkyPSItMTg0LjQ1IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDEgMCAwIC0xIC0xMTguOTggMTIwLjU0KSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzA4QTI0QiIvPjxzdG9wIG9mZnNldD0iLjE2OCIgc3RvcC1jb2xvcj0iIzBBQTE0RSIvPjxzdG9wIG9mZnNldD0iLjQwNSIgc3RvcC1jb2xvcj0iIzBCOUU1NyIvPjxzdG9wIG9mZnNldD0iLjY4MyIgc3RvcC1jb2xvcj0iIzA5OUE2NyIvPjxzdG9wIG9mZnNldD0iLjk5IiBzdG9wLWNvbG9yPSIjMDQ5NDdEIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMDQ5MzdFIi8+PC9saW5lYXJHcmFkaWVudD48cGF0aCBkPSJNNjE0LjUgMTQyLjNjLTguOC0zMy4zLTE3LTY0LjctMTguOC05Mi0xLjQtMjEuMiAxLjQtMzIgOC45LTUwLjNoLTM1LjRjNS43IDUzLjktMy44IDEwNi43LTEzLjYgMTY2LjgtNS43IDM1LTExLjcgNzEuMy0xMy4yIDEwMC42LTEuMSAyMS4xLjQgMzIuOCAxLjggMzloOTMuNWM0LjgtNTcuOS0xMC4zLTExNC44LTIzLjItMTY0LjEiIHN0eWxlPSJmaWxsOnVybCgjU1ZHSURfOF8pIi8+PHBhdGggZD0iTTY2NC42IDE1OC45Yy0xLjQgNS4xLTIuOCAxMC4xLTQuMiAxNS4xLTguOCAzMS0xNyA2MC4yLTE4LjggODUuNi0xLjQgMTkuNyAxLjQgMzQuMiA5IDQ2LjloMzNjNC4yLTUxLjgtNy4yLTEwMi4zLTE5LTE0Ny42IiBzdHlsZT0iZmlsbDojMWM5YTQ4Ii8+PGxpbmVhckdyYWRpZW50IGlkPSJTVkdJRF85XyIgeDE9IjgxMi44MyIgeDI9IjgxMi44MyIgeTE9IjEyMC41NCIgeTI9Ii0xODUuOTYiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMSAwIDAgLTEgLTExOC45OCAxMjAuNTQpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjNjlBMDYwIi8+PHN0b3Agb2Zmc2V0PSIuMDQiIHN0b3AtY29sb3I9IiM2MzlENUMiLz48c3RvcCBvZmZzZXQ9Ii4yMTkiIHN0b3AtY29sb3I9IiM0Qzk0NEYiLz48c3RvcCBvZmZzZXQ9Ii40MTgiIHN0b3AtY29sb3I9IiMzNzhFNDciLz48c3RvcCBvZmZzZXQ9Ii42NTEiIHN0b3AtY29sb3I9IiMyOThCNDQiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMyMzhBNDMiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGQ9Ik02ODAuNSAwYzEwLjcgNTUuMy0yLjUgMTEwLjQtMTUuOSAxNTguOSAxMS43IDQ1LjMgMjMuMiA5NS44IDE4LjkgMTQ3LjZoMzkuNlYweiIgc3R5bGU9ImZpbGw6dXJsKCNTVkdJRF85XykiLz48bGluZWFyR3JhZGllbnQgaWQ9IlNWR0lEXzEwXyIgeDE9IjY1Mi40NSIgeDI9IjY1Mi40NSIgeTE9IjEyMC41NCIgeTI9Ii0xODUuODYiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMSAwIDAgLTEgLTExOC45OCAxMjAuNTQpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMDVCNURDIi8+PHN0b3Agb2Zmc2V0PSIuMjIiIHN0b3AtY29sb3I9IiMwNEIwRDciLz48c3RvcCBvZmZzZXQ9Ii41MzciIHN0b3AtY29sb3I9IiMwNUE0QzkiLz48c3RvcCBvZmZzZXQ9Ii45MTIiIHN0b3AtY29sb3I9IiMwNTkxQjQiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMwNThDQUUiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGQ9Ik01NDIuMyAyNjcuNGMxLjUtMjkuNCA3LjUtNjUuNiAxMy4yLTEwMC42QzU2NS4zIDEwNi43IDU3NC44IDU0IDU2OS4xIDBoLTcwLjhjLTEuNCAxMS40LTIuOSAxOS4yLTEuOCA0MS44IDEuNSAzMS42IDcuNSA3MC41IDEzLjIgMTA4LjIgOC40IDU1LjQgMTYuNiAxMDguOCAxNS4xIDE1Ni40SDU0NGMtMS4zLTYuMi0yLjgtMTcuOS0xLjctMzkiIHN0eWxlPSJmaWxsOnVybCgjU1ZHSURfMTBfKSIvPjxwYXRoIGQ9Ik0zNzUuNyAxNTMuMiAzNTguMSAwdjMwNi40eiIgc3R5bGU9ImZpbGw6IzJhMzg4NiIvPjxsaW5lYXJHcmFkaWVudCBpZD0iU1ZHSURfMTFfIiB4MT0iNzUxLjA1IiB4Mj0iNzk2LjcxIiB5MT0iLTQuMzI4IiB5Mj0iNzcuMTM2IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDEgMCAwIC0xIC0xMTguOTggMTIwLjU0KSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzYyQjE2RSIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzg3Qjk1NyIvPjwvbGluZWFyR3JhZGllbnQ+PHBhdGggZD0iTTY0MS42IDUwLjZjMS43IDI3LjMgMTAgNTguNyAxOC44IDkycTIuMSA3Ljk1IDQuMiAxNi4yQzY3OC4xIDExMC40IDY5MS4yIDU1LjMgNjgwLjUgMGgtMzBjLTcuNSAxMy42LTEwLjMgMjkuNC04LjkgNTAuNiIgc3R5bGU9ImZpbGw6dXJsKCNTVkdJRF8xMV8pIi8+PGxpbmVhckdyYWRpZW50IGlkPSJTVkdJRF8xMl8iIHgxPSI1NTAuNCIgeDI9IjYzMS41OSIgeTE9IjExMy43MSIgeTI9Ii0xODkuMjgiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMSAwIDAgLTEgLTExOC45OCAxMjAuNTQpIiBncmFkaWVudFVuaXRzPSJ1c2VXU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMDY5QUQ0Ii8+PHN0b3Agb2Zmc2V0PSIuMzUyIiBzdG9wLWNvbG9yPSIjMzBBMENFIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjNUJCMEMwIi8+PC9saW5lYXJHcmFkaWVudD48cGF0aCBkPSJNNTA5LjggMTUwYy01LjctMzcuNy0xMS43LTc2LjYtMTMuMi0xMDguMi0xLjEtMjIuNy40LTMwLjQgMS44LTQxLjhoLTQxLjVjMS41IDQwLjEtMS41IDg1LjMtNyAxNjAuOC0zLjEgNDMuNS04IDExMC41LTcgMTQ1LjdINTI1YzEuNC00Ny43LTYuOC0xMDEuMS0xNS4yLTE1Ni41IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzEyXykiLz48bGluZWFyR3JhZGllbnQgaWQ9IlNWR0lEXzEzXyIgeDE9IjUwNS4zMyIgeDI9IjUwNS4zMyIgeTE9IjEyMC41NCIgeTI9Ii0xODUuODYiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMSAwIDAgLTEgLTExOC45OCAxMjAuNTQpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMUU0NThFIi8+PHN0b3Agb2Zmc2V0PSIuMjQxIiBzdG9wLWNvbG9yPSIjMUY0Rjk2Ii8+PHN0b3Agb2Zmc2V0PSIuNzI5IiBzdG9wLWNvbG9yPSIjMkI2QUFCIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMzM3QkI5Ii8+PC9saW5lYXJHcmFkaWVudD48cGF0aCBkPSJNMzU4LjEgMzA2LjRoNTYuNVYwaC01Ni41bDE3LjYgMTUzLjJ6IiBzdHlsZT0iZmlsbDp1cmwoI1NWR0lEXzEzXykiLz48bGluZWFyR3JhZGllbnQgaWQ9IlNWR0lEXzE0XyIgeDE9IjU1NC45MiIgeDI9IjU1NC45MiIgeTE9Ii0xODUuODYiIHkyPSIxMjAuNTQiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMSAwIDAgLTEgLTExOC45OCAxMjAuNTQpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjM0Y5QUM5Ii8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMjA2MkEyIi8+PC9saW5lYXJHcmFkaWVudD48cGF0aCBkPSJNNDQ5LjkgMTYwLjhjNS41LTc1LjUgOC41LTEyMC42IDctMTYwLjhoLTQyLjJsLS4xIDMwNi40aDI4LjNjLTEtMzUuMSAzLjgtMTAyLjEgNy0xNDUuNiIgc3R5bGU9ImZpbGw6dXJsKCNTVkdJRF8xNF8pIi8+PC9nPjwvc3ZnPg==
```

### Pattern A — One-pager / centered column (`::after` on masthead)

Ribbon as the **lower edge** of a titled masthead; full-bleed when the content column is narrower than the viewport:

```css
.masthead {
  position: relative;
  padding-bottom: calc(var(--space-unit) * 3);
}

.masthead::after {
  content: "";
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 0;
  width: 100vw;
  height: 6px;
  background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0i..."); /* paste full data URI above */
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 50% 50%;
  pointer-events: none;
}
```

### Pattern B — Full-width site header (`::before` on header, bosch.com–style)

Ribbon pinned to the **top** of a full-width header shell; inner wrapper uses **top padding** equal to the strip height so logo and nav are not covered.

```css
.site-header {
  position: relative;
  z-index: 10;
  width: 100%;
}

.site-header::before {
  content: "";
  display: block;
  width: 100%;
  height: 6px;
  background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0i..."); /* paste full data URI above */
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
}

.site-header__bar {
  background-color: var(--color-background);
  min-height: 54px;
  padding-top: 6px;
  width: 100%;
}
```

Use the **full data URI** from the block above in place of `PHN2ZyB4bWxucz0i...`. Never use a hand-authored CSS `linear-gradient` as a substitute.

On **bosch.com**, this maps to the same structure under different class names (e.g. `.O-Header` + `::before` for the supergraphic, `.O-Header__wrapper` for the white bar with `padding-top: 6px`, `.O-Header__brandLogo` for the logo link). Use those names when reviewing scraped markup; use semantic names like `.site-header` in new static pages unless you must mirror their framework.

**Review checklist**

- Supergraphic is `100vw` wide and **6px** tall (unless brand updates the asset).
- `background-image` uses the official data URI from this skill — not a hand-authored `linear-gradient`.
- White/light header bar sits **immediately under** the strip; logo and nav align to a clear horizontal grid with generous spacing.
- Logo is the official inline SVG from this skill — not simplified shapes or `<text>` elements.
- Main content follows the header in DOM order; no overlap with the fixed header strip.

---

## Imagery

Authentic, human-centric scenes aligned with “Invented for life.” Prefer real people in realistic contexts.

- **Good `alt` example:** “A female Bosch service technician smiling as she uses a diagnostic tool on a modern vehicle in a clean workshop.”
- **Bad `alt` example:** “Picture.”

---

## Tone of voice

- Clear and simple; avoid unnecessary jargon.
- Confident and knowledgeable, not arrogant.
- Direct and approachable.

---

## Accessibility

Verify text/background contrast for WCAG AA when using accent colors for text or small UI. Use a contrast checker when in doubt.

---

## Example user request

When asked for a section in this style, generate complete, responsive HTML and CSS. Example:

> Generate the full HTML and responsive CSS for a “Features” section: background `--color-background-alt`, three feature blocks in a grid. Each block includes (1) a circular icon placeholder (`div` with accent background), (2) an `h3`, (3) a short `p`. Use the spacing system for all gaps and padding.
