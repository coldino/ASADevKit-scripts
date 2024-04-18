from operator import itemgetter
from typing import Any, Optional
import unreal
from unreal import PrimalDinoCharacter, PrimalItem

from clean_numbers import clean_float as cf, clean_double as cd


__all__ = [
    'gather_breeding_data',
]


def gather_breeding_data(char_props: PrimalDinoCharacter) -> dict[str, Any]:
    data: dict[str, Any] = dict(gestationTime=0, incubationTime=0)

    gestation_breeding = char_props.use_baby_gestation
    fert_eggs = char_props.fertilized_egg_items_to_spawn
    fert_egg_weights = char_props.fertilized_egg_weights_to_spawn

    if gestation_breeding:
        gestation_speed = round(char_props.baby_gestation_speed, 6)
        extra_gestation_speed_m = round(char_props.extra_baby_gestation_speed_multiplier, 6)
        try:
            data['gestationTime'] = cd(1 / gestation_speed / extra_gestation_speed_m)
        except ZeroDivisionError:
            unreal.log_error(f"Species {char_props.get_full_name()} tried dividing by zero for its gestationTime")

    elif fert_eggs and fert_eggs:
        eggs = []
        for index, egg in enumerate(fert_eggs):
            weight = fert_egg_weights[index] if fert_egg_weights else 1
            # Verify the egg is a valid Object and that weight isn't 0
            if str(egg) == 'None' or weight == 0:
                continue

            eggs.append((egg, weight))

        # Sort eggs by highest weighting
        eggs.sort(reverse=True, key=itemgetter(1))

        if eggs:
            # We only provide the highest possibility egg to ASB
            egg: Optional[PrimalItem] = None
            try:
                egg = unreal.get_default_object(eggs[0][0])
            except Exception as e:
                unreal.log_error(f"Error loading egg: {e}")

            if egg:
                egg_decay = round(egg.egg_lose_durability_per_second, 6)
                extra_egg_decay_m = round(egg.extra_egg_lose_durability_per_second_multiplier, 6)

                # 'incubationTime' = 100 / (Egg Lose Durability Per Second × Extra Egg Lose Durability Per Second Multiplier)
                try:
                    data['incubationTime'] = cd(100 / egg_decay / extra_egg_decay_m)
                except ZeroDivisionError:
                    unreal.log_warning(
                        f"Species {char_props.get_full_name()} tried dividing by zero for its incubationTime")
                data['eggTempMin'] = cd(egg.egg_min_temperature)
                data['eggTempMax'] = cd(egg.egg_max_temperature)

    # 'maturationTime' = 1 / (Baby Age Speed × Extra Baby Age Speed Multiplier)
    baby_age_speed = round(char_props.baby_age_speed, 6)
    extra_baby_age_speed_m = round(char_props.extra_baby_age_speed_multiplier, 6)

    try:
        data['maturationTime'] = cd(1 / baby_age_speed / extra_baby_age_speed_m)
    except ZeroDivisionError:
        unreal.log_warning(f"Species {char_props.get_full_name()} tried dividing by zero for its maturationTime")
    data['matingCooldownMin'] = cd(char_props.new_female_min_time_between_mating)
    data['matingCooldownMax'] = cd(char_props.new_female_max_time_between_mating)

    return data
