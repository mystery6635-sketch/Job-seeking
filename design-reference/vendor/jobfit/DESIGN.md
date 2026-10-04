# JobFit Design System

Brand: JobFit, a Korean-language AI job-seeking competency diagnosis service (education/career/certificate/skill-based 100-point score, deduction reasons, static certificate/training recommendations). This is an original brand — do not use any real job-board or diagnostic-service logo, wordmark, slogan, or payment/subscription checkout UI. Only the general layout/typography structure (white canvas, single accent color, rounded cards, generous whitespace) is referenced from external style research (e.g. Apple's restrained typography and spacing rhythm); no trademarked visual elements are reused.

## Colors
- Canvas background: pure white (#FFFFFF), never dark mode.
- Primary text: dark charcoal gray (#1D1D1F), never pure black.
- Secondary text: medium gray (#4A4C50), muted text: (#7A7A7A).
- Primary accent (CTA, active states, selected chips): trust blue (#1668E3), chosen to read as credible/professional like major Korean job-board brands (e.g. JobKorea). Used sparingly — most of the screen stays white + dark gray text with one or two blue moments per screen.
- Semantic colors distinct from the primary accent: error/validation red (#D92D20), warning/incomplete amber (#B54708), info/empty-state color must NOT reuse the primary blue — use a muted teal (#0E7490) for neutral informational notices instead. Never reuse the primary blue for errors or warnings.
- Hairline borders: light gray (#E3E1DD).

## Typography
- Font: Inter for Latin characters/numbers, with system Korean font fallback for Korean text (Apple SD Gothic Neo / Malgun Gothic). All UI copy is in natural, complete Korean sentences — no Lorem ipsum, no placeholder text like '준비 중' or '정보 확인 필요'.
- Headlines are modest in weight (600-700), not oversized; the 100-point score is the one place large, bold numerals are used.

## Shape & Elevation
- Cards: ~14px corner radius.
- Buttons and inputs: 8px corner radius; chips and the "진단하기" primary CTA: fully rounded (pill).
- Elevation: flat by default; one subtle shadow tier for the deduction-reason Drawer/Modal only. No heavy drop shadows.

## Layout
- Desktop content max width: 1200-1280px, centered, generous side gutters.
- Section vertical padding: 64-96px on desktop, 40-64px on mobile.
- Hero sections must NOT fill the full viewport height — at 1440px width, the start of the next section should already be visible below the fold.
- Card grids: 2-3 columns desktop, 1 column mobile, 16-20px gaps.
- Every content section needs a clear title, a 1-3 sentence description, and either real content or a clear call-to-action — never a large empty decorative area.

## Imagery
- Minimal photography; this is a form/data-driven diagnosis product, not a photo-led product. Where illustration or icon imagery is used (3-step guidance, certificate/training cards), use descriptive alt text.
- No stock 'lorem picture' placeholders without a described purpose.

## Components
- Buttons: solid trust-blue primary button ("진단하기", "추천 확인하기"), white background outline secondary button, plain text tertiary link ("다시 진단하기").
- Score display: large numeral (100점 만점) with a ring/gauge indicator, flat, no shadow.
- Deduction reason Drawer/Modal: list of category + status ("감점 있음"/"감점 없음") + reason text, opens over SCR-002 without a route change.
- Chips: pill-shaped, trust-blue fill when selected/flagged as a deduction category, gray outline when neutral ("감점 없음").
- Empty states (no deduction items, e.g. a perfect score): always include a short explanatory sentence, how-to-use guidance, and a next-step call-to-action — never a bare 'no data' message.
- No admin dashboard, no analytics charts — this product has no admin screen in v1.
- Do not depict payment, subscription, or checkout UI — diagnosis is free in v1 and nothing is purchased in-app.
