"""Runner for the raw-text verification lanes.

Tasks:
  r1         - strong-model panel (Sonnet 5 + GPT-5.5 + Gemini 3.1 Pro) over the 96-row audit set
  r2         - Layer-2 trio (Kimi K2.6 + GLM-5.1 + DeepSeek V3.2) over all 476 rows
  adjudicate - Opus 4.8 over adjudication_record.json (built by verification_compute.py)

Reads full opinion text from disk (50,000-char head/tail truncation per pipeline convention).
Evidence quotes are verified in-runner against the truncated text (normalized substring match);
a failed quote triggers a stricter retry; the final read records quote_verified true/false.

API key from OPENROUTER_API_KEY env var only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import request, error

HERE = Path(__file__).resolve().parent
RTV = HERE.parent / "raw_text_verification"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT = 300
HEAD, TAIL, MAXC = 25_000, 25_000, 50_000

MODEL_SLUGS = {
    "sonnet5": "anthropic/claude-sonnet-5",
    "gpt55": "openai/gpt-5.5",
    "gemini31pro": "google/gemini-3.1-pro-preview",
    "opus48": "anthropic/claude-opus-4.8",
    "kimi": "moonshotai/kimi-k2.6",
    "glm": "z-ai/glm-5.1",
    "deepseek": "deepseek/deepseek-v3.2",
}
MODEL_EXTRA = {
    "kimi": {"reasoning": {"enabled": False}},
    "deepseek": {"reasoning": {"enabled": False}},
}
MODEL_MAX_TOKENS = {"sonnet5": 12000, "gpt55": 16000, "gemini31pro": 12000, "opus48": 12000,
                    "kimi": 1200, "glm": 4000, "deepseek": 1200}

FAMS = {"A", "B", "C", "UNCLEAR", "MISFILTER"}


def truncate(text: str) -> str:
    if len(text) <= MAXC:
        return text
    return text[:HEAD] + "\n\n[... TRUNCATED ...]\n\n" + text[-TAIL:]


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def read_text(path: str) -> str:
    p = Path(path)
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="latin-1")


def call_model(api_key, mkey, system_prompt, user_text, strict_retry=False):
    user = user_text + ("\n\nREMINDER: respond with ONLY the JSON object; the evidence_quote must be a single contiguous passage copied verbatim from the opinion text, no ellipses." if strict_retry else "")
    body = {
        "model": MODEL_SLUGS[mkey],
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user}],
        "temperature": 0.2,
        "max_tokens": MODEL_MAX_TOKENS[mkey],
    }
    body.update(MODEL_EXTRA.get(mkey, {}))
    req = request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}",
                 "HTTP-Referer": "https://github.com/NickGillArizona/Duty-Without-Data",
                 "X-Title": "Comparator raw-text verification"},
        method="POST")
    try:
        with request.urlopen(req, timeout=TIMEOUT) as resp:
            return {"ok": True, "payload": json.loads(resp.read().decode("utf-8"))}
    except error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}", "body": e.read().decode("utf-8", "replace")[:400]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def parse_obj(text):
    if not text:
        return None
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    if start < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
        return obj
    except json.JSONDecodeError:
        return None


def valid(task, obj):
    if not isinstance(obj, dict):
        return False
    key = "final_family" if task == "adjudicate" else "family"
    return str(obj.get(key, "")).strip().upper() in FAMS and bool(str(obj.get("evidence_quote", "")).strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["r1", "r2", "adjudicate"])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        sys.exit("OPENROUTER_API_KEY not set")

    if args.task == "r1":
        rows = json.loads((RTV / "verification_inputs_r1.json").read_text(encoding="utf-8"))
        models = ["sonnet5", "gpt55", "gemini31pro"]
        prompt = (RTV / "verification_recode_prompt.txt").read_text(encoding="utf-8")
        out_name = "r1_{m}_raw_results.json"
    elif args.task == "r2":
        rows = json.loads((RTV / "verification_inputs_r2.json").read_text(encoding="utf-8"))
        rows = [r for r in rows if r.get("text_path")]
        models = ["kimi", "glm", "deepseek"]
        prompt = (RTV / "verification_recode_prompt.txt").read_text(encoding="utf-8")
        out_name = "r2_{m}_raw_results.json"
    else:
        rows = json.loads((RTV / "adjudication_record.json").read_text(encoding="utf-8"))
        models = ["opus48"]
        prompt = (RTV / "verification_adjudicator_prompt.txt").read_text(encoding="utf-8")
        out_name = "adjudication_{m}_raw_results.json"

    if args.limit:
        rows = rows[: args.limit]

    out_paths = {m: RTV / out_name.format(m=m) for m in models}
    locks = {m: threading.Lock() for m in models}
    existing = {}
    for m in models:
        if args.resume and out_paths[m].exists():
            existing[m] = {r["row_id"]: r for r in json.loads(out_paths[m].read_text(encoding="utf-8")) if r.get("ok")}
        else:
            existing[m] = {}

    total = sum(sum(1 for r in rows if r["row_id"] not in existing[m]) for m in models)
    print(f"task={args.task} rows={len(rows)} models={models} todo={total}", flush=True)
    done = {"n": 0}
    start = time.time()
    plock = threading.Lock()

    def checkpoint(m):
        with locks[m]:
            out_paths[m].write_text(json.dumps(list(existing[m].values()), indent=1, ensure_ascii=False),
                                    encoding="utf-8", newline="\n")

    def build_user(row, text):
        if args.task == "adjudicate":
            votes = json.dumps(row["panel_votes"], indent=1)
            return (f"Case: {row.get('case_name') or row['row_id']}\n\n"
                    f"MASKED-LANE CONSENSUS CODE: {row['masked_consensus_family']}\n\n"
                    f"PANEL CODES AND QUOTES:\n{votes}\n\n"
                    f"=== OPINION TEXT ===\n{text}\n=== END OPINION ===")
        return (f"Case: {row.get('case_name') or row['row_id']}\n\n"
                f"=== OPINION TEXT ===\n{text}\n=== END OPINION ===")

    def one(m, row):
        raw = read_text(row["text_path"])
        text = truncate(raw)
        ntext = norm(text)
        rec = {"row_id": row["row_id"], "arm": row.get("arm"), "r1_role": row.get("r1_role"),
               "masked_consensus_family": row.get("masked_consensus_family"),
               "model_key": m, "model_slug": MODEL_SLUGS[m], "attempts": 0,
               "text_chars": len(raw), "truncated": len(raw) > MAXC}
        best = None
        for attempt in range(3):
            rec["attempts"] = attempt + 1
            res = call_model(api_key, m, prompt, build_user(row, text), strict_retry=attempt > 0)
            if not res["ok"]:
                rec.update({"ok": False, "error": res.get("error"), "error_body": res.get("body", "")})
                time.sleep(3 * (attempt + 1))
                continue
            content = ((res["payload"].get("choices") or [{}])[0].get("message") or {}).get("content") or ""
            obj = parse_obj(content)
            if obj is not None and valid(args.task, obj):
                qok = norm(obj.get("evidence_quote", "")) in ntext
                rec.update({"ok": True, "raw_text": content, "classification": obj,
                            "quote_verified": qok, "usage": res["payload"].get("usage")})
                best = rec.copy()
                if qok:
                    break
                # quote failed: retry stricter, but keep this as fallback
            else:
                rec.update({"ok": False, "raw_text": content, "parse_error": "invalid_schema_or_parse"})
        final = best if best is not None else rec
        existing[m][row["row_id"]] = final
        done["n"] += 1
        if done["n"] % 15 == 0:
            checkpoint(m)
        with plock:
            el = time.time() - start
            rate = done["n"] / el if el else 0
            eta = (total - done["n"]) / rate / 60 if rate else 0
            fam = "ERR"
            if final.get("ok"):
                c = final["classification"]
                fam = c.get("family") or c.get("final_family") or "?"
                fam += "" if final.get("quote_verified") else "*"
            print(f"[{done['n']:4d}/{total}] {m:11s} {row['row_id'][:48]:48s} -> {fam:10s} eta={eta:.0f}m", flush=True)

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
                print(f"WORKER ERROR: {e}", file=sys.stderr, flush=True)

    for m in models:
        checkpoint(m)
        recs = list(existing[m].values())
        ok = sum(1 for r in recs if r.get("ok"))
        qv = sum(1 for r in recs if r.get("quote_verified"))
        print(f"[{m}] {ok}/{len(recs)} ok, {qv} quote-verified -> {out_paths[m].name}", flush=True)


if __name__ == "__main__":
    main()
