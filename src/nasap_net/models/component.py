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

    def __repr__(self):
        # <Component kind='M', site_ids=[0, 1], aux_edges=[(0, 1, 'cis')]>
        site_ids_str = ', '.join(str(s) for s in sorted(self.site_ids))
        if not self.aux_edges:
            return (
                f'<Component kind={self.kind!r}, '
                f'site_ids=[{site_ids_str}]>'
            )

        # If there are auxiliary edges
        def aux_edge_to_str(aux_edge: AuxEdge) -> str:
            site_ids_str = (
                ', '.join(str(s) for s in sorted(aux_edge.site_ids))
            )
            if aux_edge.kind is None:
                return f'({site_ids_str})'
            return f'({site_ids_str}, {aux_edge.kind})'

        aux_edges_str = ', '.join(
            aux_edge_to_str(aux_edge) for aux_edge in sorted(self.aux_edges)
        )

        return (
            f'<Component kind={self.kind!r}, '
            f'site_ids=[{site_ids_str}], '
            f'aux_edges=[{aux_edges_str}]>'
        )

    def get_binding_sites(self, comp_id: ID) -> frozenset[BindingSite]:
        """Return the binding sites of this component."""
        return frozenset(
            BindingSite(component_id=comp_id, site_id=site_id)
            for site_id in self.site_ids
        )
