"""Optional challenge: route the event bot's inbox. No API key needed.

The BK UNDERGROUND SESSIONS #12 inbox is filling up. Right now every message
goes to an LLM, which is the slow, expensive default. Route each message to the
smallest tier that can handle it safely:

    "rules"  - a plain fact from the notice (doors, date, curfew, age). Code can answer. Cost: $0.
    "model"  - needs language skills (vibe, captions, advice). A light model can draft it.
    "human"  - money, safety, or exceptions to policy. A person must decide.

Step 1: change ATTEMPTING to True so the challenge tests run.
Step 2: rewrite route() until all router tests pass.
See the report any time with:  python router.py
"""

import re

ATTEMPTING = True

def has_word(message, word):
    pattern = r"\b" + re.escape(word) + r"\b"
    return re.search(pattern, message) is not None


def route(message):
    """Return 'rules', 'model', or 'human'."""
    message = message.lower()

    # 1. Check high-risk requests first
    human_words = [
        "hurt", "injured", "injury", "emergency","harassing", "harassment",
        "unsafe", "charged", "refund", "payment",
        "lost my id", "without id", "exception",
    ]

    for word in human_words:
        if has_word(message, word):
            return "human"

    # 2. Check simple factual questions
    rules_words = [
        "doors", "curfew", "date",
        "age", "end",
    ]
    if "21+" in message:
        return "rules"
        
    for word in rules_words:
        if has_word(message, word):
            return "rules"

    # 3. Everything else goes to the model
    return "model"



if __name__ == "__main__":
    counts = {"rules": 0, "model": 0, "human": 0}
    for message in INBOX:
        tier = route(message)
        counts[tier] = counts.get(tier, 0) + 1
        print(f"{tier:>6}  {message}")
    print(f"\nLLM calls: {counts['model']} of {len(INBOX)} messages")
