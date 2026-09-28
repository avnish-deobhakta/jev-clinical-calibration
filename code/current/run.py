"""Build every pre-registered condition and run it against one model.

Usage:
  python run.py --model jev --cases data/cases.csv --options data/options.json \
      [--vague data/vague.csv] [--out results.jsonl] [--max-calls 5000]

Resumable: jobs already in the output file for this model are skipped.
Seeds are fixed, so re-running produces the same permutations.
"""
import argparse
import os
import csv
import json
import random
import time
from collections import OrderedDict

from clients import get_client

SEED = 20260926
N_REPEATS = 5        # H0
N_PERMS = 5          # H1
NOTA_KEY = "none_of_these"
NOTA_DESC = "None of the listed diagnoses"
N_OPTIONS_ONLY = 5   # H7 (v7, exploratory, Deviation D6): repeats of the options-only baseline
OPTIONS_ONLY_STATE = "(No patient information provided.)"


def load_cases(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def canonical(opts):
    return OrderedDict(sorted(opts.items()))


def build_jobs(cases, options, vague):
    """Yield dicts: job_id, condition, case_id, dataset, state, options(ordered), meta."""
    rng = random.Random(SEED)
    for c in cases:
        ds, cid, text = c["dataset"], c["case_id"], c["text"]
        base = canonical(options[ds]["options"])
        common = {"case_id": cid, "dataset": ds, "true_dx": c.get("true_dx", "")}

        # H0: identical repeats (rep 0 doubles as the canonical run for H1 to H6)
        is_ddx = ds.lower().startswith("ddxplus")
        for r in range(1 if is_ddx else N_REPEATS):
            yield {**common, "job_id": f"H0|{cid}|rep{r}", "condition": "H0",
                   "state": text, "options": base, "meta": {"rep": r}}

        # H6 on DDXPlus only needs the canonical run; skip perturbations there
        if is_ddx:
            continue

        # H1: seeded permutations
        keys = list(base)
        for i in range(N_PERMS):
            perm = keys[:]
            rng.shuffle(perm)
            yield {**common, "job_id": f"H1|{cid}|perm{i}", "condition": "H1",
                   "state": text, "options": OrderedDict((k, base[k]) for k in perm),
                   "meta": {"perm": i}}

        # H2: clinician-approved paraphrases
        for j in (1, 2, 3):
            para = (c.get(f"paraphrase_{j}") or "").strip()
            if para:
                yield {**common, "job_id": f"H2|{cid}|para{j}", "condition": "H2",
                       "state": para, "options": base, "meta": {"para": j}}

        # H3: confirmed impossible distractors, appended then randomly inserted
        dkeys = [d for d in (c.get("distractors") or "").split(";") if d]
        if dkeys:
            dmap = options[ds]["distractors"]
            appended = OrderedDict(list(base.items()) + [(d, dmap[d]) for d in dkeys])
            yield {**common, "job_id": f"H3|{cid}|append", "condition": "H3",
                   "state": text, "options": appended, "meta": {"distractors": dkeys, "mode": "append"}}
            mixed = list(base.items())
            for d in dkeys:
                mixed.insert(rng.randrange(len(mixed) + 1), (d, dmap[d]))
            yield {**common, "job_id": f"H3|{cid}|random", "condition": "H3",
                   "state": text, "options": OrderedDict(mixed),
                   "meta": {"distractors": dkeys, "mode": "random"}}

        # H5: truth removed, without and with "none of these"
        if c.get("true_dx") in base:
            removed = OrderedDict((k, v) for k, v in base.items() if k != c["true_dx"])
            yield {**common, "job_id": f"H5|{cid}|no_nota", "condition": "H5",
                   "state": text, "options": removed, "meta": {"nota": False}}
            with_nota = OrderedDict(list(removed.items()) + [(NOTA_KEY, NOTA_DESC)])
            yield {**common, "job_id": f"H5|{cid}|nota", "condition": "H5",
                   "state": text, "options": with_nota, "meta": {"nota": True}}

    # H7 (v7, exploratory, D6): options-only baseline. The input carries no patient
    # information, so it is identical for every case in a dataset; one short series per
    # dataset measures what each model picks from the option list alone.
    for ds in options:
        base = canonical(options[ds]["options"])
        for r in range(N_OPTIONS_ONLY):
            yield {"case_id": "options_only", "dataset": ds, "true_dx": "",
                   "job_id": f"H7|options_only|rep{r}", "condition": "H7",
                   "state": OPTIONS_ONLY_STATE, "options": base, "meta": {"rep": r}}

    # H4: uninformative inputs against each vignette set's option set
    # H4N (v4, exploratory, Deviation D3): same inputs with "none of these" appended
    for v in vague:
        for ds in options:
            if ds.lower().startswith("ddxplus"):
                continue
            base = canonical(options[ds]["options"])
            yield {"case_id": v["input_id"], "dataset": ds, "true_dx": "",
                   "job_id": f"H4|{v['input_id']}|{ds}", "condition": "H4",
                   "state": v["text"], "options": base, "meta": {}}
            yield {"case_id": v["input_id"], "dataset": ds, "true_dx": "",
                   "job_id": f"H4N|{v['input_id']}|{ds}", "condition": "H4N",
                   "state": v["text"], "options": OrderedDict(list(base.items()) + [(NOTA_KEY, NOTA_DESC)]),
                   "meta": {"nota": True}}


def done_ids(path, model):
    ids = set()
    try:
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                if r["model"] == model and not r.get("error"):
                    ids.add((r["dataset"], r["job_id"]))
    except FileNotFoundError:
        pass
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True,
                    choices=["jev", "opus_verbalized", "opus5_nothink", "opus_sampled", "mock"])  # opus_sampled records as opus_sampled_v2
    ap.add_argument("--cases", required=True)
    ap.add_argument("--options", required=True)
    ap.add_argument("--vague")
    ap.add_argument("--out", default="results.jsonl")
    ap.add_argument("--conditions", default="H0,H1,H2,H3,H4,H4N,H5,H7")
    ap.add_argument("--max-calls", type=int, default=5000, help="hard budget cap")
    args = ap.parse_args()

    cases = load_cases(args.cases)
    options = json.load(open(args.options))
    vague = load_cases(args.vague) if args.vague else []
    wanted = set(args.conditions.split(","))
    client = get_client(args.model)
    skip = done_ids(args.out, client.name)

    jobs = [j for j in build_jobs(cases, options, vague)
            if j["condition"] in wanted and (j["dataset"], j["job_id"]) not in skip]
    if args.model == "opus_sampled":  # pre-reg: sampled mode on vignette sets, H0 rep0 only
        jobs = [j for j in jobs if j["job_id"].endswith("rep0")
                and not j["dataset"].lower().startswith("ddxplus")]
    print(f"{len(jobs)} jobs to run for {client.name} ({len(skip)} already done)")
    if len(jobs) > args.max_calls:
        raise SystemExit(f"Refusing: {len(jobs)} jobs exceeds --max-calls {args.max_calls}")

    with open(args.out, "a") as out:
        for n, j in enumerate(jobs, 1):
            rec = {k: j[k] for k in ("job_id", "condition", "case_id", "dataset", "true_dx", "meta")}
            rec.update(model=client.name, model_version=client.version,
                       harness_commit=os.environ.get("HARNESS_COMMIT", "unrecorded"),
                       option_order=list(j["options"]), ts=time.time())
            try:
                probs, raw = client.classify(j["state"], j["options"])
                rec.update(probs=probs, raw=raw, resolved_model=raw.get("resolved_model"))
            except Exception as e:  # logged, excluded from that condition only
                rec.update(error=repr(e))
            out.write(json.dumps(rec) + "\n")
            out.flush()
            if n % 25 == 0:
                print(f"  {n}/{len(jobs)}")


if __name__ == "__main__":
    main()
