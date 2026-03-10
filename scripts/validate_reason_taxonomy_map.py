#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ALLOWED_SEVERITY = {"info", "warn", "error"}
ALLOWED_ACTION = {
    "none",
    "review_primary_provider_health",
    "fix_request_shape",
    "check_provider_outage_or_timeout",
}


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")


def validate_map_doc(map_doc: dict, taxonomy_doc: dict):
    errors = []

    taxonomy_codes = taxonomy_doc.get("reason_codes") if isinstance(taxonomy_doc, dict) else {}
    map_codes = map_doc.get("reason_code_map") if isinstance(map_doc, dict) else {}

    if not isinstance(taxonomy_codes, dict) or not taxonomy_codes:
        errors.append("taxonomy reason_codes must be a non-empty object")
        taxonomy_codes = {}
    if not isinstance(map_codes, dict) or not map_codes:
        errors.append("reason_code_map must be a non-empty object")
        map_codes = {}

    if map_doc.get("taxonomy_source") != "config/provider-reason-taxonomy.json":
        errors.append("taxonomy_source must be config/provider-reason-taxonomy.json")

    if map_doc.get("taxonomy_version") != taxonomy_doc.get("version"):
        errors.append(
            f"taxonomy_version mismatch: map={map_doc.get('taxonomy_version')} taxonomy={taxonomy_doc.get('version')}"
        )

    missing_codes = sorted(set(taxonomy_codes) - set(map_codes))
    extra_codes = sorted(set(map_codes) - set(taxonomy_codes))
    if missing_codes:
        errors.append(f"missing reason_code_map entries={missing_codes}")
    if extra_codes:
        errors.append(f"unknown reason_code_map entries={extra_codes}")

    for code, row in map_codes.items():
        if not isinstance(row, dict):
            errors.append(f"reason_code_map[{code}] must be an object")
            continue

        severity = row.get("severity")
        if severity not in ALLOWED_SEVERITY:
            errors.append(f"reason_code_map[{code}].severity invalid: {severity}")

        retryable = row.get("retryable")
        if not isinstance(retryable, bool):
            errors.append(f"reason_code_map[{code}].retryable must be boolean")

        action = row.get("operator_action")
        if action not in ALLOWED_ACTION:
            errors.append(f"reason_code_map[{code}].operator_action invalid: {action}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate provider reason taxonomy map")
    parser.add_argument("--map", default="config/provider-reason-taxonomy-map.json")
    parser.add_argument("--taxonomy", default="config/provider-reason-taxonomy.json")
    parser.add_argument("--output", default="runtime-artifacts/validation/provider-reason-taxonomy-map-report.json")
    args = parser.parse_args()

    map_path = Path(args.map)
    taxonomy_path = Path(args.taxonomy)

    map_doc = load_json(map_path)
    taxonomy_doc = load_json(taxonomy_path)

    errors = validate_map_doc(map_doc, taxonomy_doc)
    verdict = "pass" if not errors else "fail"

    report = {
        "generated_at_utc": now_utc(),
        "verdict": verdict,
        "map_path": args.map,
        "taxonomy_path": args.taxonomy,
        "error_count": len(errors),
        "errors": errors,
    }
    save_json(Path(args.output), report)

    print(f"report written: {args.output}")
    print(f"verdict={verdict} error_count={len(errors)}")
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
