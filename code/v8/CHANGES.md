# v8 changes (2026-09-27)

Analysis only; no model calls. Holds only analyze.py; the notebook loads run.py from code/v7/, plots.py from code/v6/, and clients.py and ddxplus_to_cases.py from code/v5/.

- Bug fix: the canonical run is now identified as the H0 repeat 0 only. In v7 the options-only (H7) jobs also ended in rep0, so each dataset's options-only series was counted as one extra case, with no true diagnosis, in the paired model comparisons (paired accuracy, ECE and Brier differences) and in the informative-case entropy of H4. Per-model accuracy and calibration, zero-probability rates, McNemar discordance counts and the H7 results were not affected.
- Exploratory: top-1 accuracy by number of descriptors for paired case sets (case ids ending _d3 and _d5, the Zandi set), with an exact McNemar test within each model.
