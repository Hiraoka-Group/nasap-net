import yaml

from recsa import MleKind

__all__ = ['mle_kind_representer', 'add_mle_kind_representer']


def mle_kind_representer(dumper, data: MleKind):
    d = {
        'metal': data.metal,
        'leaving': data.leaving,
        'entering': data.entering,
    }
    return dumper.represent_dict(d)


def add_mle_kind_representer():
    yaml.add_representer(MleKind, mle_kind_representer)
