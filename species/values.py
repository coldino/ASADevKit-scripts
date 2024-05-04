from typing import Any, Optional

import unreal
from unreal import PrimalDinoStatusComponent, PrimalDinoCharacter

from consts import COLOR_REGION_WHITELIST, OUTPUT_OVERRIDES, STAT_COUNT, VALUE_DEFAULTS, VARIANT_OVERRIDES
from clean_numbers import clean_float as cf, clean_double as cd
from species.bones import gather_damage_mults
from species.breeding import gather_breeding_data
from species.taming import gather_taming_data
from species.colors import gather_color_data
from species.stats import DEFAULT_IMPRINT_MULTS, DEFAULT_MAX_STATUS_VALUES, gather_stat_data


def values_for_species(bp: str, char: PrimalDinoCharacter, dcsc: PrimalDinoStatusComponent) -> Optional[dict[str, str]]:
    unreal.log(f'Using Character: {char.get_full_name()}')
    unreal.log(f'Using DCSC: {dcsc.get_full_name()}')

    short_bp = bp.split('.')[0]

    # Having no name or tag is an indication that this is an intermediate class, not a spawnable species
    name = (str(char.descriptive_name) or str(char.dino_name_tag)).strip()
    if not name:
        unreal.log(f"Species {char.get_full_name()} has no DescriptiveName or DinoNameTag - skipping")
        return None

    # Also consider anything that doesn't override any base status value as non-spawnable
    max_status_values: List[float] = list(dcsc.max_status_values) # type: ignore
    if max_status_values == DEFAULT_MAX_STATUS_VALUES:
        unreal.log(f"Species {char.get_full_name()} has no overridden stats - skipping")
        return None

    if bp.endswith('_C'):
        bp = bp[:-2]

    species: dict[str, Any] = dict(blueprintPath=bp, name=name)


    # Skip vehicles
    if char.is_vehicle:
        return None


    # Variants
    variants = VARIANT_OVERRIDES.get(short_bp, None)
    if variants:
        species['variants'] = sorted(variants)


    # Stat data
    is_flyer = bool(char.is_flyer_dino)
    if is_flyer:
        species['isFlyer'] = True
    normal_stats = gather_stat_data(dcsc, dcsc, is_flyer)
    species['fullStatsRaw'] = normal_stats


    # Imprint multipliers
    stat_imprint_mults: list[float] = list()
    unique_mults = False
    for stat_index in range(STAT_COUNT):
        imprint_mult = dcsc.dino_max_stat_add_multiplier_imprinting[stat_index] # type: ignore
        stat_imprint_mults.append(cf(imprint_mult)) # type: ignore

        diff = abs(imprint_mult - DEFAULT_IMPRINT_MULTS[stat_index])
        if diff > 0.0001:
            unique_mults = True

    if unique_mults:
        # print(f'Default imprint mults: {DEFAULT_IMPRINT_MULTS}')
        # print(f'Unique imprint mults: {stat_imprint_mults}')
        species['statImprintMult'] = stat_imprint_mults


    # Breeding data
    if char.can_have_baby:
        breeding_data = None
        breeding_data = gather_breeding_data(char)
        if breeding_data:
            species['breeding'] = breeding_data


    # Taming data
    taming = gather_taming_data(short_bp, char, dcsc)
    if taming:
        species['taming'] = taming


    # Bone damage multipliers
    dmg_mults = None
    dmg_mults = gather_damage_mults(char)
    if dmg_mults:
        species['boneDamageAdjusters'] = dmg_mults


    # Misc data
    usesOxyWild = dcsc.can_suffocate # type: ignore
    usesOxyTamed = True if usesOxyWild else dcsc.can_suffocate_if_tamed # type: ignore
    forceOxy = dcsc.force_gain_oxygen # type: ignore
    doesntUseOxygen = not (usesOxyTamed or forceOxy)

    ETBHM: float = char.extra_tamed_base_health_multiplier # type: ignore
    TBHM: float = dcsc.tamed_base_health_multiplier * ETBHM # type: ignore

    displayed_stats: int = 0

    for i in range(STAT_COUNT):
        use_stat = not dcsc.dont_use_value[i] # type: ignore
        if use_stat and not (i == 3 and doesntUseOxygen):
            displayed_stats |= (1 << i)

    species['TamedBaseHealthMultiplier'] = cf(TBHM)
    species['displayedStats'] = displayed_stats

    if not char.uses_gender:
        species['noGender'] = True


    # Mutation multipliers
    mutation_mults: List[float] = list(dcsc.mutation_multiplier) # type: ignore
    if any(True for mult in mutation_mults if mult != 1.0):
        species['mutationMult'] = mutation_mults


    # Skip wild level-ups
    skip_wild_levels: List[int] = list(dcsc.skip_wild_level_up_value) # type: ignore
    skip_wild_level_bitmap = 0
    for i in range(STAT_COUNT):
        if skip_wild_levels[i]:
            skip_wild_level_bitmap |= (1 << i)
    if skip_wild_level_bitmap:
        species['skipWildLevelStats'] = skip_wild_level_bitmap


    # Color data
    if short_bp in COLOR_REGION_WHITELIST:
        colors = gather_color_data(short_bp, char)
        if colors:
            species['colors'] = colors


    # General output overrides
    overrides = OUTPUT_OVERRIDES.get(short_bp, None)
    if overrides:
        species.update(overrides)


    # Remove values that match the defaults
    for key, value in list(VALUE_DEFAULTS.items()):
        if species.get(key, None) == value:
            del species[key]


    return species
