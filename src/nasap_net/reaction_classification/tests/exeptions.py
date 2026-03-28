from nasap_net import Reaction
from nasap_net.reaction_classification import IncompleteClassificationRuleError


class StubReaction:
    def __str__(self):
        return "A + B -> C (x2)"


def test_attributes_are_stored():
    r: Reaction = StubReaction()  # type: ignore
    e = IncompleteClassificationRuleError(r, error_id="case_1")

    assert e.reaction is r
    assert e.error_id == "case_1"


def test_str_includes_error_id_and_reaction():
    r: Reaction = StubReaction()  # type: ignore
    e = IncompleteClassificationRuleError(r, error_id="case_1")

    s = str(e)

    assert "Incomplete reaction classification rule" in s
    assert "error_id=case_1" in s
    assert "reaction:" in s
    assert "A + B -> C (x2)" in s


def test_str_without_error_id():
    r: Reaction = StubReaction()  # type: ignore
    e = IncompleteClassificationRuleError(r)

    s = str(e)

    assert "Incomplete reaction classification rule" in s
    assert "error_id=" not in s
    assert "reaction:" in s
