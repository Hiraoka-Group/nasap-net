from nasap_net.models import Assembly
from .exceptions import NoIsomorphismFoundError
from .lib import color_vertices_and_edges, convert_assembly_to_igraph


def is_isomorphic(assem1: Assembly, assem2: Assembly) -> bool:
    g1 = convert_assembly_to_igraph(assem1).graph
    g2 = convert_assembly_to_igraph(assem2).graph

    try:
        colors = color_vertices_and_edges(g1, g2)
    except NoIsomorphismFoundError:
        return False

    return g1.isomorphic_vf2(
        g2,
        color1=colors.v_color1,
        color2=colors.v_color2,
        edge_color1=colors.e_color1,
        edge_color2=colors.e_color2,
    )
