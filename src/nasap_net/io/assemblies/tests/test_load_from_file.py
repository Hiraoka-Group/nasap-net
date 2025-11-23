import pytest

from nasap_net.io.assemblies import dump, load_assemblies
from nasap_net.models import Assembly, AuxEdge, Bond, Component


@pytest.fixture
def sample_assemblies():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    M_aux = Component(
        kind='M(aux)', sites=[0, 1, 2],
        aux_edges=[AuxEdge(0, 1), AuxEdge(0, 2, kind='cis')]
    )

    assemblies = [
        Assembly(components={'X0': X}, bonds=[]),
        Assembly(
            id_='MX2',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
        ),
        Assembly(
            components={'M0': M_aux, 'X0': X, 'X1': X, 'X2': X},
            bonds=[
                Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0), Bond('M0', 2, 'X2', 0)
            ]
        ),
    ]

    return assemblies


def test_reads_file_and_contents(tmp_path, sample_assemblies):
    assemblies = sample_assemblies
    f = tmp_path / "in.yaml"
    # write YAML using dump()
    f.write_text(dump(assemblies))

    loaded = load_assemblies(f, strict=True, verbose=False)

    assert isinstance(loaded, list)
    assert loaded == assemblies


def test_raises_if_missing_and_strict(tmp_path):
    missing = tmp_path / "noexist.yaml"
    with pytest.raises(FileNotFoundError):
        load_assemblies(missing, strict=True, verbose=False)


def test_returns_empty_if_missing_and_not_strict(tmp_path):
    missing = tmp_path / "noexist.yaml"
    res = load_assemblies(missing, strict=False, verbose=False)
    assert res == []


def test_verbose_prints_loaded_message(tmp_path, capsys, sample_assemblies):
    assemblies = sample_assemblies
    f = tmp_path / "v_in.yaml"
    f.write_text(dump(assemblies))

    load_assemblies(f, strict=True, verbose=True)

    captured = capsys.readouterr()
    assert 'Loaded' in captured.out
    assert str(f) in captured.out
