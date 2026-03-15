# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
When I first ran the app, it loaded visually — text input, submit button, sidebar difficulty settings — but it was impossible to win. The hints were completely backwards: when my guess was too high, the game told me to go higher, and when too low, it told me to go lower. On every even-numbered attempt, the secret was silently cast to a string (secret = str(st.session_state.secret)), so comparisons used lexicographic ordering — meaning a guess of 19 appeared "higher" than 50 because "1" sorts after "5" as a character. There was also an off-by-one error where attempts was initialized to 1 instead of 0, and the New Game button didn't reset status or history, so old game state bled into new rounds.



## 2. How did you use AI as a teammate?
I used Claude Code as my primary AI tool throughout this project. One AI suggestion that was correct: it identified that check_guess had the "Too High" and "Too Low" labels swapped and pointed to the exact inverted emoji lines — I verified by tracing a known example by hand (guess = 60, secret = 50 should give "Too High" / "Go LOWER"). One AI suggestion I had to push back on: AI initially proposed fixing the string/int mismatch by casting the guess to a string as well — that would have silenced the TypeError but introduced broken lexicographic ordering for all comparisons; the correct fix was to remove the cast on the secret entirely and always compare integers.
---

## 3. Debugging and testing your fixes

I decided a bug was fixed by first tracing the code logic manually, then confirming in the running app with the Developer Debug Info panel open so I could see the secret number and attempt count in real time. I ran the pytest suite in tests/test_game_logic.py, which tests check_guess with three known cases: check_guess(50, 50) → "Win", check_guess(60, 50) → "Too High", check_guess(40, 50) → "Too Low" — before my fix, all three hint tests produced the wrong outcome because the labels were inverted. AI helped me realize the tests import from logic_utils, so fixing only app.py was not enough — the functions needed to be correctly implemented in logic_utils.py too.
---

## 4. What did you learn about Streamlit and state?

In the original app, the secret appeared to change on every interaction because the type-conversion bug made comparisons behave inconsistently — on even attempts the secret was a string, producing different hint outputs for the same number. Streamlit "reruns" means the entire Python script re-executes from top to bottom every time a user clicks a button; regular local variables are wiped out and recomputed each time. Session state (st.session_state) is a persistent dictionary that survives reruns — anything stored there keeps its value. The fix that gave the game a stable secret was guarding generation with if "secret" not in st.session_state: so the number is picked only once, then always reading it back as an integer with no casting.

---

## 5. Looking ahead: your developer habits
One habit I want to carry forward is adding a visible debug panel early in development — exposing internal state like the secret number, attempt count, and history directly in the UI made it much faster to see what was actually happening. Next time I work with AI on a coding task, I would test the suggestion immediately rather than reading it and assuming it is correct — the string-cast proposal looked plausible but would have created a new bug. This project changed how I think about AI-generated code: it can produce something that looks right and runs without crashing while being subtly wrong in ways that only surface under specific conditions, so treating AI output as a first draft to verify — not a finished answer — is the right mindset.