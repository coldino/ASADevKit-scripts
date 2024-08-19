from typing import Optional

import unreal
from unreal import PrimalDinoCharacter, PrimalColorSet, ColorSetDefinition, Class

from consts import COLOR_REGION_BAD_NAMES, COLOR_OVERRIDES, NUM_REGIONS, RegionInfo


def gather_color_data(short_bp: str, char: PrimalDinoCharacter) -> Optional[list[Optional[RegionInfo]]]:
    # Extract raw data
    color_data = extract_color_data(char)
    if not color_data:
        return None

    # Convert to output format
    output_data: list[Optional[RegionInfo]] = [{'name':name.capitalize(), 'colors':colors} if name else None for name, colors in color_data]

    # Handle bad region names
    for i, region in enumerate(output_data):
        if region is None:
            continue
        region_name = region.get('name', None)
        if region_name is None:
            continue
        region_name = region_name.lower()
        if region_name.lower() in COLOR_REGION_BAD_NAMES:
            output_data[i] = None

    # Apply any overrides
    overrides = COLOR_OVERRIDES.get(short_bp, None)
    if overrides:
        print(f"Applying color overrides for {short_bp}")
        for i, override in overrides.items():
            region = output_data[i]
            if region and override is None:
                print(f"Removing region {i}")
                region = None
            elif region and override:
                print(f"Overriding region {i} with {override}")
                region.update(override)
            elif not region and override:
                print(f"Overriding region {i} with {override}")
                region = override
            output_data[i] = region

    return output_data


def extract_color_data(char: PrimalDinoCharacter) -> Optional[list[tuple[Optional[str], list[str]]]]:
    '''Gather color region definitions for a species.'''
    if char.is_corrupted:
        return None

    colors: list[tuple[Optional[str], list[str]]] = list()
    male_colorset: Optional[Class] = None
    female_colorset: Optional[Class] = None

    try:
        male_colorset = char.random_color_sets_male
    except ValueError:
        pass
    try:
        female_colorset = char.random_color_sets_female
    except ValueError:
        pass

    # TODO: Incorporate both male and female colorsets, as well as if multiple colorsets are listed
    colorset_cls = male_colorset or female_colorset
    if not colorset_cls:
        print("No colorset or color set definitions")
        return None

    colorset: PrimalColorSet = unreal.get_default_object(colorset_cls)
    regions = colorset.color_set_definitions

    # Export a list of color names for each region
    for i in range(NUM_REGIONS):
        prevent_region = char.prevent_colorization_regions[i] # type: ignore
        if prevent_region:
            colors.append((None, list()))
            continue

        name: Optional[str] = None
        color_names: list[str] = list()

        region: ColorSetDefinition = regions[i] # type: ignore

        name = region.region_name # type: ignore
        color_names = list(map(str, region.color_entry_names))

        colors.append((name, color_names))

    return colors
