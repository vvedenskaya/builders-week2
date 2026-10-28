# Decision: The Three C's

One or two sentences each. Replace the text after each arrow.

## Level 1 (required)

**Complexity:**

This is mostly a rule-based task, so I used Python instead of an LLM. The dates have a predictable format, and I can use regex and keywords to find them. Understanding which date belongs to the event requires some context, but for these notices, simple rules are enough.

**Context:**

My code needed to look at the words around each date, not just the date itself. For example, "RSVP", "presale", and "registration closes" indicate a deadline, while "doors open" or "join us on" indicate an event. I used this context to avoid putting the wrong date on the calendar.

**Criticism:**

A test like `assert len(date) > 0` only checks that something was returned. It doesn't check if it's the correct date, if the format is valid, or if it's actually the event date rather than an RSVP deadline.

Before adding the event to the calendar, a human should still verify the date, time, timezone, and location against the original notice, especially if there are multiple dates or ambiguous information.
→

## Level 2 (optional challenge)

**Order matters:**

The human check has to run first because some messages contain both a simple keyword and a serious issue. For example, "I got hurt near the doors" contains "doors", but it's a safety issue. If we check rules first, it could be routed incorrectly. So I prioritized human intervention.

**Cost:**

Before my changes, all 8 messages were sent to the LLM. After adding the router, only 2 out of 8 go to the LLM. The other 6 are handled by rules or escalated to a human. So we reduced LLM calls by 75%.

**Your call:**

I would pick "What's the vibe, more techno or house?" I routed it to the model because it requires understanding the event's atmosphere, not just extracting a fact. But I could argue it belongs in rules if the music genre was explicitly stated in the notice.
→

## Level 3 (optional bonus)

**Escalation:**

I would escalate messages when the light model cannot provide a reliable answer. The heavy model is worth the extra tokens only if it meaningfully improves the response. I would compare both answers before deciding.

**One change:**

I would first try changing the escalation rule to avoid sending simple requests to the heavy model. Then I would compare the token totals before and after the change to see how much it saved without reducing answer quality.
