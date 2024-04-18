from typing import Optional
from unreal import PrimalDinoCharacter

from clean_numbers import clean_float as cf, clean_double as cd


__all__ = [
    'gather_damage_mults',
]


def gather_damage_mults(char: PrimalDinoCharacter) -> Optional[dict[str, float]]:
    damage_adjusters = char.bone_damage_adjusters
    if not damage_adjusters:
        return None

    result = dict()
    for bone_info in damage_adjusters:
        name = str(bone_info.bone_name)
        mult = cf(bone_info.damage_multiplier)
        result[name] = mult

    print(result)

    return result
