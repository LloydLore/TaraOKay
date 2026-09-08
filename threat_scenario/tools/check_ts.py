#!/usr/bin/env python3
"""Validate threat scenario catalogues for the threat_scenario skill.

Checks performed:
- TS headers use TS-[DOMAIN]-[NNN] and are unique.
- Core required sections are present.
- Target Asset contains an AST-ID.
- Linked DS-IDs exist in an optional damage scenario catalogue.
- Referenced AST-IDs exist in an optional asset list.
- AFR includes all 5 factors and the factor sum matches the total.
- Titles stay under 80 characters.
- No unresolved placeholders remain.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DOMAIN_RE = r"(?:CAN|OTA|EXT|BCK|IVI|IMM|ADAS|CCU)"
TS_HEADER_RE = re.compile(rf"^#{{2,3}}\s+(TS-{DOMAIN_RE}-\d{{3}}):\s+(.+?)\s*$", re.MULTILINE)
AST_RE = re.compile(r"\bAST-[A-Z]{2,3}-\d{3}\b")
DS_RE = re.compile(rf"\bDS-{DOMAIN_RE}-\d{{3}}\b")
PLACEHOLDER_RE = re.compile(r"\[(?:TODO|TBD|FIXME|PLACEHOLDER)\]|\{\{[A-Z0-9_]+\}\}", re.IGNORECASE)
AFR_TOTAL_RE = re.compile(r"AFR:\s*(\d{1,2})\s*\((Very Low|Low|Moderate|High)\)")
AFR_FACTOR_RE = re.compile(
    r"-\s*(Elapsed Time|Specialist Expertise|Knowledge of Item|Window of Opportunity|Equipment):\s*([0-3])\s*\(([^)]+)\)\s*-\s*(.+)"
)

CORE_SECTIONS = (
    "**Threat Description**:",
    "**Target Asset**:",
    "**Attack Surface / Entry Point**:",
    "**STRIDE Category**:",
    "**Damage Scenario Categories**:",
    "**Attack Feasibility Rating (AFR)**:",
    "**CIA Triad**:",
    "**Affected Vehicle Systems**:",
)

OPTIONAL_SECTION_PREFIXES = (
    "**UN R155 Annex 5 Reference**",
    "**MITRE ATT&CK Reference**",
    "**OWASP Reference**",
    "**Real-world Examples / CVEs**",
    "**Last Updated**",
    "**Confidence Level**",
    "**Attack Vector**",
)


@dataclass(frozen=True)
class Scenario:
    ts_id: str
    title: str
    body: str
    line: int


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def load_ids(path: Path | None, pattern: re.Pattern[str], label: str) -> set[str]:
    if path is None:
        return set()
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    return set(pattern.findall(path.read_text(encoding="utf-8")))


def parse_scenarios(text: str) -> list[Scenario]:
    matches = list(TS_HEADER_RE.finditer(text))
    scenarios: list[Scenario] = []
    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        scenarios.append(
            Scenario(
                ts_id=match.group(1),
                title=match.group(2).strip(),
                body=text[body_start:body_end],
                line=line_number(text, match.start()),
            )
        )
    return scenarios


def extract_section(body: str, heading: str) -> str:
    start = body.find(heading)
    if start == -1:
        return ""
    content_start = start + len(heading)
    next_heading = re.search(r"\n\*\*[^*]+\*\*:?", body[content_start:])
    if next_heading:
        return body[content_start : content_start + next_heading.start()].strip()
    return body[content_start:].strip()


def validate_afr(section: str, location: str, errors: list[str]) -> None:
    total_match = AFR_TOTAL_RE.search(section)
    if not total_match:
        errors.append(f"{location}: missing or invalid 'AFR: N (Band)' line.")
        return

    total = int(total_match.group(1))
    if not 0 <= total <= 15:
        errors.append(f"{location}: AFR total {total} must be in 0-15.")

    factors = AFR_FACTOR_RE.findall(section)
    factor_map = {name: int(score) for name, score, _label, _why in factors}
    expected_names = {
        "Elapsed Time",
        "Specialist Expertise",
        "Knowledge of Item",
        "Window of Opportunity",
        "Equipment",
    }
    missing = expected_names - set(factor_map)
    if missing:
        errors.append(f"{location}: missing AFR factors: {', '.join(sorted(missing))}.")
        return

    factor_sum = sum(factor_map.values())
    if factor_sum != total:
        errors.append(f"{location}: AFR total {total} != sum of factor scores {factor_sum}.")


def validate(text: str, asset_ids: set[str], ds_ids: set[str]) -> list[str]:
    errors: list[str] = []
    scenarios = parse_scenarios(text)
    if not scenarios:
        errors.append("No threat scenario entries found; expected headers like '## TS-IVI-001: Title' or '### TS-IVI-001: Title'.")
        return errors

    seen: dict[str, int] = {}
    for scenario in scenarios:
        location = f"{scenario.ts_id} (line {scenario.line})"

        if scenario.ts_id in seen:
            errors.append(f"{location}: duplicate TS-ID; first seen on line {seen[scenario.ts_id]}.")
        else:
            seen[scenario.ts_id] = scenario.line

        if len(scenario.title) > 80:
            errors.append(f"{location}: title exceeds 80 characters.")

        if PLACEHOLDER_RE.search(scenario.body):
            errors.append(f"{location}: contains unresolved placeholder text.")

        for section in CORE_SECTIONS:
            if section not in scenario.body:
                errors.append(f"{location}: missing required section {section!r}.")

        target_asset = extract_section(scenario.body, "**Target Asset**:")
        target_asset_ids = AST_RE.findall(target_asset)
        if not target_asset_ids:
            errors.append(f"{location}: Target Asset must contain at least one AST-ID.")
        elif asset_ids and target_asset_ids[0] not in asset_ids:
            errors.append(f"{location}: target asset {target_asset_ids[0]} not found in provided asset list.")

        damage_section = extract_section(scenario.body, "**Damage Scenario Categories**:")
        linked_ds_ids = sorted(set(DS_RE.findall(damage_section)))
        if not linked_ds_ids:
            errors.append(f"{location}: Damage Scenario Categories must include at least one DS-ID.")
        elif ds_ids:
            for ds_id in linked_ds_ids:
                if ds_id not in ds_ids:
                    errors.append(f"{location}: linked damage scenario {ds_id} not found in provided damage catalogue.")

        afr_section = extract_section(scenario.body, "**Attack Feasibility Rating (AFR)**:")
        validate_afr(afr_section, location, errors)

        affected_section = extract_section(scenario.body, "**Affected Vehicle Systems**:")
        affected_lines = [line for line in affected_section.splitlines() if line.strip().startswith("-")]
        if not affected_lines:
            errors.append(f"{location}: Affected Vehicle Systems must contain at least one bullet item.")

        if asset_ids:
            for ast_id in sorted(set(AST_RE.findall(affected_section))):
                if ast_id not in asset_ids:
                    errors.append(f"{location}: affected-system AST-ID {ast_id} not found in provided asset list.")

        for heading in OPTIONAL_SECTION_PREFIXES:
            if heading in scenario.body:
                section = extract_section(scenario.body, heading if heading.endswith(":") else heading + ":")
                if not section:
                    errors.append(f"{location}: optional section {heading!r} is present but empty.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a threat scenario Markdown catalogue.")
    parser.add_argument("ts_file", type=Path, help="Path to data/ts.md or another TS catalogue Markdown file")
    parser.add_argument("--asset-list", type=Path, default=None, help="Optional path to data/asset_list.md for AST-ID validation")
    parser.add_argument("--ds", type=Path, default=None, help="Optional path to data/ds.md for DS-ID validation")
    args = parser.parse_args()

    text = args.ts_file.read_text(encoding="utf-8")
    try:
        asset_ids = load_ids(args.asset_list, AST_RE, "asset list")
        ds_ids = load_ids(args.ds, DS_RE, "damage scenario catalogue")
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate(text, asset_ids, ds_ids)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.ts_file} passed threat scenario validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
