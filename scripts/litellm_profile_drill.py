#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys


REQUIRED_PROFILE_KEYS = [
    "execution_mode",
    "litellm_base_url",
    "langfuse_host",
    "nanoclaw_endpoint",
]


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def validate_profile(doc: dict, profile_name: str):
    profiles = doc.get("profiles", {})
    profile = profiles.get(profile_name)
    if not profile:
        return {
            "profile": profile_name,
            "verdict": "fail",
            "reason": "profile_missing",
            "missing_keys": REQUIRED_PROFILE_KEYS,
            "profile_payload": None,
        }

    missing_keys = [k for k in REQUIRED_PROFILE_KEYS if k not in profile or not profile.get(k)]
    if missing_keys:
        return {
            "profile": profile_name,
            "verdict": "fail",
            "reason": "profile_keys_missing",
            "missing_keys": missing_keys,
            "profile_payload": profile,
        }

    return {
        "profile": profile_name,
        "verdict": "pass",
        "reason": "ok",
        "missing_keys": [],
        "profile_payload": profile,
    }


def main():
    parser = argparse.ArgumentParser(description="LiteLLM local/oracle profile drill")
    parser.add_argument(
        "--runtime-profile-file",
        default="../platform-planningops/planningops/config/runtime-profiles.json",
        help="Path to runtime profile catalog",
    )
    parser.add_argument(
        "--profiles",
        default="local,oracle_cloud",
        help="Comma-separated profile names to validate",
    )
    parser.add_argument(
        "--run-id",
        default=f"profile-drill-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
    )
    args = parser.parse_args()

    profile_path = Path(args.runtime_profile_file)
    if not profile_path.exists():
        print(f"runtime profile file not found: {profile_path}")
        return 2

    doc = json.loads(profile_path.read_text(encoding="utf-8"))
    profile_names = [x.strip() for x in args.profiles.split(",") if x.strip()]
    checks = [validate_profile(doc, name) for name in profile_names]
    failed = [c for c in checks if c["verdict"] != "pass"]

    report = {
        "generated_at_utc": now_utc(),
        "run_id": args.run_id,
        "runtime_profile_file": str(profile_path),
        "checks": checks,
        "verdict": "pass" if not failed else "fail",
    }

    out = Path(f"artifacts/launcher/{args.run_id}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print(f"report written: {out}")
    print(f"profiles={','.join(profile_names)} verdict={report['verdict']}")

    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
