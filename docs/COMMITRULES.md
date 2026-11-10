# Commit Rules

- This repository is a **Quarto book** — chapters under `notes/<part>/`, front
  and back matter at the root (`index.qmd`, `summary.qmd`, `notation.qmd`,
  `glossary.qmd`, `references.qmd`), and a build configured by `_quarto.yml`.
- It follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
  specification, adapted so that the `<type>` describes a change to **content**,
  not only to code.
- A consistent history makes it easy to answer "when did this chapter land?",
  "which explanations were wrong and when were they fixed?", and "which commits
  touched the build?" — and it keeps the generated changelog readable.

## Commit Message Format

```text
<type>(<scope>): <description>   ← single line, mandatory

[optional body]

[optional footer(s)]
```

- The **header** is the first line and is mandatory — it is always a **single line**.
- The **scope** is optional but strongly encouraged; it is usually the chapter
  slug, the part, or the reference file touched.
- A blank line separates the header from the body, and the body from the footer.

### Examples

A new chapter:

```text
chapter(binary-search): add binary search chapter

Introduces lower bound on a half-open interval [l, r) and derives the
O(log n) bound from the halving of the search interval.
```

A substantive edit to an existing chapter:

```text
edit(complexity): 償却計算量の節を追加
```

A correction of something that was wrong:

```text
errata(binary-search): fix off-by-one when target exceeds all elements

The previous implementation returned n instead of -1 when x was larger
than every element of A.
```

A reference-material change:

```text
ref(bib): add CLRS 4th edition
```

Site-wide infrastructure:

```text
build(epub): enable section numbering in epub output
```

## Type

The `<type>` describes the kind of change and must be one of the following.
The first group is **content**; the second is **site and tooling**.

### Content types

| Type      | Description                                                                          |
| --------- | ------------------------------------------------------------------------------------ |
| `chapter` | Add a **new** chapter, including its registration in `book.chapters` of `_quarto.yml` |
| `edit`    | Substantive addition to an existing chapter — new section, example, proof, exercise   |
| `errata`  | Correct something that was **wrong** — complexity, proof, definition, buggy code     |
| `ref`     | Reference material — glossary, notation, bibliography                                |
| `toc`     | Restructure the book — reorder, split, or merge chapters and parts                   |
| `fig`     | Figures and diagrams — TikZ, algorithm traces, plots                                 |
| `typo`    | Typos, notation consistency, wording touch-ups with no change in meaning             |

> [!NOTE]
> `edit` vs `errata` vs `typo` is the distinction that matters most here.
>
> - `edit`: the reader learns something **new**.
> - `errata`: what the reader learned before was **wrong**.
> - `typo`: the reader learns **nothing different**.
>
> Keeping `errata` separate means `git log --grep '^errata'` doubles as the
> book's errata list.

### Site & tooling types

| Type       | Description                                                                   |
| ---------- | ----------------------------------------------------------------------------- |
| `style`    | Presentation only — SCSS under `include/scss/`, layout, fonts, theming         |
| `feat`     | New book capability — MathJax macros, filters, shortcodes, Quarto extensions  |
| `fix`      | A bug fix in site code, a filter, or a broken render                          |
| `refactor` | Code or file reorganisation that neither fixes a bug nor adds a feature       |
| `perf`     | Faster build or render (e.g. `_freeze` caching)                               |
| `build`    | Quarto config, `_quarto.yml` options, output formats, `pyproject.toml`, `uv.lock` |
| `ci`       | CI workflows, `.pre-commit-config.yaml`, deployment automation                |
| `docs`     | Repository documentation — `README.md`, `docs/`, agent instructions           |
| `chore`    | Housekeeping — `.gitignore`, cleanup of stray render artifacts                |
| `revert`   | Reverts a previous commit                                                     |

> [!NOTE]
> Editing `_quarto.yml` is not automatically `build`. Registering a new chapter
> belongs to `chapter`, and reordering `book.chapters` belongs to `toc`. Use
> `build` only for options that change how the book is rendered.

## Scope

The `<scope>` is optional and names the part of the book affected. Use a short,
lowercase noun. Omit it when the change is genuinely global.

| Target                  | Scope                                   | Example                                          |
| ----------------------- | --------------------------------------- | ------------------------------------------------ |
| A chapter               | File name stem                          | `chapter(binary-search):`, `errata(complexity):` |
| A part                  | Directory name directly under `notes/`  | `toc(search):`, `toc(foundations):`              |
| Front / back matter     | File name stem                          | `edit(index):`, `edit(summary):`                 |
| Reference material      | `glossary`, `notation`, `bib`           | `ref(glossary):`, `ref(notation):`, `ref(bib):`  |
| Site internals          | Subsystem                               | `style(dark):`, `feat(math):`, `build(epub):`    |

## Description

- Keep the description on a **single line** — never wrap it onto multiple lines.
- Keep the `<type>(<scope>):` prefix in **ASCII**.
- The description may be written in **Japanese or English**. Do not mix the two
  within one description.
- When writing in English:
  - Use the **imperative, present tense**: "add", not "added" or "adds".
  - Do **not** capitalize the first letter.
- Do **not** end with a period (`.` or `．` / `。`).
- Keep the header concise — aim for **50 characters or fewer**, hard limit **72**
  (count a full-width character as two).
- Wrap file, function, and option names in backticks, e.g.
  ``errata(binary-search): fix loop condition in `binary_search` ``
- If more explanation is needed, put it in the **body**, not the description.

## Body

- Optional. Use it to explain **what** and **why**, not **how**.
- Wrap lines at **72 characters**.
- Separate from the header with one blank line.
- For a new chapter, a one-or-two-sentence summary of what it covers is more
  useful than a list of the sections you wrote.
- For `errata`, state what was wrong and what is correct now.

## Footer

- Optional. Used for metadata such as issue references and breaking changes.
- Reference issues with `Closes #<id>`, `Fixes #<id>`, or `Refs #<id>`.
- Note when a change shifts the numbers readers see, written as the sidebar
  shows them. Two kinds of number can shift:
  - **Chapter numbers** are assigned by Quarto (`number-sections: true`) and run
    continuously across parts — `1 アルゴリズムとは`, `2 計算量`, `3 二分探索`:
    `Renumbers: 3 二分探索 → 2, 2 計算量 → 3`
  - **Part numbers** are hand-written in the `part:` titles of `_quarto.yml`, so
    inserting or removing a part means renaming the later ones in the same commit:
    `Renumbers: Part 2 → Part 3`

### Breaking Changes

In this book, a "breaking change" is one that **breaks existing URLs or inbound
links**:

- renaming, moving, or deleting a chapter file
  (e.g. `/notes/search/binary-search.html` no longer resolves)
- renaming a cross-reference label that may be linked from outside
  (e.g. `#def-lower-bound`)

Indicate it with a `!` after the type/scope, a `BREAKING CHANGE:` footer, or both.

```text
toc(foundations)!: move binary-search before complexity

BREAKING CHANGE: /notes/search/binary-search.html no longer resolves.
Renumbers: 3 二分探索 → 2, 2 計算量 → 3
```

> [!NOTE]
> A reorder that only shifts chapter or part numbers is **not** breaking — URLs
> stay the same. Record it with a `Renumbers:` footer instead of `!`.

## One Change, One Commit

- Keep a chapter and everything it needs together in one commit: the `.qmd`
  file, its figures, its entry in `_quarto.yml`, and the `references.bib` and
  `glossary.qmd` entries it introduces.
- When renaming a cross-reference label, update every `@label` that points to it
  in the same commit — never leave a commit whose render is broken.
- Split unrelated work apart: adding a chapter and bumping a dependency are two
  commits, even when done in the same sitting.
- Do **not** commit build output. `_book/`, `_freeze/`, `.quarto/`, `*_files/`,
  and stray `*.quarto_ipynb` files are generated.
- If `pre-commit` enforces file-size limits, compress or down-scale images
  rather than raising the limit.

## Quick Reference

```text
chapter:  a new chapter (incl. registration in _quarto.yml)
edit:     substantive addition to an existing chapter
errata:   correct something that was wrong
ref:      glossary, notation, bibliography
toc:      reorder, split, merge chapters and parts
fig:      figures, diagrams, algorithm traces
typo:     typos and wording, no change in meaning

style:    SCSS, layout, fonts
feat:     new book capability (macros, filters, extensions)
fix:      bug fix in site code or a broken render
refactor: reorganisation, no feature/fix
perf:     faster build or render
build:    Quarto options, output formats, dependencies
ci:       CI workflows, pre-commit, deployment
docs:     repo documentation
chore:    housekeeping
revert:   revert a previous commit
```
