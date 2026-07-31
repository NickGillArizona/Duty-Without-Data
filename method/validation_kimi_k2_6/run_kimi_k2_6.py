#!/usr/bin/env python3
"""Run Kimi K2.6 (via OpenRouter) over the validation sample.

Usage:
    OPENROUTER_API_KEY=sk-... python run_kimi_k2_6.py [--limit N] [--resume]

Reads sample.json, calls the API for each case, writes
method/validation_kimi_k2_6/kimi_k2_6_raw_results.json incrementally.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import request, error

HERE = Path(__file__).parent
REPO = HERE.parent
SAMPLE_PATH = HERE / "sample.json"
PROMPT_PATH = HERE / "mechanism_prompt.txt"
OUT_PATH = HERE / "kimi_k2_6_raw_results.json"

MODEL_SLUG = "moonshotai/kimi-k2.6"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_INPUT_CHARS = 50_000
HEAD_CHARS = 25_000
TAIL_CHARS = 25_000
TIMEOUT = 120


def load_json_utf8(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json_utf8(p, data):
    with io.open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def truncate_case_text(text):
    if len(text) <= MAX_INPUT_CHARS:
        return text, False
    return text[:HEAD_CHARS] + "\n\n[... TRUNCATED ...]\n\n" + text[-TAIL_CHARS:], True


def call_kimi(api_key, system_prompt, case_text, case_name):
    body = {
        "model": MODEL_SLUG,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Case: {case_name}\n\n"
                    f"=== OPINION TEXT ===\n{case_text}\n\n"
                    f"=== END OPINION ===\n\n"
                    f"Respond with ONLY the JSON object."
                ),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 6000,
        "reasoning": {"enabled": False},
    }
    data = json.dumps(body).encode("utf-8")
    req = request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/NickGillArizona/Duty-Without-Data",
            "X-Title": "FHA mechanism-classification validation",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return {"ok": True, "payload": payload}
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"ok": False, "error": f"HTTP {e.code}", "body": body}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def parse_classification(text):
    if not text:
        return None, "empty"
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None, "no_json_object"
    raw = m.group(0)
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as e:
        return None, f"json_decode: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Run only the first N cases (for smoke-test).")
    ap.add_argument("--resume", action="store_true", help="Skip cases already in output.")
    ap.add_argument("--delay", type=float, default=0.2, help="Delay between API calls (seconds).")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY env var not set", file=sys.stderr)
        sys.exit(1)

    sample = load_json_utf8(SAMPLE_PATH)
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    cases = sample["cases"]
    if args.limit:
        cases = cases[: args.limit]

    existing = []
    existing_ids = set()
    if args.resume and OUT_PATH.exists():
        existing = load_json_utf8(OUT_PATH)
        existing_ids = {r["source_file"] for r in existing}
        print(f"Resuming with {len(existing)} already-done results.")

    results = list(existing)

    for idx, case in enumerate(cases):
        sf = case["source_file"]
        if sf in existing_ids:
            continue
        path = Path(case["case_text_path"])
        if not path.is_absolute() and not path.exists():
            path = REPO / path  # committed store: <repo>/case_texts/<source_file>.txt
        try:
            raw_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw_text = path.read_text(encoding="latin-1")
        truncated_text, was_truncated = truncate_case_text(raw_text)

        t0 = time.time()
        api_result = call_kimi(api_key, prompt, truncated_text, case["case_name"] or sf)
        elapsed = time.time() - t0

        record = {
            "source_file": sf,
            "case_name": case["case_name"],
            "strata_key": case["strata_key"],
            "original_family": case["original_family"],
            "original_mechanism": case["original_mechanism"],
            "original_model": case["original_model"],
            "representation": case["representation"],
            "case_text_chars": len(raw_text),
            "truncated": was_truncated,
            "elapsed_s": round(elapsed, 2),
        }
        if api_result["ok"]:
            payload = api_result["payload"]
            choice = (payload.get("choices") or [{}])[0]
            msg = choice.get("message", {}) or {}
            content = msg.get("content") or ""
            parsed, parse_err = parse_classification(content)
            record.update({
                "ok": True,
                "raw_text": content,
                "classification": parsed,
                "parse_error": parse_err,
                "usage": payload.get("usage"),
                "provider_response_id": payload.get("id"),
            })
        else:
            record.update({
                "ok": False,
                "error": api_result.get("error"),
                "error_body": api_result.get("body", "")[:500],
            })

        results.append(record)
        fam = (record.get("classification") or {}).get("pleading_failure_family", "?") if record.get("ok") else "ERR"
        print(f"[{idx + 1}/{len(cases)}] {sf[:50]:50s}  orig={case['original_family'][:12]:12s}  new={fam:18s}  {elapsed:.1f}s")

        # Checkpoint every 10 records
        if (idx + 1) % 10 == 0 or idx == len(cases) - 1:
            save_json_utf8(OUT_PATH, results)

        time.sleep(args.delay)

    save_json_utf8(OUT_PATH, results)
    ok_count = sum(1 for r in results if r.get("ok"))
    print(f"\nDone. {ok_count}/{len(results)} successful. Output: {OUT_PATH}")


if __name__ == "__main__":
    main()
