from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WEEK_PATTERN = re.compile(r"^(\d{4})-W(\d{2})$")
AREA_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
AUTHORS = {"gerrit", "ricardo"}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def require_exact_keys(data: dict[str, Any], expected: set[str], path: Path) -> None:
    actual = set(data)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValidationError(f"{path}: key mismatch; missing={missing}, extra={extra}")


def parse_week(value: Any, path: Path) -> tuple[int, int]:
    if not isinstance(value, str) or not (match := WEEK_PATTERN.fullmatch(value)):
        raise ValidationError(f"{path}: invalid ISO week {value!r}")
    year, week = int(match.group(1)), int(match.group(2))
    try:
        date.fromisocalendar(year, week, 1)
    except ValueError as exc:
        raise ValidationError(f"{path}: impossible ISO week {value!r}") from exc
    return year, week


def parse_date(value: Any, path: Path, field: str) -> date:
    if not isinstance(value, str):
        raise ValidationError(f"{path}: {field} must be a date string")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"{path}: invalid {field} date {value!r}") from exc


def validate_summary(value: Any, path: Path) -> None:
    if not isinstance(value, str):
        raise ValidationError(f"{path}: summary must be a string")
    normalized = " ".join(value.split())
    if not 40 <= len(normalized) <= 420:
        raise ValidationError(f"{path}: summary length must be 40-420 characters")
    if any(token in normalized.lower() for token in ("github.com/odea-project/cogniflow-playground", "commit sha", "refs/heads/")):
        raise ValidationError(f"{path}: summary appears to expose private source metadata")


def validate_areas(value: Any, path: Path, maximum: int) -> None:
    if not isinstance(value, list) or not 1 <= len(value) <= maximum:
        raise ValidationError(f"{path}: areas must contain 1-{maximum} entries")
    if len(value) != len(set(value)):
        raise ValidationError(f"{path}: areas must be unique")
    for area in value:
        if not isinstance(area, str) or not AREA_PATTERN.fullmatch(area):
            raise ValidationError(f"{path}: invalid area {area!r}")


def expected_window(week_id: str, path: Path) -> tuple[date, date]:
    year, week = parse_week(week_id, path)
    start = date.fromisocalendar(year, week, 1)
    return start, start + timedelta(days=6)


def validate_contribution(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top-level value must be an object")
    require_exact_keys(data, {"week", "author", "source_window", "summary", "areas"}, path)
    start_expected, end_expected = expected_window(data["week"], path)
    author = data["author"]
    if author not in AUTHORS:
        raise ValidationError(f"{path}: invalid author {author!r}")
    if path.stem != author:
        raise ValidationError(f"{path}: filename must match author")
    window = data["source_window"]
    if not isinstance(window, dict):
        raise ValidationError(f"{path}: source_window must be an object")
    require_exact_keys(window, {"start", "end"}, path)
    start = parse_date(window["start"], path, "source_window.start")
    end = parse_date(window["end"], path, "source_window.end")
    if (start, end) != (start_expected, end_expected):
        raise ValidationError(f"{path}: source window does not match ISO week")
    validate_summary(data["summary"], path)
    validate_areas(data["areas"], path, 6)


def validate_week(path: Path) -> str:
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top-level value must be an object")
    require_exact_keys(data, {"week", "start", "end", "summary", "areas", "contributors"}, path)
    week_id = data["week"]
    if path.stem != week_id:
        raise ValidationError(f"{path}: filename must match week")
    start_expected, end_expected = expected_window(week_id, path)
    start = parse_date(data["start"], path, "start")
    end = parse_date(data["end"], path, "end")
    if (start, end) != (start_expected, end_expected):
        raise ValidationError(f"{path}: dates do not match ISO week")
    validate_summary(data["summary"], path)
    validate_areas(data["areas"], path, 8)
    contributors = data["contributors"]
    if not isinstance(contributors, list) or not 1 <= len(contributors) <= 2:
        raise ValidationError(f"{path}: contributors must contain 1-2 entries")
    if len(contributors) != len(set(contributors)) or not set(contributors) <= AUTHORS:
        raise ValidationError(f"{path}: invalid or duplicate contributors")
    return week_id


def validate_manifest(valid_week_ids: set[str]) -> None:
    path = ROOT / "data" / "weeks" / "index.json"
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top-level value must be an object")
    require_exact_keys(data, {"schema_version", "weeks"}, path)
    if data["schema_version"] != 1:
        raise ValidationError(f"{path}: schema_version must be 1")
    weeks = data["weeks"]
    if not isinstance(weeks, list) or not all(isinstance(item, str) for item in weeks):
        raise ValidationError(f"{path}: weeks must be a string array")
    if len(weeks) != len(set(weeks)):
        raise ValidationError(f"{path}: weeks must be unique")
    if set(weeks) != valid_week_ids:
        raise ValidationError(f"{path}: manifest entries do not match week files")
    expected_order = sorted(weeks, reverse=True)
    if weeks != expected_order:
        raise ValidationError(f"{path}: weeks must be ordered newest first")


def main() -> int:
    try:
        for path in sorted((ROOT / "data" / "contributions").glob("[0-9][0-9][0-9][0-9]/W[0-9][0-9]/*.json")):
            validate_contribution(path)

        week_ids: set[str] = set()
        for path in sorted((ROOT / "data" / "weeks").glob("[0-9][0-9][0-9][0-9]-W[0-9][0-9].json")):
            week_ids.add(validate_week(path))

        validate_manifest(week_ids)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Timeline validation passed: {len(week_ids)} published week(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
