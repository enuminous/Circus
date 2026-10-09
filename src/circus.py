#!/usr/bin/env python3
"""CIRCUS report gate checker. Checks declared gate logic, not scientific truth."""
import json, sys
from pathlib import Path


def decide(report):
    pipeline = report.get("pipeline", [])
    deps = report.get("dependencies", [])
    risks = report.get("risks", [])
    checks = report.get("independent_checks", [])
    missing_material = any(p.get("provenance_status") != "documented" for p in pipeline if p.get("stage") in {"definition", "data_selection", "labels", "scoring", "validation"})
    material_na = any(r.get("materiality") == "material" and r.get("status") == "na" for r in risks)
    material_unknown = any(d.get("materiality") == "unknown" for d in deps) or any(r.get("materiality") == "unknown" for r in risks)
    feedback = any(d.get("materiality") == "material" and d.get("feedback") is True for d in deps)
    risk_open = any(r.get("materiality") == "material" and r.get("status") in {"present", "unresolved", "na"} for r in risks)
    check_bad = any(c.get("status") == "failed" for c in checks)
    checks_incomplete = any(c.get("status") != "passed" or not c.get("frozen") or not c.get("independently_sourced") for c in checks)
    if feedback or risk_open or check_bad:
        return "FAIL"
    if missing_material or material_na or material_unknown or checks_incomplete or not checks:
        return "N/A"
    return "PASS"


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/circus.py REPORT.json", file=sys.stderr)
        return 2
    report = json.loads(Path(sys.argv[1]).read_text())
    if report.get("animal") != "CIRCUS":
        print("ERROR: animal must be CIRCUS", file=sys.stderr)
        return 2
    actual = decide(report)
    declared = report.get("decision")
    print(f"declared={declared} computed={actual}")
    if actual != declared:
        print("GATE MISMATCH", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
