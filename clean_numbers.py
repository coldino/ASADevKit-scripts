from math import isinf
from typing import Union


def clean_float(value) -> Union[None, int, float]:
    '''Round to 7 significant figures. Should be used for outputting all single-precision float data.'''
    if value is None:
        return None
    if isinf(value):
        return value
    value = float(format(value, '.7g'))
    try:
        int_value = int(value)
    except OverflowError:
        return value
    except ValueError:
        return value

    if value == int_value:
        return int_value
    else:
        return value


def clean_double(value) -> Union[None, int, float]:
    '''Round to 9 significant figures. Should be used for outputting all double-precision float data.'''
    if value is None:
        return None
    if isinf(value):
        return value
    value = float(format(value, '.9g'))
    try:
        int_value = int(value)
    except OverflowError:
        return value
    except ValueError:
        return value

    if value == int_value:
        return int_value
    else:
        return value
