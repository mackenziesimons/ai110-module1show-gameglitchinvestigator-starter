import ast
from pathlib import Path


def _load_get_range_for_difficulty_from_app():
    source = Path("app.py").read_text(encoding="utf-8")
    tree = ast.parse(source, filename="app.py")

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "get_range_for_difficulty":
            module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(module)
            namespace = {}
            exec(compile(module, filename="app.py", mode="exec"), namespace)
            return namespace["get_range_for_difficulty"]

    raise AssertionError("get_range_for_difficulty function not found in app.py")


def _load_check_guess_from_app():
    source = Path("app.py").read_text(encoding="utf-8")
    tree = ast.parse(source, filename="app.py")

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "check_guess":
            module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(module)
            namespace = {}
            exec(compile(module, filename="app.py", mode="exec"), namespace)
            return namespace["check_guess"]

    raise AssertionError("check_guess function not found in app.py")


def _find_attempts_initial_value_from_app():
    source = Path("app.py").read_text(encoding="utf-8")
    tree = ast.parse(source, filename="app.py")

    for node in tree.body:
        if not isinstance(node, ast.If):
            continue

        test = node.test
        is_attempts_guard = (
            isinstance(test, ast.Compare)
            and len(test.ops) == 1
            and isinstance(test.ops[0], ast.NotIn)
            and isinstance(test.left, ast.Constant)
            and test.left.value == "attempts"
        )
        if not is_attempts_guard:
            continue

        for stmt in node.body:
            if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
                continue

            target = stmt.targets[0]
            is_attempts_assignment = (
                isinstance(target, ast.Attribute)
                and target.attr == "attempts"
                and isinstance(target.value, ast.Attribute)
                and target.value.attr == "session_state"
                and isinstance(target.value.value, ast.Name)
                and target.value.value.id == "st"
            )
            if not is_attempts_assignment:
                continue

            if isinstance(stmt.value, ast.Constant):
                return stmt.value.value
            raise AssertionError("attempts initializer must be a constant integer")

    raise AssertionError("Could not find attempts initialization block in app.py")


def test_check_guess_hint_direction_regression():
    """Too High must say LOWER and Too Low must say HIGHER."""
    check_guess = _load_check_guess_from_app()

    too_high_outcome, too_high_hint = check_guess(60, 50)
    too_low_outcome, too_low_hint = check_guess(40, 50)

    assert too_high_outcome == "Too High"
    assert too_high_hint == "📉 Go LOWER!"
    assert too_low_outcome == "Too Low"
    assert too_low_hint == "📈 Go HIGHER!"


def test_hard_difficulty_range_is_not_smaller_than_normal_regression():
    """Hard mode must have a larger range than Normal mode."""
    get_range_for_difficulty = _load_get_range_for_difficulty_from_app()

    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    assert hard_low == normal_low
    assert hard_high > normal_high


def test_attempts_initialize_to_zero_regression():
    """Attempts must initialize to 0 so attempt_limit is enforced correctly."""
    attempts_initial_value = _find_attempts_initial_value_from_app()
    assert attempts_initial_value == 0


def test_guess_info_uses_dynamic_range_and_attempts_left_regression():
    """Guess info text must use difficulty range and computed attempts_left."""
    source = Path("app.py").read_text(encoding="utf-8")
    tree = ast.parse(source, filename="app.py")

    has_attempts_left_assignment = False
    has_dynamic_range_text = False
    has_attempts_left_text = False

    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == "attempts_left":
                has_attempts_left_assignment = True

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if (
                isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == "st"
                and call.func.attr == "info"
                and call.args
            ):
                arg = call.args[0]
                if isinstance(arg, ast.JoinedStr):
                    formatted_names = {
                        value.value.id
                        for value in arg.values
                        if isinstance(value, ast.FormattedValue)
                        and isinstance(value.value, ast.Name)
                    }
                    has_dynamic_range_text = {"low", "high"}.issubset(formatted_names)
                    has_attempts_left_text = "attempts_left" in formatted_names

    assert has_attempts_left_assignment
    assert has_dynamic_range_text
    assert has_attempts_left_text
