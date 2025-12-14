from nasap_net import Assembly, NasapNetError


class ComponentIDCollisionError(NasapNetError):
    pass


def union_assemblies(
        init_assem: Assembly, entering_assem: Assembly,
        ) -> Assembly:
    """Create the union of two assemblies.

    The union consists of all components and bonds from both assemblies,
    without adding bonds between them.

    Parameters
    ----------
    init_assem : Assembly
        The initial assembly.
    entering_assem : Assembly
        The entering assembly.

    Returns
    -------
    Assembly
        The union of the two assemblies.

    Raises
    ------
    ComponentIDCollisionError
        If there are component ID collisions between the two assemblies.
    """
    if set(init_assem.components) & set(entering_assem.components):
        raise ComponentIDCollisionError(
            "Component ID collision detected between the two assemblies.")

    new_components = (
            dict(init_assem.components) | dict(entering_assem.components))
    new_bonds = init_assem.bonds | entering_assem.bonds
    return Assembly(components=new_components, bonds=new_bonds)
