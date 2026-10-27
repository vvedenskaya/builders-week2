"""Week 2 homework: fix the date extractor.

Our event bot reads show notices and puts the EVENT date on the calendar.
Right now it grabs the first date it sees, which is often the RSVP deadline.

Your job: change extract_event_date() so it returns the date of the event itself.
Only edit this file. Run the tests with:  python -m unittest -v
"""

import re
from datetime import datetime

NOTICE = (
    "BK UNDERGROUND SESSIONS #12: Presale RSVP lottery drops October 14, 2026 at 6:00 PM online. "
    "Secret warehouse doors open October 21, 2026 at 11:00 PM for the live set. "
    "Curfew strictly midnight. 21+ only."
)

DATE_PATTERN = r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (\d{4})"


def to_iso(match):
    """Turn a regex match like 'October 21, 2026' into '2026-10-21'."""
    return datetime.strptime(match.group(0), "%B %d, %Y").strftime("%Y-%m-%d")


def extract_event_date(text):
    """Return the event date as 'YYYY-MM-DD', or None if the notice has no event date."""
    deadline_words = ["rsvp", "deadline", "presale", "pre-sale", "lottery", "register",
                      "registration", "sign up", "signup", "tickets", "on sale", "due", "by"]
    event_words = ["doors", "show", "event", "concert", "live", "performance",
                   "takes place", "starts", "begins", "party", "festival"]

    deadline_re = re.compile(r"\b(" + "|".join(map(re.escape, deadline_words)) + r")\b")
    event_re = re.compile(r"\b(" + "|".join(map(re.escape, event_words)) + r")\b")

    fallback = None
    prev_end = 0

    for match in re.finditer(DATE_PATTERN, text):
        # The words leading up to this date: since the previous date,
        # and only within the current sentence.
        before = text[prev_end:match.start()].lower()
        before = re.split(r"[.!?;]\s", before)[-1]
        prev_end = match.end()

        if deadline_re.search(before):
            continue                      # an RSVP/presale date, skip it
        if event_re.search(before):
            return to_iso(match)          # clearly the event
        if fallback is None:
            fallback = match              # unlabeled, keep as a backup

    return to_iso(fallback) if fallback else None

if __name__ == "__main__":
    print("Event date:", extract_event_date(NOTICE))
