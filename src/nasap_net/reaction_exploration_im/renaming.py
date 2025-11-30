from dataclasses import dataclass
from typing import Callable

from nasap_net.models import Assembly, BindingSite, Bond, MLE
from nasap_net.types import ID


@dataclass(frozen=True)
class Renamed:
    init_assembly: Assembly
    entering_assembly: Assembly
    mle: MLE


def rename_for_inter_reaction(
        init_assembly: Assembly,
        entering_assembly: Assembly,
        mle: MLE,
        *,
        init_prefix: str = 'init_',
        entering_prefix: str = 'entering_'
) -> Renamed:
    def init_renaming_func(comp_id: ID) -> ID:
        return f'{init_prefix}{comp_id}'

    def entering_renaming_func(comp_id: ID) -> ID:
        return f'{entering_prefix}{comp_id}'

    renamed_init_assem = _rename_component_ids_in_assembly(
        init_assembly, init_renaming_func)
    renamed_entering_assem = _rename_component_ids_in_assembly(
        entering_assembly, entering_renaming_func)
    renamed_mle = MLE(
        metal=BindingSite(
            component_id=init_renaming_func(mle.metal.component_id),
            site_id=mle.metal.site_id),
        leaving=BindingSite(
            component_id=init_renaming_func(mle.leaving.component_id),
            site_id=mle.leaving.site_id),
        entering=BindingSite(
            component_id=entering_renaming_func(mle.entering.component_id),
            site_id=mle.entering.site_id),
        duplication=mle.duplication_or_none
    )
    return Renamed(
        init_assembly=renamed_init_assem,
        entering_assembly=renamed_entering_assem,
        mle=renamed_mle
    )


def _rename_component_ids_in_assembly(
        assembly: Assembly, renaming_func: Callable[[ID], ID]
) -> Assembly:
    """Rename component IDs in an assembly using the provided renaming function.

    Parameters
    ----------
    assembly : Assembly
        The assembly whose component IDs are to be renamed.
    renaming_func : Callable[[ID], ID]
        A function that takes a component ID and returns the renamed component ID.

    Returns
    -------
    Assembly
        A new assembly with renamed component IDs.

    Notes
    -----
    Assembly ID is preserved.
    """
    renamed_components = {
        renaming_func(id_): comp
        for id_, comp in assembly.components.items()}
    renamed_bonds = {
        Bond(
            comp_id1=renaming_func(site1.component_id), site1=site1.site_id,
            comp_id2=renaming_func(site2.component_id), site2=site2.site_id
        )
        for (site1, site2) in assembly.bonds}
    return assembly.copy_with(
        components=renamed_components,
        bonds=renamed_bonds,
        id_=assembly.id_or_none
    )
