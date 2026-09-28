"""Model clients. Each returns (probs: dict[key -> float], raw: any).

Jev is called through OpenRouter's System One API (no TypeSafe waitlist).
VERIFY on first live call: the exact shape of the Choice answer. This parser
expects answers[<question>]["probabilities"] = {key: p}; it saves the raw
response either way so nothing is lost if the shape differs.
"""
import hashlib
import json
import os
import re
import time

import numpy as np
import requests

INSTRUCTION = "Which diagnosis best explains this patient's presentation?"

JEV_URL = "https://openrouter.ai/api/v1/systemone"
JEV_MODEL = "jev-1.13"            # pinned; never the moving jev-latest alias
OPUS_MODEL = "claude-opus-5-5"    # pinned


def _retry(fn, tries=3):
    for i in range(tries):
        try:
            return fn()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def _normalize(probs, keys):
    p = {k: max(float(probs.get(k, 0.0)), 0.0) for k in keys}
    s = sum(p.values())
    if s <= 0:
        raise ValueError("all-zero distribution")
    return {k: v / s for k, v in p.items()}, s


class JevClient:
    name = "jev"
    version = JEV_MODEL

    def __init__(self):
        self.key = os.environ["OPENROUTER_API_KEY"]

    def classify(self, state, options):
        """options: ordered dict key -> description (order is what we test)."""
        body = {
            "model": JEV_MODEL,
            "state": state,
            "questions": {
                "dx": {"type": "choice", "instructions": INSTRUCTION,
                       "criteria": dict(options)},
            },
        }

        def call():
            r = requests.post(JEV_URL, json=body, timeout=60,
                              headers={"Authorization": f"Bearer {self.key}"})
            r.raise_for_status()
            return r.json()

        raw = _retry(call)
        ans = raw.get("answers", {}).get("dx", {})
        probs = ans.get("probabilities")
        if not isinstance(probs, dict):
            raise ValueError(f"Unexpected Jev answer shape: {json.dumps(ans)[:300]}")
        p, s = _normalize(probs, list(options))
        return p, {"response": raw, "raw_sum": s, "resolved_model": raw.get("model")}


def _claude_prompt(state, options, mode):
    lines = "\n".join(f"{k}: {v}" for k, v in options.items())
    if mode == "verbalized":
        tail = ("Return a JSON object mapping EVERY option key above to your probability "
                "that it is the correct answer. Probabilities must sum to 1. Output only the JSON.")
    else:
        tail = "Output only the single option key you choose, nothing else."
    return (f"Patient presentation:\n{state}\n\nQuestion: {INSTRUCTION}\n\n"
            f"Options (key: description):\n{lines}\n\n{tail}")


class OpusClient:
    """mode='verbalized' (primary) or 'sampled' (n single-answer calls)."""
    version = OPUS_MODEL

    def __init__(self, mode="verbalized", n_samples=20):
        import anthropic
        self.client = anthropic.Anthropic()
        self.mode = mode
        self.n = n_samples
        self.name = f"opus_{mode}"

    def _ask(self, prompt, max_tokens):
        def call():
            m = self.client.messages.create(
                model=OPUS_MODEL, max_tokens=max_tokens,
                system="You are a diagnostic classifier. Follow the output format exactly.",
                messages=[{"role": "user", "content": prompt}])
            self.resolved_model = getattr(m, "model", None)
            return "".join(b.text for b in m.content if getattr(b, "type", "") == "text")
        return _retry(call)

    def classify(self, state, options):
        keys = list(options)
        if self.mode == "verbalized":
            text = self._ask(_claude_prompt(state, options, "verbalized"), 3000)
            match = re.search(r"\{.*\}", text, re.S)
            parsed = json.loads(match.group(0)) if match else {}
            unknown = [k for k in parsed if k not in options]
            p, s = _normalize(parsed, keys)
            return p, {"text": text, "raw_sum": s, "unknown_keys": unknown,
                       "resolved_model": getattr(self, "resolved_model", None),
                       "malformed": abs(s - 1) > 0.02 or bool(unknown)}
        counts = {k: 0 for k in keys}
        invalid = 0
        for _ in range(self.n):
            ans = self._ask(_claude_prompt(state, options, "sampled"), 50).strip().strip("`\"' ")
            if ans in counts:
                counts[ans] += 1
            else:
                invalid += 1
        p, _ = _normalize(counts, keys)
        return p, {"counts": counts, "invalid": invalid,
                   "resolved_model": getattr(self, "resolved_model", None)}


class MockClient:
    """Offline stand-in. Deterministic in (state, option set), with a small
    order effect so the analysis code has something to detect."""
    name = "mock"
    version = "mock-0"

    def __init__(self, order_bias=0.15):
        self.order_bias = order_bias

    def classify(self, state, options):
        keys = list(options)
        seed = int(hashlib.md5((state + "|".join(sorted(keys))).encode()).hexdigest()[:8], 16)
        rng = np.random.default_rng(seed)
        logits = rng.normal(0, 1.5, len(keys))
        # crude "understanding": boost options whose words appear in the state
        for i, k in enumerate(keys):
            if any(w in state.lower() for w in k.split("_") if len(w) > 4):
                logits[i] += 3
        logits[0] += self.order_bias * 5  # first-position bias
        p = np.exp(logits - logits.max())
        p /= p.sum()
        return dict(zip(keys, p.tolist())), {"mock": True}


def get_client(name):
    if name == "jev":
        return JevClient()
    if name == "opus_verbalized":
        return OpusClient("verbalized")
    if name == "opus_sampled":
        return OpusClient("sampled")
    if name == "mock":
        return MockClient()
    raise ValueError(name)
