# CogniFlow Timeline Policy

## Purpose

The timeline communicates meaningful CogniFlow development progress in a form
that is understandable outside the development team. It is not a commit log,
release ledger, validation report, or mirror of private repositories.

## Editorial rules

- Use English.
- Publish one consolidated entry per ISO week when material progress occurred.
- Keep the public summary to one or two sentences.
- Describe outcomes, capabilities, architectural decisions, or user-visible
  improvements rather than individual commits.
- Combine overlapping work into one coherent project-level narrative.
- Use neutral, factual language and avoid promotional claims.
- Do not claim that something is stable, validated, production-ready, released,
  or publicly available unless that status is supported by public evidence.

## Confidentiality rules

Never publish:

- links to private repositories;
- private pull-request or issue numbers;
- commit SHAs;
- internal branch names;
- local paths, usernames, credentials, tokens, or secrets;
- unpublished package versions;
- internal review language or validation evidence;
- implementation details that would expose confidential work.

Public repository links may be included only when they directly support the
published statement.

## Materiality rules

Normally exclude:

- merge-only commits;
- formatting and spelling corrections;
- generated files and evidence archives;
- lockfile-only changes;
- routine dependency or version updates;
- mechanical refactoring without a material capability change;
- abandoned or reverted work.

Several related changes may be summarized as one outcome. A week without
material progress receives no placeholder entry.

## Data ownership

- Contributors may modify only their own contribution file.
- The Gerrit consolidation task owns the final weekly entry and manifest update.
- Published week files are changed only through a reviewed pull request to
  `main`.
