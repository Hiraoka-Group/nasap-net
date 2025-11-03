from nasap_net.exceptions import DuplicateIDError, IDNotSetError
from nasap_net.types import ID


def validate_unique_assembly_ids(assemblies):
    """Validate that all assemblies have unique IDs.

    Parameters
    ----------
    assemblies : Iterable[Assembly]
        The assemblies to validate.

    Raises
    ------
    IDNotSetError
        If any assembly does not have an ID set.
    DuplicateIDError
        If any duplicate assembly IDs are found.
    """
    assembly_ids: set[ID] = set()
    # All assemblies must have IDs and unique IDs
    for assem in assemblies:
        if assem.id_or_none is None:
            raise IDNotSetError(
                'All assemblies must have IDs for reaction exploration.'
            )
        if assem.id_ in assembly_ids:
            raise DuplicateIDError(
                f'Duplicate assembly ID found: {assem.id_}'
            )
        assembly_ids.add(assem.id_)
