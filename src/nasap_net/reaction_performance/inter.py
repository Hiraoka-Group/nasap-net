from nasap_net.models import Assembly, MLE
from .separation import separate_if_possible
from nasap_net.helpers.assembly_union import ComponentIDCollisionError, \
    union_assemblies


def perform_inter_reaction(
        init_assem: Assembly,
        entering_assem: Assembly,
        mle: MLE
) -> tuple[Assembly, Assembly | None]:
    """Perform an inter-molecular reaction between two assemblies based on the given MLE.

    The following process is performed:
      1. Remove the bond between the metal and leaving binding sites.
      2. Add a bond between the metal and entering binding sites.

    Parameters
    ----------
    init_assem : Assembly
        The initial assembly containing the metal and leaving binding sites.
    entering_assem : Assembly
        The entering assembly containing the entering binding site.
    mle : MLE
        The MLE (metal, leaving, entering binding sites) defining the reaction.

    Returns
    -------
    product : Assembly
        The resulting assembly after the reaction.
    leaving : Assembly | None
        The leaving assembly if it can be separated; otherwise, None.

    Raises
    ------
    ComponentIDCollisionError
        If there are component ID collisions between the two assemblies.
    """
    if set(init_assem.components) & set(entering_assem.components):
        raise ComponentIDCollisionError(
            "Component ID collision detected between the two assemblies.")

    raw_product = (
        union_assemblies(init_assem, entering_assem)
            .remove_bond(mle.metal, mle.leaving)
            .add_bond(mle.metal, mle.entering)
    )
    product, leaving = separate_if_possible(
        raw_product,
        metal_comp_id=mle.metal.component_id
    )
    return product, leaving
