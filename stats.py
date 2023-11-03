from typing import List, Optional, Dict, Any
import unreal
from unreal import PrimalDinoStatusComponent, PrimalDinoCharacter

from consts import IS_PERCENT_STAT, STAT_COUNT
from clean_numbers import clean_float as cf, clean_double as cd


DEFAULT_IMPRINT_MULTS = [0.2, 0, 0.2, 0, 0.2, 0.2, 0, 0.2, 0.2, 0.2, 0, 0]
DEFAULT_MAX_STATUS_VALUES = [100]*6 + [0]*6



def gather_stat_data(dcsc: PrimalDinoStatusComponent, meta_props: PrimalDinoStatusComponent, is_flyer: bool) -> List[Optional[List[float]]]:
    statsArray = list()

    iw_values: List[float] = [0] * STAT_COUNT
    for ark_index in range(STAT_COUNT):
        can_level: bool = (ark_index == 2) or meta_props.can_level_up_value[ark_index] # type: ignore
        dont_use: bool = meta_props.dont_use_value[ark_index] # type: ignore

        # Creates a null value in the JSON for stats that are unused
        if dont_use and not can_level:
            stat_data: Optional[List[float]] = None

        else:
            add_one = 1 if IS_PERCENT_STAT[ark_index] else 0

            # Zero-out stats that can't level
            wild_mult = 1 if can_level else 0

            # Also zero-out domestic stats that can't level, adding exception for flyer speed :(
            dom_mult = 1 if ark_index == 9 and is_flyer else wild_mult

            ETHM = cf(dcsc.extra_tamed_health_multiplier) if ark_index == 0 else 1 # type: ignore

            # Overrides the IW value for Torpor. While this hasn't been seen before, a species may allow torpor
            #   to be leveled in the wild. Unsure how Ark would handle this.
            if ark_index == 2:
                iw_values[ark_index] = cf(dcsc.the_max_torpor_increase_per_base_level) # type: ignore
            else:
                iw_values[ark_index] = cf(dcsc.amount_max_gained_per_level_up_value[ark_index]) # type: ignore

            stat_data = [
                cf(dcsc.max_status_values[ark_index] + add_one), # type: ignore
                cf(iw_values[ark_index] * wild_mult),
                cf(dcsc.amount_max_gained_per_level_up_value_tamed[ark_index] * ETHM * dom_mult), # type: ignore
                cf(dcsc.taming_max_stat_additions[ark_index]), # type: ignore
                cf(dcsc.taming_max_stat_multipliers[ark_index]), # type: ignore
            ] # type: ignore

        statsArray.append(stat_data)

    return statsArray


def values_for_species(bp: str, char: PrimalDinoCharacter, dcsc: PrimalDinoStatusComponent) -> Optional[Dict[str, str]]:
    unreal.log(f'Using Character: {char.get_full_name()}')
    unreal.log(f'Using DCSC: {dcsc.get_full_name()}')

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

    species: Dict[str, Any] = dict(blueprintPath=bp)


    # Stat data
    is_flyer = bool(char.is_flyer_dino)
    if is_flyer:
        species['isFlyer'] = True
    normal_stats = gather_stat_data(dcsc, dcsc, is_flyer)
    species['fullStatsRaw'] = normal_stats


    # Imprint multipliers
    stat_imprint_mults: List[float] = list()
    unique_mults = False
    for stat_index in range(STAT_COUNT):
        imprint_mult = dcsc.dino_max_stat_add_multiplier_imprinting[stat_index] # type: ignore
        stat_imprint_mults.append(cf(imprint_mult))

        diff = abs(imprint_mult - DEFAULT_IMPRINT_MULTS[stat_index])
        if diff > 0.0001:
            unique_mults = True

    if unique_mults:
        print(f'Default imprint mults: {DEFAULT_IMPRINT_MULTS}')
        print(f'Unique imprint mults: {stat_imprint_mults}')
        species['statImprintMult'] = stat_imprint_mults


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

    return species
