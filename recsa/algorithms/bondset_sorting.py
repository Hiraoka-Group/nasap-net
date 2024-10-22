__all__ = ['sort_bondsets']


def sort_bondsets(
        bond_subsets: set[frozenset[str]]) -> list[set[str]]:
    """Sort assemblies by the number of bonds and the bond IDs.

    The number of bonds is the primary key, and the sorted tuple of
    bond IDs is the secondary key.

    Duplicate bond IDs may cause unexpected behavior.

    # TODO: Add an example.
    """
    return sorted(
        bond_subsets,  # type: ignore
        # mypy states that the `sorted` function expects
        # `Iterable[set[str]]`, but the reason is unclear.

        key=lambda subset: (len(subset), sorted(subset))
        )
