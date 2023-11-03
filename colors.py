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
