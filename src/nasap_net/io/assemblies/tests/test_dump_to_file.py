import pytest

from nasap_net.io.assemblies import dump, export_assemblies_to_file
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


def test_writes_file_and_contents(tmp_path, sample_assemblies):
    assemblies = sample_assemblies
    out = tmp_path / "out.yaml"

    # write
    export_assemblies_to_file(assemblies, out, overwrite=False, verbose=False)

    # file exists and contents match dump()
    assert out.exists()
    text = out.read_text()
    assert text == dump(assemblies)


def test_raises_if_exists_and_no_overwrite(tmp_path, sample_assemblies):
    assemblies = sample_assemblies
    out = tmp_path / "already.yaml"
    out.write_text("old")

    try:
        export_assemblies_to_file(assemblies, out, overwrite=False, verbose=False)
        raised = False
    except FileExistsError:
        raised = True

    assert raised is True
    # original content unchanged
    assert out.read_text() == "old"


def test_overwrite_ok(tmp_path, sample_assemblies):
    assemblies = sample_assemblies
    out = tmp_path / "to_overwrite.yaml"
    out.write_text("old content")

    export_assemblies_to_file(assemblies, out, overwrite=True, verbose=False)

    assert out.read_text() == dump(assemblies)


def test_creates_parent_dirs(tmp_path, sample_assemblies):
    assemblies = sample_assemblies
    out = tmp_path / "nested" / "a" / "dump.yaml"

    export_assemblies_to_file(assemblies, out, overwrite=False, verbose=False)

    assert out.exists()
    assert (tmp_path / "nested" / "a").exists()


def test_verbose_prints_saved_message(tmp_path, capsys, sample_assemblies):
    assemblies = sample_assemblies
    out = tmp_path / "v.yaml"

    export_assemblies_to_file(assemblies, out, overwrite=False, verbose=True)

    captured = capsys.readouterr()
    # message should include path
    assert 'Saved! -->' in captured.out
    assert str(out) in captured.out
