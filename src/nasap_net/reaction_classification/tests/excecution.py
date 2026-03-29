import logging

import pytest

from nasap_net import Reaction
from nasap_net.reaction_classification import classify_reactions


class StubReaction:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"R({self.name})"


def test_classify_reactions_basic():
    reactions: list[Reaction] = [  # type: ignore
        StubReaction("A"), StubReaction("B")  # type: ignore
    ]

    def classifier(r):
        return f"class_{r.name}"

    result = classify_reactions(reactions, classifier)

    assert len(result) == 2
    assert result[reactions[0]] == "class_A"
    assert result[reactions[1]] == "class_B"


def test_classifier_is_called_for_each_reaction():
    reactions: list[Reaction] = [  # type: ignore
        StubReaction("A"), StubReaction("B"), StubReaction("C")  # type: ignore
    ]
    called = []

    def classifier(r):
        called.append(r)
        return "x"

    classify_reactions(reactions, classifier)

    assert called == reactions


def test_exception_propagates():
    reactions: list[Reaction] = [  # type: ignore
        StubReaction("A"), StubReaction("B")  # type: ignore
    ]

    def classifier(r):
        if r.name == "B":
            raise ValueError("boom")
        return "ok"

    with pytest.raises(ValueError):
        classify_reactions(reactions, classifier)


def test_logging_output(caplog):
    reactions: list[Reaction] = [StubReaction("A")]  # type: ignore

    def classifier(r):
        return "class_A"

    caplog.set_level(logging.INFO)

    classify_reactions(reactions, classifier)

    # reaction と classification の両方がログに出ていることを確認
    logs = [record.getMessage() for record in caplog.records]

    assert any("R(A)" in msg for msg in logs)
    assert any("class_A" in msg for msg in logs)
