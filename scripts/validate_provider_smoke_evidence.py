#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

from provider_smoke_contract import validate_report


DEFAULT_SCHEMA = Path("contracts/c4-provider-invocation-artifact.schema.json")
DEFAULT_TAXONOMY = Path("config/provider-reason-taxonomy.json")


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Validate provider smoke evidence against schema and reason taxonomy")
    parser.add_argument("--report", required=True)
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--taxonomy", default=str(DEFAULT_TAXONOMY))
    parser.add_argument("--output", default="runtime-artifacts/validation/provider-smoke-evidence-report.json")
    args = parser.parse_args()

    report_doc = load_json(Path(args.report))
    errors = []
    try:
        validate_report(report_doc, Path(args.schema), Path(args.taxonomy))
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))

    verdict = "pass" if not errors else "fail"
    payload = {
        "generated_at_utc": now_utc(),
        "report_path": args.report,
        "schema_path": args.schema,
        "taxonomy_path": args.taxonomy,
        "error_count": len(errors),
        "errors": errors,
        "verdict": verdict,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"report written: {out}")
    print(f"verdict={verdict} error_count={len(errors)}")
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
