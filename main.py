#!/usr/bin/env python3
"""Pick the best one-liner from a shortlist and write it to /output/entry.txt.

Contest: "Fridge Roast: One Line, Biggest Laugh" (make.fun, slug
u-gentle-badger-68-fridge-roast-one-line-biggest-laugh-a7c354bb, $5, entries
close 26 Nov 2026 22:40 WIB, at most 200 characters).

How the winner was chosen (staging scorecard, 26 Nov 2026 ~08:30 WIB):
- Rubric (/10 per dimension, total = 0.4*theme + 0.3*originality
  + 0.15*density + 0.15*format) over 10 candidates; the top 5 are the
  FINALISTS below, with their exact rubric totals.
- Model-combo panel (Gemini): FAILED TOTALLY — gemini-4-hydrogen and
  gemini-3.6-flash both returned 503 UNAVAILABLE three times. No panel
  score exists and none was invented, so the combined score here is the
  rubric score alone.
- Winner: #2, "I'm not a restaurant, stop staring at me like the menu is
  going to change." (9.15) — the most universal and densest roast:
  everyone has stared into an empty fridge hoping its contents changed,
  and the fridge answers in one line. Theme 9, originality 9, density 9:
  no wasted word, the fridge's voice is clear, the punchline lands at once.

The program re-derives the pick from the scores: highest combined score
wins, ties go to the earliest candidate in the list.

v6 adds JUDGES_NOTES (the per-finalist judging notes from the scorecard)
and stricter validation: the entry must be exactly one line with no
leading/trailing whitespace, so a stray newline can never slip into the
submitted text.
"""

import os

WINNER = "I'm not a restaurant, stop staring at me like the menu is going to change."
MAX_CHARS = 200
ONE_WORD = False

# Top 5 of 10 candidates by rubric total, highest first.
FINALISTS = [
    "I'm not a restaurant, stop staring at me like the menu is going to change.",
    "You bought kale again. We both know how this ends: me, holding it until it becomes a science experiment.",
    "I've seen you eat ice cream straight from the tub at midnight. There are no secrets between us now.",
    "My light turns on every time you open me, not because I'm happy to see you — it's a warning.",
    "You open me at 2 a.m. like I owe you a miracle, and all I have is expired yogurt.",
]

# Rubric totals (/10) from candidates.md, exactly as staged.
RUBRIC = {
    "I'm not a restaurant, stop staring at me like the menu is going to change.": 9.15,
    "You bought kale again. We both know how this ends: me, holding it until it becomes a science experiment.": 9.00,
    "I've seen you eat ice cream straight from the tub at midnight. There are no secrets between us now.": 8.85,
    "My light turns on every time you open me, not because I'm happy to see you — it's a warning.": 8.75,
    "You open me at 2 a.m. like I owe you a miracle, and all I have is expired yogurt.": 8.55,
}

# Gemini panel scores: none — the panel failed totally (503), see docstring.
PANEL = {}

# Final combined score = rubric score (panel unavailable).
SCORES = dict(RUBRIC)

# Judging notes per finalist, quoted from the staging scorecard.
# The winner's note explains why it beat the runner-up; the runner-up
# notes explain why each fell short. Panel: no scores (503, see above).
JUDGES_NOTES = {
    "I'm not a restaurant, stop staring at me like the menu is going to change.":
        "WINNER. Most universal and densest roast — everyone has stared "
        "into an empty fridge hoping its contents changed. Theme 9, "
        "originality 9, density 9: no wasted word, the fridge's voice is "
        "clear, the punchline lands at once.",
    "You bought kale again. We both know how this ends: me, holding it until it becomes a science experiment.":
        "Runner-up (9.00). Loses narrowly: the premise is more specific — "
        "not everyone buys kale.",
    "I've seen you eat ice cream straight from the tub at midnight. There are no secrets between us now.":
        "Strong midnight-confession angle; the 'no secrets' payoff is a "
        "touch softer than the winner's menu gag.",
    "My light turns on every time you open me, not because I'm happy to see you — it's a warning.":
        "Clever light-as-warning twist; slightly less relatable than the "
        "empty-fridge stare.",
    "You open me at 2 a.m. like I owe you a miracle, and all I have is expired yogurt.":
        "Good 2 a.m. premise; the expired-yogurt payoff is familiar ground.",
}


def score(text: str) -> float:
    """Final combined score (/10) for a candidate."""
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
    # Stricter than the contest minimum: the entry must be exactly one
    # line, with no leading/trailing whitespace and no line breaks, so
    # the file we write is exactly the staged winner text.
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
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
        print(f"{score(candidate):>6.2f}  {candidate}{mark}")
    print(f"judge: {JUDGES_NOTES[winner]}")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
