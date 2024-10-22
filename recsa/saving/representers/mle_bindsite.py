import yaml

from recsa import MleBindsite

__all__ = ['mle_bindsite_representer', 'add_mle_bindsite_representer']


def mle_bindsite_representer(dumper, data: MleBindsite):
    d = {
        'metal': data.metal,
        'leaving': data.leaving,
        'entering': data.entering,
    }
    return dumper.represent_dict(d)


def add_mle_bindsite_representer():
    yaml.add_representer(MleBindsite, mle_bindsite_representer)
