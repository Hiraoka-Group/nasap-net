from nasap_net.types import ID
from ..assembly import Assembly


def assembly_to_id_or_none_or_unknown(assembly: Assembly | None) -> ID | None:
    """Return the ID of the assembly, or '??' if not set, or None if assembly
    is None.
    """
    if assembly is None:
        return None
    if assembly.id_or_none is None:
        # ID not set
        return '??'
    return assembly.id_or_none
