import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        #FIX: AI assisted - Adjusted the range for Hard difficulty.
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
            #FIX: AI assisted - Handling decimal inputs by converting to int.
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."
        #FIX: AI assisted - Added clear error handling after reviewing AI suggestions for input validation.

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
            #FIX: AI assisted - Corrected the reverse logic after debugging with AI explanation of comparison logic.
        else:
            return "Too Low", "📈 Go HIGHER!"
            #FIX: AI assisted - Adjusted hint direction based on AI debugging feedback.
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"
        #FIX: AI assisted - Kept fallback comparison but corrected hint logic with AI help.


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
        #FIX: AI assisted - AI helped verify scoring formula so early wins would reward more points.

    if outcome in ("Too High", "Too Low"):
        return current_score - 5
        #FIX: AI assisted - Simplified scoring logic with AI guidance so both wrong guesses reduce score consistently.

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
    #FIX: AI assisted - AI suggested using difficulty based range when generating the secret number.

if "attempts" not in st.session_state:
    st.session_state.attempts = 0
    #FIX: AI assisted - Changed starting attempts to 0 after AI debugging pointed out the player lost an attempt immediately.

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_id" not in st.session_state:
    st.session_state.game_id = 0
    #FIX: AI assisted - Added game_id after AI suggested it properly reset Streamlit input fields when starting a new game.

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.game_id += 1
    #FIX: AI assisted - AI helped reset all game state values when difficulty changes to avoid leftover data bugs.
    st.rerun()

st.subheader("Make a guess")

attempts_info = st.empty()

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.game_id}"
)
#FIX: AI assisted - AI reccomended dynamic keys so Streamlit refreshes the input field correctly when starting a new game or changing difficulty.

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.game_id += 1
    #FIX: AI assisted - Reset all session variables after reviewing AI debugging suggestions to ensure a clean state for a new game.
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    elif guess_int < low or guess_int > high:
        st.session_state.history.append(guess_int)
        st.error(f"Please enter a number between {low} and {high}.")
        #FIX: AI assisted - AI helped add range validation so guesses outside difficulty limits are rejected.
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret
        #FIX: AI assisted - Removed earlier bug where the secret was converted to a string after AI debugging identified comparison issues.

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

attempts_left = max(attempt_limit - st.session_state.attempts, 0)
attempts_info.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)
#FIX: AI assisted - AI helped correct attempt display so it never shows negative attempts left.

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
