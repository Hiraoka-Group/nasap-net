from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import yaml

from nasap_net.light_assembly import convert_assemblies_to_light_ones
from nasap_net.models import Assembly
from nasap_net.types import ID
from .lib import ComponentDumper, LightAssemblyDumper

DEFAULT_KWARGS_FOR_COMPONENTS = {
    'Dumper': ComponentDumper,
    'sort_keys': True,
    'default_flow_style': None,
}

DEFAULT_KWARGS_FOR_ASSEMBLIES = {
    'Dumper': LightAssemblyDumper,
    'sort_keys': False,
    'default_flow_style': None,
}


def dump_into_documents(
        assemblies: Mapping[ID, Assembly],
        *,
        kwargs_for_components: Mapping[str, Any] | None = None,
        kwargs_for_assemblies: Mapping[str, Any] | None = None,
        ) -> str:
    dumped = dump_assemblies_and_components_separately(
        assemblies,
        kwargs_for_components=kwargs_for_components,
        kwargs_for_assemblies=kwargs_for_assemblies,
    )
    return '---\n'.join([dumped.components, dumped.assemblies])


@dataclass(frozen=True)
class Dumped:
    assemblies: str
    components: str


def dump_assemblies_and_components_separately(
        assemblies: Mapping[ID, Assembly],
        *,
        kwargs_for_components: Mapping[str, Any] | None = None,
        kwargs_for_assemblies: Mapping[str, Any] | None = None,
        ) -> Dumped:
    yaml_kwargs_components = _resolve_kwargs(
        DEFAULT_KWARGS_FOR_COMPONENTS, kwargs_for_components)
    yaml_kwargs_assemblies = _resolve_kwargs(
        DEFAULT_KWARGS_FOR_ASSEMBLIES, kwargs_for_assemblies)

    res = convert_assemblies_to_light_ones(assemblies)

    return Dumped(
        assemblies=yaml.dump(
            dict(sorted(res.light_assemblies.items())),
            **yaml_kwargs_assemblies,
        ),
        components=yaml.dump(
            dict(sorted(res.components.items())),
            **yaml_kwargs_components,
        ),
    )


def _resolve_kwargs(
        default_kwargs: Mapping[str, Any],
        custom_kwargs: Mapping[str, Any] | None
        ) -> Mapping[str, Any]:
    if custom_kwargs is None:
        return default_kwargs
    resolved_kwargs = dict(default_kwargs)
    resolved_kwargs.update(custom_kwargs)
    return resolved_kwargs
