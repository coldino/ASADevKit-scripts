import sys
from pathlib import Path
from importlib import reload
from typing import Iterator, List, Optional, Union, cast

import unreal


asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
assert asset_registry
subobject_data_system = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
assert subobject_data_system


def reload_local_modules(base_path: Path):
    # Force reload all local modules, else changes won't be picked up
    for name,mod in list(sys.modules.items()):
        if (path:=getattr(mod, '__file__', None)) and Path(path).is_relative_to(base_path):
            try:
                reload(mod)
                unreal.reload(name)
            except Exception as e:
                print(f"Error reloading {mod}: {e}")
    # [reload(mod) for mod in list(sys.modules.values()) if (path:=getattr(mod, '__file__', None)) and Path(path).is_relative_to(BASE_PATH)]


def get_cdo_from_asset(asset: Union[unreal.Object,unreal.AssetData]) -> Optional[unreal.Object]:
    if isinstance(asset, unreal.AssetData):
        return unreal.VictoryCore.get_class_default_object_from_asset(asset)
    if not isinstance(asset, unreal.Blueprint):
        return None
    cls = asset.generated_class()
    if not cls:
        return None
    return unreal.get_default_object(cls)


def load_asset(asset_data_or_package_name: Union[unreal.AssetData,str]) -> unreal.Object:
    if isinstance(asset_data_or_package_name, unreal.AssetData):
        if not (pkg_name := asset_data_or_package_name.package_name):
            raise ValueError(f"AssetData {asset_data_or_package_name} has no package name")
        asset_data_or_package_name = str(pkg_name)
    return unreal.load_asset(asset_data_or_package_name)


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
    # Using Dino_Character_BP_C instead of PrimalDinoCharacter skips some unwanted things like vehicles and scripted boss spawns
    filter = unreal.ARFilter(
        class_paths=[unreal.TopLevelAssetPath('/Game/PrimalEarth/CoreBlueprints/Dino_Character_BP', 'Dino_Character_BP_C')],
        recursive_classes=True
    )
    all_species: list[unreal.AssetData] = list(filter.get_blueprint_assets())

    with unreal.ScopedSlowTask(len(all_species), "Exporting all species") as slow_task:
        slow_task.make_dialog_delayed(2, True)

        for asset_data in all_species:
            slow_task.enter_progress_frame(1, f"Checking {str(asset_data.package_path)}")
            asset = load_asset(asset_data)
            cdo_untyped = get_cdo_from_asset(asset)
            if not cdo_untyped:
                continue
            cdo = cast(unreal.PrimalDinoCharacter, cdo_untyped)
            yield asset, cdo

            if slow_task.should_cancel():
                raise KeyboardInterrupt


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
