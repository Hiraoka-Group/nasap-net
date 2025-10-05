from nasap_net.reaction_exploration_im import BindingSite
from nasap_net.reaction_exploration_im.lib.intra_reaction_performance import _T


def separate_if_possible(
        assembly: _T,
        metal_site: BindingSite
        ) -> tuple[_T, _T | None]:
    """Separate the assembly into product and leaving assemblies if possible."""
    raise NotImplementedError()
