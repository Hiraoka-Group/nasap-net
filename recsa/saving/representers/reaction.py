import yaml

from recsa.classes.reaction import InterReaction, IntraReaction


def intra_reaction_representer(dumper, data: IntraReaction):
    d = {
        'init_assem_id': data.init_assem_id,
        'product_assem_id': data.product_assem_id,
        'leaving_assem_id': data.leaving_assem_id,
        'metal_bs': data.metal_bs,
        'leaving_bs': data.leaving_bs,
        'entering_bs': data.entering_bs,
        'metal_kind': data.metal_kind,
        'leaving_kind': data.leaving_kind,
        'entering_kind': data.entering_kind,
        'duplicate_count': data.duplicate_count
    }
    return dumper.represent_dict(d)


def inter_reaction_representer(dumper, data: InterReaction):
    d = {
        'init_assem_id': data.init_assem_id,
        'entering_assem_id': data.entering_assem_id,
        'product_assem_id': data.product_assem_id,
        'leaving_assem_id': data.leaving_assem_id,
        'metal_bs': data.metal_bs,
        'leaving_bs': data.leaving_bs,
        'entering_bs': data.entering_bs,
        'metal_kind': data.metal_kind,
        'leaving_kind': data.leaving_kind,
        'entering_kind': data.entering_kind,
        'duplicate_count': data.duplicate_count
    }
    return dumper.represent_dict(d)


def add_reaction_representer():
    yaml.add_representer(InterReaction, inter_reaction_representer)
    yaml.add_representer(IntraReaction, intra_reaction_representer)
