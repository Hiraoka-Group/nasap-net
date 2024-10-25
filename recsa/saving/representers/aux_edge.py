import yaml

from recsa import AuxEdge


def aux_edge_representer(dumper, data: AuxEdge):
    aux_edge_dict = {
        'bindsite1': data.local_bindsite1,
        'bindsite2': data.local_bindsite2,
        'kind': data.aux_kind
    }
    return dumper.represent_dict(aux_edge_dict)


def add_aux_edge_representer():
    yaml.add_representer(AuxEdge, aux_edge_representer)
