import unreal
from clean_numbers import clean_double as cd

def color_hex_to_decimal(hex: str) -> tuple:
    """Converts a hex color string to a tuple of decimal values from 0-1."""
    hex = hex.strip()
    if hex.startswith('#'):
        hex = hex[1:]
    if len(hex) == 3:
        hex = ''.join(c * 2 for c in hex)
    if len(hex) != 6:
        raise ValueError(f"Invalid hex color: {hex}")
    return tuple(cd(int(hex[i:i+2], 16) / 255.0) for i in (0, 2, 4)) + (0,)


def parse_dyes(dye_list: unreal.Array):
    """Parses the dye list from PrimalGameData into a dictionary of dye name to color."""
    dyes = []
    for dye in dye_list:
        cdo = unreal.get_default_object(dye)
        if not isinstance(cdo, unreal.PrimalItem_Dye):
            continue

        name = cdo.descriptive_name_base
        color = [cdo.dye_color.r, cdo.dye_color.g, cdo.dye_color.b, cdo.dye_color.a]
        color = [round(c, 6) for c in color]
        dyes.append((name, color))

    if len(dyes) != 127:
        raise ValueError(f"Unexpected number of dyes: {len(dyes)}")

    return dyes
