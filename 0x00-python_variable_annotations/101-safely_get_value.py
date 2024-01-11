#!/usr/bin/env python3
''' 101-safely_get_value.py '''

from typing import Mapping, Any, TypeVar, Union, Optional

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default: Optional[T] = None) -> Union[Any, T]:
    '''takes a sequence of any and returns any type or none '''
    if key in dct:
        return dct[key]
    else:
        return default
