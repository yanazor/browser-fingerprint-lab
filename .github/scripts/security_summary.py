#!/usr/bin/env python3
"""Create a readable GitHub Actions summary from security scan reports."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    """Read a JSON report, returning None when it is absent or invalid."""
    if not path.is_file() or path.stat().st_size == 0:
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def escape_markdown(value: object) -> str:
    """Escape a value for one Markdown table cell."""
    text = str(value).replace("\n", " ").replace("\r", " ")
    return text.replace("|", r"\|").strip()


def truncate(value: object, limit: int = 180) -> str:
    """Return a compact single-line representation."""
    text = escape_markdown(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def pip_audit_section(report: Any) -> list[str]:
    """Build the pip-audit section."""
    lines = ["## pip-audit", ""]

    if report is None:
        return lines + [
            "⚠️ The pip-audit JSON report was not produced.",
            "",
        ]

    if isinstance(report, dict):
        dependencies = report.get("dependencies", [])
    elif isinstance(report, list):
        dependencies = report
    else:
        dependencies = []

    vulnerabilities: list[tuple[str, str, str, str]] = []

    for dependency in dependencies:
        if not isinstance(dependency, dict):
            continue

        package = str(dependency.get("name", "unknown"))
        version = str(dependency.get("version", "unknown"))

        for vulnerability in dependency.get("vulns", []) or []:
            if not isinstance(vulnerability, dict):
                continue

            vulnerability_id = str(
                vulnerability.get("id", "unknown")
            )
            fixes = vulnerability.get("fix_versions", []) or []
            fix_text = ", ".join(str(item) for item in fixes) or "None listed"

            vulnerabilities.append(
                (package, version, vulnerability_id, fix_text)
            )

    if not vulnerabilities:
        return lines + [
            f"✅ No known vulnerabilities found across "
            f"{len(dependencies)} resolved packages.",
            "",
        ]

    lines.extend(
        [
            f"❌ Found **{len(vulnerabilities)}** known vulnerabilities.",
            "",
            "| Package | Version | Vulnerability | Fix versions |",
            "|---|---:|---|---|",
        ]
    )

    for package, version, vulnerability_id, fixes in vulnerabilities:
        lines.append(
            f"| {escape_markdown(package)} "
            f"| {escape_markdown(version)} "
            f"| {escape_markdown(vulnerability_id)} "
            f"| {escape_markdown(fixes)} |"
        )

    lines.append("")
    return lines


def bandit_section(report: Any) -> list[str]:
    """Build the Bandit section from a SARIF report."""
    lines = ["## Bandit", ""]

    if report is None:
        return lines + [
            "⚠️ The Bandit SARIF report was not produced.",
            "",
        ]

    findings: list[dict[str, str]] = []

    for run in report.get("runs", []) if isinstance(report, dict) else []:
        if not isinstance(run, dict):
            continue

        for result in run.get("results", []) or []:
            if not isinstance(result, dict):
                continue

            properties = result.get("properties", {}) or {}
            message = result.get("message", {}) or {}
            locations = result.get("locations", []) or []

            path = "unknown"
            line = "?"

            if locations and isinstance(locations[0], dict):
                physical = (
                    locations[0].get("physicalLocation", {}) or {}
                )
                artifact = physical.get("artifactLocation", {}) or {}
                region = physical.get("region", {}) or {}

                path = str(artifact.get("uri", "unknown"))
                line = str(region.get("startLine", "?"))

            findings.append(
                {
                    "rule": str(result.get("ruleId", "unknown")),
                    "severity": str(
                        properties.get(
                            "issue_severity",
                            result.get("level", "unknown"),
                        )
                    ),
                    "confidence": str(
                        properties.get("issue_confidence", "unknown")
                    ),
                    "location": f"{path}:{line}",
                    "message": str(message.get("text", "")),
                }
            )

    if not findings:
        return lines + [
            "✅ No active medium-or-higher Bandit findings.",
            "",
        ]

    lines.extend(
        [
            f"❌ Found **{len(findings)}** Bandit findings.",
            "",
            "| Rule | Severity | Confidence | Location | Message |",
            "|---|---|---|---|---|",
        ]
    )

    for finding in findings:
        lines.append(
            f"| {escape_markdown(finding['rule'])} "
            f"| {escape_markdown(finding['severity'])} "
            f"| {escape_markdown(finding['confidence'])} "
            f"| `{escape_markdown(finding['location'])}` "
            f"| {truncate(finding['message'])} |"
        )

    lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip-audit", type=Path, required=True)
    parser.add_argument("--bandit", type=Path, required=True)
    args = parser.parse_args()

    summary_path_raw = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path_raw:
        raise SystemExit("GITHUB_STEP_SUMMARY is not set.")

    summary_path = Path(summary_path_raw)
    pip_report = read_json(args.pip_audit)
    bandit_report = read_json(args.bandit)

    lines = [
        "# Python security checks",
        "",
        "Reports are also retained in the workflow logs. "
        "Bandit findings from trusted branch runs are uploaded "
        "to GitHub Code Scanning.",
        "",
    ]

    lines.extend(pip_audit_section(pip_report))
    lines.extend(bandit_section(bandit_report))

    summary_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
