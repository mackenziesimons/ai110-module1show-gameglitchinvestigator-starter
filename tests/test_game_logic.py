import ast
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from logic_utils import check_guess


def _load_update_score_from_app():
    source = Path("app.py").read_text(encoding="utf-8")
    tree = ast.parse(source, filename="app.py")

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "update_score":
            module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(module)
            namespace = {}
            exec(compile(module, filename="app.py", mode="exec"), namespace)
            return namespace["update_score"]

    raise AssertionError("update_score function not found in app.py")

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


def test_update_score_too_high_always_deducts_five_points():
    # Regression test for the parity bug: "Too High" should always deduct 5 points.
    update_score = _load_update_score_from_app()

    start_score = 20
    odd_attempt_score = update_score(start_score, "Too High", 1)
    even_attempt_score = update_score(start_score, "Too High", 2)

    assert odd_attempt_score == 15
    assert even_attempt_score == 15
