"""Phase 5 remediation model runner (mirrors companion method/validation_three_model/run_three_model.py).

Tasks:
  rationale    - three-model ensemble (Kimi K2.6 + GLM-5.1 + DeepSeek V3.2) over the 476 masked rows
  reread       - MiniMax M2.7 stratified independent re-read (Layer-3 analog, 150 rows)
  classguess   - Gemini 3.1 Flash Lite class-guess probe over all 476 masked rows (leakage assay)
  undetermined - three-model primary-class classification of the 187 UNDETERMINED/empty rows

API key from OPENROUTER_API_KEY env var ONLY; never written to disk.

Usage: OPENROUTER_API_KEY=... python consensus_run_models.py --task rationale [--limit N] [--resume] [--workers 8]
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import request, error

HERE = Path(__file__).resolve().parent
P5 = HERE.parent / "consensus_stage"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT = 180

MODEL_SLUGS = {
    "kimi": "moonshotai/kimi-k2.6",
    "glm": "z-ai/glm-5.1",
    "deepseek": "deepseek/deepseek-v3.2",
    "minimax": "minimax/minimax-m2.7",
    "flash": "google/gemini-3.1-flash-lite",
}
MODEL_EXTRA = {
    "kimi": {"reasoning": {"enabled": False}},
    "glm": {},
    "deepseek": {"reasoning": {"enabled": False}},
    "minimax": {},
    "flash": {"reasoning": {"enabled": False}},
}
# GLM-5.1 and MiniMax reason internally (observed ~1.1k reasoning tokens), so give them headroom;
# 800 starves content and returns empty strings.
MODEL_MAX_TOKENS = {"kimi": 800, "glm": 4000, "deepseek": 800, "minimax": 4000, "flash": 800}

VALID_FAMILIES = {"A", "B", "C", "UNCLEAR", "MISFILTER"}
VALID_CLASSES = {"disability", "race", "familial_status", "cannot_tell"}
VALID_PRIMARY = {"race", "disability", "familial_status", "national_origin", "sex", "religion",
                 "color", "retaliation_only", "other", "undetermined"}

CLASSGUESS_PROMPT = (
    "You will receive a masked excerpt from a housing-discrimination case summary in which "
    "protected-class terms and claim-type names were replaced with [CLASS] and [CLAIM]. Using any "
    "residual clues in the text (statutes cited, remedies discussed, fact patterns), guess which "
    "protected class the case is actually about. Respond with ONLY a JSON object: "
    '{"guess": "<disability|race|familial_status|cannot_tell>", "clue": "<the specific residual clue, or none>"}'
)

UNDETERMINED_PROMPT = (
    "You will receive summary text from a federal Fair Housing Act case whose primary protected "
    "class could not be determined by an earlier pipeline. Determine the PRIMARY protected class "
    "the plaintiff's housing-discrimination claim rests on. Respond with ONLY a JSON object: "
    '{"primary_protected_class": "<race|disability|familial_status|national_origin|sex|religion|color|retaliation_only|other|undetermined>", '
    '"confidence": "<HIGH|MEDIUM|LOW>", "basis": "<one sentence>"}'
)


def call_model(api_key, slug, extra, system_prompt, user_text, strict_retry=False, max_tokens=800):
    user = user_text + ("\n\nREMINDER: respond with ONLY the JSON object, no other text." if strict_retry else "")
    body = {
        "model": slug,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user}],
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }
    body.update(extra)
    req = request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}",
                 "HTTP-Referer": "https://github.com/NickGillArizona/Duty-Without-Data",
                 "X-Title": "Comparator Phase 5 remediation"},
        method="POST")
    try:
        with request.urlopen(req, timeout=TIMEOUT) as resp:
            return {"ok": True, "payload": json.loads(resp.read().decode("utf-8"))}
    except error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}", "body": e.read().decode("utf-8", "replace")[:400]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def parse_json_obj(text):
    if not text:
        return None, "empty"
    text = text.strip()
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    if start < 0:
        return None, "no_json_object"
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
        return obj, None
    except json.JSONDecodeError as e:
        return None, f"json_decode: {e}"


def validate(task, obj):
    if not isinstance(obj, dict):
        return False
    if task in ("rationale", "reread"):
        return str(obj.get("family", "")).strip().upper() in VALID_FAMILIES
    if task == "classguess":
        return str(obj.get("guess", "")).strip().lower() in VALID_CLASSES
    if task == "undetermined":
        return str(obj.get("primary_protected_class", "")).strip().lower() in VALID_PRIMARY
    return False


def build_reread_sample(rows, n=150, seed=20260707):
    rng = random.Random(seed)
    strata = {}
    for r in rows:
        strata.setdefault((r["arm"], r["proxy_family_first_pass"]), []).append(r)
    for v in strata.values():
        rng.shuffle(v)
    chosen, keys = [], sorted(strata)
    i = 0
    while len(chosen) < n and any(strata[k] for k in keys):
        k = keys[i % len(keys)]
        if strata[k]:
            chosen.append(strata[k].pop())
        i += 1
    return chosen[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["rationale", "reread", "classguess", "undetermined"])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.task in ("rationale", "reread", "classguess"):
        rows = json.loads((P5 / "consensus_inputs.json").read_text(encoding="utf-8"))
    else:
        rows = json.loads((P5 / "undetermined_inputs.json").read_text(encoding="utf-8"))
        for r in rows:
            r["row_id"] = f"UND|{r['source_file']}"

    if args.task == "rationale":
        models = ["kimi", "glm", "deepseek"]
        prompt = (P5 / "consensus_rationale_prompt.txt").read_text(encoding="utf-8")
        out_name = "{m}_raw_results.json"
        text_key = "masked_text"
    elif args.task == "reread":
        models = ["minimax"]
        prompt = (P5 / "consensus_rationale_prompt.txt").read_text(encoding="utf-8")
        out_name = "reread_{m}_raw_results.json"
        rows = build_reread_sample(rows)
        text_key = "masked_text"
    elif args.task == "classguess":
        models = ["flash"]
        prompt = CLASSGUESS_PROMPT
        out_name = "classguess_{m}_raw_results.json"
        text_key = "masked_text"
    else:
        models = ["kimi", "glm", "deepseek"]
        prompt = UNDETERMINED_PROMPT
        out_name = "undetermined_{m}_raw_results.json"
        text_key = "text"

    if args.limit:
        rows = rows[: args.limit]

    out_paths = {m: P5 / out_name.format(m=m) for m in models}
    locks = {m: threading.Lock() for m in models}
    existing = {}
    for m in models:
        if args.resume and out_paths[m].exists():
            # keep only successful rows so a resume pass retries failures
            existing[m] = {r["row_id"]: r for r in json.loads(out_paths[m].read_text(encoding="utf-8")) if r.get("ok")}
        else:
            existing[m] = {}

    total_calls = sum(sum(1 for r in rows if r["row_id"] not in existing[m]) for m in models)
    print(f"task={args.task} rows={len(rows)} models={models} todo_calls={total_calls}")
    done = {"n": 0}
    start = time.time()
    plock = threading.Lock()

    def checkpoint(m):
        with locks[m]:
            out_paths[m].write_text(json.dumps(list(existing[m].values()), indent=1, ensure_ascii=False),
                                    encoding="utf-8", newline="\n")

    def one(m, row):
        user_text = f"Excerpt for classification:\n\n{row[text_key]}"
        rec = {"row_id": row["row_id"], "source_file": row.get("source_file"), "arm": row.get("arm"),
               "model_key": m, "model_slug": MODEL_SLUGS[m], "attempts": 0}
        parsed = None
        for attempt in range(3):
            rec["attempts"] = attempt + 1
            res = call_model(api_key, MODEL_SLUGS[m], MODEL_EXTRA[m], prompt, user_text,
                             strict_retry=attempt > 0, max_tokens=MODEL_MAX_TOKENS.get(m, 800))
            if not res["ok"]:
                rec.update({"ok": False, "error": res.get("error"), "error_body": res.get("body", "")})
                time.sleep(2 * (attempt + 1))
                continue
            content = ((res["payload"].get("choices") or [{}])[0].get("message") or {}).get("content") or ""
            obj, perr = parse_json_obj(content)
            if obj is not None and validate(args.task, obj):
                rec.update({"ok": True, "raw_text": content, "classification": obj,
                            "usage": res["payload"].get("usage")})
                parsed = obj
                break
            rec.update({"ok": False, "raw_text": content, "parse_error": perr or "invalid_schema"})
        existing[m][row["row_id"]] = rec
        done["n"] += 1
        if done["n"] % 20 == 0:
            checkpoint(m)
        with plock:
            el = time.time() - start
            rate = done["n"] / el if el else 0
            eta = (total_calls - done["n"]) / rate / 60 if rate else 0
            label = (parsed or {}).get("family") or (parsed or {}).get("guess") or \
                    (parsed or {}).get("primary_protected_class") or "ERR"
            print(f"[{done['n']:4d}/{total_calls}] {m:9s} {row['row_id'][:52]:52s} -> {str(label)[:14]:14s} eta={eta:.1f}m")
        return rec

    futures = []
    with ThreadPoolExecutor(max_workers=args.workers * len(models)) as ex:
        for m in models:
            for row in rows:
                if row["row_id"] not in existing[m]:
                    futures.append(ex.submit(one, m, row))
        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                print(f"WORKER ERROR: {e}", file=sys.stderr)

    for m in models:
        checkpoint(m)
        recs = list(existing[m].values())
        ok = sum(1 for r in recs if r.get("ok"))
        print(f"[{m}] {ok}/{len(recs)} ok -> {out_paths[m].name}")


if __name__ == "__main__":
    main()
