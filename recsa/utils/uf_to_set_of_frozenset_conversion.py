from networkx.utils import UnionFind


def uf_to_set_of_frozenset(uf: UnionFind) -> set[frozenset]:
    """Convert a UnionFind object to a set of frozensets."""
    return {frozenset(group) for group in uf.to_sets()}
