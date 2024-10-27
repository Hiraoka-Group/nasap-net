from recsa import Assembly, BindsiteIdConverter, Component


def get_connected_num(
        assembly: Assembly, source_comp_id: str,
        target_comp_kind: str,
        source_component: Component
        ) -> int:
    id_converter = BindsiteIdConverter()
    num = 0
    for bindsite in source_component.bindsites:
        global_bindsite = id_converter.local_to_global(
            source_comp_id, bindsite)
        connected = assembly.get_connected_bindsite(global_bindsite)
        if connected is None:
            continue
        if assembly.get_component_kind_of_bindsite(
                connected) == target_comp_kind:
            num += 1
    return num
