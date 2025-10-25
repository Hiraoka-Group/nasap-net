from collections.abc import Iterable
from dataclasses import dataclass

from nasap_net.types import ID
from .aux_edge import AuxEdge
from .binding_site import BindingSite


@dataclass(frozen=True, init=False)
class Component:
    """Component"""
    kind: str
    site_ids: frozenset[ID]
    aux_edges: frozenset[AuxEdge]

    def __init__(
            self, kind: str, sites: Iterable[ID],
            aux_edges: Iterable[AuxEdge] | None = None
            ):
        object.__setattr__(self, 'kind', kind)
        object.__setattr__(self, 'site_ids', frozenset(sites))
        if aux_edges is None:
            aux_edges = frozenset()
        else:
            aux_edges = frozenset(aux_edges)
        object.__setattr__(self, 'aux_edges', aux_edges)

    def get_binding_sites(self, comp_id: ID) -> frozenset[BindingSite]:
        """Return the binding sites of this component."""
        return frozenset(
            BindingSite(component_id=comp_id, site_id=site_id)
            for site_id in self.site_ids
        )
