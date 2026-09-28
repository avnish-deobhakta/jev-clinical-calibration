# jev-clinical-calibration

Code, data and results for **"Do Calibrated-Probability Claims Hold Up in Clinical Diagnosis? A Pre-registered Evaluation of a Decision Model Against Frontier Language Models"** (Deobhakta, 2026; preprint link to be added).

The study compares Jev 1.13 (TypeSafe AI), a single-pass decision model that returns a probability for every option, with Claude Opus 5.5 (adaptive reasoning, always on) and Claude Opus 5 (reasoning disabled) on three diagnostic case sets. Pre-registration: [osf.io/fpmg3](https://osf.io/fpmg3) (26 September 2026, before the first study model call).

## Main results

| Case set | Measure | Jev | Opus 5, reasoning off | Opus 5.5, reasoning on |
| --- | --- | --- | --- | --- |
| DDXPlus (n = 1,000) | Top-1 accuracy | 72.0% | 79.5% | 87.4% |
| DDXPlus | Expected calibration error | 0.116 | 0.073 | 0.109 |
| DDXPlus | True diagnosis given exactly 0% | 62 | 0 | 0 |
| Ophthalmic complaints (n = 80) | Top-1 accuracy | 88.8% | 91.2% | 88.8% |
| Ophthalmic complaints | Expected calibration error | 0.065 | 0.122 | 0.146 |
| Semigran vignettes (n = 45) | Top-1 accuracy | 84.4% | 88.9% | 93.3% |

Full outputs are in `results/summary.md`; figures are in `results/figures/`.

## Repository layout

| Path | Contents |
| --- | --- |
| `code/current/` | The harness as used for the final analysis: `clients.py` (model calls), `run.py` (conditions, resumable runner), `analyze.py` (all outcomes), `plots.py` (calibration figures), `ddxplus_to_cases.py` (DDXPlus rendering) |
| `code/v3/` to `code/v8/` | Every version of the harness, unchanged since use, each with a `CHANGES.md` |
| `notebooks/` | The Google Colab notebook for each version, in the order they were run |
| `data/` | Case files, option lists and sign-offs (see Data below) |
| `results/` | `results.jsonl.gz` (every model call, one JSON object per line), `summary.md`, figures, the run manifest and the Opus 5.5 reasoning-token audit |
| `CHANGELOG.md` | Version history of the study |

Every result row records the harness commit it ran under (`harness_commit`) and the model version the provider resolved (`resolved_model`). Version folders were never edited after creation; each Colab notebook verifies its code against SHA-256 hashes before running.

## Data

| File | Source | License | Included |
| --- | --- | --- | --- |
| `data/ddxplus_cases.csv`, `data/ddxplus_options.json` | 1,000 cases sampled (stratified, seed 20260926) from the DDXPlus test set, Fansi Tchango et al. 2022, rendered to prose by `ddxplus_to_cases.py` | CC BY 4.0 | Yes |
| `data/zandi_cases.csv`, `data/zandi_options.json` | Zandi et al., Bioengineering 2024;11(2):120, Supplementary Tables S1 to S4, verbatim | CC BY 4.0 | Yes |
| `data/vague.csv` | 30 uninformative inputs written for this study | CC BY 4.0 | Yes |
| `data/semigran_case_index.csv`, `data/options.json` | Semigran et al., BMJ 2015;351:h3480 | Case text not redistributed | Case identifiers, diagnoses and triage levels only; obtain the vignette text from the BMJ supplementary appendix |

The raw DDXPlus release files are not included; download them from the official figshare record (English version) to regenerate `ddxplus_cases.csv`.

## Reproducing the analysis

No API keys are needed to reproduce the reported numbers from the stored results:

```
pip install numpy scipy matplotlib
gunzip -k results/results.jsonl.gz
cd code/current
python analyze.py ../../results/results.jsonl --cases ../../data/ddxplus_cases.csv > summary.md
python plots.py ../../results/results.jsonl --outdir figures
```

To rerun model calls, set `OPENROUTER_API_KEY` (Jev) and `ANTHROPIC_API_KEY` (Claude) and use `run.py`; see the notebooks for the exact commands. Model outputs vary between runs, and hosted models change over time, so new calls will not reproduce the stored outputs exactly.

## Disclosures

The harness, analysis code and a first draft of the manuscript were written with assistance from Claude (Anthropic), a model family that is also a comparator in this study. The analysis plan was pre-registered before data collection, and every deviation is listed in the manuscript and in the version `CHANGES.md` files. The author is CEO of Avant Sciences, Inc., a medical device company with no financial relationship with TypeSafe AI, OpenRouter or Anthropic.

## Citation

See `CITATION.cff`. Code is released under the MIT License (`LICENSE`); data files carry the licenses listed above.
