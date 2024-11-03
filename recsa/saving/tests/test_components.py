import pytest
import yaml

from recsa import Component, save_components


def test_basic(tmp_path):
    COMPONENTS = {'M': Component(['a', 'b'])}
    OUTPUT_PATH = tmp_path / 'output.yaml'

    save_components(COMPONENTS, OUTPUT_PATH)

    with open(OUTPUT_PATH) as f:
        data = yaml.safe_load(f)

    assert data == COMPONENTS
    assert OUTPUT_PATH.exists()


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
