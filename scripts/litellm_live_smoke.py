#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, env=env)


def python_first_env():
    env = os.environ.copy()
    python_bin = str(Path(sys.executable).resolve().parent)
    env["PATH"] = f"{python_bin}:{env.get('PATH', '')}"
    env["PYTHON_BIN"] = sys.executable
    return env


def main():
    parser = argparse.ArgumentParser(description="Run a launcher-backed LiteLLM local smoke wrapper")
    parser.add_argument(
        "--runtime-profile-file",
        default="../platform-planningops/planningops/config/runtime-profiles.json",
        help="Path to the shared runtime profile catalog",
    )
    parser.add_argument("--profile", default="local", help="Runtime profile name to validate")
    parser.add_argument("--launcher-mode", choices=["dry-run", "start"], default="start")
    parser.add_argument("--scenario", choices=["primary_success", "primary_fail_fallback_success"], default="primary_success")
    parser.add_argument(
        "--run-id",
        default=f"litellm-live-smoke-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional manifest path. Defaults to runtime-artifacts/live/<run_id>.json",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    runtime_profile_file = (repo_root / args.runtime_profile_file).resolve()
    if not runtime_profile_file.exists():
        raise SystemExit(f"runtime profile file not found: {runtime_profile_file}")

    env = python_first_env()
    launcher_run_id = f"{args.run_id}-launcher"
    launcher_report = repo_root / "runtime-artifacts" / "launcher" / f"{launcher_run_id}.json"
    smoke_report = repo_root / "runtime-artifacts" / "smoke" / f"{args.run_id}-{args.scenario}.json"
    validation_report = repo_root / "runtime-artifacts" / "validation" / f"{args.run_id}-{args.scenario}-validation.json"

    launcher = run(
        [
            "bash",
            "scripts/litellm_stack_launcher.sh",
            "--mode",
            args.launcher_mode,
            "--runtime-profile-file",
            str(runtime_profile_file),
            "--profiles",
            args.profile,
            "--run-id",
            launcher_run_id,
        ],
        cwd=repo_root,
        env=env,
    )

    smoke = run(
        [
            sys.executable,
            "scripts/litellm_gateway_smoke.py",
            "--scenario",
            args.scenario,
            "--run-id",
            args.run_id,
            "--routing-profile",
            args.profile,
            "--output-dir",
            "runtime-artifacts/smoke",
        ],
        cwd=repo_root,
        env=env,
    )

    validation = run(
        [
            sys.executable,
            "scripts/validate_provider_smoke_evidence.py",
            "--report",
            str(smoke_report),
            "--output",
            str(validation_report),
        ],
        cwd=repo_root,
        env=env,
    )

    if args.launcher_mode == "start":
        run(["bash", "scripts/litellm_stack_launcher.sh", "--mode", "stop"], cwd=repo_root, env=env)

    verdict = "pass" if launcher.returncode == 0 and smoke.returncode == 0 and validation.returncode == 0 else "fail"
    reason_code = "ok" if verdict == "pass" else "litellm_live_smoke_failed"
    report = {
        "generated_at_utc": now_utc(),
        "run_id": args.run_id,
        "runtime_profile_file": str(runtime_profile_file),
        "profile": args.profile,
        "launcher_mode_requested": args.launcher_mode,
        "scenario": args.scenario,
        "launcher": {
            "exit_code": launcher.returncode,
            "stdout": launcher.stdout.strip(),
            "stderr": launcher.stderr.strip(),
            "report_path": str(launcher_report),
        },
        "smoke": {
            "exit_code": smoke.returncode,
            "stdout": smoke.stdout.strip(),
            "stderr": smoke.stderr.strip(),
            "report_path": str(smoke_report),
        },
        "validation": {
            "exit_code": validation.returncode,
            "stdout": validation.stdout.strip(),
            "stderr": validation.stderr.strip(),
            "report_path": str(validation_report),
        },
        "verdict": verdict,
        "reason_code": reason_code,
    }

    output_path = Path(args.output) if args.output else repo_root / "runtime-artifacts" / "live" / f"{args.run_id}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    print(f"report written: {output_path}")
    print(f"verdict={verdict} reason_code={reason_code}")
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
