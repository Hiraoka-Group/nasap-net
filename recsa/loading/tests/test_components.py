import pytest
import yaml

from recsa import Component, load_component_structures


# Helper function
def write_safe_data_to_file(tmp_path, data):
    file = tmp_path / 'comp_kinds.yaml'
    with file.open('w') as f:
        yaml.safe_dump(data, f)
    return file


def test_typical_case(tmp_path):
    COMPONENTS = {
        'M': {'bindsites': ['a', 'b'],
              'aux_edges': [['a', 'b', 'cis']]},
        'X': {'bindsites': ['a'],}
    }
    data = {'comp_kinds': COMPONENTS}

    component_structures_file = write_safe_data_to_file(tmp_path, data)
    
    loaded = load_component_structures(component_structures_file)

    assert loaded == {
        'M': Component(bindsites=['a', 'b'], 
                       aux_edges=[('a', 'b', 'cis')]),
        'X': Component(bindsites=['a'], aux_edges=[])
    }


def test_component_without_bindsites(tmp_path):
    COMPONENTS: dict[str, dict] = {'M': {}}
    data = {'comp_kinds': COMPONENTS}

    component_structures_file = write_safe_data_to_file(tmp_path, data)
    
    loaded = load_component_structures(component_structures_file)

    assert loaded == {'M': Component(bindsites=[], aux_edges=[])}


def test_component_without_aux_edges(tmp_path):
    COMPONENTS: dict[str, dict] = {'M': {'bindsites': ['a']}}
    data = {'comp_kinds': COMPONENTS}

    component_structures_file = write_safe_data_to_file(tmp_path, data)
    
    loaded = load_component_structures(component_structures_file)

    assert loaded == {'M': Component(bindsites=['a'], aux_edges=[])}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
