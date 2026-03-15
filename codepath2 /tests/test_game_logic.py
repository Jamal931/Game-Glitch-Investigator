from logic_utils import check_guess, parse_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# Regression test: original bug — hints were backwards (Too High fired "Go HIGHER!")
def test_high_guess_is_not_too_low():
    """A guess well above the secret must never come back as Too Low."""
    result = check_guess(99, 1)
    assert result == "Too High"


# Regression test: original bug — no range validation in parse_guess
def test_out_of_range_guess_rejected():
    """A guess outside [low, high] must be rejected with an error message."""
    ok, _, err = parse_guess("150", 1, 100)
    assert not ok
    assert "between" in err
