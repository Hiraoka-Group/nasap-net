import pytest
import yaml

from recsa import Assembly, Component, cap_bindsites_pipeline, is_isomorphic


def test_basic(tmp_path):
    ASSEMBLIES_PATH = tmp_path / 'assemblies.yaml'
    COMP_STRUCTURE_PATH = tmp_path / 'comp_structure.yaml'
    CAP_PARAMS_PATH = tmp_path / 'cap_params.yaml'
    OUTPUT_PATH = tmp_path / 'output.yaml'

    ASSEMBLIES = [{'assembly': Assembly({'M1': 'M'})}, 
                  {'assembly': Assembly({'L1': 'L'})}]
    with ASSEMBLIES_PATH.open('w') as f:
        yaml.dump_all(ASSEMBLIES, f)

    COMPONENTS = {'M': Component(['a', 'b']), 'L': Component(['a', 'b'])}
    with COMP_STRUCTURE_PATH.open('w') as f:
        yaml.dump(COMPONENTS, f)

    CAP_PARAMS = {
        'component_kind_to_be_capped': 'M',
        'cap_component_kind': 'X',
        'cap_bindsite': 'a'
        }
    with CAP_PARAMS_PATH.open('w') as f:
        yaml.safe_dump(CAP_PARAMS, f)

    cap_bindsites_pipeline(
        ASSEMBLIES_PATH, COMP_STRUCTURE_PATH, CAP_PARAMS_PATH,
        OUTPUT_PATH)
    
    assemblies = list(yaml.safe_load_all(OUTPUT_PATH.open()))

    assert len(assemblies) == 2
    assert is_isomorphic(
        assemblies[0]['assembly'], 
        Assembly({'M1': 'M', 'X1': 'X', 'X2': 'X'}, 
                 [('M1.a', 'X1.a'), ('M1.b', 'X2.a')]),
        COMPONENTS)
    assert assemblies[1] == {
        'index': 1,
        'assembly': Assembly({'L1': 'L'})
        }


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
