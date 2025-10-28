from .conversion import GraphConversionResult
from ..models import Isomorphism


def decode_mapping(
        mapping: list[int],
        conv_res1: GraphConversionResult,
        conv_res2: GraphConversionResult,
) -> Isomorphism:
    comp_id_mapping = {}
    binding_site_mapping = {}
    for v1, v2 in enumerate(mapping):
        if v1 in conv_res1.core_mapping.inv:
            comp_id1 = conv_res1.core_mapping.inv[v1]
            comp_id2 = conv_res2.core_mapping.inv[v2]
            comp_id_mapping[comp_id1] = comp_id2
        else:
            assert v1 in conv_res1.binding_site_mapping.inv
            site1 = conv_res1.binding_site_mapping.inv[v1]
            site2 = conv_res2.binding_site_mapping.inv[v2]
            binding_site_mapping[site1] = site2
    return Isomorphism(
        comp_id_mapping=comp_id_mapping,
        binding_site_mapping=binding_site_mapping
    )
