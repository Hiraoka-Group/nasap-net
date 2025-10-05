from dataclasses import dataclass
from functools import cache
from typing import Literal

import networkx as nx

from nasap_net.types import ID
from .. import BindingSite
from ..models import Assembly


@dataclass(frozen=True)
class Core:
    component_id: ID


def _isom_key(
        core_or_site: Literal['core', 'site'],
        component_kind: str
        ) -> str:
    return f"{core_or_site}-{component_kind}"


@cache
def convert_assembly_to_graph(assembly: Assembly):
    g = nx.Graph()
    for comp_id, comp in assembly.components.items():
        # Add the core node
        g.add_node(
            Core(comp_id), isom_key=_isom_key('core', comp.kind))
        # Add the binding sites
        for site_id in comp.site_ids:
            g.add_node(
                BindingSite(comp_id, site_id),
                isom_key=_isom_key('site', comp.kind))
            g.add_edge(Core(comp_id), BindingSite(comp_id, site_id))
        # Add the auxiliary edges
        for aux in comp.aux_edges:
            if aux.kind is None:
                g.add_edge(
                    BindingSite(comp_id, aux.site1),
                    BindingSite(comp_id, aux.site2))
            else:
                g.add_edge(
                    BindingSite(comp_id, aux.site1),
                    BindingSite(comp_id, aux.site2),
                    aux_kind=aux.kind)
    # Add the bonds
    for bond in assembly.bonds:
        g.add_edge(*bond.sites)
