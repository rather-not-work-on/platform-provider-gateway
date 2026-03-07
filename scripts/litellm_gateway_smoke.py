#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

from provider_smoke_contract import load_json, validate_report


DEFAULT_SCHEMA = Path("contracts/c4-provider-invocation-artifact.schema.json")
DEFAULT_TAXONOMY = Path("config/provider-reason-taxonomy.json")


def now_utc():
    return datetime.now(timezone.utc).isoformat()


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
                "estimated_cost_usd": 0.0022,
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
                    "estimated_cost_usd": 0.0,
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
                "estimated_cost_usd": 0.0,
            },
            {
                "provider": fb["provider"],
                "model": fb["model"],
                "latency_ms": 380,
                "status": "success",
                "estimated_cost_usd": 0.0014,
            },
        ]

    if scenario == "contract_violation":
        # Intentionally malformed attempt payload (missing provider/model)
        return [
            {
                "latency_ms": 10,
                "status": "failed",
                "error_code": "malformed_invocation",
                "estimated_cost_usd": 0.0,
            }
        ]

    raise ValueError(f"unknown scenario: {scenario}")


def normalize_attempts(raw_attempts):
    normalized = []
    missing_fields = []
    fallback_used = False
    for idx, attempt in enumerate(raw_attempts):
        missing = validate_invocation_payload(attempt)
        if missing:
            missing_fields.append({"attempt_index": idx, "missing_fields": missing})
        route_role = "primary" if idx == 0 else "fallback"
        if route_role == "fallback":
            fallback_used = True
        row = {
            "attempt_index": idx,
            "route_role": route_role,
            "provider": attempt.get("provider"),
            "model": attempt.get("model"),
            "latency_ms": int(attempt.get("latency_ms", 0)),
            "status": attempt.get("status", "failed"),
            "validation_status": "invalid" if missing else "valid",
            "missing_fields": missing,
            "estimated_cost_usd": float(attempt.get("estimated_cost_usd", 0.0)),
        }
        error_code = attempt.get("error_code")
        if error_code:
            row["error_code"] = error_code
        normalized.append(row)
    return normalized, missing_fields, fallback_used


def resolve_reason_code(missing_fields, attempts):
    if missing_fields:
        return "contract_violation"
    success_count = sum(1 for row in attempts if row["status"] == "success")
    failure_count = sum(1 for row in attempts if row["status"] == "failed")
    if success_count and failure_count:
        return "fallback_recovered"
    if success_count:
        return "ok"
    return "all_providers_failed"


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
    parser.add_argument(
        "--routing-profile",
        default="example-local",
        help="logical routing profile name recorded in smoke evidence",
    )
    parser.add_argument(
        "--output-dir",
        default="runtime-artifacts/smoke",
        help="directory where smoke report is written",
    )
    args = parser.parse_args()

    cfg = load_json(Path(args.config))
    taxonomy = load_json(DEFAULT_TAXONOMY)
    routing = cfg.get("routing", {})
    run_id = args.run_id or f"smoke-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    raw_attempts = scenario_attempts(routing, args.scenario)
    attempts, missing_fields, fallback_used = normalize_attempts(raw_attempts)
    reason_code = resolve_reason_code(missing_fields, attempts)
    verdict = "pass" if reason_code in {"ok", "fallback_recovered"} else "fail"
    success_count = sum(1 for row in attempts if row["status"] == "success")
    failure_count = sum(1 for row in attempts if row["status"] == "failed")
    selected_provider = next((row["provider"] for row in attempts if row["status"] == "success"), None)

    report = {
        "generated_at_utc": now_utc(),
        "run_id": run_id,
        "routing_profile": args.routing_profile,
        "scenario": args.scenario,
        "verdict": verdict,
        "reason_code": reason_code,
        "reason_taxonomy_version": int(taxonomy.get("version", 0)),
        "summary": {
            "attempt_count": len(attempts),
            "success_count": success_count,
            "failure_count": failure_count,
            "total_latency_ms": sum(row["latency_ms"] for row in attempts),
            "total_estimated_cost_usd": round(sum(row["estimated_cost_usd"] for row in attempts), 6),
            "fallback_used": fallback_used,
            "selected_provider": selected_provider,
        },
        "attempts": attempts,
        "missing_fields": missing_fields,
    }

    validate_report(report, DEFAULT_SCHEMA, DEFAULT_TAXONOMY)

    out = Path(args.output_dir) / f"{run_id}-{args.scenario}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print(f"report written: {out}")
    print(f"scenario={args.scenario} verdict={verdict} reason_code={reason_code} attempts={len(attempts)}")

    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
