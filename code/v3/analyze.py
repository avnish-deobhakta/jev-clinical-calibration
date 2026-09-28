"""Compute pre-registered outcomes from results.jsonl.

Usage: python analyze.py results.jsonl [--cases data/cases.csv] > summary.md

Margins (fixed in the pre-registration): TVD 0.05, distractor mass 0.02.
Amendment 1 (2026-09-26, before any study data): NLL is computed after mixing
each distribution with 1% uniform (NLL_smoothed, primary); raw NLL with 1e-12
clipping is reported alongside. Output resolution and the exact-zero rate are
reported descriptively for every model.
"""
import argparse
import csv
import itertools
import json
import math
from collections import defaultdict

import numpy as np
from scipy import stats

TVD_MARGIN = 0.05
NLL_EPS = 0.01  # Amendment 1: uniform mixing weight for smoothed NLL
DISTRACTOR_MARGIN = 0.02
NOTA_KEY = "none_of_these"
B = 10_000
rng = np.random.default_rng(20260926)


# ---------- basic measures ----------
def tvd(p, q):
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0) - q.get(k, 0)) for k in keys)


def restrict(p, keys):
    s = sum(p.get(k, 0) for k in keys)
    return {k: p.get(k, 0) / s for k in keys} if s > 0 else None


def norm_entropy(p):
    v = np.array([x for x in p.values() if x > 0])
    return float(-(v * np.log(v)).sum() / math.log(len(p))) if len(p) > 1 else 0.0


def log_ratio_shift(p, q, floor=0.01):
    """Mean |change in log(p_i / p_top)| over options above floor in both."""
    top = max(p, key=p.get)
    ks = [k for k in p if k != top and p.get(k, 0) > floor and q.get(k, 0) > floor
          and q.get(top, 0) > floor]
    if not ks:
        return 0.0
    return float(np.mean([abs(math.log(p[k] / p[top]) - math.log(q[k] / q[top])) for k in ks]))


def wilson(k, n):
    if n == 0:
        return (float("nan"),) * 3
    z = 1.96
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return ph, c - h, c + h


def boot_ci(x):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float("nan"),) * 3
    idx = rng.integers(0, len(x), (B, len(x)))
    m = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


# ---------- calibration ----------
def calibration(rows):
    """rows: list of (probs, true_key). Returns ECE, Brier, NLL (smoothed and raw), top1, top3."""
    conf, correct, brier, nll, nll_raw, top3 = [], [], [], [], [], []
    for p, t in rows:
        ranked = sorted(p, key=p.get, reverse=True)
        conf.append(p[ranked[0]])
        correct.append(ranked[0] == t)
        top3.append(t in ranked[:3])
        brier.append(sum((v - (k == t)) ** 2 for k, v in p.items()))
        k = len(p)
        nll.append(-math.log((1 - NLL_EPS) * p.get(t, 0) + NLL_EPS / k))
        nll_raw.append(-math.log(max(p.get(t, 0), 1e-12)))
    conf, correct = np.array(conf), np.array(correct, float)
    bins = np.minimum((conf * 10).astype(int), 9)
    ece = sum(abs(conf[bins == b].mean() - correct[bins == b].mean()) * (bins == b).mean()
              for b in range(10) if (bins == b).any())
    return {"n": len(rows), "ECE": float(ece), "Brier": float(np.mean(brier)),
            "NLL_smoothed": float(np.mean(nll)), "NLL_raw": float(np.mean(nll_raw)), "top1": float(correct.mean()), "top3": float(np.mean(top3))}


def jsd(p, q):
    keys = sorted(set(p) | set(q))
    a = np.array([p.get(k, 0) for k in keys]) + 1e-12
    b = np.array([q.get(k, 0) for k in keys]) + 1e-12
    a, b = a / a.sum(), b / b.sum()
    m = (a + b) / 2
    return float(0.5 * (a * np.log2(a / m)).sum() + 0.5 * (b * np.log2(b / m)).sum())


def resolution(recs):
    """Amendment 1: descriptive output-resolution stats over all distributions."""
    vals = [v for r in recs for v in r["raw_probs"].values()]
    if not vals:
        return None
    v = np.array(vals, float)
    on_grid = np.abs(v * 100 - np.round(v * 100)) < 1e-6
    return {"n_values": len(v), "exact_zero_rate": float((v == 0).mean()),
            "on_0.01_grid_rate": float(on_grid.mean()),
            "min_nonzero": float(v[v > 0].min()) if (v > 0).any() else float("nan")}


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--cases", help="needed only for DDXPlus reference differentials")
    args = ap.parse_args()

    recs = [json.loads(l) for l in open(args.results)]
    errors = defaultdict(int)
    R = defaultdict(dict)  # (model, dataset) -> job_id -> rec
    for r in recs:
        if r.get("error"):
            errors[(r["model"], r["condition"])] += 1
            continue
        R[(r["model"], r["dataset"])][r["job_id"]] = r

    ref = {}
    if args.cases:
        for c in csv.DictReader(open(args.cases)):
            if c.get("reference_differential"):
                ref[c["case_id"]] = json.loads(c["reference_differential"])

    out = ["# Results summary", ""]
    commits = sorted({r.get("harness_commit", "unrecorded") for r in recs})
    versions = sorted({f'{r["model"]}={r.get("resolved_model") or r.get("model_version")}' for r in recs})
    out += [f"Harness commit(s): {', '.join(commits)}", f"Resolved model versions: {', '.join(versions)}", ""]
    out += ["## Output resolution (Amendment 1, descriptive)", ""]
    by_model = defaultdict(list)
    for r in recs:
        if not r.get("error"):
            r["raw_probs"] = r.get("raw_probs_unnormalized") or r["probs"]
            by_model[r["model"]].append(r)
    for m, rs in sorted(by_model.items()):
        res = resolution(rs)
        if res:
            out.append(f"- {m}: exact-zero rate {res['exact_zero_rate']:.1%}; values on a 0.01 grid "
                       f"{res['on_0.01_grid_rate']:.1%}; smallest nonzero {res['min_nonzero']:.2g} (n={res['n_values']})")
    out.append("")
    case_flags = defaultdict(dict)  # (dataset, test) -> model -> {case: violated}
    calib_rows = defaultdict(dict)

    for (model, ds), jobs in sorted(R.items()):
        out.append(f"## {model} / {ds}")
        by_case = defaultdict(dict)
        for jid, r in jobs.items():
            by_case[r["case_id"]][jid] = r

        # H0 noise floor
        h0_tvd, h0_lr, identical = [], [], 0
        for cid, js in by_case.items():
            reps = [js[k]["probs"] for k in sorted(js) if k.startswith("H0|")]
            for a, b in itertools.combinations(reps, 2):
                h0_tvd.append(tvd(a, b))
                h0_lr.append(log_ratio_shift(a, b))
                identical += a == b
        floor = float(np.percentile(h0_tvd, 95)) if h0_tvd else 0.0
        lr_floor = float(np.percentile(h0_lr, 95)) if h0_lr else 0.0
        if h0_tvd:
            out.append(f"- H0: {identical}/{len(h0_tvd)} repeat pairs byte-identical; "
                       f"TVD noise floor (p95) = {floor:.4f}; log-ratio floor = {lr_floor:.4f}")

        def canon(js):
            return next((js[k]["probs"] for k in js if k.endswith("|rep0")), None)

        # H1 / H2
        for test in ("H1", "H2"):
            viol, flips, tv = {}, [], []
            for cid, js in by_case.items():
                c0 = canon(js)
                vs = [js[k]["probs"] for k in js if k.startswith(test + "|")]
                if c0 is None or not vs:
                    continue
                d = [tvd(c0, v) for v in vs]
                top0 = max(c0, key=c0.get)
                flips += [max(v, key=v.get) != top0 for v in vs]
                tv.append(max(d))
                viol[cid] = max(d) > max(floor, TVD_MARGIN)
            if viol:
                k = sum(viol.values())
                ph, lo, hi = wilson(k, len(viol))
                w = stats.wilcoxon(np.array(tv) - floor, alternative="greater") if len(tv) > 5 and np.any(np.array(tv) != floor) else None
                out.append(f"- {test}: violation rate {ph:.1%} [{lo:.1%}, {hi:.1%}] (n={len(viol)}); "
                           f"top-1 flip rate {np.mean(flips):.1%}; mean max-TVD {np.mean(tv):.3f}"
                           + (f"; Wilcoxon p={w.pvalue:.3g}" if w else ""))
                case_flags[(ds, test)][model] = viol

        # H3
        viol, dmass, lrs = {}, [], []
        for cid, js in by_case.items():
            c0 = canon(js)
            for jid in (k for k in js if k.startswith("H3|")):
                r = js[jid]
                dk = r["meta"]["distractors"]
                m = sum(r["probs"].get(d, 0) for d in dk)
                sub = restrict(r["probs"], list(c0)) if c0 else None
                lr = log_ratio_shift(c0, sub) if sub else 0.0
                dmass.append(m)
                lrs.append(lr)
                viol[cid] = viol.get(cid, False) or m > DISTRACTOR_MARGIN or lr > max(lr_floor, 1e-9)
        if viol:
            ph, lo, hi = wilson(sum(viol.values()), len(viol))
            out.append(f"- H3: violation rate {ph:.1%} [{lo:.1%}, {hi:.1%}] (n={len(viol)}); "
                       f"mean distractor mass {np.mean(dmass):.4f}; mean log-ratio shift {np.mean(lrs):.3f}")
            case_flags[(ds, "H3")][model] = viol

        # H4 (vague inputs vs informative canonical runs on this dataset)
        vague = [norm_entropy(r["probs"]) for r in jobs.values() if r["condition"] == "H4"]
        inform = [norm_entropy(canon(js)) for js in by_case.values() if canon(js)]
        if vague and inform:
            u = stats.mannwhitneyu(vague, inform, alternative="less")
            out.append(f"- H4: normalized entropy vague {np.mean(vague):.3f} vs informative "
                       f"{np.mean(inform):.3f}; P(vague lower) test p={u.pvalue:.3g}; "
                       f"mean max-prob on vague {np.mean([max(r['probs'].values()) for r in jobs.values() if r['condition']=='H4']):.3f}")

        # H5
        nota_m, wrong_m, nota_top = [], [], []
        for js in by_case.values():
            for jid in js:
                if jid.endswith("|nota"):
                    p = js[jid]["probs"]
                    nota_m.append(p.get(NOTA_KEY, 0))
                    wrong_m.append(max(v for k, v in p.items() if k != NOTA_KEY))
                    nota_top.append(max(p, key=p.get) == NOTA_KEY)
        if nota_m:
            out.append(f"- H5: mean mass on none_of_these {np.mean(nota_m):.3f}; mean max wrong-option "
                       f"mass {np.mean(wrong_m):.3f}; none_of_these is top in {np.mean(nota_top):.1%}")

        # H6
        rows = [(canon(js), next(iter(js.values()))["true_dx"]) for js in by_case.values()
                if canon(js) and next(iter(js.values()))["true_dx"]]
        if rows:
            cal = calibration(rows)
            out.append("- H6: " + "; ".join(f"{k} {v:.3f}" if isinstance(v, float) else f"{k} {v}"
                                          for k, v in cal.items()))
            calib_rows[ds][model] = {cid: (canon(js), next(iter(js.values()))["true_dx"])
                                     for cid, js in by_case.items() if canon(js)}
            j = [jsd(canon(js), ref[cid]) for cid, js in by_case.items() if cid in ref and canon(js)]
            if j:
                out.append(f"- H6 (DDXPlus): mean JSD to reference differential {np.mean(j):.3f}")
        out.append("")

    # ---------- paired comparisons ----------
    out += ["## Paired model comparisons", ""]
    for (ds, test), per_model in sorted(case_flags.items()):
        for m1, m2 in itertools.combinations(sorted(per_model), 2):
            common = set(per_model[m1]) & set(per_model[m2])
            b = sum(per_model[m1][c] and not per_model[m2][c] for c in common)
            c_ = sum(per_model[m2][c] and not per_model[m1][c] for c in common)
            p = stats.binomtest(b, b + c_, 0.5).pvalue if b + c_ else float("nan")
            out.append(f"- {ds} {test}: {m1} vs {m2}, discordant {b} vs {c_}, exact McNemar p={p:.3g} (n={len(common)})")
    for ds, per_model in sorted(calib_rows.items()):
        for m1, m2 in itertools.combinations(sorted(per_model), 2):
            common = sorted(set(per_model[m1]) & set(per_model[m2]))
            if len(common) < 10:
                continue
            a = [per_model[m1][c] for c in common]
            b = [per_model[m2][c] for c in common]
            diffs = []
            for _ in range(2000):  # ECE is not a mean, so resample cases
                idx = rng.integers(0, len(common), len(common))
                diffs.append(calibration([a[i] for i in idx])["ECE"] - calibration([b[i] for i in idx])["ECE"])
            d0 = calibration(a)["ECE"] - calibration(b)["ECE"]
            bd = [sum((v - (k == t)) ** 2 for k, v in pa.items()) - sum((v - (k == t)) ** 2 for k, v in pb.items())
                  for (pa, t), (pb, _) in zip(a, b)]
            e1 = np.array([max(p, key=p.get) != t for p, t in a])
            e2 = np.array([max(p, key=p.get) != t for p, t in b])
            phi = float(np.corrcoef(e1, e2)[0, 1]) if e1.std() and e2.std() else float("nan")
            bm, blo, bhi = boot_ci(bd)
            out.append(f"- {ds} H6: ECE {m1} minus {m2} = {d0:.3f} [{np.percentile(diffs, 2.5):.3f}, "
                       f"{np.percentile(diffs, 97.5):.3f}]; Brier diff {bm:.3f} [{blo:.3f}, {bhi:.3f}]; "
                       f"top-1 error correlation (phi, exploratory) {phi:.2f}")

    if errors:
        out += ["", "## Exclusions (API failures after retries)", ""]
        out += [f"- {m} {c}: {n}" for (m, c), n in sorted(errors.items())]
    print("\n".join(out))
    print("\nNote: Holm correction across H1, H3 and H6-ECE comparisons is applied by hand "
          "from the p-values above, as pre-registered.")


if __name__ == "__main__":
    main()
