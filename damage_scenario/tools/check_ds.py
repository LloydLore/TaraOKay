#!/usr/bin/env python3
"""Validate damage scenario catalogues for the damage_scenario skill.

Checks performed:
- DS headers use DS-[DOMAIN]-[NNN] and are unique.
- Titles and final DS sections avoid threat/attack-method vocabulary.
- Required sections are present.
- SFOP scores are integers in [1, 4].
- Impact Score equals max(Safety, Financial, Operational, Privacy).
- Referenced AST-IDs exist in an optional asset list.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DOMAIN_RE = r"(?:CAN|OTA|EXT|BCK|IVI|IMM|ADAS|CCU)"
DS_HEADER_RE = re.compile(rf"^###\s+(DS-{DOMAIN_RE}-\d{{3}}):\s+(.+?)\s*$", re.MULTILINE)
AST_RE = re.compile(r"\bAST-[A-Z]{3}-\d{3}\b")
IMPACT_RE = re.compile(r"\*\*Impact Score\*\*:\s*([1-4])\s*\(([^)]+)\)")
OVERALL_RE = re.compile(r"Overall Impact:\s*([1-4])\s*\(([^)]+)\)\s*\[max of S=([1-4]), F=([1-4]), O=([1-4]), P=([1-4])\]")
DIMENSION_RE_TEMPLATE = r"-\s*{name}:\s*([1-4])\s*\(([^)]+)\)"
PLACEHOLDER_RE = re.compile(r"\[(?:TODO|TBD|FIXME|PLACEHOLDER)\]", re.IGNORECASE)

THREAT_WORD_RE = re.compile(
    r"\b(attack|attacker|exploit|vulnerability|injection|spoofing|spoof|malware|ransomware|dos|ddos|denial of service|cve)\b",
    re.IGNORECASE,
)

REQUIRED_SECTIONS = (
    "**Linked Assets**:",
    "**SFOP Dimensions Affected**:",
    "**Impact Score**:",
    "Overall Impact:",
    "**Assessment Context**:",
    "**Rationale**:",
)


@dataclass(frozen=True)
class Scenario:
    ds_id: str
    title: str
    body: str
    line: int


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def load_asset_ids(path: Path | None) -> set[str]:
    if path is None:
        return set()
    if not path.exists():
        raise FileNotFoundError(f"asset list not found: {path}")
    return set(AST_RE.findall(path.read_text(encoding="utf-8")))


def parse_scenarios(text: str) -> list[Scenario]:
    matches = list(DS_HEADER_RE.finditer(text))
    scenarios: list[Scenario] = []
    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        scenarios.append(
            Scenario(
                ds_id=match.group(1),
                title=match.group(2).strip(),
                body=text[body_start:body_end],
                line=line_number(text, match.start()),
            )
        )
    return scenarios


def find_dimension_score(body: str, name: str) -> int | None:
    match = re.search(DIMENSION_RE_TEMPLATE.format(name=name), body)
    if not match:
        return None
    return int(match.group(1))


def final_ds_text(body: str) -> str:
    """Return the final DS entry text, excluding derivation notes if present."""
    markers = ["**Linked Assets**:", "**SFOP Dimensions Affected**:", "**Impact Score**:", "**Assessment Context**:", "**Rationale**:"]
    starts = [body.find(marker) for marker in markers if body.find(marker) != -1]
    if not starts:
        candidate = body
    else:
        candidate = body[min(starts):]
    separator = re.search(r"\n---\s*(?:\n|$)", candidate)
    if separator:
        return candidate[: separator.start()]
    return candidate


def validate(text: str, asset_ids: set[str]) -> list[str]:
    errors: list[str] = []
    scenarios = parse_scenarios(text)
    if not scenarios:
        errors.append("No damage scenario entries found; expected headers like '### DS-IVI-001: Title'.")
        return errors

    seen: dict[str, int] = {}
    for scenario in scenarios:
        location = f"{scenario.ds_id} (line {scenario.line})"

        if scenario.ds_id in seen:
            errors.append(f"{location}: duplicate DS-ID; first seen on line {seen[scenario.ds_id]}.")
        else:
            seen[scenario.ds_id] = scenario.line

        if THREAT_WORD_RE.search(scenario.title):
            errors.append(f"{location}: title contains threat/attack-method vocabulary: {scenario.title!r}.")

        body_threat = THREAT_WORD_RE.search(final_ds_text(scenario.body))
        if body_threat:
            errors.append(f"{location}: final DS entry contains threat/attack-method vocabulary: {body_threat.group(0)!r}.")

        if PLACEHOLDER_RE.search(scenario.body):
            errors.append(f"{location}: contains unresolved placeholder text such as [TODO]/[TBD].")

        for section in REQUIRED_SECTIONS:
            if section not in scenario.body:
                errors.append(f"{location}: missing required section {section!r}.")

        impact_match = IMPACT_RE.search(scenario.body)
        overall_match = OVERALL_RE.search(scenario.body)
        if not impact_match:
            errors.append(f"{location}: missing or invalid '**Impact Score**: N (Label)' line.")
        if not overall_match:
            errors.append(f"{location}: missing or invalid 'Overall Impact: N (...) [max of S=..., F=..., O=..., P=...]' line.")

        dim_scores: dict[str, int] = {}
        for label, name in (("S", "Safety"), ("F", "Financial"), ("O", "Operational"), ("P", "Privacy")):
            score = find_dimension_score(scenario.body, name)
            if score is None:
                errors.append(f"{location}: missing {name} score line under Impact Score.")
            else:
                dim_scores[label] = score

        if impact_match and dim_scores:
            impact = int(impact_match.group(1))
            expected = max(dim_scores.values())
            if impact != expected:
                errors.append(f"{location}: Impact Score {impact} != max dimension score {expected}.")

        if overall_match:
            overall = int(overall_match.group(1))
            listed = {
                "S": int(overall_match.group(3)),
                "F": int(overall_match.group(4)),
                "O": int(overall_match.group(5)),
                "P": int(overall_match.group(6)),
            }
            expected_overall = max(listed.values())
            if overall != expected_overall:
                errors.append(f"{location}: Overall Impact {overall} != max listed SFOP {expected_overall}.")
            for label, score in dim_scores.items():
                if listed.get(label) != score:
                    errors.append(f"{location}: Overall line {label}={listed.get(label)} does not match {label} score {score}.")

        if asset_ids:
            linked_asset_block = scenario.body.split("**SFOP Dimensions Affected**:", 1)[0]
            for ast_id in sorted(set(AST_RE.findall(linked_asset_block))):
                if ast_id not in asset_ids:
                    errors.append(f"{location}: linked asset {ast_id} not found in provided asset list.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a damage scenario Markdown catalogue.")
    parser.add_argument("ds_file", type=Path, help="Path to data/ds.md or another DS catalogue Markdown file")
    parser.add_argument("--asset-list", type=Path, default=None, help="Optional path to data/asset_list.md for AST-ID validation")
    args = parser.parse_args()

    text = args.ds_file.read_text(encoding="utf-8")
    try:
        asset_ids = load_asset_ids(args.asset_list)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate(text, asset_ids)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.ds_file} passed damage scenario validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
