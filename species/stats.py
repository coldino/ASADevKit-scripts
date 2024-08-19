from typing import Optional

from unreal import PrimalDinoStatusComponent

from consts import IS_PERCENT_STAT, STAT_COUNT
from clean_numbers import clean_float as cf, clean_double as cd


DEFAULT_IMPRINT_MULTS = [0.2, 0, 0.2, 0, 0.2, 0.2, 0, 0.2, 0.2, 0.2, 0, 0]
DEFAULT_MAX_STATUS_VALUES = [100]*6 + [0]*6



def gather_stat_data(dcsc: PrimalDinoStatusComponent, meta_props: PrimalDinoStatusComponent, is_flyer: bool) -> list[Optional[list[float]]]:
    statsArray = list()

    iw_values: list[float] = [0] * STAT_COUNT
    for ark_index in range(STAT_COUNT):
        can_level: bool = (ark_index == 2) or meta_props.can_level_up_value[ark_index] # type: ignore
        dont_use: bool = meta_props.dont_use_value[ark_index] # type: ignore

        # Creates a null value in the JSON for stats that are unused
        if dont_use and not can_level:
            stat_data: Optional[list[float]] = None

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
                cd(dcsc.max_status_values[ark_index] + add_one), # type: ignore
                cf(iw_values[ark_index] * wild_mult),
                cf(dcsc.amount_max_gained_per_level_up_value_tamed[ark_index] * ETHM * dom_mult), # type: ignore
                cf(dcsc.taming_max_stat_additions[ark_index]), # type: ignore
                cf(dcsc.taming_max_stat_multipliers[ark_index]), # type: ignore
            ] # type: ignore

        statsArray.append(stat_data)

    return statsArray
