from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

from recsa.bondset_enumeration import normalize_bondset_under_sym_ops


def compare_bondsets_under_sym_ops(
        bondsets1: Iterable[Iterable[str]],
        bondsets2: Iterable[Iterable[str]],
        sym_ops: Mapping[str, Mapping[str, str]] | None = None
        ) -> tuple[set[frozenset[str]], set[frozenset[str]]]:
    """Compare bondsets under symmetry operations.

    The bondsets are compared by normalizing them under symmetry operations.
    The normalized bondsets are the smallest bondsets among symmetry-equivalent bondsets.

    Parameters
    ----------
    bondsets1 : Iterable[Iterable[str]]
        First set of bondsets.
    bondsets2 : Iterable[Iterable[str]]
        Second set of bondsets.
    sym_ops : Mapping[str, Mapping[str, str]], optional
        Symmetry operations, by default None.

    Returns
    -------
    tuple[set[frozenset[str]], set[frozenset[str]]]
        Unique bondsets in the first and second sets, respectively.
    """
    _validate_bondsets(bondsets1)
    _validate_bondsets(bondsets2)

    normalized_to_orig_1 = _calc_normalized_to_orig_bondsets(
        bondsets1, sym_ops)
    normalized_to_orig_2 = _calc_normalized_to_orig_bondsets(
        bondsets2, sym_ops)
    
    unique_1 = set()
    unique_2 = set()

    for normalized, orig in normalized_to_orig_1.items():
        if normalized not in normalized_to_orig_2:
            unique_1.add(orig)
    for normalized, orig in normalized_to_orig_2.items():
        if normalized not in normalized_to_orig_1:
            unique_2.add(orig)
    
    return unique_1, unique_2


def _validate_bondsets(
        bondsets: Iterable[Iterable[str]]
        ) -> None:
    """Validate bondsets.

    Check if bondsets contain duplicate bonds or duplicates among them.

    Parameters
    ----------
    bondsets : Iterable[Iterable[str]]
        Bondsets to validate.
        
    Raises
    ------
    RecsaValueError
        If bondsets contain duplicate bonds or duplicates among them.
    """
    for bondset in bondsets:
        duplicate_bonds = _find_duplicates(bondset)
        if duplicate_bonds:
            raise ValueError(
                f'Bondset contains duplicate bonds: '
                f'bondset={sorted(bondset)}, '
                f'duplicate_bonds={sorted(duplicate_bonds)}')
    bondsets = [frozenset(bondset) for bondset in bondsets]
    duplicate_bondsets = _find_duplicates(bondsets)
    if duplicate_bondsets:
        raise ValueError(
            f'Duplicate bondset found: '
            f'{sorted(sorted(bondset) for bondset in duplicate_bondsets)}')


T = TypeVar('T')

def _find_duplicates(items: Iterable[T]) -> list[T]:
    duplicates: set[T] | list[T]
    seen: set[T] | list[T]

    if isinstance(next(iter(items)), Hashable):
        duplicates = set()
        seen = set()
        add_dup = duplicates.add
        add_seen = seen.add
    else:
        duplicates = []
        seen = []
        add_dup = duplicates.append
        add_seen = seen.append

    for item in items:
        if item in seen:
            add_dup(item)
        add_seen(item)

    return list(duplicates)


def _calc_normalized_to_orig_bondsets(
        bondsets: Iterable[Iterable[str]],
        sym_ops: Mapping[str, Mapping[str, str]] | None = None
        ) -> dict[frozenset[str], frozenset[str]]:
    """Calculate normalized bondsets under symmetry operations.
    
    The normalized bondsets are the smallest bondsets among symmetry-equivalent bondsets.
    
    Parameters
    ----------
    bondsets : Iterable[Iterable[str]]
        Bondsets to normalize.
    sym_ops : Mapping[str, Mapping[str, str]], optional
        Symmetry operations, by default None.

    Returns
    -------
    dict[frozenset[str], frozenset[str]]
        Mapping from normalized bondsets to original bondsets.
    """
    d = dict[frozenset[str], frozenset[str]]()
    if sym_ops is None:
        return {
            frozenset(bondset): frozenset(bondset) 
            for bondset in bondsets}
    for bondset in bondsets:
        bondset = set(bondset)
        normalized = frozenset(
            normalize_bondset_under_sym_ops(bondset, sym_ops))
        if normalized in d:
            raise ValueError(
                f'Duplicate bondset found: '
                f'{sorted(bondset)} and {sorted(d[normalized])}'
                )
        d[normalized] = frozenset(bondset)
    return d
