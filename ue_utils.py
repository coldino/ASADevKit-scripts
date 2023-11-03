from typing import Iterator, List, Optional

import unreal

from consts import SPECIES_ROOTS


asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
assert asset_registry
subobject_data_system = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
assert subobject_data_system


def load_asset(asset: unreal.AssetData) -> unreal.Object:
    return unreal.load_asset(str(asset.package_name))


def get_components_from_blueprint(bp: unreal.Blueprint) -> Iterator[unreal.Object]:
    component_handles = subobject_data_system.k2_gather_subobject_data_for_blueprint(bp)
    for component_handle in component_handles:
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(component_handle)
        component = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
        if component:
            yield component


def filter_components_by_class(components: Iterator[unreal.Object], cls: type) -> Iterator[unreal.Object]:
    for component_object in components:
        if isinstance(component_object, cls):
            yield component_object


def is_creature(default: unreal.Object) -> bool:
    return isinstance(default, unreal.PrimalDinoCharacter)


def find_all_species() -> Iterator[tuple[unreal.Object, unreal.PrimalDinoCharacter]]:
    for root in SPECIES_ROOTS:
        assets = asset_registry.get_assets_by_path(root, recursive=True)
        assert assets
        for asset_data in assets:
            asset = load_asset(asset_data)
            if not isinstance(asset, unreal.Blueprint):
                continue
            cls = asset.generated_class()
            if not cls:
                continue
            cdo = unreal.get_default_object(cls)
            if cdo and is_creature(cdo):
                yield asset, cdo


def get_dcsc_from_bp(bp: unreal.Object) -> Optional[unreal.PrimalDinoStatusComponent]:
    if not isinstance(bp, unreal.Blueprint):
        return None

    try:
        components = get_components_from_blueprint(bp) # type: ignore
        dcsc_options: List[unreal.PrimalDinoStatusComponent] = list(filter_components_by_class(components, unreal.PrimalDinoStatusComponent)) # type: ignore
    except Exception as e:
        if bp:
            unreal.log_error(f"Error getting components for {bp.get_path_name()}: {e}")
            return None
        else:
            unreal.log_error(f"Error getting components: {e}")
            return None

    if not dcsc_options:
        unreal.log(f"Warning: Blueprint {bp.get_path_name()} has no PrimalDinoStatusComponent")
        return None

    # Easy case - only one DCSC
    if len(dcsc_options) == 1:
        return dcsc_options[0]

    # Hard case - multiple DCSCs
    # We take the last one, but allow priority overrides
    dcsc_options.sort(key=lambda dcsc: dcsc.character_status_component_priority)
    for dcsc in dcsc_options:
        print(f'  DCSC: {dcsc.character_status_component_priority} {dcsc.get_path_name()}')
    dcsc = dcsc_options[-1]
    return dcsc
