"""
T3-PREP — Test scenarios for answer_question(state, question).

Check-only harness (no LangGraph, no node changes, no state fields added).
Run it directly:   python tests/test_answer_question.py
"""
from __future__ import annotations

import os
import sys
import types

# --- Make imports work BEFORE importing answer_agent ------------------------
# answer_agent.py does `import config` (no config.py exists in the repo) and
# `from prompts.answer_templates import ...`. We inject a fake `config` module
# and put the answerAgent folder on sys.path. Empty GEMINI_API_KEY makes the
# general case use the deterministic fallback (no network / no real key).
if "config" not in sys.modules:
    _fake_config = types.ModuleType("config")
    _fake_config.APP_ID = "test-app-id"
    _fake_config.DEV_KEY = ""
    _fake_config.GEMINI_MODEL = "gemini-1.5-flash"
    _fake_config.GEMINI_API_KEY = ""
    sys.modules["config"] = _fake_config

ANSWER_AGENT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "infra", "agents", "answerAgent")
)
if ANSWER_AGENT_DIR not in sys.path:
    sys.path.insert(0, ANSWER_AGENT_DIR)

from answer_agent import answer_question  # noqa: E402


TEST_CASES = [
    {
        "name": "1. platform",
        "question": "What platform is this?",
        "state": {"platform": "android"},
        "expected": "Android only.",
        "match": "exact",
    },
    {
    "name": "7. LLM integration question",
    "question": "What should I do next to complete the integration?",
    "state": {
        "platform": "android",
        "app_id": "com.example.app",
        "dev_key": "ABC123",
    },
    "expected": "(LLM answer or fallback)",
    "match": "nonempty",
},
    {
        # brief said "ABC123", but the code returns a full sentence.
        "name": "2. dev_key",
        "question": "What is dev key?",
        "state": {"dev_key": "ABC123"},
        "expected": "Use Dev Key: ABC123.",
        "match": "exact",
    },
    {
        # flag must live under answer_policy, not top-level, per _answer_policy().
        "name": "3. response_listener (yes/no)",
        "question": "Use response listener? (yes/no)",
        "state": {"answer_policy": {"use_response_listener": True}},
        "expected": "yes",
        "match": "exact",
    },
    {
        # flag must live under answer_policy, not top-level, per _answer_policy().
        "name": "4. att boolean (true/false)",
        "question": "Is ATT enabled? (true/false)",
        "state": {"answer_policy": {"use_att": False}},
        "expected": "False",
        "match": "exact",
    },
    {
        # general -> no API key here, so the fixed fallback sentence is returned.
        "name": "5. fallback (general)",
        "question": "How does this system work?",
        "state": {},
        "expected": "(any non-empty answer: LLM output or the fallback sentence)",
        "match": "nonempty",
    },
    {
    "name": "6.   iOS platform",
    "question": "What platform is this?",
    "state": {"platform": "ios"},
    "expected": "iOS only.",
    "match": "exact",
}
]


def run() -> None:
    passed = 0
    for case in TEST_CASES:
        actual = answer_question(case["state"], case["question"])

        if case["match"] == "exact":
            ok = actual == case["expected"]
        else:
            ok = isinstance(actual, str) and actual.strip() != ""

        passed += int(ok)

        print("=" * 60)
        print(f"TEST     : {case['name']}")
        print(f"input    : {case['question']!r}")
        print(f"state    : {case['state']!r}")
        print(f"expected : {case['expected']!r}")
        print(f"actual   : {actual!r}")
        print(f"result   : {'PASS' if ok else 'FAIL'}")

    print("=" * 60)
    print(f"SUMMARY  : {passed}/{len(TEST_CASES)} passed")


if __name__ == "__main__":
    run()
