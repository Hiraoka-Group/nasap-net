from nasap_net.models import Assembly
from .exceptions import NoIsomorphismFoundError
from .lib import color_vertices_and_edges, convert_assembly_to_igraph, \
    decode_mapping
from .models import Isomorphism


def get_isomorphism(assem1: Assembly, assem2: Assembly) -> Isomorphism:
    conv_res1 = convert_assembly_to_igraph(assem1)
    conv_res2 = convert_assembly_to_igraph(assem2)

    g1 = conv_res1.graph
    g2 = conv_res2.graph

    try:
        colors = color_vertices_and_edges(g1, g2)
    except NoIsomorphismFoundError:
        raise NoIsomorphismFoundError() from None

    mapping: list[int]
    _, mapping, _ = g1.isomorphic_vf2(
        g2,
        color1=colors.v_color1,
        color2=colors.v_color2,
        edge_color1=colors.e_color1,
        edge_color2=colors.e_color2,
        return_mapping_12=True,
    )

    return decode_mapping(mapping, conv_res1, conv_res2)


def get_all_isomorphisms(
        assem1: Assembly, assem2: Assembly) -> set[Isomorphism]:
    conv_res1 = convert_assembly_to_igraph(assem1)
    conv_res2 = convert_assembly_to_igraph(assem2)

    try:
        colors = color_vertices_and_edges(conv_res1.graph, conv_res2.graph)
    except NoIsomorphismFoundError:
        raise NoIsomorphismFoundError() from None

    res: list[list[int]] = conv_res1.graph.get_isomorphisms_vf2(
        conv_res2.graph,
        color1=colors.v_color1,
        color2=colors.v_color2,
        edge_color1=colors.e_color1,
        edge_color2=colors.e_color2,
    )

    return {decode_mapping(mapping, conv_res1, conv_res2) for mapping in res}
