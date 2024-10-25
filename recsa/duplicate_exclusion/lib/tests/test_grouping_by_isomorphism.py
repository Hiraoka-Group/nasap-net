import pytest

from recsa import Assembly, Component
from recsa.duplicate_exclusion import group_assemblies_by_isomorphism


def test_group_assemblies_by_isomorphism():
    component_structures = {
        'M': Component({'a', 'b'}),
        'L': Component({'a', 'b'}),
        'X': Component({'a'}),
    }

    id_to_graph = {
        'MLX-1': Assembly(
            component_structures,
            {'M1': 'M', 'L1': 'L', 'X1': 'X'}, 
            [('M1.a', 'L1.a'), ('M1.b', 'X1.a')]),
        'MLX-2': Assembly(
            component_structures,
            {'M2': 'M', 'L2': 'L', 'X2': 'X'}, 
            [('M2.a', 'L2.a'), ('M2.b', 'X2.a')]),
        'MLX-3': Assembly(
            component_structures,
            {'M3': 'M', 'L3': 'L', 'X3': 'X'}, 
            [('M3.a', 'L3.a'), ('M3.b', 'X3.a')]),
        'MX2': Assembly(
            component_structures,
            {'M1': 'M', 'X1': 'X', 'X2': 'X'}, 
            [('M1.a', 'X1.a'), ('M1.b', 'X2.a')]),
        'L': Assembly(
            component_structures,
            {'L1': 'L'}, 
            []),
    }

    grouped_ids = group_assemblies_by_isomorphism(id_to_graph, component_structures)

    assert grouped_ids == {
        'MLX-1': {'MLX-1', 'MLX-2', 'MLX-3'},
        'MX2': {'MX2'},
        'L': {'L'}
    }


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
