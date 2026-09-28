"""v6: reliability diagrams (calibration curves) per dataset, one line per model.

Usage: python plots.py results.jsonl --outdir runs/figures [--exclude opus_sampled,opus_sampled_v2]

Uses each model's canonical run (H0 rep0) on every case with a known diagnosis. Top-1
confidence is binned into 10 equal-width bins; each point is mean confidence vs observed
accuracy in that bin, with marker area proportional to the number of cases. Writes one PNG
and one CSV of bin statistics per dataset.
"""
import argparse
import csv
import json
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LABELS = {"jev": "Jev 1.13", "opus5_nothink": "Claude Opus 5 (thinking off)",
          "opus_verbalized": "Claude Opus 5.5 (thinking on)"}
STYLE = {"jev": ("o", "-", "#c0392b"), "opus5_nothink": ("s", "--", "#2c7fb8"),
         "opus_verbalized": ("^", ":", "#41ab5d")}


def top1(p):
    return max(sorted(p), key=p.get)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--exclude", default="opus_sampled,opus_sampled_v2")
    a = ap.parse_args()
    excluded = set(filter(None, a.exclude.split(",")))
    os.makedirs(a.outdir, exist_ok=True)

    rows = defaultdict(lambda: defaultdict(list))  # dataset -> model -> [(conf, correct)]
    for line in open(a.results):
        r = json.loads(line)
        if (r["model"] in excluded or r.get("error") or not r.get("true_dx")
                or not r["job_id"].startswith("H0|") or not r["job_id"].endswith("|rep0")):
            continue
        p = r["probs"]
        k = top1(p)
        rows[r["dataset"]][r["model"]].append((p[k], k == r["true_dx"]))

    edges = np.linspace(0, 1, 11)
    for ds, per_model in sorted(rows.items()):
        fig, ax = plt.subplots(figsize=(5.5, 5.5))
        ax.plot([0, 1], [0, 1], color="0.6", lw=1, label="Perfect calibration")
        stats_out = []
        for m in sorted(per_model):
            conf = np.array([c for c, _ in per_model[m]])
            corr = np.array([x for _, x in per_model[m]], float)
            idx = np.minimum(np.digitize(conf, edges) - 1, 9)
            xs, ys, ns = [], [], []
            for b in range(10):
                sel = idx == b
                if sel.any():
                    xs.append(conf[sel].mean()); ys.append(corr[sel].mean()); ns.append(int(sel.sum()))
                    stats_out.append({"model": m, "bin": f"{edges[b]:.1f}-{edges[b + 1]:.1f}",
                                      "n": ns[-1], "mean_confidence": round(xs[-1], 4),
                                      "accuracy": round(ys[-1], 4)})
            mk, ls, col = STYLE.get(m, ("d", "-", "0.4"))
            ax.plot(xs, ys, ls, color=col, lw=1.2)
            ax.scatter(xs, ys, s=[max(12, 400 * n / len(conf)) for n in ns], marker=mk, color=col,
                       label=f"{LABELS.get(m, m)} (n={len(conf)})", alpha=0.8)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xlabel("Top-1 confidence"); ax.set_ylabel("Observed accuracy")
        ax.set_title(f"Calibration on {ds}")
        ax.legend(loc="upper left", fontsize=8, frameon=False)
        fig.tight_layout()
        fig.savefig(os.path.join(a.outdir, f"reliability_{ds}.png"), dpi=200)
        plt.close(fig)
        with open(os.path.join(a.outdir, f"reliability_{ds}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["model", "bin", "n", "mean_confidence", "accuracy"])
            w.writeheader(); w.writerows(stats_out)
        print(f"wrote reliability_{ds}.png and .csv")


if __name__ == "__main__":
    main()
