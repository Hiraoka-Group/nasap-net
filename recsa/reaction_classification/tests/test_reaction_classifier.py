import pytest

from recsa import Assembly, InterReactionEmbedded, ReactionClassifier


def test():
    def classification_rule(reaction):
        if (reaction.leaving_kind == 'X'
                and reaction.entering_kind == 'L'):
            return 'X-L exchange'
        else:
            return 'other'
    
    classifier = ReactionClassifier(classification_rule)
    reaction1 = InterReactionEmbedded(
        init_assem=Assembly(), entering_assem=Assembly(),
        product_assem=Assembly(), leaving_assem=Assembly(),
        metal_bs='', leaving_bs='', entering_bs='',
        metal_kind='', leaving_kind='X', entering_kind='L',
        duplicate_count=1
        )
    reaction2 = InterReactionEmbedded(
        init_assem=Assembly(), entering_assem=Assembly(),
        product_assem=Assembly(), leaving_assem=Assembly(),
        metal_bs='', leaving_bs='', entering_bs='',
        metal_kind='', leaving_kind='X', entering_kind='X',
        duplicate_count=1
        )
    assert classifier.classify(reaction1) == 'X-L exchange'
    assert classifier.classify(reaction2) == 'other'


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
