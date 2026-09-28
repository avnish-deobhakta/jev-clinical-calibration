# v4 changes (2026-09-27)

Made after the first Semigran-45 run (OSF registration osf.io/c8w9k, 2026-09-27). Each is a logged deviation in the pre-registration doc.

- D1, analyze.py: matched H1 comparison. The registered H1 criterion compares the maximum of 5 permutation distances with the 95th percentile of single repeat pairs, which flags about 23% of cases from noise alone. D1 compares per-case mean distance to the 5 permutations with mean distance to the 4 repeats. Reported alongside the registered H1 result, which is unchanged.
- D2, clients.py: the sampled-mode parser accepted only an exact key, so 13 of 45 cases in the v3 sampled arm failed with all 20 answers discarded. The v4 parser takes the exact key, else the earliest key or display name found in the answer, and logs invalid and recovered counts plus example bad answers. The arm is rerun in full as opus_sampled_v2; the v3 arm (opus_sampled) stays in results.jsonl, unused.
- D3, run.py and analyze.py: exploratory H4N condition, the 30 vague inputs with "none of these" offered.
- analyze.py: exclusions count only jobs that never succeeded.
- Notebook: data fingerprinting skips Google-native files (.gsheet and similar), which crashed the v3 setup cell.

Unchanged from v3: ddxplus_to_cases.py.
