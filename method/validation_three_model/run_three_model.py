#!/usr/bin/env python3
"""Run three-model ensemble (Kimi K2.6 + GLM-5.1 + DeepSeek V3.2) on the 676-case universe.

Calls three OpenRouter models in parallel per case, writes per-model checkpointed results.

Usage:
    OPENROUTER_API_KEY=sk-... python run_three_model.py [--limit N] [--resume] [--workers 8]
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import request, error

HERE = Path(__file__).parent
REPO = HERE.parent
UNIVERSE_PATH = REPO / "validation_kimi_k2_6" / "universe.json"
PROMPT_PATH = REPO / "validation_kimi_k2_6" / "mechanism_prompt.txt"

MODEL_SLUGS = {
    "kimi": "moonshotai/kimi-k2.6",
    "glm": "z-ai/glm-5.1",
    "deepseek": "deepseek/deepseek-v3.2",
}

OUT_PATHS = {k: HERE / f"{k}_raw_results.json" for k in MODEL_SLUGS}

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_INPUT_CHARS = 50_000
HEAD_CHARS = 25_000
TAIL_CHARS = 25_000
TIMEOUT = 180

# Per-model options. reasoning disabled where supported (some providers ignore the flag).
MODEL_EXTRA = {
    "kimi": {"reasoning": {"enabled": False}},
    "glm": {},
    "deepseek": {"reasoning": {"enabled": False}},
}

OUT_LOCKS = {k: threading.Lock() for k in MODEL_SLUGS}


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


def call_model(api_key, model_slug, extra, system_prompt, case_text, case_name):
    body = {
        "model": model_slug,
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
    }
    body.update(extra)
    data = json.dumps(body).encode("utf-8")
    req = request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/NickGillArizona/Duty-Without-Data",
            "X-Title": "FHA mechanism three-model ensemble",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return {"ok": True, "payload": payload}
    except error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        return {"ok": False, "error": f"HTTP {e.code}", "body": body_text[:500]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def parse_classification(text):
    """Parse first JSON object out of text. Tolerates concatenated objects."""
    if not text:
        return None, "empty"
    text = text.strip()
    # Try direct parse
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        pass
    # Find first { and use raw_decode to get just the first object
    start = text.find("{")
    if start < 0:
        return None, "no_json_object"
    try:
        obj, _end = json.JSONDecoder().raw_decode(text[start:])
        return obj, None
    except json.JSONDecodeError as e:
        return None, f"json_decode: {e}"


def classify_case(api_key, model_key, case, prompt):
    sf = case["source_file"]
    path = Path(case["case_text_path"])
    if not path.is_absolute() and not path.exists():
        path = REPO / path  # committed store: <repo>/case_texts/<source_file>.txt
    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw_text = path.read_text(encoding="latin-1")
    truncated_text, was_truncated = truncate_case_text(raw_text)

    t0 = time.time()
    api_result = call_model(
        api_key,
        MODEL_SLUGS[model_key],
        MODEL_EXTRA[model_key],
        prompt,
        truncated_text,
        case["case_name"] or sf,
    )
    elapsed = time.time() - t0

    record = {
        "source_file": sf,
        "case_name": case["case_name"],
        "year": case.get("year"),
        "pro_se_bool": case.get("pro_se_bool"),
        "representation": case.get("representation"),
        "original_family": case["original_family"],
        "original_mechanism": case["original_mechanism"],
        "original_model": case["original_model"],
        "case_text_chars": len(raw_text),
        "truncated": was_truncated,
        "elapsed_s": round(elapsed, 2),
        "model_key": model_key,
        "model_slug": MODEL_SLUGS[model_key],
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
        })
    else:
        record.update({
            "ok": False,
            "error": api_result.get("error"),
            "error_body": api_result.get("body", ""),
        })
    return record


def checkpoint(model_key, all_results_by_sf):
    with OUT_LOCKS[model_key]:
        save_json_utf8(OUT_PATHS[model_key], list(all_results_by_sf.values()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Run only the first N cases (smoke-test).")
    ap.add_argument("--resume", action="store_true", help="Skip cases already in output per model.")
    ap.add_argument("--workers", type=int, default=6, help="Parallel workers per model.")
    ap.add_argument("--models", default="kimi,glm,deepseek", help="Comma-separated subset of models.")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY env var not set", file=sys.stderr)
        sys.exit(1)

    active_models = [m.strip() for m in args.models.split(",") if m.strip()]
    for m in active_models:
        if m not in MODEL_SLUGS:
            print(f"ERROR: unknown model key '{m}' (expected one of {list(MODEL_SLUGS)})", file=sys.stderr)
            sys.exit(1)

    universe = load_json_utf8(UNIVERSE_PATH)
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    cases = universe
    if args.limit:
        cases = cases[: args.limit]

    # Load existing results
    existing_by_model = {}
    for m in active_models:
        if args.resume and OUT_PATHS[m].exists():
            recs = load_json_utf8(OUT_PATHS[m])
            existing_by_model[m] = {r["source_file"]: r for r in recs}
            print(f"[{m}] resuming with {len(existing_by_model[m])} existing results.")
        else:
            existing_by_model[m] = {}

    total_todo_by_model = {m: sum(1 for c in cases if c["source_file"] not in existing_by_model[m]) for m in active_models}
    print(f"Cases: {len(cases)}. Per-model todo: {total_todo_by_model}.")

    done_counters = {m: 0 for m in active_models}
    total_calls = sum(total_todo_by_model.values())
    start = time.time()
    print_lock = threading.Lock()

    def one_call(model_key, case):
        rec = classify_case(api_key, model_key, case, prompt)
        existing_by_model[model_key][rec["source_file"]] = rec
        done_counters[model_key] += 1
        total_done = sum(done_counters.values())
        # checkpoint every 20 new items per model
        if done_counters[model_key] % 20 == 0:
            checkpoint(model_key, existing_by_model[model_key])
        fam = "?"
        if rec.get("ok") and rec.get("classification"):
            fam = rec["classification"].get("pleading_failure_family", "?")
        elif not rec.get("ok"):
            fam = "ERR"
        with print_lock:
            elapsed = time.time() - start
            rate = total_done / elapsed if elapsed > 0 else 0
            eta = (total_calls - total_done) / rate if rate > 0 else 0
            print(
                f"[{total_done:4d}/{total_calls}] {model_key:8s} {rec['source_file'][:40]:40s} "
                f"orig={rec['original_family'][:12]:12s} new={fam[:18]:18s} "
                f"{rec.get('elapsed_s',0):5.1f}s  rate={rate:.1f}/s  eta={eta/60:.1f}min"
            )
        return rec

    futures = []
    # One thread pool per model to limit concurrency per-provider
    with ThreadPoolExecutor(max_workers=args.workers * len(active_models)) as ex:
        for m in active_models:
            todo = [c for c in cases if c["source_file"] not in existing_by_model[m]]
            for case in todo:
                futures.append(ex.submit(one_call, m, case))
        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                print(f"WORKER ERROR: {e}", file=sys.stderr)

    # Final checkpoint
    for m in active_models:
        checkpoint(m, existing_by_model[m])

    # Summary
    for m in active_models:
        recs = list(existing_by_model[m].values())
        ok = sum(1 for r in recs if r.get("ok") and r.get("classification"))
        print(f"\n[{m}] {ok}/{len(recs)} successful classifications. Output: {OUT_PATHS[m]}")


if __name__ == "__main__":
    main()
