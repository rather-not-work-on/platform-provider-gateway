#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_invocation_payload(payload: dict):
    required = ["provider", "model", "latency_ms", "status"]
    missing = [k for k in required if k not in payload]
    return missing


def scenario_attempts(routing: dict, scenario: str):
    primary = routing["primary"]
    fallbacks = routing.get("fallbacks", [])

    if scenario == "primary_success":
        return [
            {
                "provider": primary["provider"],
                "model": primary["model"],
                "latency_ms": 220,
                "status": "success",
            }
        ]

    if scenario == "primary_fail_fallback_success":
        if not fallbacks:
            return [
                {
                    "provider": primary["provider"],
                    "model": primary["model"],
                    "latency_ms": 45000,
                    "status": "failed",
                    "error_code": "timeout",
                }
            ]
        fb = fallbacks[0]
        return [
            {
                "provider": primary["provider"],
                "model": primary["model"],
                "latency_ms": 45000,
                "status": "failed",
                "error_code": "timeout",
            },
            {
                "provider": fb["provider"],
                "model": fb["model"],
                "latency_ms": 380,
                "status": "success",
            },
        ]

    if scenario == "contract_violation":
        # Intentionally malformed attempt payload (missing provider/model)
        return [
            {
                "latency_ms": 10,
                "status": "failed",
                "error_code": "malformed_invocation",
            }
        ]

    raise ValueError(f"unknown scenario: {scenario}")


def main():
    parser = argparse.ArgumentParser(description="LiteLLM gateway smoke scenarios")
    parser.add_argument(
        "--config",
        default="config/provider-routing.example.json",
        help="routing config path",
    )
    parser.add_argument(
        "--scenario",
        choices=["primary_success", "primary_fail_fallback_success", "contract_violation"],
        default="primary_success",
    )
    parser.add_argument(
        "--run-id",
        default=None,
    )
    args = parser.parse_args()

    cfg = load_json(Path(args.config))
    routing = cfg.get("routing", {})
    run_id = args.run_id or f"smoke-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    attempts = scenario_attempts(routing, args.scenario)

    missing_fields = []
    for idx, a in enumerate(attempts):
        miss = validate_invocation_payload(a)
        if miss:
            missing_fields.append({"attempt_index": idx, "missing_fields": miss})

    if missing_fields:
        verdict = "fail"
        reason_code = "contract_violation"
    else:
        any_success = any(a.get("status") == "success" for a in attempts)
        verdict = "pass" if any_success else "fail"
        reason_code = "ok" if any_success else "all_providers_failed"

    report = {
        "generated_at_utc": now_utc(),
        "run_id": run_id,
        "scenario": args.scenario,
        "verdict": verdict,
        "reason_code": reason_code,
        "attempts": attempts,
        "missing_fields": missing_fields,
    }

    out = Path(f"artifacts/smoke/{run_id}-{args.scenario}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print(f"report written: {out}")
    print(f"scenario={args.scenario} verdict={verdict} attempts={len(attempts)}")

    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
