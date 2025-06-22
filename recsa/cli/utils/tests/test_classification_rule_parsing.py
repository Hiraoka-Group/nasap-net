import pytest

from recsa import InterReaction, IntraReaction
from recsa.cli.utils import read_rule


@pytest.fixture
def rule_yaml():
    return [
    'IFS', [
        [
            'IF',
            {
                'CONDITION': [
                    'AND',
                    [
                        ['NAME', {'OF': 'init', 'IS': '(2,4,1)'}],
                        ['NAME', {'OF': 'product', 'IS': '(2,4,0)'}]
                    ]
                ],
                'THEN': ['RETURN', 6]
            }
        ],
        [
            'IF',
            {
                'CONDITION': [
                    'AND',
                    [
                        ['NAME', {'OF': 'init', 'IS': '(2,4,0)'}],
                        ['NAME', {'OF': 'product', 'IS': '(2,4,1)'}]
                    ]
                ],
                'THEN': ['RETURN', 7]
            }
        ],
        [
            'IF',
            {
                'CONDITION': [['REACTION_TYPE', {'IS': 'intra'}]],
                'THEN': ['RETURN', 4]
            }
        ],
        [
            'IF',
            {
                'CONDITION': ['REV', ['REACTION_TYPE', {'IS': 'intra'}]],
                'THEN': ['RETURN', 5]
            }
        ],
        [
            'IF',
            {
                'CONDITION': ['AND', ['LEAVING_KIND', 'X'], ['ENTERING_KIND', 'L']],
                'THEN': [
                    'IF',
                    {
                        'CONDITION': [
                            'AND',
                            [
                                ['COUNT', {'OF': 'M', 'IN': 'init', 'IS': '1'}],
                                ['COUNT', {'OF': 'M', 'IN': 'product', 'IS': '2'}]
                            ]
                        ],
                        'THEN': ['RETURN', 2],
                        'ELSE': ['RETURN', 0]
                    }
                ]
            }
        ],
        [
            'IF',
            {
                'CONDITION': ['AND', ['LEAVING_KIND', 'L'], ['ENTERING_KIND', 'X']],
                'THEN': [
                    'IF',
                    {
                        'CONDITION': [
                            'AND',
                            [
                                ['COUNT', {'OF': 'M', 'IN': 'init', 'IS': '2'}],
                                ['COUNT', {'OF': 'M', 'IN': 'product', 'IS': '1'}]
                            ]
                        ],
                        'THEN': ['RETURN', 3],
                        'ELSE': ['RETURN', 1]
                    }
                ]
            }
        ]
    ]]


def test_return():
    rule_yaml = ['RETURN', 10]
    rule = read_rule(rule_yaml)
    assert rule(IntraReaction(
        0, 1, 2, 'metal', 'leaving', 'entering', 1
    )) == 10
    assert rule(InterReaction(
        0, 1, 2, 3, 'metal', 'leaving', 'entering', 1
    )) == 10
    with pytest.raises(TypeError):
        rule('not a reaction')  # type: ignore


# def test_id_of():
#     rule_yaml = ['RETURN', ['ID', {'OF': 'init'}]]
#     rule = read_rule(rule_yaml)
#     assert rule(IntraReaction(
#         0, 1, 2, 'metal', 'leaving', 'entering', 1
#     )) == 0
#     assert rule(InterReaction(
#         0, 1, 2, 3, 'metal', 'leaving', 'entering', 1
#     )) == 0
#     assert rule(IntraReaction(
#         10, 1, 2, 'metal', 'leaving', 'entering', 1
#     )) == 10



# def test_if_block():
#     rule_yaml = [
#         'IF',
#         {
#             'CONDITION': ['NAME', {'OF': 'init', 'IS': '(2,4,1)'}],
#             'THEN': ['RETURN', 10],
#             'ELSE': ['RETURN', 20]
#         }
#     ]
#     rule = read_rule(rule_yaml)
#     assert rule(IntraReaction(
#         0, 1, 2, 'metal', 'leaving', 'entering', 1
#     )) == 20


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
