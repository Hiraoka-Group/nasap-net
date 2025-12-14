from nasap_net import Assembly, NasapNetError


class ComponentIDCollisionError(NasapNetError):
    pass


def union_assemblies(
        assembly1: Assembly,
        assembly2: Assembly,
        ) -> Assembly:
    """Create the union of two assemblies.

    The union consists of all components and bonds from both assemblies,
    without adding bonds between them.

    Parameters
    ----------
    assembly1 : Assembly
        The first assembly.
    assembly2 : Assembly
        The second assembly.

    Returns
    -------
    Assembly
        The union of the two assemblies.

    Raises
    ------
    ComponentIDCollisionError
        If there are component ID collisions between the two assemblies.
    """
    if set(assembly1.components) & set(assembly2.components):
        raise ComponentIDCollisionError(
            "Component ID collision detected between the two assemblies.")

    new_components = (
            dict(assembly1.components) | dict(assembly2.components))
    new_bonds = assembly1.bonds | assembly2.bonds
    return Assembly(components=new_components, bonds=new_bonds)
