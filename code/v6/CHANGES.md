# v6 changes (2026-09-27)

Analysis only; no model calls and no change to how data are collected. This folder holds only the files that changed; the notebook loads clients.py, run.py and ddxplus_to_cases.py unchanged from code/v5/.

- analyze.py: paired exact McNemar test on top-1 accuracy for every model pair and dataset; per model, the rate of exactly zero probability on the true diagnosis (with Wilson interval) and the rate of the true diagnosis falling outside the top 3; paired test on zero-on-truth. All other outputs unchanged from v5.
- plots.py (new): reliability diagram per dataset with one line per model (canonical runs, 10 equal-width bins on top-1 confidence, marker area proportional to bin size), plus a CSV of bin statistics. Written to runs/figures/.
