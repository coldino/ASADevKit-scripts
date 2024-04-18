from typing import Any, Optional
import unreal
from unreal import PrimalDinoStatusComponent, PrimalDinoCharacter

from consts import TAMING_OVERRIDES
from clean_numbers import clean_float as cf, clean_double as cd


def gather_taming_data(bp_short: str, char: PrimalDinoCharacter, dcsc: PrimalDinoStatusComponent) -> dict[str, Any]:
    data: dict[str, Any] = dict()

    # Currently unable to gather the foods list
    eats: Optional[list[str]] = None
    special_food_values: Optional[list[dict[str, dict[str, list[int]]]]] = None

    method_overrides = TAMING_OVERRIDES.get(bp_short, None)

    if method_overrides:
        can_tame = method_overrides.get('violent', False) or method_overrides.get('nonViolent', False)
        data.update(method_overrides)
    else:
        can_tame = char.can_be_tamed
        can_knockout = char.can_be_torpid
        can_basket_tame = char.allow_trapping and not char.prevent_wild_trapping and char.is_trap_tamed
        data['nonViolent'] = (char.support_waking_tame and can_tame) or can_basket_tame
        data['violent'] = not char.prevent_sleeping_tame and can_tame and can_knockout

    if can_tame or True:
        data['tamingIneffectiveness'] = cf(round(char.tame_ineffectiveness_by_affinity, 6))
        data['affinityNeeded0'] = cf(round(char.required_tame_affinity, 6))
        data['affinityIncreasePL'] = cf(round(char.required_tame_affinity_per_base_level, 6))

        torpor_depletion = round(dcsc.knocked_out_torpidity_recovery_rate_multiplier, 6) \
            * round(dcsc.recovery_rate_status_value[2], 6) # type: ignore

        if data['violent']:
            data['torporDepletionPS0'] = cd(-torpor_depletion)
        if data['nonViolent']:
            data['wakeAffinityMult'] = cf(round(char.waking_tame_food_affinity_multiplier, 6))
            data['wakeFoodDeplMult'] = cf(round(dcsc.waking_tame_food_consumption_rate_multiplier, 6))

        data['foodConsumptionBase'] = cf(-round(dcsc.base_food_consumption_rate, 6))
        data['foodConsumptionMult'] = cf(round(dcsc.prone_water_food_consumption_multiplier, 6))
        data['babyFoodConsumptionMult'] = cf(round(dcsc.baby_dino_consuming_food_rate_multiplier, 6) *
                                             round(dcsc.extra_baby_dino_consuming_food_rate_multiplier, 6))

        adultFoodConsumptionMult = round(dcsc.dino_tamed_adult_consuming_food_rate_multiplier, 6)

        if adultFoodConsumptionMult != 1:
            data['adultFoodConsumptionMult'] = cf(adultFoodConsumptionMult)

        if eats is not None:
            data['eats'] = eats
        if special_food_values is not None:
            data['specialFoodValues'] = special_food_values

    return data
