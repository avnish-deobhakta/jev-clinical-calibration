# jev_bench changelog

Layout: notebooks/ holds one notebook per version; code/<version>/ holds that version's harness, never edited after creation (a change means a new version folder). Each notebook verifies its code folder against SHA-256 hashes before running. data/ holds study data (hashed, never committed). runs/ holds the latest manifest, notebook snapshot and summary. versions/ holds timestamped manifest copies. The folder is also a git repository, committed by the notebook at setup, before each run and after analysis.

## v3 (2026-09-26)
- Harness code and notebook stored directly in Drive by Claude; no local download or upload needed.
- Notebook loads code/v3/ and refuses to run on any hash mismatch.
- Snapshots write to runs/ and versions/; git history covers the whole folder.
- Harness code identical to v2.

## v2 (2026-09-26, delivered as a download; not run)
- Amendment 1: smoothed NLL (1% uniform mix) primary, raw NLL alongside; output resolution and exact-zero rate reported per model.
- Result rows record harness commit and provider-resolved model version.
- Data sections skip cleanly when files are missing.

## v1 (2026-09-26)
- Initial harness. Pilot confirmed the Jev response format (typesafe/jev-1.13-20260917) and Opus verbalized parsing on one toy case.
