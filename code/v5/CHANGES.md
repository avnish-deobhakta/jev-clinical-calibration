# v5 changes (2026-09-27)

Made after a diagnostic call showed Claude Opus 5.5 thinks before answering on every request (thinking blocks in both the sampled and verbalized modes). Claude Opus 5.5 does not accept thinking disabled, so the pre-registered rule that Claude answers without chain-of-thought could not be met with the registered model.

- D4, clients.py and run.py: new arm opus5_nothink, Claude Opus 5 (claude-opus-5) with thinking={"type": "disabled"} and effort "high", the highest effort at which Opus 5 allows thinking off. Same prompt, options and instruction as the Opus 5.5 arm. This is the single-pass comparator the pre-registration intended; the Opus 5.5 arm is kept as the registered, real-world comparator.
- clients.py: every Opus call now records input, output and thinking token counts, stop reason and response block types.
- D5, analyze.py: Opus sampled arms (opus_sampled, opus_sampled_v2) excluded from analysis by default. In v4 the 14 failures were Opus 5.5 spending its 50-token budget on thinking, and every successful case gave the same answer 20 of 20 times, so the arm cannot measure calibration.
- analyze.py: top-1 ties broken alphabetically; previously ties were broken by option order, which could register a spurious top-1 flip under permutation for tied outputs (relevant to Jev's 0.01-grid probabilities). Adds a token-usage section.
- Notebook: live check covers all three models; optional Opus 5.5 thinking audit (45 calls, saved outside results.jsonl); sampled cell removed.

Unchanged from v4: ddxplus_to_cases.py.
