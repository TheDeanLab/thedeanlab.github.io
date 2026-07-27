# Meetings and Presentation Expectations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the brief Dean Lab meeting guidance with comprehensive, scannable expectations for research presentations, rapid fire, journal club, and audience participation.

**Architecture:** Keep the existing Sphinx page and navigation structure. Express the approved guidance as semantic reStructuredText, use a reusable `meeting-checklist` container for all quick-reference insets, and load one focused CSS file through the existing Sphinx static-asset configuration. Validate this documentation change through direct comparison with the approved specification, a warning-free complete Sphinx build, and rendered desktop, narrow-screen, and print inspection.

**Tech Stack:** Sphinx, reStructuredText, sphinx-rtd-theme, CSS

## Global Constraints

- Preserve the recurring schedule, whole-team guidance, one-on-one guidance, and general punctuality and absence expectations.
- Describe the cadence exactly as Week 1 research presentation plus rapid fire, followed by Week 2 journal club on the selected paper.
- Keep comprehensive guidance visible in the page body.
- Add one persistent `Quick checklist` inset for Research Presentations, Rapid Fire, and Journal Club.
- Do not add accordions, foldable sections, JavaScript, a separate rubric table, or navigation changes.
- Use one reusable checklist style compatible with the existing Sphinx theme.
- Checklist meaning must not depend on color, and the markup must remain semantic and printable.
- Keep unrelated pages and navigation unchanged.
- Use the approved copy and requirements in `docs/superpowers/specs/2026-07-27-meetings-presentation-expectations-design.md`.
- Do not add tests that assert exact phrases in human-facing documentation.

## File Structure

- Modify `source/meetings.rst`: the public meeting expectations and all three checklist containers.
- Create `source/_static/meetings.css`: reusable checklist inset styling, narrow-screen adjustments, and print behavior.
- Modify `source/conf.py`: append `meetings.css` to the existing `html_css_files` list.

---

### Task 1: Rewrite the Dean Lab meeting guidance

**Files:**
- Modify: `source/meetings.rst:25-63`

**Interfaces:**
- Consumes: the approved content in `docs/superpowers/specs/2026-07-27-meetings-presentation-expectations-design.md`.
- Produces: three `.. container:: meeting-checklist` elements that `meetings.css` will style and complete public guidance for each meeting format.

- [ ] **Step 1: Preserve the out-of-scope sections**

Before editing, record the current content of:

- `Recurring Schedule`
- `Whole-Team Meeting`
- `One-on-One Meetings`
- `General Expectations`

Do not alter their wording, schedule, room numbers, links, or ordering.

- [ ] **Step 2: Replace the existing Dean Lab Meeting Format body**

Use this exact section hierarchy:

```rst
Dean Lab Meeting Format
-----------------------

Research Presentations
^^^^^^^^^^^^^^^^^^^^^^

Motivation and question
"""""""""""""""""""""""

Approach and rationale
""""""""""""""""""""""

Results and interpretation
""""""""""""""""""""""""""

Conclusions, decisions, and feedback
""""""""""""""""""""""""""""""""""""

Presentation standard
"""""""""""""""""""""

Rapid Fire
^^^^^^^^^^

Choosing a paper
""""""""""""""""

The two-minute pitch
""""""""""""""""""""

Selecting the journal-club paper
""""""""""""""""""""""""""""""""

Journal Club
^^^^^^^^^^^^

Context, claims, and experimental logic
"""""""""""""""""""""""""""""""""""""""

Claim-evidence analysis
"""""""""""""""""""""""

Creative and critical analysis
""""""""""""""""""""""""""""""

Conclusions and relevance to the lab
""""""""""""""""""""""""""""""""""""

Audience Expectations
^^^^^^^^^^^^^^^^^^^^^
```

Immediately after `Dean Lab Meeting Format`, state the two-week cadence:

```rst
The Monday Dean Lab meeting follows a two-week cycle:

- **Week 1:** a polished research presentation followed by rapid fire
- **Week 2:** journal club focused on the paper selected from the preceding
  rapid-fire pitches
```

- [ ] **Step 3: Add the Research Presentations guidance**

Implement the approved `Research Presentations` content from the design
specification, including:

- its purpose as a coherent scientific argument rather than a chronological
  progress report
- explicit permission to present failures, ambiguous results, and unfinished
  ideas when the reasoning is organized
- motivation, significance, broader context, and the central question,
  hypothesis, or objective
- approach rationale, material controls, replication, assumptions, and
  discriminating evidence
- results organized around claims, with observations separated from inference
  and speculation
- alternative explanations, confounders, limitations, and contradictory
  evidence
- conclusions mapped to the original question
- one to three prioritized next steps and the decisions they enable
- a final **Questions for the group** slide with specific feedback requests
- rehearsed timing, legible figures, visible controls and replicate
  information, consistent visual conventions, and backup slides

Insert this exact persistent checklist near the top:

```rst
.. container:: meeting-checklist

   **Quick checklist**

   - State the central question and why it matters.
   - Explain the approach and its rationale.
   - Organize results around scientific claims.
   - Separate evidence, inference, and uncertainty.
   - Conclude with confidence and remaining unknowns.
   - End with prioritized next steps and specific questions.
```

- [ ] **Step 4: Add the Rapid Fire guidance**

Implement the approved `Rapid Fire` content from the design specification,
including:

- its purpose as scientific triage and high-level communication training rather
  than compressed journal club
- substantive primary research published within the past year, preferably
  within three to six months
- a reputable venue, while giving scientific merit and discussion value
  priority over prestige
- rare, explicitly identified preprint exceptions
- full-paper reading
- one slide, one central figure or schematic at most, no animations, a strict
  two-minute pitch, and no more than one minute of clarification
- the six required questions: problem, claim, approach, strongest evidence,
  importance, and recommendation
- one independent high-level critical judgment
- independent synthesis rather than abstract reading, graphical-abstract
  language, figure-by-figure narration, jargon, or vague novelty claims
- paper selection based on importance, evidence, discussion potential,
  transferable value, learning potential, and pitch accuracy and clarity
- one vote per person with reasoning available

Insert this exact persistent checklist near the top:

```rst
.. container:: meeting-checklist

   **Quick checklist**

   - Use one slide and finish within two minutes.
   - State the problem and central claim.
   - Explain the approach at the level needed to understand the claim.
   - Identify the strongest evidence.
   - Explain why the paper matters.
   - Offer one independent critical judgment.
   - Recommend for or against journal club.
   - Show the citation, journal, and publication date.
```

- [ ] **Step 5: Add the Journal Club and audience guidance**

Implement the approved `Journal Club` and `Audience Expectations` content from
the design specification, including:

- the purpose of understanding unfamiliar science, reconstructing logic,
  evaluating claims, identifying assumptions and alternatives, designing better
  experiments, and extracting transferable ideas
- field-level context and two to four central claims before individual figures
- experimental logic and claim-evidence matching
- directness, quantification, replication, controls, statistics, and agreement
  between representative data and quantification when material
- strongest and weakest evidence, hidden assumptions, alternative explanations,
  important limitations, and the most informative missing experiment
- what the paper establishes versus suggests, whether its title and abstract
  are justified, likely impact, unresolved questions, and lessons for the lab
- full-paper reading and at least two substantive questions or observations
  from every attendee
- clarifying questions before criticism, separation of conceptual and technical
  concerns, actionable suggestions, balanced participation, and respectful
  challenges to claims

Insert this exact persistent checklist near the top of `Journal Club`:

```rst
.. container:: meeting-checklist

   **Quick checklist**

   - Explain why the paper and problem matter.
   - Identify two to four central claims.
   - Match each claim to its strongest evidence.
   - Evaluate the logic, controls, assumptions, and limitations.
   - Offer alternative explanations.
   - Propose the most informative missing experiment.
   - Distinguish what is established from what is suggested.
   - Translate the paper into lessons for the lab.
```

End the Dean Lab section with the shared cultural expectation that presenters
must demonstrate ownership of the scientific reasoning, not merely show work or
summarize literature.

- [ ] **Step 6: Review the source against the approved specification**

Read `source/meetings.rst` and
`docs/superpowers/specs/2026-07-27-meetings-presentation-expectations-design.md`
side by side. Confirm every approved requirement is represented, the three
checklists are identical to the plan, the two-week sequence is unambiguous, and
no new scientific or administrative claims were added.

- [ ] **Step 7: Confirm only the intended source section changed**

Run:

```bash
git diff --check -- source/meetings.rst
git diff -- source/meetings.rst
```

Expected: no whitespace errors, and changes are confined to the Dean Lab
Meeting Format body.

- [ ] **Step 8: Commit the content rewrite**

```bash
git add source/meetings.rst
git commit -m "docs: expand lab meeting expectations"
```

---

### Task 2: Add the persistent checklist inset style

**Files:**
- Create: `source/_static/meetings.css`
- Modify: `source/conf.py:60`

**Interfaces:**
- Consumes: the `meeting-checklist` classes generated by the three RST
  container directives in `source/meetings.rst`.
- Produces: a reusable inset style loaded through `html_css_files`; it has no
  visible effect on pages without `meeting-checklist`.

- [ ] **Step 1: Create the checklist stylesheet**

Create `source/_static/meetings.css` with:

```css
.meeting-checklist {
  background: #eef5fa;
  border: 1px solid #c9dce9;
  border-left: 0.35rem solid #3975a8;
  border-radius: 4px;
  margin: 1rem 0 1.5rem;
  padding: 1rem 1.1rem;
}

.rst-content .meeting-checklist > p:first-child {
  color: #214b70;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.rst-content .meeting-checklist ul {
  margin-bottom: 0;
}

.rst-content .meeting-checklist li {
  margin-bottom: 0.25rem;
}

.rst-content .meeting-checklist li:last-child {
  margin-bottom: 0;
}

@media screen and (max-width: 760px) {
  .meeting-checklist {
    padding: 0.85rem 0.9rem;
  }
}

@media print {
  .meeting-checklist {
    background: transparent;
    border: 1px solid #7f8f9f;
    break-inside: avoid;
    page-break-inside: avoid;
  }
}
```

- [ ] **Step 2: Register the stylesheet**

Change the existing line in `source/conf.py` to:

```python
html_css_files = ["profile.css", "meetings.css"]
```

- [ ] **Step 3: Build the complete site with warnings treated as errors**

Run:

```bash
uv run sphinx-build -W --keep-going -b html source build/html
```

Expected: exit code 0, no Sphinx warnings, and an updated
`build/html/meetings.html`.

- [ ] **Step 4: Confirm the rendered structure**

Inspect `build/html/meetings.html` and confirm:

- `Research Presentations`, `Rapid Fire`, `Journal Club`, and
  `Audience Expectations` are distinct rendered sections
- exactly three elements use the `meeting-checklist` class
- each checklist has a visible `Quick checklist` label and semantic list
- `_static/meetings.css` is linked
- Week 1 and Week 2 appear before the three detailed meeting formats

- [ ] **Step 5: Commit the inset style**

```bash
git add source/_static/meetings.css source/conf.py
git commit -m "style: add meeting checklist insets"
```

---

### Task 3: Validate the final documentation artifact

**Files:**
- Verify: `source/meetings.rst`
- Verify: `source/_static/meetings.css`
- Verify: `source/conf.py`
- Verify: `build/html/meetings.html`

**Interfaces:**
- Consumes: the complete Sphinx source and static assets from Tasks 1 and 2.
- Produces: warning-free HTML and visual evidence that the approved wording and
  persistent checklists work at desktop, narrow-screen, and print widths.

- [ ] **Step 1: Rebuild from a clean output directory**

Use a fresh temporary output directory so stale build artifacts cannot satisfy
validation:

```bash
validation_dir="$(mktemp -d)"
uv run sphinx-build -W --keep-going -b html source "$validation_dir"
```

Expected: exit code 0 and no Sphinx warnings.

- [ ] **Step 2: Inspect the rendered wording against the specification**

Open the freshly rendered `meetings.html` and compare it with
`docs/superpowers/specs/2026-07-27-meetings-presentation-expectations-design.md`.
Confirm the two-week cadence, the complete guidance for all three meeting
formats, all checklist items, audience responsibilities, and the shared
cultural expectation are present and accurate.

- [ ] **Step 3: Serve the fresh build locally**

Run:

```bash
uv run python -m http.server 8000 --directory "$validation_dir"
```

Keep the server running only for the following visual checks.

- [ ] **Step 4: Inspect the desktop layout**

Open `http://127.0.0.1:8000/meetings.html` at approximately 1440 × 1000 and
verify:

- the two-week cadence is visible before the detailed format sections
- each checklist is distinct but compatible with the existing theme
- checklist labels and bullets are legible
- nested headings make the long page easy to scan
- no text or border overflows the content column
- the existing schedule and one-on-one sections remain unchanged

- [ ] **Step 5: Inspect the narrow-screen layout**

View the same URL at approximately 390 × 844 and verify:

- the content remains a single readable column
- checklist padding does not crowd the text
- long headings wrap without clipping
- lists remain aligned and fully visible
- the side navigation and page retain normal theme behavior

- [ ] **Step 6: Inspect print preview**

Verify:

- each checklist has a visible border without requiring its blue background
- checklist blocks avoid splitting internally when space permits
- no checklist content is clipped or obscured
- all detailed guidance remains printable

- [ ] **Step 7: Correct any visual defect and repeat validation**

If a defect is found, make only the smallest relevant change in
`source/_static/meetings.css` or `source/meetings.rst`, rebuild into a new
temporary directory, and repeat the affected desktop, narrow-screen, or print
check. Do not change unrelated theme or navigation styles.

- [ ] **Step 8: Run final repository checks**

Run:

```bash
uv run pytest -q
final_validation_dir="$(mktemp -d)"
uv run sphinx-build -W --keep-going -b html source "$final_validation_dir"
git diff --check
git status --short
```

Expected: all existing tests pass, the final Sphinx build exits 0 without
warnings, `git diff --check` produces no output, and the worktree contains only
the intended plan, page, stylesheet, and configuration changes. The
visual-companion `.superpowers/` directory must not be staged.

- [ ] **Step 9: Commit any visual-validation corrections**

If Step 7 required a correction:

```bash
git add source/meetings.rst source/_static/meetings.css
git commit -m "style: refine meetings page presentation"
```

If no correction was required, do not create an empty commit.
