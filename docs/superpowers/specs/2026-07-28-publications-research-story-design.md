# Publications Research Story Design

**Status:** Approved for implementation planning
**Date:** 2026-07-28
**Page:** `source/publications.rst`
**Public URL:** `https://thedeanlab.github.io/publications.html`

## Purpose

Replace the placeholder publications page with a curated account of the research
program. The page should explain how the work fits together rather than reproduce
another bibliography that must be maintained by hand.

The organizing idea is:

> **Build → Scale → Discover**

The page will connect the development of open and adaptive imaging systems, their
extension across biological scales, and the discoveries they make possible.
Complete and continuously maintained publication records will remain in
authoritative external systems.

## Audience

The page should work for:

- prospective trainees trying to understand the lab's scientific direction;
- collaborators and scientists evaluating the lab's capabilities;
- funders, institutional visitors, and non-specialists seeking a concise overview;
- readers looking for a representative entry point into the publication record.

The writing should remain intelligible to scientists outside the immediate
microscopy subfield without oversimplifying the technical contributions.

## Goals

- Tell a coherent research story through a deliberately selective group of papers.
- Show the relationship between instrumentation, scale, and biological discovery.
- Give each selected paper a short explanation of its role in that story.
- Clearly distinguish a curated narrative from a comprehensive bibliography.
- Direct readers to stable, authoritative sources for the complete record.
- Keep the CV current without requiring a separate website maintenance step.
- Preserve the existing visual language of the Sphinx Read the Docs site.

## Non-goals

- Reproduce every publication or a reverse-chronological bibliography.
- Display citation counts, h-index values, or other rapidly changing metrics.
- Repeat the detailed paper-to-code index already maintained on the Repositories
  page.
- Include full author lists or complete journal citation formatting.
- Imply that every collaborative biological study was solely led by the Dean Lab.
- Add automatic publication ingestion, metadata parsing, or client-side API calls.

## Page Structure

### Page title

The navigation label remains **Publications**. The page heading becomes:

> **Our Research Story**

This signals that the page is interpretive and selective rather than exhaustive.

### Opening thesis

The opening should establish the central scientific problem and the three-part
arc in one compact paragraph:

> Modern biological imaging often forces a trade-off between resolution, scale,
> adaptability, and accessibility. Our research program works across that
> boundary: we build open and adaptive light-sheet microscopes, scale them from
> subcellular dynamics to intact tissues, and use them with collaborators to
> discover how cells and organs are organized and function.

Immediately below, a short note should state that this is a curated view and
provide compact links to:

- [NCBI My Bibliography](https://www.ncbi.nlm.nih.gov/myncbi/kevin.dean.1/bibliography/public/)
- [Google Scholar](https://scholar.google.com/citations?user=Uv0B5xIAAAAJ&hl=en)
- [ORCID](https://orcid.org/0000-0003-0839-2320)
- the website's stable CV path, `_static/kevin-dean-cv.pdf`

### Editorial flow

The page will use a continuous editorial layout rather than a grid of thematic
cards. Each theme will have:

1. a descriptive heading;
2. a one- or two-sentence framing paragraph;
3. a compact sequence of representative publications;
4. thin separators and restrained spacing to make the sequence scannable.

Each publication entry will contain:

- the paper title as a descriptive PubMed link;
- the venue and year;
- one plain-language sentence explaining why the paper belongs in the story.

The page will not include full author lists, DOI strings, PMIDs in visible text,
abstract excerpts, thumbnails, or citation metrics.

## Theme 1: Build Open and Adaptive Imaging Systems

### Framing

The section should explain that advanced microscopy is most useful when strong
optical performance is paired with accessibility, open control, adaptable sample
geometry, and reproducible operation.

### Representative publications

1. **[A versatile oblique plane microscope for large-scale and high-resolution
   imaging of subcellular dynamics](https://pubmed.ncbi.nlm.nih.gov/33179596/)**

   *eLife, 2020*

   Combined high-numerical-aperture optics with a versatile sample geometry to
   support high-resolution imaging across cells, embryos, and tissue sections.

2. **[Navigate: an open-source platform for smart light-sheet
   microscopy](https://pubmed.ncbi.nlm.nih.gov/39261640/)**

   *Nature Methods, 2024*

   Created an open control platform that turns light-sheet microscopes into
   programmable systems for intelligent and adaptive acquisition.

3. **[Mechanically sheared axially swept light-sheet
   microscopy](https://pubmed.ncbi.nlm.nih.gov/39296406/)**

   *Biomedical Optics Express, 2024*

   Placed acquired data directly into its spatial context while enlarging the
   field of view and reducing interpolation-heavy post-processing.

4. **[A high-resolution, easy-to-build light-sheet microscope for subcellular
   imaging](https://pubmed.ncbi.nlm.nih.gov/41642252/)**

   *eLife, 2026*

   Paired simplified alignment and open-source control with subcellular
   resolution, lowering the practical barrier to high-performance light-sheet
   imaging.

## Theme 2: Scale from Cells to Whole Tissues

### Framing

The section should explain that biological mechanisms span spatial scales, but
conventional imaging often forces a choice between detailed local measurements
and the tissue context in which those measurements matter.

### Representative publications

1. **[Light-sheet microscopy of cleared tissues with isotropic, subcellular
   resolution](https://pubmed.ncbi.nlm.nih.gov/31673159/)**

   *Nature Methods, 2019*

   Brought isotropic subcellular resolution to millimeter-scale cleared tissues
   across diverse immersion media.

2. **[Isotropic imaging across spatial scales with axially swept light-sheet
   microscopy](https://pubmed.ncbi.nlm.nih.gov/35831614/)**

   *Nature Protocols, 2022*

   Made ASLM reproducible across expanded samples, living cells, and cleared
   organisms through detailed build guidance, operating procedures, and software.

3. **[Feature-driven whole-tissue imaging with subcellular
   resolution](https://pubmed.ncbi.nlm.nih.gov/40902591/)**

   *Cell Reports Methods, 2025*

   Combined centimeter-scale survey imaging with targeted high-resolution
   interrogation, concentrating acquisition on rare or informative biology.

## Theme 3: Discover Biological Mechanisms

### Framing

The section should make clear that the instrumentation is not an endpoint. Its
value is demonstrated through biological collaborations that connect molecular
organization and cell morphology to cell behavior and whole-organ function.

### Representative publications

1. **[Pre-complexation of talin and vinculin without tension is required for
   efficient nascent adhesion maturation](https://pubmed.ncbi.nlm.nih.gov/33783351/)**

   *eLife, 2021*

   Showed that talin and vinculin must assemble before mechanical loading for
   efficient maturation of nascent adhesions.

2. **[Blebs promote cell survival by assembling oncogenic signalling
   hubs](https://pubmed.ncbi.nlm.nih.gov/36859545/)**

   *Nature, 2023*

   Used three-dimensional imaging to reveal blebs as signaling hubs that support
   anoikis resistance in melanoma cells.

3. **[An epithelial morphogenetic program for maximal urine
   concentration](https://pubmed.ncbi.nlm.nih.gov/41862496/)**

   *Nature Communications, 2026*

   Integrated transcriptomics and high-resolution imaging to connect ascending
   thin-limb epithelial architecture with whole-organ urine-concentrating
   function.

## Complete Record Inset

The page will end with a persistent, understated inset:

> **Explore the complete publication record**
>
> This page presents a curated research narrative rather than a comprehensive
> bibliography. Browse NCBI My Bibliography, Google Scholar, ORCID, or the full
> CV for the complete record.

The inset repeats the four record links. This repetition is intentional: the
first set gives direct access to readers who already know what they need, while
the closing inset gives readers a natural next step after completing the story.

## Visual Design

- Preserve the Read the Docs theme, current typography, and existing blue-gray
  site palette.
- Use a single readable text column.
- Use semantic section headings rather than card headings.
- Use restrained rules or spacing between publication entries.
- Style record links as compact text buttons consistent with the profile page.
- Use one low-contrast closing inset with a visible border and sufficient
  padding.
- On narrow screens, allow link buttons to wrap and preserve a comfortable
  reading width.
- Do not introduce publication images, journal logos, carousels, animation, or
  hover-dependent information.

## Accessibility

- Maintain a logical heading hierarchy beneath the page title.
- Ensure every link has descriptive visible text.
- Do not use color alone to distinguish venue metadata, links, or sections.
- Preserve keyboard focus indicators from the site theme.
- Meet WCAG AA contrast for added text, borders, and link treatments.
- Keep publication annotations as real text, not generated content or images.
- Verify that the layout remains readable at mobile widths and browser zoom.

## CV Synchronization

### Authority

The authoritative CV artifact is:

`https://github.com/AdvancedImagingUTSW/CV/blob/main/kevin_dean_cv.pdf`

The public website link remains stable:

`_static/kevin-dean-cv.pdf`

### Build behavior

Every production website deployment will fetch the current
`kevin_dean_cv.pdf` from the `main` branch of
`AdvancedImagingUTSW/CV` before the Sphinx build.

The synchronization step must:

1. use the public raw-file URL from the authoritative repository;
2. download to a temporary file rather than directly overwriting the destination;
3. fail on HTTP or network errors and retry transient failures;
4. verify that the result is nonempty and begins with the PDF signature;
5. atomically replace `source/_static/kevin-dean-cv.pdf` only after validation;
6. fail the deployment if any download or validation step fails.

The repository's committed PDF will also be synchronized during this update.
It is a current fallback for local or offline Sphinx builds, but production
deployments must not silently fall back to it if the upstream refresh fails.

This behavior refreshes the CV whenever the website is deployed. A change only
to the CV repository does not independently trigger a website deployment.

## Relationship to Other Pages

- **Repositories:** remains the detailed index linking publications to software,
  data, and hardware resources. The publications page may link to it in prose but
  will not duplicate its list.
- **Kevin Dean profile:** may retain its short selected-publications list. Its
  purpose is a compact profile snapshot, whereas this page explains the research
  program.
- **Homepage:** keeps the existing Publications navigation entry and description
  unless implementation reveals a small wording change is needed for consistency.

## Validation

The implementation will be validated as documentation, not through brittle
phrase-presence tests.

Required checks:

1. Review the final wording against this approved specification.
2. Build Sphinx from a fresh output directory with warnings treated as errors.
3. Confirm that the Sphinx build is warning-free.
4. Inspect the rendered publications page at desktop and narrow/mobile widths.
5. Check heading hierarchy, wrapping, spacing, link focus, and closing-inset
   readability.
6. Open or otherwise verify every PubMed and complete-record destination.
7. Confirm that the deployed CV path contains the same validated PDF fetched
   from the authoritative CV repository during the build.
8. Confirm that the Repositories and profile pages continue to render correctly.

No new tests will assert exact prose fragments. Existing structural checks may
be updated only when required by stylesheet registration or other site-level
contracts.

## Success Criteria

The redesign is successful when a reader can:

- understand the Build → Scale → Discover research arc without reading a full
  bibliography;
- identify representative contributions within each theme;
- recognize which entries describe collaborative biological discovery;
- reach a complete publication record in one obvious action;
- download the current authoritative CV from the stable website link;
- read and navigate the page comfortably on desktop and mobile.
