# mhjaso_public site design specification

Status: **proposed, pending owner approval.** Implementation must not start before approval.

Sources: product list and support/contact source confirmed by the owner on 2026-10-31 (only Turnera is listed; support and privacy structure and contact come from `Maquert/Ecelyo_public`). No legal terms, contacts or product claims are invented; unverified copy is shown as labeled placeholders.

## Renders

Real renders of the prototypes in `prototype/`, produced with a WebKit snapshot at 390 px (mobile) and 1280 px (desktop). Light is the default; dark follows system appearance.

| Page | Mobile (390 px) | Desktop (1280 px) |
| --- | --- | --- |
| Product index | `renders/index-mobile-light.png`, `renders/index-mobile-dark.png` | `renders/index-desktop-light.png` |
| Product page (Turnera) | `renders/turnera-mobile-light.png` | `renders/turnera-desktop-light.png`, `renders/turnera-desktop-dark.png` |
| Turnera support | `renders/turnera-support-mobile-light.png` | `renders/turnera-support-desktop-light.png` |
| Turnera privacy policy | `renders/turnera-privacy-mobile-light.png` | `renders/turnera-privacy-desktop-light.png` |

## Structure and URLs

Reusable per-product path pattern, served by GitHub Pages at `https://maquert.github.io/mhjaso_public/`:

| Page | Path |
| --- | --- |
| Product index | `/` |
| Product page | `/<product-slug>/` |
| Support | `/<product-slug>/support/` |
| Privacy policy | `/<product-slug>/privacy/` |

First release: `/turnera/`, `/turnera/support/`, `/turnera/privacy/`. Products are defined as data (slug, name, tagline, icon, order) so adding a product adds a card, a product page and its two policy pages without changing layout code. Index order is owner-defined; Turnera is first.

## Hierarchy and navigation

- Header: site name (links to `/`) and a primary nav (Products, then one link per product). Single row; wraps on narrow screens.
- Breadcrumb on product, support and privacy pages: Products / Product / Page.
- Index: H1, lead paragraph, product card grid (1 column below 48 rem, 2 columns from 48 rem).
- Product page: H1, tagline, Support and Privacy Policy buttons, icon (beside the text from 48 rem, below it on narrow screens), screenshots section, resources list.
- Support and privacy pages: H1, content sections as H2, contact block.
- Footer: links to the product page, support and privacy of each product, then copyright line.

## Visual design

- Typography: system font stack (`-apple-system`, `Segoe UI`, Roboto). Body 1 rem / 1.6. H1 `clamp(2rem, 6vw, 3rem)`, H2 1.4 rem. Lead 1.2 rem, muted.
- Layout: single column, content max width 44 rem, 1.25 rem gutters, centered.
- Color tokens (light / dark): background `#fff` / `#0e1013`; surface `#f4f5f7` / `#1a1d23`; text `#16181d` / `#eef0f4`; muted `#5b6270` / `#a1a8b5`; accent `#0a64d6` / `#5aa2ff`; border `#dfe2e8` / `#2c313a`.
- Cards and notes use a 14 px radius, buttons are pill shaped. The app icon is a placeholder gradient until the owner supplies the real icon.
- Dark appearance follows `prefers-color-scheme` and is a first-class design.
- Placeholder notes (dashed amber boxes) appear only in the design; the implementation shows them solely where content is genuinely missing, and none may ship on a published policy page.

## Accessibility

- Semantic landmarks (`header`, `nav`, `main`, `footer`), one H1 per page, skip link, `lang="en"`.
- Text and control contrast at least 4.5:1 in both appearances; focus ring 3 px accent with offset; `aria-current="page"` on the active nav link.
- Layout reflows to 320 px without horizontal scrolling and respects text zoom up to 200%; sizes are in `rem`.
- Motion is limited to a border-color transition and disabled under `prefers-reduced-motion`.

## Responsive behavior

- Breakpoint at 48 rem: card grid goes from 1 to 2 columns; product hero goes from stacked to text plus icon.
- Below the breakpoint, buttons wrap onto separate lines rather than shrinking.

## Content rules

- Support page: contact and "Reporting a problem" list from the approved Ecelyo_public support page, Ecelyo-specific sections removed.
- Privacy page: section structure follows the approved Ecelyo_public privacy page; all Turnera data-practice text is a labeled placeholder until the owner verifies it against the submitted build (calendar access, notifications, iCloud, Google Calendar integration). Ecelyo-specific sections (Satellite, AI agents) are excluded.
- Product page: tagline from the Turnia repository description; marketing copy, screenshots and App Store link are placeholders.

## Open items for the owner

1. Approve the layout, color, typography and URL structure above.
2. Supply or approve the real app icon, any marketing copy and screenshots (otherwise shown as placeholders).
3. Verify the Turnera privacy-policy text before the policy task publishes it.
