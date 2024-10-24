import networkx as nx
import pytest

from recsa import Assembly, Component, LocalAuxEdge, draw_3d


@pytest.mark.skip(reason='This is a visual test.')
def test_draw_3d():
    MLX3 = Assembly(
        {'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'L1.a')],
    )
    COMPONENT_STRUCTURES = {
        'M': Component(
            'M', {'a', 'b', 'c', 'd'}, {
                LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('b', 'c', 'cis'),
                LocalAuxEdge('c', 'd', 'cis'), LocalAuxEdge('d', 'a', 'cis')}),
        'L': Component('L', {'a', 'b'}),
        'X': Component('X', {'a'}),
    }

    positions = nx.spring_layout(
        MLX3.g_snapshot(COMPONENT_STRUCTURES), dim=3)
    draw_3d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode='component_kind')
    draw_3d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode='component_id')
    draw_3d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode='core_and_bindsite_ids')
    draw_3d(MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode=None)
    draw_3d(
        MLX3, COMPONENT_STRUCTURES, positions, node_labeling_mode=None,
        label_aux_edges=False)


if __name__ == '__main__':
    test_draw_3d()
