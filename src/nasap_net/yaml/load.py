from nasap_net.models import Assembly, Component, LightAssembly
from nasap_net.models.conversion import convert_light_assemblies_to_rich_ones
from nasap_net.types import ID
from nasap_net.yaml.helper import split_yaml_documents
from nasap_net.yaml.lib import load_components, load_light_assemblies


def load(yaml_str: str) -> dict[ID, Assembly]:
    components, light_assemblies = _load_components_and_light_assemblies(
        yaml_str=yaml_str,
    )
    return convert_light_assemblies_to_rich_ones(
        light_assemblies, components
    )


def _load_components_and_light_assemblies(
        yaml_str: str,
) -> tuple[dict[str, Component], dict[ID, LightAssembly]]:
    docs = list(split_yaml_documents(yaml_str))
    if len(docs) != 2:
        raise ValueError(
            f"Expected exactly 2 YAML documents, found {len(docs)}.")
    components = load_components(docs[0])
    light_assemblies = load_light_assemblies(docs[1])
    return components, light_assemblies
