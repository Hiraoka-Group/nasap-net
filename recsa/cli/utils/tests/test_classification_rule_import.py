import pytest

from recsa import IntraReaction
from recsa.cli.utils import import_classify_func


def test_import(tmp_path):
    rule_file = tmp_path / "classification_rule.py"
    rule_file.write_text(
        # Simple classification function that returns a fixed string
        """
def classify(reaction):
    return "test_classification"
"""
    )

    classify_func = import_classify_func(rule_file)

    reaction = IntraReaction(0, 1, 2, 'm', 'l', 'e', 1)
    result = classify_func(reaction)
    
    assert result == "test_classification"


def test_classification_by_init_assem(tmp_path):
    rule_file = tmp_path / "classification_rule.py"
    rule_file.write_text(
        # Classification function that classifies based on the ID of 
        # the initial assembly
        """
def classify(reaction):
    return reaction.init_assem_id
"""
    )

    classify_func = import_classify_func(rule_file)
    reaction = IntraReaction(0, 1, 2, 'm', 'l', 'e', 1)

    assert classify_func(reaction) == 0


if __name__ == "__main__":
    pytest.main(['-v', __file__])
