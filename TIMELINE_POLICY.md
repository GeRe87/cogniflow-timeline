# CogniFlow Timeline Policy

## Purpose

The timeline communicates meaningful CogniFlow development progress in a form
that is understandable outside the development team. It is not a commit log,
release ledger, validation report, or mirror of private repositories.

## Intended audience

The timeline is written for interested members of the public. Do not assume
knowledge of software architecture, data engineering, laboratory automation, or
analytical chemistry. Common words such as software, data, laboratory, and
research may be used without explanation.

## Editorial rules

- Use English.
- Publish one consolidated entry per ISO week when material progress occurred.
- Keep the public summary to one or two short sentences.
- Describe the project-level result rather than individual commits or internal
  implementation steps.
- Begin with what CogniFlow can now do, what became easier or clearer, or which
  concrete problem was addressed.
- Include enough detail to distinguish the update from a generic statement such
  as "the platform was improved".
- Combine overlapping work into one coherent project-level narrative.
- Use neutral, factual language and avoid promotional claims.
- Do not claim that something is stable, validated, production-ready, released,
  or publicly available unless that status is supported by public evidence.

## Plain-language requirements

- Prefer familiar words, short sentences, and active constructions.
- Replace internal architecture terms with their practical meaning whenever
  possible.
- Use a specialist term only when it adds essential precision, and explain it in
  plain language in the same sentence.
- Do not stack unexplained technical terms, abbreviations, or internal component
  names in one sentence.
- Do not merely list components, modules, interfaces, or architecture changes.
- State the practical relevance without overstating benefits that have not yet
  been demonstrated.
- Use public-facing `areas` labels where possible. Avoid internal subsystem names
  when a clear everyday label is available.

Before publication, a reader outside the project should be able to answer both:

1. What changed?
2. Why does that change matter for using or developing CogniFlow?

The summary must also remain specific. If the wording could describe almost any
software project, add one concrete capability, use case, or improvement.

Example:

- Too technical: "CogniFlow gained declarative profiles and capability-based
  artifact selection."
- Preferred: "CogniFlow can now select the software tools needed for different
  uses, making installation easier to adapt to different environments."

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
