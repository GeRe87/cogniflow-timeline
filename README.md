# CogniFlow Development Timeline

A public, human-readable timeline of material CogniFlow development outcomes.
The repository receives short weekly summaries derived from private development
repositories without exposing private links, commit identifiers, branch names,
or implementation details that are not intended for publication.

## Repository model

- `main` contains the reviewed public timeline and is the GitHub Pages source.
- `weekly` is the integration branch for weekly contributions.
- Contributor branches add one author-specific contribution for one ISO week.
- A consolidated week entry is reviewed through a pull request from `weekly` to
  `main` before publication.

## Content layout

- `data/contributions/<YEAR>/W<WEEK>/<author>.json`: author-specific draft input.
- `data/weeks/<YEAR>-W<WEEK>.json`: harmonized public weekly entry.
- `data/weeks/index.json`: ordered manifest consumed by the website.
- `schemas/`: JSON Schemas for contributions and published weeks.
- `scripts/validate_timeline.py`: dependency-free local validation.
- `TIMELINE_POLICY.md`: editorial and confidentiality rules.
- `AGENTS.md`: operating rules for scheduled ChatGPT tasks.

## Local validation

```powershell
python scripts/validate_timeline.py
```

## GitHub Pages

This repository intentionally uses no GitHub Actions. After merging the initial
setup, configure GitHub Pages once in the repository settings:

1. Open **Settings → Pages**.
2. Select **Deploy from a branch**.
3. Select branch **main** and folder **/(root)**.
4. Save.

The root `index.html` reads the public timeline directly from `data/weeks/`.

## Weekly publication flow

1. Ricardo adds `data/contributions/<YEAR>/W<WEEK>/ricardo.json` through a pull
   request to `weekly`.
2. Gerrit adds `gerrit.json`, harmonizes the final week entry, updates
   `data/weeks/index.json`, and opens a pull request from `weekly` to `main`.
3. The final pull request is reviewed and merged manually.

See `AGENTS.md` and `TIMELINE_POLICY.md` for the binding rules.
