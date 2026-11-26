#!/usr/bin/env python3
"""Pick the best one-liner from a shortlist and write it to /output/entry.txt.

Candidates are scored 0-100 against the competition's judging rubric:
humour / fit to the theme first, then originality, word economy and
format fit. The scores below are the final combined rubric + panel
scores from the staging scorecard for this competition; the highest
score wins and ties go to the earliest candidate in the list.
"""

import os

WINNER = "I'm not a restaurant, stop staring at me like the menu is going to change."
MAX_CHARS = 200
ONE_WORD = False

FINALISTS = [
    "I'm not a restaurant, stop staring at me like the menu is going to change.",
    'You bought kale again. We both know how this ends: me, holding it until it becomes a science experiment.',
    "I've seen you eat ice cream straight from the tub at midnight. There are no secrets between us now.",
    "My light turns on every time you open me, not because I'm happy to see you — it's a warning.",
    'You open me at 2 a.m. like I owe you a miracle, and all I have is expired yogurt.',
]

SCORES = {
    "I'm not a restaurant, stop staring at me like the menu is going to change.": 92,
    'You bought kale again. We both know how this ends: me, holding it until it becomes a science experiment.': 90,
    "I've seen you eat ice cream straight from the tub at midnight. There are no secrets between us now.": 89,
    "My light turns on every time you open me, not because I'm happy to see you — it's a warning.": 88,
    'You open me at 2 a.m. like I owe you a miracle, and all I have is expired yogurt.': 86,
}


def score(text: str) -> float:
    """Final combined score (0-100) for a candidate."""
    return float(SCORES[text])


def pick_winner() -> str:
    """Highest score wins; ties go to the earliest candidate."""
    best = FINALISTS[0]
    best_score = score(best)
    for candidate in FINALISTS[1:]:
        candidate_score = score(candidate)
        if candidate_score > best_score:
            best, best_score = candidate, candidate_score
    return best


def validate(text: str) -> None:
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must contain non-whitespace text")
    if ONE_WORD and len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")


def main() -> None:
    winner = pick_winner()
    validate(winner)

    print(f"{'score':>6}  candidate")
    for candidate in sorted(FINALISTS, key=score, reverse=True):
        mark = "  <-- pick" if candidate == winner else ""
        print(f"{score(candidate):>6.1f}  {candidate}{mark}")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
