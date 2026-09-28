"""Render DDXPlus structured cases to prose with one frozen template.

Usage:
  python ddxplus_to_cases.py --patients release_test_patients.csv \
      --evidences release_evidences.json --conditions release_conditions.json \
      --n 1000 --out data/ddxplus_cases.csv --options-out data/ddxplus_options.json

VERIFY against your download: field names below follow the public DDXPlus
release (AGE, SEX, PATHOLOGY, EVIDENCES, DIFFERENTIAL_DIAGNOSIS; evidence
entries with question_en, data_type, value_meaning). Adjust if they differ.
"""
import argparse
import ast
import csv
import json
import random
import re
from collections import defaultdict

SEED = 20260926


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def eng_name(cond_key, conditions):
    c = conditions.get(cond_key, {})
    return c.get("cond-name-eng") or c.get("condition_name") or cond_key


def render(row, ev):
    """Frozen template: demographics, then one sentence per positive finding."""
    sex = {"M": "male", "F": "female"}.get(row["SEX"], row["SEX"])
    parts = [f"{row['AGE']}-year-old {sex}."]
    for item in ast.literal_eval(row["EVIDENCES"]):
        code, _, val = item.partition("_@_")
        e = ev.get(code, {})
        q = e.get("question_en", code).rstrip("?")
        if not val:
            parts.append(f"Answers yes to: {q}.")
        else:
            meaning = e.get("value_meaning", {}).get(val, {})
            v = meaning.get("en", val) if isinstance(meaning, dict) else val
            parts.append(f"{q}: {v}.")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--patients", required=True)
    ap.add_argument("--evidences", required=True)
    ap.add_argument("--conditions", required=True)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--out", required=True)
    ap.add_argument("--options-out", required=True)
    a = ap.parse_args()

    ev = json.load(open(a.evidences))
    conditions = json.load(open(a.conditions))
    by_path = defaultdict(list)
    with open(a.patients, newline="") as f:
        for i, row in enumerate(csv.DictReader(f)):
            by_path[row["PATHOLOGY"]].append((i, row))

    # stratified: equal share per pathology, remainder filled at random
    rng = random.Random(SEED)
    per = a.n // len(by_path)
    chosen = []
    for rows in by_path.values():
        chosen += rng.sample(rows, min(per, len(rows)))
    rest = [r for rows in by_path.values() for r in rows if r not in chosen]
    chosen += rng.sample(rest, a.n - len(chosen))

    options = {slug(eng_name(k, conditions)): eng_name(k, conditions) for k in by_path}
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["case_id", "dataset", "text", "true_dx",
                                          "reference_differential"])
        w.writeheader()
        for i, row in chosen:
            diff = {slug(eng_name(n, conditions)): float(p)
                    for n, p in ast.literal_eval(row["DIFFERENTIAL_DIAGNOSIS"])}
            w.writerow({"case_id": f"ddx{i}", "dataset": "ddxplus", "text": render(row, ev),
                        "true_dx": slug(eng_name(row["PATHOLOGY"], conditions)),
                        "reference_differential": json.dumps(diff)})
    json.dump({"ddxplus": {"options": options, "distractors": {}}},
              open(a.options_out, "w"), indent=2)
    print(f"wrote {len(chosen)} cases, {len(options)} options")


if __name__ == "__main__":
    main()
