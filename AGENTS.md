# Agent Operating Rules

These rules apply to scheduled ChatGPT tasks and any other automated editor.
They supplement `TIMELINE_POLICY.md` and are binding for repository writes.

## General procedure

1. Determine the previous fully completed ISO week, Monday through Sunday.
2. Inspect only changes within that date window.
3. Deduplicate changes shared by an upstream repository and a personal fork.
4. Apply the materiality, confidentiality, and plain-language rules before
   drafting text.
5. Validate all changed data with `python scripts/validate_timeline.py`.
6. Stop without opening a pull request when validation fails or required source
   access is unavailable.

## Public-summary drafting procedure

1. Identify the material technical result from the source repositories without
   copying commit messages into the public text.
2. Translate that result into a project-level statement that answers:
   - What can CogniFlow now do, or what became easier or clearer?
   - Why is this relevant to users, researchers, or future development?
3. Replace internal architecture names and specialist terminology with familiar
   wording. When a technical term is essential, explain it immediately.
4. Retain at least one concrete capability or effect so that the summary does not
   become vague or promotional.
5. Rewrite any sentence that contains several unexplained technical concepts.
6. Apply the same language standard to contributor summaries and the final
   consolidated week entry.
7. Use understandable public-facing area labels wherever possible.

A summary fails the drafting check when a reader outside software development
cannot explain its main point after one reading, or when the wording could apply
to almost any software project.

## Ricardo task boundary

The Ricardo task may create or update only:

`data/contributions/<YEAR>/W<WEEK>/ricardo.json`

It opens a pull request to `weekly`. It must not modify Gerrit's contribution,
the consolidated week file, the manifest, website files, schemas, policies, or
scripts.

## Gerrit task boundary

The Gerrit task may:

- review and integrate Ricardo's contribution for the reporting week;
- create or update `gerrit.json`;
- create or update the consolidated `data/weeks/<YEAR>-W<WEEK>.json`;
- update `data/weeks/index.json`;
- open the final pull request from `weekly` to `main`.

The final pull request must not be merged automatically.

## Data conventions

- Use ISO week identifiers in the form `YYYY-Www`, for example `2026-W31`.
- Use ISO dates in the form `YYYY-MM-DD`.
- Use lowercase contributor IDs: `gerrit` and `ricardo`.
- Keep `areas` concise, lowercase, reusable across weeks, and understandable to
  non-specialists where possible.
- The consolidated summary must read as one project-level narrative and must
  not attribute separate sentences to individual contributors.

## Prohibited repository changes

Automated tasks must not:

- add or modify GitHub Actions workflows;
- alter branch protection or repository settings;
- publish private source metadata;
- change schemas or policy files as part of a routine weekly update;
- merge the final publication pull request.
