# v7 changes (2026-09-27)

Holds only changed files; the notebook loads clients.py and ddxplus_to_cases.py from code/v5/ and plots.py from code/v6/.

- D6, data: the Zandi et al. 2024 (Bioengineering 11:120, CC BY 4.0) ophthalmic set replaces the Lyons et al. set, whose vignette text is published only as a low-resolution image. data/zandi_cases.csv holds 80 cases (40 diagnoses, each with a 3-descriptor and a 5-descriptor version, verbatim from Supplementary Tables S1 to S4, with the published acuity); data/zandi_options.json holds the 40 diagnosis labels as published, with short keys.
- D6, run.py: exploratory H7 options-only baseline, 5 calls per dataset per model with the state "(No patient information provided.)" and the full option list. Added to the default conditions.
- D6, analyze.py: H7 summary per model and dataset: top choice and its probability, entropy, stability across repeats, the accuracy that choice would achieve if applied to every case, and mean probability on the true diagnosis.
