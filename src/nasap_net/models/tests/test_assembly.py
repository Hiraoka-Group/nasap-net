from nasap_net.models import Assembly, Bond, Component


def test_assembly():
    L = Component(kind="L", sites={"a", "b"})
    M = Component(kind="M", sites={"a", "b"})
    assembly = Assembly(
        components={"L1": L, "M1": M},
        bonds={Bond(comp_id1="L1", site1="a", comp_id2="M1", site2="a")}
        )
    assert assembly.components == {"L1": L, "M1": M}
    assert assembly.bonds == frozenset({
        Bond(comp_id1="L1", site1="a", comp_id2="M1", site2="a")})
