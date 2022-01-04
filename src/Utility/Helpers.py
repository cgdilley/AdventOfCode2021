from typing import Any, List, Dict, TypeVar, Hashable, Iterable, Callable


def binary_insertion(val: Any, items: List[Any]) -> None:
    left = 0
    right = len(items)
    while left < right:
        m = int((left + right) / 2)
        if items[m] > val:
            right = m
        elif items[m] < val:
            left = m + 1
        else:
            items.insert(m, val)
            return
    items.insert(left, val)


THash = TypeVar('THash', bound=Hashable)
T = TypeVar('T')


def group_by(items: Iterable[T], key: Callable[[T], THash]) -> Dict[THash, List[T]]:
    d = dict()
    for item in items:
        k = key(item)
        if k in d:
            d[k].append(item)
        else:
            d[k] = [item]
    return d
